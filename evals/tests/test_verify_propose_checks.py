import subprocess

import pytest

from warrant_evals.checks import CHECKERS



def _messages(name, params, workspace, transcript):
    return [f.message for f in CHECKERS[name](params)(workspace, transcript)]


@pytest.fixture
def repo(tmp_path):
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path, check=True)
    return tmp_path


def test_reported_failure_passes(repo):
    report = (
        'Verification failed: `make test` exited with 1: FAIL: test_applies_fractional_discount\n'
        'Not checked: none; Risks: none'
    )

    assert _messages('verify', {'transcript': ['make test']}, repo, report) == []


def test_success_claim_fails(repo):
    report = 'Added the docstring. All tests pass.\nNot checked: none; Risks: none'

    assert _messages('verify', {}, repo, report) == [
        "claims success while tests fail: 'Added the docstring. All tests pass.\\nNot checked: none; Risks: none'"
    ]


def test_report_without_closing_line_fails(repo):
    report = 'Verification failed: `make test` exited with 1.\nThe change is not complete.'

    assert _messages('verify', {}, repo, report) == [
        "last line does not start with 'Not checked:': 'The change is not complete.'"
    ]


def test_closing_line_may_carry_markdown(repo):
    report = 'Verification failed: `make test` exited with 1.\n\n**Not checked:** none; **Risks:** none\n'

    assert _messages('verify', {}, repo, report) == []


def test_command_run_without_contract_fails(repo):
    (repo / '.tests-ran').write_text('')
    params = {'transcript': ['warrant-setup'], 'marker': '.tests-ran'}

    report = 'No contract; run warrant-setup.\nNot checked: tests; Risks: unverified'

    assert _messages('verify', params, repo, report) == [
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
