import json
import shutil
from pathlib import Path
import subprocess

import pytest

from warrant_evals import benchmark
from warrant_evals.benchmark import Run
from warrant_evals.requirements import check_proposal, check_spec

CONTRACT = """# Quota demo

Intro.

## Warrant contract

### Verification

- tests: `make test`

### Destructive actions

### Glossary

none

### Standards

- `docs/standards.md`

## Other

Kept.
"""


def test_claude_tokens_sum_input_cache_and_output(tmp_path):
    stdout = json.dumps({'result': 'ok', 'usage': {
        'input_tokens': 2, 'cache_creation_input_tokens': 10, 'cache_read_input_tokens': 100, 'output_tokens': 4,
    }})

    assert benchmark.tokens('claude', stdout, tmp_path / 'usage.json') == 116


def test_codex_tokens_from_usage_line(tmp_path):
    assert benchmark.tokens('codex', 'done\ntokens used\n21,806\n', tmp_path / 'usage.json') == 21806


def test_missing_usage_is_not_measured(tmp_path):
    assert benchmark.tokens('codex', 'ok', tmp_path / 'usage.json') is None
    assert benchmark.tokens('claude', 'not json', tmp_path / 'usage.json') is None


def test_claude_report_is_the_json_result():
    assert benchmark.report_text('claude', json.dumps({'result': 'Review done.'})) == 'Review done.'
    assert benchmark.report_text('codex', 'Review done.') == 'Review done.'


def test_contract_becomes_plain_text():
    text = benchmark.contract_as_text(CONTRACT)

    assert '## Warrant contract' not in text
    assert '`make test`' in text
    assert '`docs/standards.md`' in text
    assert text.startswith('# Quota demo\n\nIntro.\n')
    assert text.endswith('## Other\n\nKept.\n')


def test_claude_benchmark_command_skips_user_settings(tmp_path):
    agents = {a.name: a for a in benchmark.bench_agents(tmp_path / 'usage.json')}

    claude = agents['claude'].argv('go')
    assert claude[claude.index('--setting-sources') + 1] == 'project,local'
    assert claude[claude.index('--output-format') + 1] == 'json'
    assert sorted(agents) == ['claude', 'codex']


def test_review_score_counts_named_problems():
    problems = [['formatReport'], ['retries'], ['swap', 'args.free']]

    assert benchmark.review_score('formatReport is camelCase; RETRIES is unused.', problems) == (pytest.approx(2 / 3), ['swap'])


REFERENCE = 'def double(x):\n    return 2 * x\n'
FAULTS = {'add.py': 'def double(x):\n    return x + 2\n', 'same.py': 'def double(x):\n    return x * 2\n'}


@pytest.fixture
def task(tmp_path):
    workspace = tmp_path / 'workspace'
    (workspace / 'app').mkdir(parents=True)
    (workspace / 'tests').mkdir()
    (workspace / 'app' / '__init__.py').write_text('')
    (workspace / 'tests' / '__init__.py').write_text('')
    (workspace / 'app' / 'calc.py').write_text(REFERENCE)
    hidden = tmp_path / 'hidden'
    (hidden / 'faults').mkdir(parents=True)
    (hidden / 'reference.py').write_text(REFERENCE)
    for name, code in FAULTS.items():
        (hidden / 'faults' / name).write_text(code)
    (hidden / 'acceptance').mkdir()
    (hidden / 'acceptance' / 'test_acceptance.py').write_text(
        'import unittest\nfrom app.calc import double\n\n'
        'class T(unittest.TestCase):\n'
        '    def test_two(self):\n        self.assertEqual(double(2), 4)\n'
        '    def test_three(self):\n        self.assertEqual(double(3), 6)\n'
    )
    return workspace, hidden


def _agent_test(workspace, body):
    (workspace / 'tests' / 'test_calc.py').write_text(
        'import unittest\nfrom app.calc import double\n\nclass T(unittest.TestCase):\n'
        f'    def test_it(self):\n        {body}\n'
    )


