import subprocess

import pytest

from warrant_evals.checks import CHECKERS, question_sentences

GOOD = """I read pyproject.toml: the tool supports Python 3.12 and later, so I won't ask about that.

First decision: where should the free-capacity report go?

- **stdout as JSON** (recommended): scripts already read JSON, see decision 0001.
- **a file**: needs a path option.

Which one do you want?
"""


@pytest.fixture
def repo(tmp_path):
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path, check=True)
    return tmp_path


def _messages(name, params, repo, transcript):
    return [f.message for f in CHECKERS[name](params)(repo, transcript)]


def test_question_sentences_skip_lists_and_code():
    text = 'Use `x?` here.\n\n- Option a?\n| a? |\n\nIs that ok? Yes. Really?\n'

    assert question_sentences(text) == ['Is that ok?', 'Really?']


PARAMS = {'not_asked': ['Python']}


def test_first_question_passes(repo):
    text = GOOD.replace('First decision: where should the free-capacity report go?\n\n', 'First decision, the output target.\n\n')

    assert _messages('first-question', PARAMS, repo, text) == []


def test_choice_prompt_alone_is_the_question(repo):
    text = 'Options:\n\n- **JSON** (recommended)\n- **text**\n\nWhich do you want?\n'

    assert _messages('first-question', PARAMS, repo, text) == []


def test_closing_choice_prompt_repeats_the_question(repo):
    assert _messages('first-question', PARAMS, repo, GOOD) == []


def test_two_questions_fail(repo):
    text = GOOD.replace('Which one do you want?', 'And should it also exit with code 1 when capacity is low?')

    assert _messages('first-question', PARAMS, repo, text) == ['2 questions asked, expected 1']


def test_no_recommendation_fails(repo):
    text = GOOD.replace(' (recommended)', '').replace('First decision: where should the free-capacity report go?\n\n', '')

    assert _messages('first-question', PARAMS, repo, text) == ['no recommended option']


def test_asking_a_known_fact_fails(repo):
    text = 'Which Python versions should the tool support?\n\n- **3.12+** (recommended)\n'

    assert _messages('first-question', PARAMS, repo, text) == ['asked about a known fact: Python']


def test_changed_file_fails(repo):
    (repo / 'notes.md').write_text('x')
    text = GOOD.replace('First decision: where should the free-capacity report go?\n\n', '')

    assert _messages('first-question', PARAMS, repo, text) == ['files changed: ?? notes.md']


GLOSSARY = '# Project terms\n\n| Term | Meaning |\n| --- | --- |\n| Quota | The limit a cloud project sets on a resource |\n'
DECISION = '# Use JSON\n\n## Context\n\nx\n\n## Decision\n\ny\n\n## Consequences\n\nz\n'
RECORD = {
    'glossary': 'docs/glossary.md', 'terms': ['Headroom'],
    'decisions': 'docs/decisions', 'decision_terms': ['stdout'],
}


@pytest.fixture
def project(repo):
    (repo / 'docs' / 'decisions').mkdir(parents=True)
    (repo / 'docs' / 'glossary.md').write_text(GLOSSARY)
    (repo / 'docs' / 'decisions' / '0001-use-json.md').write_text(DECISION)
    (repo / 'openspec' / 'changes' / 'archive').mkdir(parents=True)
    subprocess.run(['git', 'add', '-A'], cwd=repo, check=True)
    subprocess.run(['git', '-c', 'user.name=t', '-c', 'user.email=t@invalid', 'commit', '-qm', 'f'], cwd=repo, check=True)
    return repo


def _record(project, decision=DECISION.replace('JSON', 'stdout'), name='0002-report-to-stdout.md'):
    with (project / 'docs' / 'glossary.md').open('a') as f:
        f.write('| Headroom | Free quota after reservations |\n')
    (project / 'docs' / 'decisions' / name).write_text(decision)


def test_recorded_term_and_decision_pass(project):
    _record(project)

    assert _messages('design-record', RECORD, project, 'Next: run openspec-propose.') == []


def test_missing_records_fail(project):
    assert _messages('design-record', RECORD, project, 'Next: run openspec-propose.') == [
        'docs/glossary.md lacks: Headroom', 'no new decision file 0002-*.md in docs/decisions',
    ]


def test_decision_without_sections_fails(project):
    _record(project, decision='# Report to stdout\n\nWe chose stdout.\n')

    assert _messages('design-record', RECORD, project, 'Next: run openspec-propose.') == [
        '0002-report-to-stdout.md lacks ## Context', '0002-report-to-stdout.md lacks ## Decision',
        '0002-report-to-stdout.md lacks ## Consequences',
    ]


def test_changed_existing_records_and_new_change_fail(project):
    _record(project)
    (project / 'docs' / 'decisions' / '0001-use-json.md').write_text('rewritten\n')
    (project / 'openspec' / 'changes' / 'add-report').mkdir()

    assert _messages('design-record', RECORD, project, 'done') == [
        'existing record changed: docs/decisions/0001-use-json.md',
        'OpenSpec change created: add-report',
        'transcript lacks: openspec-propose',
    ]


def test_rewritten_glossary_entry_fails(project):
    _record(project)
    path = project / 'docs' / 'glossary.md'
    path.write_text(path.read_text().replace('on a resource', 'on any resource'))

    assert _messages('design-record', RECORD, project, 'Next: run openspec-propose.') == [
        'existing glossary line changed: | Quota | The limit a cloud project sets on a resource |'
    ]


def test_repeated_identical_question_counts_once(repo):
    text = 'Should CI pass the numbers in?\n\n- **yes** (recommended)\n\nShould CI pass the numbers in?\n'

    assert _messages('first-question', PARAMS, repo, text) == []
