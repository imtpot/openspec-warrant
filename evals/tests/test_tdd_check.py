import shutil
import subprocess
from pathlib import Path

import pytest

from warrant_evals.checks import CHECKERS

FIXTURE = Path(__file__).resolve().parents[1] / 'fixtures' / 'tdd-project'
PARAMS = {
    'scenarios': ['Not enough free'],
    'red_green': ['Not enough free'],
    'already': ['Negative request'],
    'count': {'app/quota.py': {'must not be negative': 1}},
    'narrowed': r'python3 -m unittest (?!discover)\S*test',
    'full': 'python3 -m unittest discover',
}
REPORT = """Not enough free: `python3 -m unittest tests.test_quota.QuotaTest.test_not_enough_free`
failed (AssertionError: None != 'short'), then passed after adding the branch (OK).
Negative request: the test passed before any code change; the behavior already exists.
Full run: `python3 -m unittest discover -s tests -t .` exited 0 (OK).
"""


@pytest.fixture
def repo(tmp_path):
    shutil.copytree(FIXTURE, tmp_path, dirs_exist_ok=True)
    for args in (['init', '-q'], ['add', '-A'], ['-c', 'user.name=t', '-c', 'user.email=t@invalid', 'commit', '-qm', 'f']):
        subprocess.run(['git', *args], cwd=tmp_path, check=True)
    return tmp_path


def _implement(repo, comment='    # Shortfall verdict: Not enough free\n'):
    q = repo / 'app' / 'quota.py'
    q.write_text(q.read_text().replace("    return None\n", "    return 'short'\n"))
    t = repo / 'tests' / 'test_quota.py'
    t.write_text(t.read_text() + f"\n{comment}    def test_shortfall(self):\n        self.assertEqual(check(2, 4), 'short')\n")


def _messages(repo, report=REPORT, params=PARAMS):
    return [f.message for f in CHECKERS['tdd'](params)(repo, report)]


def test_complete_tdd_run_passes(repo):
    _implement(repo)

    assert _messages(repo) == []


def test_test_named_after_scenario_passes(repo):
    _implement(repo, comment='')
    t = repo / 'tests' / 'test_quota.py'
    t.write_text(t.read_text().replace('def test_shortfall', 'def test_not_enough_free'))

    assert _messages(repo) == []


def test_untraced_test_fails(repo):
    _implement(repo, comment='')

    assert _messages(repo) == ['no added test names scenario: Not enough free']


def test_pass_without_prior_failure_fails(repo):
    _implement(repo)
    report = REPORT.replace('failed (AssertionError: None != \'short\'), then ', '')

    assert _messages(repo, report) == ['no failing result before the passing one for: Not enough free']


def test_code_written_for_present_behavior_fails(repo):
    _implement(repo)
    q = repo / 'app' / 'quota.py'
    q.write_text(q.read_text() + "\n\ndef validate(needed):\n    if needed < 0:\n        raise ValueError('needed must not be negative')\n")

    assert _messages(repo) == ['app/quota.py has 2 x "must not be negative", expected 1']


def test_missing_commands_and_checked_task_fail(repo):
    _implement(repo)
    tasks = repo / 'openspec' / 'changes' / 'add-quota-verdicts' / 'tasks.md'
    tasks.write_text(tasks.read_text().replace('- [ ]', '- [x]'))
    report = 'Not enough free failed, then passed. Negative request already exists.'

    assert _messages(repo, report) == [
        'no narrowed test command', 'transcript lacks: python3 -m unittest discover',
        'tasks.md changed: openspec/changes/add-quota-verdicts/tasks.md',
    ]


def test_transcript_groups_are_checked(repo):
    _implement(repo)

    assert _messages(repo, params={**PARAMS, 'transcript': [['Scenarios:', 'scenarios']]}) == [
        'transcript lacks: Scenarios:'
    ]


def test_red_label_and_error_class_count_as_failure(repo):
    _implement(repo)
    report = REPORT.replace("failed (AssertionError: None != 'short'), then passed after adding the branch (OK).",
                            "red - `AssertionError: None != 'short'`; green - `OK`.")

    assert _messages(repo, report) == []
