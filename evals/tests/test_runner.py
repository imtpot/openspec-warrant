import stat
from pathlib import Path

import pytest

from warrant_evals.requirements import Finding
from warrant_evals.runner import AGENTS, Agent, Scenario, run_evals, write_report


def _script(path: Path, body: str) -> Path:
    path.write_text(f'#!/bin/sh\n{body}\n')
    path.chmod(path.stat().st_mode | stat.S_IEXEC)
    return path


@pytest.fixture
def fixture_dir(tmp_path):
    fixture = tmp_path / 'fixtures' / 'demo'
    fixture.mkdir(parents=True)
    (fixture / 'README.md').write_text('fixture\n')
    return fixture


@pytest.fixture
def writer(tmp_path):
    # Writes a file in the workspace and prints its working directory.
    return Agent('writer', [str(_script(tmp_path / 'writer', 'pwd; echo done > out.txt'))])


def _passes(workspace, transcript):
    return [] if (workspace / 'out.txt').exists() else [Finding('demo', 'no out.txt')]


def _scenario(fixture, name='demo', check=_passes):
    return Scenario(name=name, fixture=fixture, prompt='do it', check=check)


def _run(tmp_path, scenarios, agents, **kwargs):
    kwargs.setdefault('prepare', lambda workspace: None)
    return run_evals(scenarios, agents, out_dir=tmp_path / 'out', **kwargs)


def test_one_result_per_scenario_and_agent(tmp_path, fixture_dir, writer):
    other = Agent('other', writer.command)

    results = _run(tmp_path, [_scenario(fixture_dir, 'a'), _scenario(fixture_dir, 'b')], [writer, other])

    assert sorted((r.scenario, r.agent) for r in results) == [
        ('a', 'other'), ('a', 'writer'), ('b', 'other'), ('b', 'writer'),
    ]
    assert {r.status for r in results} == {'pass'}


def test_agent_filter(tmp_path, fixture_dir, writer):
    other = Agent('other', writer.command)

    results = _run(tmp_path, [_scenario(fixture_dir)], [writer, other], only=['other'])

    assert [r.agent for r in results] == ['other']


def test_each_run_uses_a_fresh_copy_and_keeps_the_fixture(tmp_path, fixture_dir, writer):
    results = _run(tmp_path, [_scenario(fixture_dir, 'a'), _scenario(fixture_dir, 'b')], [writer])

    workspaces = {Path(r.transcript.read_text().splitlines()[0]).resolve() for r in results}
    assert len(workspaces) == 2
    assert fixture_dir.resolve() not in workspaces
    assert not (fixture_dir / 'out.txt').exists()


def test_failed_check_is_reported_with_messages(tmp_path, fixture_dir):
    idle = Agent('idle', [str(_script(tmp_path / 'idle', 'true'))])

    [result] = _run(tmp_path, [_scenario(fixture_dir)], [idle])

    assert result.status == 'fail'
    assert result.messages == ['demo: no out.txt']


def test_missing_agent_is_not_run_and_others_continue(tmp_path, fixture_dir, writer):
    missing = Agent('missing', ['/nonexistent/agent-cli'])

    results = _run(tmp_path, [_scenario(fixture_dir)], [missing, writer])

    by_agent = {r.agent: r for r in results}
    assert by_agent['missing'].status == 'not run'
    assert 'not installed' in by_agent['missing'].messages[0]
    assert by_agent['writer'].status == 'pass'


def test_unauthenticated_agent_is_not_run(tmp_path, fixture_dir):
    locked = Agent('locked', [str(_script(tmp_path / 'locked', 'echo "Please log in first" >&2; exit 1'))])

    [result] = _run(tmp_path, [_scenario(fixture_dir)], [locked])

    assert result.status == 'not run'
    assert 'not authenticated' in result.messages[0]


def test_timeout_fails_the_entry(tmp_path, fixture_dir):
    sleeper = Agent('sleeper', [str(_script(tmp_path / 'sleeper', 'sleep 5'))])

    [result] = _run(tmp_path, [_scenario(fixture_dir)], [sleeper], timeout=0.5)

    assert result.status == 'fail'
    assert result.messages == ['timeout']


def test_report_lists_every_entry_with_transcript(tmp_path, fixture_dir, writer):
    idle = Agent('idle', [str(_script(tmp_path / 'idle', 'true'))])
    results = _run(tmp_path, [_scenario(fixture_dir)], [writer, idle])

    report = write_report(results, tmp_path / 'out' / 'report.md').read_text()

    assert '| demo | writer | pass |' in report
    assert '| demo | idle | fail | demo: no out.txt |' in report
    assert all(str(r.transcript) in report for r in results)


def test_prompt_is_passed_to_the_agent(tmp_path, fixture_dir):
    echo = Agent('echo', [str(_script(tmp_path / 'echo', 'echo "$@" > out.txt'))])

    [result] = _run(tmp_path, [_scenario(fixture_dir)], [echo], keep=True)

    assert (result.workspace / 'out.txt').read_text().strip() == 'do it'


def test_no_agent_runs_with_a_permission_bypass_flag():
    flags = [part for agent in AGENTS for part in agent.command]

    assert not [f for f in flags if 'dangerously' in f or f.startswith('--allow-all')]


def test_scenario_path_dirs_come_first_on_path(tmp_path, fixture_dir):
    (fixture_dir / 'bin').mkdir()
    _script(fixture_dir / 'bin' / 'tool', 'echo fixture-tool')
    caller = Agent('caller', [str(_script(tmp_path / 'caller', 'tool > out.txt'))])
    scenario = Scenario(name='demo', fixture=fixture_dir, prompt='x', check=_passes, path=['bin'])

    [result] = _run(tmp_path, [scenario], [caller], keep=True)

    assert (result.workspace / 'out.txt').read_text().strip() == 'fixture-tool'


def test_kept_workspace_is_outside_the_output_directory(tmp_path, fixture_dir, writer):
    # A workspace inside a repository would let tools find that repository's
    # files by searching parent directories.
    [result] = _run(tmp_path, [_scenario(fixture_dir)], [writer], keep=True)

    assert result.workspace.exists()
    assert not result.workspace.resolve().is_relative_to((tmp_path / 'out').resolve())
    assert str(result.workspace) in write_report([result], tmp_path / 'out' / 'r.md').read_text()
