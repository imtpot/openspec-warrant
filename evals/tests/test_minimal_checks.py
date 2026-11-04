import subprocess

import pytest

from warrant_evals.checks import CHECKERS


def _git(path, *args):
    subprocess.run(['git', *args], cwd=path, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    (tmp_path / 'app').mkdir()
    (tmp_path / 'app' / 'report.py').write_text('def report(title):\n    return title\n')
    _git(tmp_path, 'init', '-q')
    _git(tmp_path, 'add', '-A')
    _git(tmp_path, '-c', 'user.name=t', '-c', 'user.email=t@invalid', 'commit', '-q', '-m', 'f')
    return tmp_path


def _messages(name, params, workspace, transcript=''):
    return [f.message for f in CHECKERS[name](params)(workspace, transcript)]


def test_reusing_the_helper_passes(repo):
    (repo / 'app' / 'report.py').write_text(
        'from app.text import slugify\n\n\ndef report(title):\n    return slugify(title)\n'
    )

    assert _messages('minimal-change', {'helper': 'slugify', 'file': 'app/report.py'}, repo) == []


def test_new_function_fails(repo):
    (repo / 'app' / 'report.py').write_text(
        'def make_slug(t):\n    return t.lower()\n\n\ndef report(title):\n    return make_slug(title)\n'
    )

    assert _messages('minimal-change', {'helper': 'slugify', 'file': 'app/report.py'}, repo) == [
        'added function make_slug; the existing helper slugify already does this'
    ]


def test_untouched_file_fails(repo):
    assert _messages('minimal-change', {'helper': 'slugify', 'file': 'app/report.py'}, repo) == [
        'app/report.py was not changed'
    ]


LEDGER = """app/fetch.py:2 - limit: first 100 items only - upgrade: paginate when a project exceeds 100
app/retry.py:2 - limit: no retries - upgrade: none no-trigger
2 shortcuts, 1 without trigger.
"""
PARAMS = {'entries': ['app/fetch.py:2', 'app/retry.py:2'], 'no_trigger': ['app/retry.py:2'], 'total': 2}


def test_complete_ledger_passes(repo):
    assert _messages('ledger', PARAMS, repo, LEDGER) == []


def test_ledger_missing_tag_and_entry_fails(repo):
    transcript = 'app/retry.py:2 - limit: no retries\n1 shortcuts, 0 without trigger.\n'

    assert _messages('ledger', PARAMS, repo, transcript) == [
        'ledger lacks app/fetch.py:2',
        'app/retry.py:2 not tagged no-trigger',
        'ledger total is not 2',
    ]


def test_ledger_that_changes_files_fails(repo):
    (repo / 'app' / 'report.py').write_text('changed\n')

    assert _messages('ledger', PARAMS, repo, LEDGER) == ['files changed: M app/report.py']


def test_leftover_file_fails(repo):
    (repo / 'app' / 'report.py').write_text(
        'from app.text import slugify\n\n\ndef report(title):\n    return slugify(title)\n'
    )
    (repo / 'app' / 'report.py.new').write_text('copy\n')

    assert _messages('minimal-change', {'helper': 'slugify', 'file': 'app/report.py'}, repo) == [
        'file left in the change: app/report.py.new'
    ]
