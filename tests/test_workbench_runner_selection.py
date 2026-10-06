"""Offline selection/seed regression; no data files, secrets, or API requests."""
import random

import pytest

from MAS.self_evolved.handoff_runtime import ARMS
from MAS.self_evolved.workbench_cases import CASE_IDS
from scripts.run_workbench_retirement import (
    case_schedule,
    manifest_call_limits,
    select_source_cases,
)


def manifest():
    return {'candidates': [{'task_id': case_id} for case_id in CASE_IDS]}


def test_default_selection_preserves_full_original_batch():
    selected = select_source_cases(manifest())
    assert [index for index, _ in selected] == list(range(6))
    assert [item['task_id'] for _, item in selected] == list(CASE_IDS)


def test_subset_preserves_manifest_order_and_original_seed_indices():
    chosen = ['project_management_40', 'email_53', 'project_management_2']
    selected = select_source_cases(manifest(), chosen)
    assert [index for index, _ in selected] == [3, 4, 5]
    assert [item['task_id'] for _, item in selected] == list(CASE_IDS[3:])
    for source_index, _ in selected:
        expected_order = list(ARMS)
        random.Random(20261007 + source_index).shuffle(expected_order)
        schedule = case_schedule(20261007, source_index)
        assert schedule == {
            'case_seed': 20261007 + source_index,
            'future_seed': 20262007 + source_index,
            'arm_order': expected_order,
        }


@pytest.mark.parametrize('selection', [[], ['email_53', 'email_53'], ['unknown'], ['email_53', 'unknown']])
def test_reject_empty_duplicate_unknown_selections(selection):
    with pytest.raises(ValueError):
        select_source_cases(manifest(), selection)


def test_invalid_full_manifest_cannot_hide_behind_valid_subset():
    frozen = manifest()
    frozen['candidates'][-1] = {'task_id': 'email_53'}
    with pytest.raises(ValueError):
        select_source_cases(frozen, ['calendar_20'])


def test_original_index_is_manifest_position_not_request_or_builtin_order():
    frozen = manifest()
    frozen['candidates'].reverse()
    selected = select_source_cases(frozen, ['calendar_20', 'email_53'])
    assert [(index, item['task_id']) for index, item in selected] == [(2, 'email_53'), (5, 'calendar_20')]


def test_manifest_limits_default_and_explicit_keys():
    assert manifest_call_limits(manifest()) == {'max_calls': 120, 'max_input': 650000}
    frozen = manifest()
    frozen['frozen_protocol'] = {'api_requests_per_case': 180, 'max_input_tokens_per_case': 1000000}
    assert manifest_call_limits(frozen) == {'max_calls': 180, 'max_input': 1000000}


@pytest.mark.parametrize('bad', [0, -1, True, '180', 180.5])
def test_invalid_limits_rejected(bad):
    frozen = manifest()
    frozen['frozen_protocol'] = {'api_requests_per_case': bad}
    with pytest.raises(ValueError):
        manifest_call_limits(frozen)
