"""Offline checks against real WorkBench tool methods and seven native tables."""
import json
from dataclasses import replace

import pandas as pd
import pytest

from benchmark.workbench import WorkBenchSandbox
from MAS.self_evolved.spec import AgentNode, GroupSpec, TopologySpec
from MAS.self_evolved.workbench_handoff import DEFAULT_AGENTS, TABLES, WorkbenchHandoffSandbox


@pytest.fixture
def sandbox(monkeypatch):
    def local_reset(native):
        native.calendar_events = pd.DataFrame([['00000001','review','a@example.com','2023-12-01 10:00:00','30']], columns=['event_id','event_name','participant_email','event_start','duration'])
        native.emails = pd.DataFrame([['1','inbox','a@example.com','review',pd.Timestamp('2023-11-30'),'hello']], columns=['email_id','folder','email_address','subject','date','body'])
        native.analytics_data = pd.DataFrame({'visitor_id':['1'], 'user_engaged':[True]})
        native.plots_data = pd.DataFrame(columns=['file_path'])
        native.project_tasks = pd.DataFrame([['00000001','review','a@example.com','To Do','2023-12-01','board','list']], columns=['task_id','task_name','assigned_to_email','status','due_date','board','list_name'])
        native.crm_data = pd.DataFrame({'customer_id':['00000001'], 'name':['alice']})
        native.company_directory = pd.DataFrame({'email_address':['a@example.com']})
    monkeypatch.setattr(WorkBenchSandbox, 'reset_state', local_reset)
    return WorkbenchHandoffSandbox('offline-test-no-file-io', 'calendar')


def topology():
    return TopologySpec(version=0, agents=tuple(AgentNode(a,'root',structural_role='coordinator' if a=='agent_0' else 'worker') for a in DEFAULT_AGENTS), groups=(GroupSpec('root','star',DEFAULT_AGENTS,leader_id='agent_0'),), root_group_id='root')


def call(sb, actor, name, **args):
    tool = next(t for t in sb.tools_for(actor) if t['name']==name)
    return tool['handler'](args)


def update(sb, actor='agent_1', value='updated'):
    return call(sb,actor,'calendar.update_event',event_id='00000001',field='event_name',new_value=value)


def test_snapshot_all_seven_tables_json_roundtrip_without_io(sandbox, monkeypatch):
    snapshot = json.loads(json.dumps(sandbox.snapshot(), allow_nan=False))
    assert set(snapshot['tables'])==set(TABLES)
    monkeypatch.setattr(WorkBenchSandbox,'__init__',lambda *a,**k:pytest.fail('restore must not initialize from files'))
    restored=WorkbenchHandoffSandbox.from_snapshot(snapshot)
    for name in TABLES:
        pd.testing.assert_frame_equal(getattr(sandbox.native,name),getattr(restored.native,name))
    assert restored.native.data_root==sandbox.native.data_root


def test_forks_isolate_native_tables_metadata_and_logs(sandbox):
    saved=sandbox.snapshot()
    left=WorkbenchHandoffSandbox.from_snapshot(saved)
    right=WorkbenchHandoffSandbox.from_snapshot(saved)
    update(left)
    assert right.snapshot()==saved==sandbox.snapshot()
    assert left.native.calendar_events.iloc[0]['event_name']=='updated'
    assert left.logs[-1]['state_changed'] and left.logs[-1]['mutation']
    assert left.logs[-1]['delta']['calendar_events']['updated']


@pytest.mark.parametrize('arm', ['direct','simple'])
def test_backup_can_write_without_owner_handoff(sandbox,arm):
    acl=sandbox.snapshot()['authorized_agents']
    spec,decision=sandbox.assess_and_apply(arm,topology(),'agent_1')
    assert decision['action']=='retire'
    assert sandbox.public_workflow()['assignment']['owner']=='agent_1'
    result=update(sandbox,'agent_2')
    assert result=='Event updated successfully.'
    assert sandbox.logs[-1]['state_changed']
    assert sandbox.snapshot()['authorized_agents']==acl
    assert 'agent_1' not in [a.agent_id for a in spec.agents]


