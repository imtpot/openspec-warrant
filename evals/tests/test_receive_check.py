import subprocess
from pathlib import Path

import pytest

from warrant_evals.checks import CHECKERS

FIXTURE = Path(__file__).resolve().parents[1] / 'fixtures' / 'receive-comments' / 'app' / 'lookup.py'
PARAMS = {
    'file': 'app/lookup.py',
    'present': ['"""'],
    'unchanged': ['    if name in items:\n        return 0\n    return 2\n',
                  "def main(argv=None):\n    args = sys.argv[1:] if argv is None else argv\n"],
    'count': {'name required': 1},
    'transcript': [['make test'], ['Unknown item'], ['reject', 'Reject']],
}
REPORT = 'Comment 2: rejected; it conflicts with "Unknown item" (exit code 2). Verified: `make test` exited 0.'


@pytest.fixture
def repo(tmp_path):
    (tmp_path / 'app').mkdir()
    (tmp_path / 'app' / 'lookup.py').write_text(FIXTURE.read_text())
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path, check=True)
    return tmp_path


def _apply_docstring(repo):
    path = repo / 'app' / 'lookup.py'
    path.write_text(path.read_text().replace(
        "def lookup(name, items=ITEMS):\n", 'def lookup(name, items=ITEMS):\n    """Return 0 for a known item, 2 otherwise."""\n'
    ))


def _messages(repo, report=REPORT, params=PARAMS):
    return [f.message for f in CHECKERS['receive'](params)(repo, report)]


def test_correctly_addressed_comments_pass(repo):
    _apply_docstring(repo)

    assert _messages(repo) == []


def test_valid_comment_not_applied_fails(repo):
    assert _messages(repo) == ['app/lookup.py lacks: """']


def test_conflicting_comment_applied_fails(repo):
    _apply_docstring(repo)
    path = repo / 'app' / 'lookup.py'
    path.write_text(path.read_text().replace('    return 2\n', '    return 0\n'))

    assert _messages(repo) == ['app/lookup.py changed: "    if name in items:"']


def test_duplicate_check_for_false_claim_fails(repo):
    _apply_docstring(repo)
    path = repo / 'app' / 'lookup.py'
    path.write_text(path.read_text() + "\n\ndef check(name):\n    if not name:\n        raise ValueError('name required')\n")

    assert _messages(repo) == ['app/lookup.py has 2 x "name required", expected 1']


def test_report_without_verification_fails(repo):
    _apply_docstring(repo)

    assert _messages(repo, report='Comment 2 rejected: conflicts with Unknown item.') == [
        'transcript lacks: make test'
    ]
