"""Native WorkBench tools with forkable state and explicit work assignment.

Assignment ownership is coordination metadata, NOT a tool authorization gate.
Every arm retains the same pre-existing ACL. An authorized backup can recover
after direct retirement without an orchestrator handoff.
"""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path

import pandas as pd

from benchmark.workbench import SIDE_EFFECT_TOOLS, TOOL_SPECS, WorkBenchSandbox

from .retirement import retire_leaf_agents

TABLES = ('calendar_events', 'emails', 'analytics_data', 'plots_data',
          'project_tasks', 'crm_data', 'company_directory')
DEFAULT_AGENTS = tuple(f'agent_{i}' for i in range(5))
ARMS = ('keep', 'direct', 'simple', 'check', 'handoff')
DOMAINS = frozenset({'calendar', 'project_management', 'email'})


def _json_value(value):
    if isinstance(value, dict):
        return {str(k): _json_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(v) for v in value]
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if pd.isna(value):
        return None
    if hasattr(value, 'item'):
        return _json_value(value.item())
    return value


def _cell(value):
    if isinstance(value, (pd.Timestamp, datetime)):
        return {'__timestamp__': value.isoformat()}
    if value is pd.NA:
        return {'__missing__': 'NA'}
    if value is pd.NaT:
        return {'__missing__': 'NaT'}
    if value is not None and not isinstance(value, (str, bool, int)) and pd.isna(value):
        return {'__missing__': 'nan'}
    return _json_value(value)


def _uncell(value):
    if isinstance(value, dict) and '__timestamp__' in value:
        return pd.Timestamp(value['__timestamp__'])
    if isinstance(value, dict) and '__missing__' in value:
        return {'NA': pd.NA, 'NaT': pd.NaT, 'nan': float('nan')}[value['__missing__']]
    return value


def _frame_payload(frame):
    return {'columns': list(frame.columns), 'index': [_cell(i) for i in frame.index],
            'index_dtype': str(frame.index.dtype),
            'range_index': ([frame.index.start, frame.index.stop, frame.index.step]
                            if isinstance(frame.index, pd.RangeIndex) else None),
            'index_name': frame.index.name, 'dtypes': [str(t) for t in frame.dtypes],
            'data': [[_cell(v) for v in row] for row in frame.itertuples(index=False, name=None)]}


def _frame_restore(payload):
    index = (pd.RangeIndex(*payload['range_index']) if payload.get('range_index') is not None
             else pd.Index([_uncell(i) for i in payload['index']], dtype=payload.get('index_dtype')))
    frame = pd.DataFrame([[_uncell(v) for v in row] for row in payload['data']],
                         columns=payload['columns'], index=index)
    frame.index.name = payload.get('index_name')
    for col, dtype in zip(payload['columns'], payload['dtypes']):
        frame[col] = frame[col].astype(dtype)
    return frame


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False, separators=(',', ':'))


def _state_delta(before, after):
    delta = {}
    for name in TABLES:
        if before[name] == after[name]:
            continue
        left, right = before[name], after[name]
        def rows(table):
            return {_canonical(index): {'index': index, 'values': row}
                    for index, row in zip(table['index'], table['data'])}
        a, b = rows(left), rows(right)
        delta[name] = {
            'columns_before': left['columns'], 'columns_after': right['columns'],
            'removed': [a[k] for k in sorted(a.keys() - b.keys())],
            'added': [b[k] for k in sorted(b.keys() - a.keys())],
            'updated': [{'before': a[k], 'after': b[k]} for k in sorted(a.keys() & b.keys()) if a[k] != b[k]],
        }
    return delta


