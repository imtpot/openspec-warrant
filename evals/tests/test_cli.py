import subprocess
import tomllib
from pathlib import Path

import pytest

from warrant_evals import benchmark, judge
from warrant_evals.__main__ import main
from warrant_evals.checks import CHECKERS as CHECKERS_REAL
from warrant_evals.requirements import Finding
from warrant_evals.runner import Result
from warrant_evals.scenarios import load_scenarios


def _fail_when(word):
    def check(workspace, transcript):
        return [Finding('check', f'saw {word}')] if word in transcript else []
    return check


CHECKERS = {'fail-when': lambda params: _fail_when(params['word'])}


@pytest.fixture
def scenario_dir(tmp_path):
    (tmp_path / 'fixtures' / 'demo').mkdir(parents=True)
    scenarios = tmp_path / 'scenarios'
    scenarios.mkdir()
    (scenarios / 'echo.toml').write_text(
        'fixture = "demo"\nprompt = "say hello"\nchecker = "fail-when"\n\n[params]\nword = "boom"\n'
    )
    return scenarios


def test_loads_scenario_from_toml(scenario_dir):
    [scenario] = load_scenarios(scenario_dir, CHECKERS)

    assert scenario.name == 'echo'
    assert scenario.fixture == scenario_dir.parent / 'fixtures' / 'demo'
    assert scenario.prompt == 'say hello'
    assert scenario.check(None, 'boom') == [Finding('check', 'saw boom')]


def test_unknown_checker_is_rejected(scenario_dir):
    (scenario_dir / 'echo.toml').write_text('fixture = "demo"\nprompt = "x"\nchecker = "nope"\n')

    with pytest.raises(ValueError, match='nope'):
        load_scenarios(scenario_dir, CHECKERS)


def test_main_filters_agents_writes_report_and_sets_exit_code(scenario_dir, tmp_path, monkeypatch):
    calls = []

    def fake_run(scenarios, agents, out_dir, **kwargs):
        calls.append(kwargs['only'])
        from warrant_evals.runner import Result
        return [Result('echo', 'codex', 'fail', ['check: saw boom'])]

    monkeypatch.setattr('warrant_evals.__main__.run_evals', fake_run)
    out = tmp_path / 'out'

    code = main(['--agent', 'codex', '--scenarios', str(scenario_dir), '--out', str(out)], CHECKERS)

    assert calls == [['codex']]
    assert code == 1
    assert '| echo | regression | codex | fail |' in (out / 'report.md').read_text()


def test_loader_reads_setup_script(scenario_dir):
    (scenario_dir / 'echo.toml').write_text(
        'fixture = "demo"\nprompt = "x"\nchecker = "fail-when"\nsetup = "setup.sh"\n\n[params]\nword = "boom"\n'
    )

    [scenario] = load_scenarios(scenario_dir, CHECKERS)

    assert scenario.setup == 'setup.sh'


def test_review_protected_scenario_loads_with_the_review_checker(tmp_path):
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path, check=True)
    scenarios = {s.name: s for s in load_scenarios(Path(__file__).parent.parent / 'scenarios', CHECKERS_REAL)}
    scenario = scenarios['review-protected']
    report = '## Spec\n- blocking, untraced: app/cli.py:13 `if args.free < 0`\n## Standards\n## Evidence\n'

    assert scenario.setup == 'setup-protected.sh'
    assert scenario.fixture.name == 'review-branch'
    assert [f.message for f in scenario.check(tmp_path, report)] == [
        'Spec section lacks: --json',
        'Spec section reports untraced: free < 0',
        'Spec section reports untraced: app/cli.py:13',
    ]


def test_review_protected_accepts_the_option_named_as_json_output(tmp_path):
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path, check=True)
    scenarios = {s.name: s for s in load_scenarios(Path(__file__).parent.parent / 'scenarios', CHECKERS_REAL)}
    report = '## Spec\n- Blocking, untraced: app/cli.py:2-7: CLI dispatch and JSON output\n## Standards\n## Evidence\n'

    assert scenarios['review-protected'].check(tmp_path, report) == []


def _spy_run(calls):
    def fake_run(scenarios, agents, out_dir, **kwargs):
        calls.append(kwargs)
        return []
    return fake_run