def test_handoff_keeps_progress_and_does_not_widen_acl(sandbox):
    update(sandbox)
    progress=sandbox.public_workflow()['assignment']['progress']
    acl=sandbox.snapshot()['authorized_agents']
    _,decision=sandbox.assess_and_apply('handoff',topology(),'agent_1')
    assert decision['action']=='handoff_and_retire'
    assert sandbox.public_workflow()['assignment']['owner']=='agent_2'
    assert sandbox.public_workflow()['assignment']['progress']==progress
    assert sandbox.snapshot()['authorized_agents']==acl
    assert update(sandbox,'agent_2','next')=='Event updated successfully.'


def test_acl_binding_and_retired_handler(sandbox):
    old=next(t['handler'] for t in sandbox.tools_for('agent_1') if t['name']=='calendar.update_event')
    readonly={t['name'] for t in sandbox.tools_for('agent_3')}
    assert 'calendar.update_event' not in readonly
    assert 'calendar.search_events' in readonly
    assert 'company_directory.find_email_address' in readonly
    assert sandbox._invoke('agent_3','calendar.update_event',{})['error']=='not_authorized'
    sandbox.assess_and_apply('direct',topology(),'agent_1')
    assert old({'event_id':'00000001','field':'event_name','new_value':'bad'})['error']=='inactive_actor'


def test_successful_changed_write_only_deduplicated(sandbox):
    update(sandbox)
    count=len(sandbox.public_workflow()['assignment']['progress'])
    duplicate=update(sandbox,'agent_2')
    assert duplicate['duplicate']
    assert sandbox.logs[-1]['duplicate']
    assert not sandbox.logs[-1]['state_changed']
    assert len(sandbox.public_workflow()['assignment']['progress'])==count
    for _ in range(2):
        result=call(sandbox,'agent_1','calendar.update_event',event_id='missing',field='event_name',new_value='x')
        assert result=='Event not found.'
        assert not sandbox.logs[-1]['duplicate']


def test_rollback_on_invalid_handoff_snapshot(sandbox,monkeypatch):
    before=sandbox.snapshot()
    def fail(data):raise ValueError('injected validation failure')
    monkeypatch.setattr(WorkbenchHandoffSandbox,'_validate_snapshot',staticmethod(fail))
    spec,decision=sandbox.assess_and_apply('handoff',topology(),'agent_1')
    assert spec==topology()
    assert decision['reason']=='transition_rejected'
    assert sandbox.snapshot()==before


def test_tool_exception_restores_partial_native_mutation(sandbox,monkeypatch):
    before=sandbox.native.calendar_events.copy()
    def broken(*args):
        sandbox.native.calendar_events.loc[0,'event_name']='partial'
        raise ValueError('injected tool failure')
    monkeypatch.setattr(sandbox.native,'invoke',broken)
    assert update(sandbox)['error']=='ValueError'
    pd.testing.assert_frame_equal(sandbox.native.calendar_events,before)
    assert not sandbox.logs[-1]['mutation']
    assert not sandbox.snapshot()['dedup']


def test_public_capabilities_intersect_topology_limits(sandbox):
    spec=topology()
    spec=replace(spec,agents=tuple(replace(n,allowed_tools=('workflow_status','calendar.search_events')) if n.agent_id=='agent_2' else n for n in spec.agents))
    sandbox.bind_topology(spec)
    assert sandbox.public_workflow()['tools_allowed']['agent_2']==['calendar.search_events','workflow_status']
    _,decision=sandbox.assess_and_apply('handoff',spec,'agent_1')
    assert decision['reason']=='no_preauthorized_successor'
    assert 'data_root' not in sandbox.public_workflow()


def test_check_preserves_continuing_assignment(sandbox):
    spec,decision=sandbox.assess_and_apply('check',topology(),'agent_1')
    assert spec==topology()
    assert decision['action']=='keep'
