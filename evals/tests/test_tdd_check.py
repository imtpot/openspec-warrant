import json
import shutil
import subprocess
from pathlib import Path

import pytest

from warrant_evals.checks import CHECKERS
from warrant_evals.record import workspace_state

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


def _run(repo, args, code, tool='python3'):
    """Append a run to the log, with the workspace state as it is now."""
    log = repo / '.git' / 'warrant' / 'runs.jsonl'
    log.parent.mkdir(exist_ok=True)
    runs = log.read_text().splitlines() if log.exists() else []
    line = json.dumps({'seq': len(runs), 'tool': tool, 'args': args.split(), 'cwd': str(repo), 'exit': code, 'state': workspace_state(repo)})
    log.write_text('\n'.join([*runs, line]) + '\n')


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


ID = '-m unittest tests.test_quota.QuotaTest.test_not_enough_free'
FULL = '-m unittest discover -s tests -t .'
RED_GREEN = 'no recorded red then green run for: Not enough free'
FULL_MESSAGE = 'full verification not run on the final files'


def _named(repo):
    _implement(repo, comment='')
    t = repo / 'tests' / 'test_quota.py'
    t.write_text(t.read_text().replace('def test_shortfall', 'def test_not_enough_free'))


def _log_runs(repo, implement, red, green=None, full=FULL):
    _run(repo, red, 1)
    implement(repo)
    _run(repo, green or red, 0)
    if full:
        _run(repo, full, 0)


def test_recorded_red_green_by_id_passes(repo):
    _log_runs(repo, _named, ID)

    assert _messages(repo) == []


def test_recorded_red_green_by_module_with_comment_passes(repo):
    _log_runs(repo, _implement, '-m unittest tests.test_quota')

    assert _messages(repo) == []


def test_recorded_red_green_by_class_passes(repo):
    _log_runs(repo, _implement, '-m unittest tests.test_quota.QuotaTest')
    assert _messages(repo) == []


def test_recorded_run_naming_only_the_class_passes(repo):
    _log_runs(repo, _implement, '-m pytest QuotaTest')

    assert _messages(repo) == []


def test_recorded_run_by_file_path_passes(repo):
    _log_runs(repo, _implement, '-m pytest tests/test_quota.py')

    assert _messages(repo) == []


def test_green_without_red_fails_naming_scenario(repo):
    _implement(repo)
    _run(repo, '-m unittest tests.test_quota', 0)
    _run(repo, FULL, 0)

    assert _messages(repo) == [RED_GREEN]


def test_only_passing_runs_fail(repo):
    _implement(repo)
    _run(repo, '-m unittest tests.test_quota', 0)
    (repo / 'notes.md').write_text('x\n')
    _run(repo, '-m unittest tests.test_quota', 0)
    _run(repo, FULL, 0)

    assert _messages(repo) == [RED_GREEN]


def test_green_before_red_fails(repo):
    _run(repo, '-m unittest tests.test_quota', 0)
    _implement(repo)
    _run(repo, '-m unittest tests.test_quota', 1)
    _run(repo, FULL, 0)

    assert _messages(repo) == [RED_GREEN]


def test_red_and_green_on_the_same_files_fail(repo):
    _implement(repo)
    _run(repo, '-m unittest tests.test_quota', 1)
    _run(repo, '-m unittest tests.test_quota', 0)
    _run(repo, FULL, 0)

    assert _messages(repo) == [RED_GREEN]


def test_discover_run_does_not_cover_the_test(repo):
    _log_runs(repo, _named, '-m pytest tests -k not_enough --co discover', full=None)
    _run(repo, FULL, 0)

    assert _messages(repo) == [RED_GREEN]


def test_run_of_another_test_does_not_cover(repo):
    _log_runs(repo, _implement, '-m unittest tests.test_other.OtherTest.test_enough_free', full=None)
    _run(repo, FULL, 0)

    assert _messages(repo) == [RED_GREEN]


def test_k_with_part_of_the_function_name_covers(repo):
    _log_runs(repo, _named, '-m pytest -k not_enough')

    assert _messages(repo) == []


def test_k_with_text_outside_the_function_name_does_not_cover(repo):
    _log_runs(repo, _named, '-m pytest -k not_enough_free_extra', full=None)
    _run(repo, FULL, 0)

    assert _messages(repo) == [RED_GREEN]


def test_full_run_before_the_last_edit_fails(repo):
    _run(repo, ID, 1)
    _named(repo)
    _run(repo, ID, 0)
    _run(repo, FULL, 0)
    (repo / 'notes.md').write_text('x\n')

    assert _messages(repo) == [FULL_MESSAGE]


def test_empty_log_fails_with_both_findings(repo):
    _named(repo)
    (repo / '.git' / 'warrant').mkdir()
    (repo / '.git' / 'warrant' / 'runs.jsonl').write_text('')

    assert _messages(repo) == [RED_GREEN, FULL_MESSAGE]