# Repeated runs: Default
@pytest.mark.parametrize(('extra', 'expected'), [(['--runs', '3'], 3), ([], 1)])
def test_runs_option_reaches_run_evals(scenario_dir, tmp_path, monkeypatch, extra, expected):
    calls = []
    monkeypatch.setattr('warrant_evals.__main__.run_evals', _spy_run(calls))

    main(['--scenarios', str(scenario_dir), '--out', str(tmp_path / 'out'), *extra], CHECKERS)

    assert calls[0]['runs'] == expected


# Invalid run count: Zero runs
def test_zero_runs_is_a_usage_error_before_any_run(scenario_dir, tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr('warrant_evals.__main__.run_evals', _spy_run(calls))

    with pytest.raises(SystemExit) as stop:
        main(['--runs', '0', '--scenarios', str(scenario_dir), '--out', str(tmp_path / 'out')], CHECKERS)

    assert stop.value.code == 2
    assert calls == []


# Scenario suite: No suite field
def test_scenario_without_suite_is_regression(scenario_dir):
    [scenario] = load_scenarios(scenario_dir, CHECKERS)

    assert scenario.suite == 'regression'


# Scenario suite
def test_scenario_reads_its_suite(scenario_dir):
    (scenario_dir / 'echo.toml').write_text('fixture = "demo"\nprompt = "x"\nchecker = "fail-when"\nsuite = "capability"\n\n[params]\nword = "boom"\n')

    [scenario] = load_scenarios(scenario_dir, CHECKERS)

    assert scenario.suite == 'capability'


# Unknown scenario suite: Misspelled suite
def test_misspelled_suite_is_rejected(scenario_dir):
    (scenario_dir / 'echo.toml').write_text('fixture = "demo"\nprompt = "x"\nchecker = "fail-when"\nsuite = "regresion"\n\n[params]\nword = "boom"\n')

    with pytest.raises(ValueError, match='echo.toml: unknown suite regresion'):
        load_scenarios(scenario_dir, CHECKERS)


def _main_with(scenario_dir, tmp_path, monkeypatch, results):
    monkeypatch.setattr('warrant_evals.__main__.run_evals', lambda *a, **k: results)
    out = tmp_path / 'out'
    code = main(['--scenarios', str(scenario_dir), '--out', str(out)], CHECKERS)
    return code, (out / 'report.md').read_text()


# Capability entries and the exit code: Failed capability scenario
def test_failed_capability_entry_does_not_set_the_exit_code(scenario_dir, tmp_path, monkeypatch):
    results = [Result('a', 'codex', 'fail', ['x'], suite='capability'), Result('b', 'codex', 'pass')]

    code, _ = _main_with(scenario_dir, tmp_path, monkeypatch, results)

    assert code == 0


# Exit code by suite: Failed regression scenario
def test_failed_regression_entry_sets_the_exit_code(scenario_dir, tmp_path, monkeypatch):
    results = [Result('a', 'codex', 'fail', ['x'], suite='regression'), Result('b', 'codex', 'pass', suite='capability')]

    code, _ = _main_with(scenario_dir, tmp_path, monkeypatch, results)

    assert code == 1


# Result report: Totals per suite
def test_report_ends_with_totals_per_suite(scenario_dir, tmp_path, monkeypatch):
    results = [
        Result('a', 'claude', 'pass'), Result('b', 'claude', 'pass'), Result('c', 'claude', 'fail', ['x']),
        Result('d', 'claude', 'pass', suite='capability'),
    ]

    _, report = _main_with(scenario_dir, tmp_path, monkeypatch, results)

    assert report.splitlines()[-2:] == ['regression: 2/3', 'capability: 1/1']
    assert '| d | capability | claude | pass |' in report


def _described(groups):
    return [group for group in groups if isinstance(group, dict)]


def test_described_items_and_calibration_cases_are_complete():
    params = []
    checkers = {name: lambda p, make=make: params.append(p) or make(p) for name, make in CHECKERS_REAL.items()}
    load_scenarios(Path(__file__).parent.parent / 'scenarios', checkers)
    items = [item for p in params for axis in ('spec', 'standards', 'evidence') for item in _described(p.get(axis, []))]
    items += [item for task in benchmark.load_tasks() for item in _described(task.get('problems', []))]
    cases = tomllib.loads(judge.CALIBRATION.read_text())['case']

    assert all(item['description'].strip() and item['terms'] for item in items)
    assert all(case['name'].strip() and case['description'].strip() and case['text'].strip() for case in cases)
    assert {case['label'] for case in cases} <= {'yes', 'no'}
