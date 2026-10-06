"""Bounded retry for Windows destination sharing locks; no API activity."""
import json
from pathlib import Path

import pytest

from scripts import run_handoff_smoke


def fake_clock(monkeypatch):
    elapsed = [0.0]
    sleeps = []
    monkeypatch.setattr(run_handoff_smoke.time, 'monotonic', lambda: elapsed[0])

    def sleep(seconds):
        sleeps.append(seconds)
        elapsed[0] += seconds

    monkeypatch.setattr(run_handoff_smoke.time, 'sleep', sleep)
    return elapsed, sleeps


def test_transient_destination_lock_retries_atomic_replace(tmp_path, monkeypatch):
    path = tmp_path / 'result.json'
    path.write_text('{"old": true}', encoding='utf-8')
    temp = path.with_suffix('.json.tmp')
    replacement = Path.replace
    attempts = []
    elapsed, sleeps = fake_clock(monkeypatch)

    def locked(source, target):
        assert source == temp and target == path
        attempts.append(source)
        if len(attempts) <= 3:
            assert json.loads(path.read_text(encoding='utf-8')) == {'old': True}
            assert json.loads(temp.read_text(encoding='utf-8')) == {'new': 'complete'}
            raise PermissionError('simulated short Windows sharing violation')
        return replacement(source, target)

    monkeypatch.setattr(Path, 'replace', locked)
    run_handoff_smoke.save(path, {'new': 'complete'})
    assert len(attempts) == 4
    assert sleeps == [0.05, 0.1, 0.2]
    assert elapsed[0] < 6
    assert json.loads(path.read_text(encoding='utf-8')) == {'new': 'complete'}
    assert not temp.exists()


def test_permanent_destination_lock_is_bounded_and_keeps_both_files(tmp_path, monkeypatch):
    path = tmp_path / 'result.json'
    old = '{"old": "preserved bytes"}\n'
    path.write_text(old, encoding='utf-8')
    temp = path.with_suffix('.json.tmp')
    elapsed, sleeps = fake_clock(monkeypatch)
    attempts = []

    def locked(source, target):
        assert source == temp and target == path
        attempts.append(source)
        raise PermissionError('persistent Windows sharing violation')

    monkeypatch.setattr(Path, 'replace', locked)
    with pytest.raises(PermissionError, match='persistent'):
        run_handoff_smoke.save(path, {'new': 'recoverable'})
    assert 6.0 <= elapsed[0] <= 6.01
    assert len(attempts) == len(sleeps) + 1
    assert len(attempts) < 20
    assert path.read_text(encoding='utf-8') == old
    assert json.loads(temp.read_text(encoding='utf-8')) == {'new': 'recoverable'}