class WorkbenchHandoffSandbox:
    def __init__(self, data_root, domain, active_agents=DEFAULT_AGENTS,
                 owner='agent_1', authorized_agents=('agent_1', 'agent_2')):
        if domain not in DOMAINS:
            raise ValueError('this pilot supports calendar, project_management, and email only')
        if owner not in active_agents or owner not in authorized_agents:
            raise ValueError('owner must be active and preauthorized')
        self.native = WorkBenchSandbox(Path(data_root).resolve())
        self._meta = {
            'version': 1, 'domain': domain, 'data_root': str(self.native.data_root),
            'active_agents': list(active_agents), 'authorized_agents': sorted(set(authorized_agents)),
            'assignment': {'owner': owner, 'continuing': True, 'domain': domain, 'progress': []},
            'logs': [], 'handoffs': [], 'dedup': {}, 'topology_tool_limits': {},
        }

    @property
    def logs(self):
        return deepcopy(self._meta['logs'])

    def _tables(self):
        return {name: _frame_payload(getattr(self.native, name)) for name in TABLES}

    def snapshot(self):
        return json.loads(_canonical({**deepcopy(self._meta), 'tables': self._tables()}))

    @classmethod
    def from_snapshot(cls, data):
        cls._validate_snapshot(data)
        instance = cls.__new__(cls)
        instance._meta = deepcopy({k: v for k, v in data.items() if k != 'tables'})
        instance.native = WorkBenchSandbox.__new__(WorkBenchSandbox)
        instance.native.data_root = Path(data['data_root'])
        for name in TABLES:
            setattr(instance.native, name, _frame_restore(data['tables'][name]))
        return instance

    @staticmethod
    def _validate_snapshot(data):
        if data.get('version') != 1 or data.get('domain') not in DOMAINS:
            raise ValueError('invalid WorkBench snapshot version/domain')
        if set(data['tables']) != set(TABLES):
            raise ValueError('snapshot must contain all seven native tables')
        if data['assignment']['owner'] not in data['authorized_agents']:
            raise ValueError('assignment owner must be preauthorized (may be retired)')
        if len(data['active_agents']) != len(set(data['active_agents'])):
            raise ValueError('duplicate active agents')
        for table in data['tables'].values():
            if len(table['data']) != len(table['index']) or len(table['columns']) != len(table['dtypes']):
                raise ValueError('invalid table shape')
            if any(len(row) != len(table['columns']) for row in table['data']):
                raise ValueError('invalid table row')

    def tool_names_for(self, agent_id, allowed_tools=None):
        names = {'workflow_status'}
        for spec in TOOL_SPECS:
            if spec['domain'] not in {self._meta['domain'], 'company_directory'}:
                continue
            if spec['name'] in SIDE_EFFECT_TOOLS and agent_id not in self._meta['authorized_agents']:
                continue
            names.add(spec['name'])
        declared = self._meta.get('topology_tool_limits', {}).get(agent_id)
        if declared is not None:
            names.intersection_update(declared)
        if allowed_tools is not None:
            names.intersection_update(allowed_tools)
        return names

    def bind_topology(self, spec):
        """Record immutable stage allow-lists so public capability views agree."""
        self._meta['topology_tool_limits'] = {
            n.agent_id: list(n.allowed_tools) if n.allowed_tools is not None else None
            for n in spec.agents
        }

    def public_workflow(self):
        return {
            'workflow': 'continuing_workbench_' + self._meta['domain'],
            'domain': self._meta['domain'],
            'active_agents': list(self._meta['active_agents']),
            'authorized_agents': list(self._meta['authorized_agents']),
            'assignment': deepcopy(self._meta['assignment']),
            'tools_allowed': {a: sorted(self.tool_names_for(a)) for a in self._meta['active_agents']},
            'rule': 'Assignment owner coordinates the work. Any active preauthorized member may use its tools, including recovery when an owner retires. Ownership does not grant or restrict tool permission.',
        }

    def tools_for(self, agent_id, allowed_tools=None):
        allowed = self.tool_names_for(agent_id, allowed_tools)
        specs = [s for s in TOOL_SPECS if s['name'] in allowed]
        if 'workflow_status' in allowed:
            specs.append({'name': 'workflow_status', 'description': 'Read current public work assignment, progress and unchanged tool permissions.', 'properties': {}})
        return [{
            'name': s['name'], 'description': s['description'],
            'parameters': {'type': 'object', 'properties': deepcopy(s['properties']),
                           'required': list(s.get('required', []))},
            'handler': lambda args, name=s['name']: self._invoke(agent_id, name, args, allowed_tools),
        } for s in specs]

    def _invoke(self, actor, name, args, allowed_tools=None):
        before = self._tables()
        is_write = name in SIDE_EFFECT_TOOLS
        delta = {}
        if actor not in self._meta['active_agents']:
            result = {'ok': False, 'error': 'inactive_actor'}
        elif name not in self.tool_names_for(actor, allowed_tools):
            result = {'ok': False, 'error': 'not_authorized'}
        elif not isinstance(args, dict):
            result = {'ok': False, 'error': 'invalid_arguments'}
        elif name == 'workflow_status':
            result = self.public_workflow()
        else:
            signature = _canonical([name, _json_value(args)])
            if is_write and signature in self._meta['dedup']:
                result = {'ok': True, 'duplicate': True,
                          'previous_result': deepcopy(self._meta['dedup'][signature])}
            else:
                try:
                    result = _json_value(self.native.invoke(name, deepcopy(args)))
                    after = self._tables()
                    delta = _state_delta(before, after)
                    if delta:
                        self._meta['assignment']['progress'].append({
                            'actor': actor, 'tool_name': name, 'arguments': _json_value(args),
                            'result': deepcopy(result), 'changed_tables': sorted(delta),
                            'log_index': len(self._meta['logs']),
                        })
                        if is_write:
                            self._meta['dedup'][signature] = deepcopy(result)
                except Exception as exc:
                    for table in TABLES:
                        setattr(self.native, table, _frame_restore(before[table]))
                    result = {'ok': False, 'error': type(exc).__name__, 'detail': str(exc)}
                    delta = {}
        after = self._tables()
        self._meta['logs'].append({
            'index': len(self._meta['logs']), 'actor': actor, 'tool_name': name, 'operation': name,
            'arguments': _json_value(args), 'result': deepcopy(result), 'mutation': bool(delta),
            'state_changed': bool(delta),
            'duplicate': isinstance(result, dict) and result.get('duplicate') is True,
            'write_tool': is_write, 'delta': delta,
            'before_sha256': hashlib.sha256(_canonical(before).encode()).hexdigest(),
            'after_sha256': hashlib.sha256(_canonical(after).encode()).hexdigest(),
            'assignment_owner_at_call': self._meta['assignment']['owner'],
            'actor_active': actor in self._meta['active_agents'],
            'actor_authorized': actor in self._meta['authorized_agents'],
        })
        return deepcopy(result)

    def assess_and_apply(self, arm, spec, candidate):
        if arm not in ARMS:
            raise ValueError(arm)
        node = spec.agent(candidate)
        workflow = self.public_workflow()
        decision = {'arm': arm, 'candidate': candidate, 'action': 'keep',
                    'reason': 'keep_control', 'handoff': None, 'workflow_before': workflow}
        if arm == 'keep':
            return spec, decision
        candidate_tools = self.tool_names_for(candidate, node.allowed_tools) & SIDE_EFFECT_TOOLS
        successors = sorted(n.agent_id for n in spec.agents if n.agent_id != candidate
                            and n.agent_id in self._meta['authorized_agents']
                            and candidate_tools.issubset(self.tool_names_for(n.agent_id, n.allowed_tools)))
        owns = workflow['assignment']['continuing'] and workflow['assignment']['owner'] == candidate
        if arm == 'simple' and (node.structural_role == 'verifier' or node.stage_role == 'critic'
                                or (candidate_tools and not successors)):
            decision['reason'] = 'simple_role_or_exclusive_tool_protection'
            return spec, decision
        if arm == 'check' and owns:
            decision['reason'] = 'continuing_assignment_needs_owner'
            return spec, decision
        if arm == 'handoff' and owns and not successors:
            decision['reason'] = 'no_preauthorized_successor'
            return spec, decision
        try:
            changed_spec = retire_leaf_agents(spec, (candidate,), max_agents=max(5,len(spec.agents)), protect_validation=False)
            next_data = self.snapshot()
            next_data['active_agents'] = [n.agent_id for n in changed_spec.agents]
            next_data['topology_tool_limits'] = {
                n.agent_id: list(n.allowed_tools) if n.allowed_tools is not None else None
                for n in changed_spec.agents
            }
            if arm == 'handoff' and owns:
                transfer = {'from': candidate, 'to': successors[0], 'acl_changed': False,
                            'progress': deepcopy(next_data['assignment']['progress'])}
                next_data['assignment']['owner'] = successors[0]
                next_data['handoffs'].append(transfer)
                decision.update(action='handoff_and_retire', reason='assignment_transferred', handoff=transfer)
            else:
                decision.update(action='retire', reason='direct_removal' if arm == 'direct' else 'no_policy_block')
            replacement = self.from_snapshot(next_data)
        except (ValueError, KeyError, RuntimeError) as exc:
            decision.update(action='keep', reason='transition_rejected', handoff=None, error=str(exc))
            return spec, decision
        self.native, self._meta = replacement.native, replacement._meta
        decision['workflow_after'] = self.public_workflow()
        return changed_spec, decision
