import json
import subprocess

import pytest

from warrant_evals.checks import CHECKERS
from warrant_evals.record import run_log, workspace_state


def _run(repo, args, code, tool='python3'):
    """Append a run to the log, with the workspace state as it is now."""
    log = run_log(repo)
    log.parent.mkdir(exist_ok=True)
    runs = log.read_text().splitlines() if log.exists() else []
    line = json.dumps({'seq': len(runs), 'tool': tool, 'args': args.split(), 'cwd': str(repo), 'exit': code, 'state': workspace_state(repo)})
    log.write_text('\n'.join([*runs, line]) + '\n')


def _messages(name, params, workspace, transcript):
    return [f.message for f in CHECKERS[name](params)(workspace, transcript)]


@pytest.fixture
def repo(tmp_path):
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path, check=True)
    return tmp_path


def test_reported_failure_passes(repo):
    report = 'Verification failed: `make test` exited with 1: FAIL: test_applies_fractional_discount'

    assert _messages('verify', {'transcript': ['make test']}, repo, report) == []


def test_success_claim_fails(repo):
    assert _messages('verify', {}, repo, 'Added the docstring. All tests pass.') == [
        "claims success while tests fail: 'Added the docstring. All tests pass.'"
    ]


def test_command_run_without_contract_fails(repo):
    (repo / '.tests-ran').write_text('')
    params = {'transcript': ['warrant-setup'], 'marker': '.tests-ran'}

    assert _messages('verify', params, repo, 'No contract; run warrant-setup.') == [
        'verification ran although the project has no contract'
    ]


SPEC = """## ADDED Requirements

### Requirement: JSON mode
WHEN `--json` is passed, the report command SHALL print one JSON object.

#### Scenario: JSON
- **WHEN** `--json` is passed
- **THEN** stdout parses as JSON
"""


def _change(repo, spec=SPEC, proposal='# Proposal\n\n## Assumptions\n\n- x. Owner: y\n'):
    change = repo / 'openspec' / 'changes' / 'add-json-report'
    (change / 'specs' / 'report').mkdir(parents=True, exist_ok=True)
    (change / 'proposal.md').write_text(proposal)
    (change / 'specs' / 'report' / 'spec.md').write_text(spec)


def test_propose_with_clean_artifacts_passes(repo):
    _change(repo)

    assert _messages('propose', {'change': 'add-json-report'}, repo, '') == []


def test_propose_reports_spec_and_proposal_findings(repo):
    _change(repo, SPEC.replace('WHEN `--json` is passed, the', 'The'), '# Proposal\n')

    assert _messages('propose', {'change': 'add-json-report'}, repo, '') == ['no Assumptions section']
    _change(repo, SPEC.replace('object.', 'object and SHALL exit 0.'))
    assert _messages('propose', {'change': 'add-json-report'}, repo, '') == [
        '2 SHALL clauses; write one requirement per outcome'
    ]


def test_missing_change_fails(repo):
    assert _messages('propose', {'change': 'add-json-report'}, repo, '') == [
        'openspec/changes/add-json-report/proposal.md missing'
    ]


def test_discovery_needs_every_skill_and_the_contract_command(repo):
    params = {'transcript': ['warrant-setup', 'warrant-minimal-change', 'warrant-verify', 'make test']}

    assert _messages('discovery', params, repo, 'warrant-setup, warrant-verify; contract runs `make test`') == [
        'transcript lacks: warrant-minimal-change'
    ]


FULL_MESSAGE = 'full verification not run on the final files'
FAILURE_REPORT = 'Verification failed: `make test` exited with 1'


def test_full_run_on_final_files_passes(repo):
    (repo / 'a.py').write_text('x = 1\n')
    _run(repo, 'test', 1, tool='make')

    assert _messages('verify', {'full': 'make test'}, repo, FAILURE_REPORT) == []


def test_edit_after_full_run_fails(repo):
    (repo / 'a.py').write_text('x = 1\n')
    _run(repo, 'test', 1, tool='make')
    (repo / 'a.py').write_text('x = 2\n')

    assert _messages('verify', {'full': 'make test'}, repo, FAILURE_REPORT) == [FULL_MESSAGE]


def test_new_file_after_full_run_fails(repo):
    _run(repo, 'test', 1, tool='make')
    (repo / 'notes.md').write_text('x\n')

    assert _messages('verify', {'full': 'make test'}, repo, FAILURE_REPORT) == [FULL_MESSAGE]


def test_full_run_never_made_fails(repo):
    _run(repo, '-m unittest', 1)

    assert _messages('verify', {'full': 'make test'}, repo, FAILURE_REPORT) == [FULL_MESSAGE]


def test_empty_log_fails(repo):
    run_log(repo).parent.mkdir()
    run_log(repo).write_text('')

    assert _messages('verify', {'full': 'make test'}, repo, FAILURE_REPORT) == [FULL_MESSAGE]


def test_last_full_run_counts(repo):
    _run(repo, 'test', 1, tool='make')
    (repo / 'a.py').write_text('x = 1\n')
    _run(repo, 'test', 1, tool='make')

    assert _messages('verify', {'full': 'make test'}, repo, FAILURE_REPORT) == []


def test_without_log_full_is_not_checked(repo):
    assert _messages('verify', {'full': 'make test'}, repo, FAILURE_REPORT) == []
