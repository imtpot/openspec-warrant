import subprocess

import pytest

from warrant_evals.checks import CHECKERS

FLAWED = {
    'flaws': [['Unserializable value'], ['0001', 'JSON'], ['report.yaml', 'output path'], ['verification']],
    'verdict': 'REVISE',
}
REPORT = """- blocking: "Unserializable value" has two SHALL clauses.
- blocking: design chooses YAML; decision 0001 says machine output is JSON.
- blocking: `reports/report.yaml` is not in the proposal.
- blocking: tasks.md has no verification group.

**Artifact review: REVISE**
"""


@pytest.fixture
def repo(tmp_path):
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path, check=True)
    return tmp_path


def _messages(params, repo, report):
    return [f.message for f in CHECKERS['artifact-review'](params)(repo, report)]


def test_flawed_report_passes(repo):
    assert _messages(FLAWED, repo, REPORT) == []


def test_missed_flaw_fails(repo):
    report = REPORT.replace('- blocking: tasks.md has no verification group.\n', '')

    assert _messages(FLAWED, repo, report) == ['report lacks: verification']


def test_wrong_or_missing_verdict_fails(repo):
    assert _messages(FLAWED, repo, REPORT.replace('REVISE**', 'PASS**')) == [
        'last line is not "Artifact review: REVISE"'
    ]
    assert _messages(FLAWED, repo, REPORT.replace('**Artifact review: REVISE**\n', 'Done.\n')) == [
        'last line is not "Artifact review: REVISE"'
    ]


def test_sound_artifacts_need_pass(repo):
    assert _messages({'verdict': 'PASS'}, repo, 'No findings.\n\nArtifact review: PASS\n') == []


def test_changed_file_fails(repo):
    (repo / 'notes.md').write_text('x')

    assert _messages({'verdict': 'PASS'}, repo, 'Artifact review: PASS') == ['files changed: ?? notes.md']