def test_fault_detection_counts_rejected_faults(task):
    workspace, hidden = task
    _agent_test(workspace, 'self.assertEqual(double(3), 6)')

    assert benchmark.fault_detection(workspace, hidden, 'app/calc.py') == (pytest.approx(1 / 2), ['same.py'])
    assert (workspace / 'app' / 'calc.py').read_text() == REFERENCE


def test_tests_failing_on_reference_are_not_measured(task):
    workspace, hidden = task
    _agent_test(workspace, 'self.assertEqual(double(3), 7)')

    assert benchmark.fault_detection(workspace, hidden, 'app/calc.py') == (None, [])


def test_no_agent_tests_detect_nothing(task):
    workspace, hidden = task

    assert benchmark.fault_detection(workspace, hidden, 'app/calc.py') == (0, ['add.py', 'same.py'])


def test_acceptance_counts_passed_hidden_tests(task):
    workspace, hidden = task
    (workspace / 'app' / 'calc.py').write_text('def double(x):\n    return 4\n')

    assert benchmark.acceptance(workspace, hidden) == 1
    assert not (workspace / 'acceptance').exists()


def test_added_lines_exclude_tests_and_openspec(task):
    workspace, _ = task
    (workspace / 'openspec').mkdir()
    (workspace / 'openspec' / 'tasks.md').write_text('- [ ] 1.1\n')
    for args in (['init', '-q'], ['add', '-A'], ['-c', 'user.name=t', '-c', 'user.email=t@invalid', 'commit', '-qm', 'f']):
        subprocess.run(['git', *args], cwd=workspace, check=True)
    (workspace / 'app' / 'calc.py').write_text(REFERENCE + '\n\ndef half(x):\n    return x / 2\n')
    _agent_test(workspace, 'pass')
    (workspace / 'openspec' / 'tasks.md').write_text('- [x] 1.1\n')

    assert benchmark.added_lines(workspace) == 4


def test_summary_shows_means_and_runs():
    runs = [
        Run('implement', 'claude', 'warrant', {'faults': 1.0, 'tokens': 100}),
        Run('implement', 'claude', 'warrant', {'faults': 2 / 3, 'tokens': None}),
        Run('implement', 'claude', 'warrant', {'faults': 1.0, 'tokens': 200}),
        Run('implement', 'claude', 'bare', {'faults': None, 'tokens': 50}),
    ]

    table = benchmark.summary(runs)

    assert '| implement | claude | bare | 1 | n/a | 50 (1) |' in table
    assert '| implement | claude | warrant | 3 | 0.89 (3) | 150 (2) |' in table
    assert table.index('| bare |') < table.index('| warrant |')


def test_prepared_arms_install_the_right_skills(tmp_path, monkeypatch):
    installed = []
    monkeypatch.setattr(benchmark, 'prepare_workspace', lambda workspace, source, extra=(): installed.append((source, *extra)))
    monkeypatch.setattr(benchmark, 'openspec_skills', lambda: tmp_path / 'openspec-skills')
    for arm in benchmark.ARMS:
        workspace = tmp_path / arm
        (workspace / 'openspec').mkdir(parents=True)
        (workspace / 'openspec' / 'config.yaml').write_text('schema: spec-driven\n')
        (workspace / 'AGENTS.md').write_text(CONTRACT)
        benchmark.prepare_arm(workspace, arm)

    assert installed == [(tmp_path / 'openspec-skills',), (benchmark.REPO, tmp_path / 'openspec-skills')]
    assert '## Warrant contract' not in (tmp_path / 'bare' / 'AGENTS.md').read_text()
    assert '## Warrant contract' not in (tmp_path / 'openspec' / 'AGENTS.md').read_text()
    assert '## Warrant contract' in (tmp_path / 'warrant' / 'AGENTS.md').read_text()
    assert '[warrant] ' in (tmp_path / 'warrant' / 'openspec' / 'config.yaml').read_text()
    assert '[warrant] ' not in (tmp_path / 'openspec' / 'openspec' / 'config.yaml').read_text()


