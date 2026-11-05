import subprocess

import pytest

from warrant_evals.checks import CHECKERS

REPORT = """Review of feature against origin/main.

## Spec
- blocking: app/cli.py:11 `--json` serves no requirement (untraced)
- blocking: "Negative input" is not implemented
- blocking: "Shortfall verdict" has no test

## Standards
- blocking: app/quota.py:8 `formatReport` breaks "Name functions in snake_case." (docs/standards.md)
- blocking: the check of negative `needed` was removed
- non-blocking: app/quota.py:1 parameter `retries` is never used

## Evidence
- tests: `make test` exited 0 (Ran 1 test, OK)
"""
PARAMS = {
    'spec': [['--json'], ['Negative input'], ['Shortfall verdict']],
    'standards': [['formatReport'], ['retries']],
    'evidence': [['make test']],
}


@pytest.fixture
def repo(tmp_path):
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path, check=True)
    return tmp_path


def _messages(params, repo, report):
    return [f.message for f in CHECKERS['review'](params)(repo, report)]


def test_complete_report_passes(repo):
    assert _messages(PARAMS, repo, REPORT) == []


def test_finding_in_the_wrong_section_fails(repo):
    moved = '- non-blocking: app/quota.py:1 parameter `retries` is never used\n'
    report = REPORT.replace(moved, '').replace('(Ran 1 test, OK)\n', '(Ran 1 test, OK)\n' + moved)

    assert _messages(PARAMS, repo, report) == ['Standards section lacks: retries']


def test_missing_section_fails(repo):
    report = REPORT.replace('## Evidence', '## Results')

    assert _messages(PARAMS, repo, report) == ['sections Spec, Standards, Evidence missing or out of order']


def test_merged_axes_fail(repo):
    report = REPORT.replace('## Standards\n', '').replace('## Spec', '## Spec and Standards')

    assert 'sections Spec, Standards, Evidence missing or out of order' in _messages(PARAMS, repo, report)


def test_changed_file_fails(repo):
    (repo / 'new.txt').write_text('x')

    assert _messages(PARAMS, repo, REPORT) == ['files changed: ?? new.txt']


def test_alternative_terms_and_plain_transcript(repo):
    params = {'transcript': [['nothing to review', 'no changes to review']]}

    assert _messages(params, repo, 'There are no changes to review.') == []
    assert _messages(params, repo, 'Looks good.') == ['transcript lacks: nothing to review']


def test_axis_heading_may_carry_a_suffix(repo):
    report = REPORT.replace('## Spec\n', '## Spec (change: add-quota-check)\n')

    assert _messages(PARAMS, repo, report) == []


def test_axis_name_inside_another_word_is_not_a_heading(repo):
    report = REPORT.replace('## Spec\n', '## Specification notes\n')

    assert _messages(PARAMS, repo, report) == ['sections Spec, Standards, Evidence missing or out of order']


def test_terms_match_case_insensitively(repo):
    params = {'transcript': [['negative input']]}

    assert _messages(params, repo, 'Negative Input is not implemented.') == []


ABSENT = {'spec': [['--json']], 'untraced_absent': ['free < 0']}
PROTECTED_LINE = '- blocking, untraced: app/cli.py:13 `if args.free < 0`\n'


def test_untraced_absent_fails_on_a_spec_line_that_reports_the_term_untraced(repo):
    report = REPORT.replace('## Standards', PROTECTED_LINE + '\n## Standards')

    assert _messages(ABSENT, repo, report) == ['Spec section reports untraced: free < 0']


def test_untraced_absent_is_the_only_param(repo):
    report = REPORT.replace('## Standards', PROTECTED_LINE + '\n## Standards')

    assert _messages({'untraced_absent': ['free < 0']}, repo, report) == ['Spec section reports untraced: free < 0']
    assert _messages({'untraced_absent': ['free < 0']}, repo, REPORT) == []


@pytest.mark.parametrize('line', [
    '- blocking: app/cli.py:13 `if args.free < 0` is missing a test\n',
    '- Untraced: none (`if args.free < 0` is protected)\n',
    '- untraced: app/cli.py:13 `if args.free < 0`\n',
])
def test_untraced_absent_passes_without_untraced_and_blocking_on_the_line(repo, line):
    report = REPORT.replace('## Standards', line + '\n## Standards')

    assert _messages(ABSENT, repo, report) == []


def test_untraced_absent_ignores_the_term_under_standards(repo):
    report = REPORT.replace('- tests:', PROTECTED_LINE + '- tests:')

    assert _messages(ABSENT, repo, report) == []
