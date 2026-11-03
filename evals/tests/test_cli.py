import pytest

from warrant_evals.__main__ import main
from warrant_evals.requirements import Finding
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
    assert '| echo | codex | fail |' in (out / 'report.md').read_text()