def test_main_runs_every_arm_and_writes_the_table(tmp_path, monkeypatch):
    fixture = tmp_path / 'fixture'
    fixture.mkdir()
    (fixture / 'AGENTS.md').write_text('# Demo\n')
    task = {'name': 'review', 'kind': 'review', 'fixture': fixture, 'prompt': 'Review.',
            'problems': [['formatReport'], ['retries']]}
    fake = benchmark.Agent('fake', ['python3', '-c', 'print("formatReport is camelCase")'])
    monkeypatch.setattr(benchmark, 'load_tasks', lambda: [task])
    monkeypatch.setattr(benchmark, 'bench_agents', lambda usage_file: [fake])
    monkeypatch.setattr(benchmark, 'prepare_arm', lambda workspace, arm: benchmark.commit_fixture(workspace))

    assert benchmark.main(['--runs', '1', '--out', str(tmp_path / 'out')]) == 0

    table = (tmp_path / 'out' / 'benchmark.md').read_text()
    for arm in benchmark.ARMS:
        assert f'| review | fake | {arm} | 1 | 0.50 (1) | n/a |' in table
    runs = (tmp_path / 'out' / 'runs.md').read_text()
    assert '| review | fake | warrant | 1 | retries |  |' in runs


def test_keep_leaves_workspaces_in_the_run_list(tmp_path, monkeypatch):
    fixture = tmp_path / 'fixture'
    fixture.mkdir()
    (fixture / 'AGENTS.md').write_text('# Demo\n')
    task = {'name': 'review', 'kind': 'review', 'fixture': fixture, 'prompt': 'Review.', 'problems': [['x']]}
    monkeypatch.setattr(benchmark, 'load_tasks', lambda: [task])
    monkeypatch.setattr(benchmark, 'bench_agents', lambda usage_file: [benchmark.Agent('fake', ['python3', '-c', 'print(1)'])])
    monkeypatch.setattr(benchmark, 'prepare_arm', lambda workspace, arm: benchmark.commit_fixture(workspace))

    benchmark.main(['--runs', '1', '--keep', '--agent', 'fake', '--out', str(tmp_path / 'out')])

    rows = [line for line in (tmp_path / 'out' / 'runs.md').read_text().splitlines() if line.startswith('| review')]
    kept = [Path(row.split('|')[6].strip()) for row in rows]
    assert len(kept) == 3 and all(path.is_dir() for path in kept)


IMPLEMENT = benchmark.TASKS / 'implement-proration'


def _acceptance_failures(tmp_path, code):
    workspace = tmp_path / 'workspace'
    shutil.rmtree(workspace, ignore_errors=True)
    shutil.copytree(IMPLEMENT / 'fixture', workspace)
    (workspace / 'app' / 'billing.py').write_text(code)
    return 11 - benchmark.acceptance(workspace, IMPLEMENT / 'hidden')


def test_reference_passes_every_acceptance_test(tmp_path):
    assert _acceptance_failures(tmp_path, (IMPLEMENT / 'hidden' / 'reference.py').read_text()) == 0


@pytest.mark.parametrize('fault', sorted(p.name for p in (IMPLEMENT / 'hidden' / 'faults').glob('*.py')))
def test_every_fault_fails_an_acceptance_test(tmp_path, fault):
    assert _acceptance_failures(tmp_path, (IMPLEMENT / 'hidden' / 'faults' / fault).read_text()) > 0


def test_implement_task_change_follows_warrant_rules():
    change = IMPLEMENT / 'fixture' / 'openspec' / 'changes' / 'add-proration'

    assert check_proposal((change / 'proposal.md').read_text()) == []
    assert check_spec((change / 'specs' / 'billing' / 'spec.md').read_text()) == []


def test_tasks_load_with_fixtures_and_kinds():
    tasks = {t['name']: t for t in benchmark.load_tasks()}

    assert sorted(tasks) == ['implement-proration', 'review-export']
    assert all(t['fixture'].is_dir() for t in tasks.values())
    assert len(tasks['review-export']['problems']) == 6
    assert (tasks['review-export']['fixture'] / tasks['review-export']['setup']).is_file()


def test_review_task_change_follows_warrant_rules():
    change = benchmark.TASKS / 'review-export' / 'fixture' / 'openspec' / 'changes' / 'add-order-export'

    assert check_proposal((change / 'proposal.md').read_text()) == []
    assert check_spec((change / 'specs' / 'order-export' / 'spec.md').read_text()) == []
