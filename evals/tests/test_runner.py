import json
import stat
from pathlib import Path

import pytest

from warrant_evals.record import recorded_runs, run_log
from warrant_evals.requirements import Finding
from warrant_evals.runner import AGENTS, Agent, Result, Scenario, combine, parse_output, run_evals, write_report
from warrant_evals.workspace import commit_fixture


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

    workspaces = {Path(r.transcripts[0].read_text().splitlines()[0]).resolve() for r in results}
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


# Agent error: Crashed agent with a clean workspace
@pytest.mark.parametrize('code', [1, 3])
def test_crashed_agent_with_clean_workspace_fails(tmp_path, fixture_dir, code):
    crashed = Agent('crashed', [str(_script(tmp_path / 'crashed', f'echo done > out.txt; exit {code}'))])

    [result] = _run(tmp_path, [_scenario(fixture_dir)], [crashed])

    assert result.status == 'fail'
    assert result.messages == [f'agent exited {code}']


def test_timeout_fails_the_entry(tmp_path, fixture_dir):
    sleeper = Agent('sleeper', [str(_script(tmp_path / 'sleeper', 'sleep 5'))])

    [result] = _run(tmp_path, [_scenario(fixture_dir)], [sleeper], timeout=0.5)

    assert result.status == 'fail'
    assert result.messages == ['timeout']


def test_report_lists_every_entry_with_transcript(tmp_path, fixture_dir, writer):
    idle = Agent('idle', [str(_script(tmp_path / 'idle', 'true'))])
    results = _run(tmp_path, [_scenario(fixture_dir)], [writer, idle])

    report = write_report(results, tmp_path / 'out' / 'report.md').read_text()

    assert '| demo | writer | pass | 1/1 |' in report
    assert '| demo | idle | fail | 0/1 | demo: no out.txt |' in report
    assert all(str(t) in report for r in results for t in r.transcripts)


def test_prompt_is_passed_to_the_agent(tmp_path, fixture_dir):
    echo = Agent('echo', [str(_script(tmp_path / 'echo', 'echo "$@" > out.txt'))])

    [result] = _run(tmp_path, [_scenario(fixture_dir)], [echo], keep=True)

    assert (result.workspaces[0] / 'out.txt').read_text().strip() == 'do it'


def test_no_agent_runs_with_a_permission_bypass_flag():
    flags = [part for agent in AGENTS for part in agent.command]

    assert not [f for f in flags if 'dangerously' in f or f.startswith('--allow-all')]


def test_scenario_path_dirs_come_first_on_path(tmp_path, fixture_dir):
    (fixture_dir / 'bin').mkdir()
    _script(fixture_dir / 'bin' / 'tool', 'echo fixture-tool')
    caller = Agent('caller', [str(_script(tmp_path / 'caller', 'tool > out.txt'))])
    scenario = Scenario(name='demo', fixture=fixture_dir, prompt='x', check=_passes, path=['bin'])

    [result] = _run(tmp_path, [scenario], [caller], keep=True)

    assert (result.workspaces[0] / 'out.txt').read_text().strip() == 'fixture-tool'


def test_kept_workspace_is_outside_the_output_directory(tmp_path, fixture_dir, writer):
    # A workspace inside a repository would let tools find that repository's
    # files by searching parent directories.
    [result] = _run(tmp_path, [_scenario(fixture_dir)], [writer], keep=True)

    assert result.workspaces[0].exists()
    assert not result.workspaces[0].resolve().is_relative_to((tmp_path / 'out').resolve())
    assert str(result.workspaces[0]) in write_report([result], tmp_path / 'out' / 'r.md').read_text()


def test_agent_gets_an_empty_stdin(tmp_path, fixture_dir, writer, monkeypatch):
    # codex exec reads stdin when it is open; an inherited pipe would block it.
    import subprocess

    from warrant_evals import runner

    seen = {}
    real_run = subprocess.run

    def spy(*args, **kwargs):
        seen.update(kwargs)
        return real_run(*args, **kwargs)

    monkeypatch.setattr(runner.subprocess, 'run', spy)

    _run(tmp_path, [_scenario(fixture_dir)], [writer])

    assert seen['stdin'] is subprocess.DEVNULL


def test_setup_script_runs_in_the_workspace_after_preparation(tmp_path, fixture_dir, writer):
    (fixture_dir / 'setup.sh').write_text('cat prepared.txt > setup-saw.txt\n')
    scenario = Scenario(name='demo', fixture=fixture_dir, prompt='x', check=_passes, setup='setup.sh')

    def prepare(workspace):
        (workspace / 'prepared.txt').write_text('prepared\n')

    [result] = _run(tmp_path, [scenario], [writer], prepare=prepare, keep=True)

    assert (result.workspaces[0] / 'setup-saw.txt').read_text() == 'prepared\n'


def test_supported_agents():
    assert [agent.name for agent in AGENTS] == ['claude', 'codex']


STREAM = '\n'.join(json.dumps(e) for e in [
    {'type': 'system', 'subtype': 'init'},
    {'type': 'assistant', 'message': {'content': [
        {'type': 'tool_use', 'name': 'Skill', 'input': {'skill': 'warrant-verify'}},
        {'type': 'tool_use', 'name': 'Read', 'input': {'file_path': '/w/.agents/skills/warrant-tdd/SKILL.md'}},
        {'type': 'tool_use', 'name': 'Agent', 'input': {'prompt': 'x', 'model': 'sonnet'}},
    ]}},
    {'type': 'result', 'result': 'Done.'},
])


def test_claude_stream_gives_report_and_tools():
    assert parse_output('claude', STREAM) == ('Done.', ['skill:warrant-verify', 'skill:warrant-tdd', 'agent:sonnet'])


def test_single_json_output_stays_unchanged():
    out = json.dumps({'type': 'result', 'result': 'ok', 'usage': {}})

    assert parse_output('claude', out) == (out, [])


def test_codex_output_gives_skill_reads():
    out = "exec\n/bin/zsh -c 'cat .agents/skills/warrant-tdd/SKILL.md' in /w\ncodex\nDone."

    assert parse_output('codex', out) == (out, ['skill:warrant-tdd'])


def test_codex_listing_of_skill_files_is_not_a_load():
    out = ("exec\n/bin/zsh -c 'cat .agents/skills/warrant-setup/SKILL.md' in /w\n"
           "exec\n/bin/zsh -c 'find .agents/skills -name SKILL.md' in /w\n"
           ".agents/skills/warrant-tdd/SKILL.md\n"
           '/bin/zsh -c "pwd; cat .agents/skills/warrant-verify/SKILL.md"\n')

    assert parse_output('codex', out)[1] == ['skill:warrant-setup', 'skill:warrant-verify']


def test_missing_required_skill_fails_the_run(tmp_path, fixture_dir, writer):
    scenario = Scenario(name='demo', fixture=fixture_dir, prompt='do it', check=_passes, loaded=['warrant-verify'])

    [result] = _run(tmp_path, [scenario], [writer])

    assert result.status == 'fail'
    assert result.messages == ['skills: skill not loaded: warrant-verify']


def test_report_lists_loaded_skills(tmp_path):
    result = Result('s', 'claude', 'pass', tools=['skill:warrant-verify', 'agent:sonnet'])

    assert '| skill:warrant-verify, agent:sonnet |' in write_report([result], tmp_path / 'r.md').read_text()


# Recorded command runs: Piped failing test
def test_recorded_tool_run_is_logged_in_the_workspace(tmp_path, fixture_dir):
    (fixture_dir / 'bin').mkdir()
    _script(fixture_dir / 'bin' / 'tool', 'exit 2')
    caller = Agent('caller', [str(_script(tmp_path / 'caller', 'tool x'))])
    scenario = Scenario(
        name='demo', fixture=fixture_dir, prompt='x', check=_passes, path=['bin'], record=['tool'],
    )

    [result] = _run(tmp_path, [scenario], [caller], prepare=commit_fixture, keep=True)

    [run] = recorded_runs(result.workspaces[0])
    assert (run['tool'], run['args'], run['exit']) == ('tool', ['x'], 2)


# Recorded command runs: a scenario without `record` leaves no log
def test_scenario_without_record_leaves_no_log(tmp_path, fixture_dir, writer):
    [result] = _run(tmp_path, [_scenario(fixture_dir)], [writer], prepare=commit_fixture, keep=True)

    assert not run_log(result.workspaces[0]).parent.exists()


# Repeated runs: Three runs
def test_three_runs_give_one_combined_result(tmp_path, fixture_dir, writer):
    [result] = _run(tmp_path, [_scenario(fixture_dir)], [writer], runs=3, keep=True)

    assert (result.status, result.passed, result.runs) == ('pass', 3, 3)
    assert [t.name for t in result.transcripts] == [f'demo-writer-{n}.log' for n in (1, 2, 3)]
    assert len(set(result.workspaces)) == 3
    assert all(w.exists() for w in result.workspaces)


# Repeated runs: Default
def test_one_run_keeps_the_plain_transcript_name(tmp_path, fixture_dir, writer):
    [result] = _run(tmp_path, [_scenario(fixture_dir)], [writer])

    assert result.runs == 1
    assert [t.name for t in result.transcripts] == ['demo-writer.log']


def _result(status, messages=(), tools=(), transcript=None, workspace=None):
    return Result('s', 'a', status, list(messages), transcript, workspace, list(tools))


# Entry status from runs: One of three fails
def test_combine_one_failure_of_three_fails_with_prefixed_messages():
    results = [_result('pass'), _result('pass'), _result('fail', ['demo: no out.txt'])]

    combined = combine(results)

    assert (combined.status, combined.passed, combined.runs) == ('fail', 2, 3)
    assert combined.messages == ['run 3: demo: no out.txt']


# Entry status from runs: Agent not installed
def test_combine_not_run_results_without_transcripts():
    combined = combine([_result('not run', ['codex not installed'])] * 3)

    assert combined.status == 'not run'
    assert combined.messages == ['run 1: codex not installed', 'run 2: codex not installed', 'run 3: codex not installed']
    assert combined.transcripts == []
    assert combined.workspaces == []


# Entry status from runs: Not run and pass
def test_combine_not_run_beats_pass():
    assert combine([_result('pass'), _result('not run', ['x'])]).status == 'not run'


def test_combine_fail_beats_not_run():
    assert combine([_result('not run', ['x']), _result('fail', ['y'])]).status == 'fail'


def test_combine_single_result_keeps_messages_unprefixed_and_joins_tools():
    one = combine([_result('fail', ['demo: no out.txt'], ['skill:a'])])
    two = combine([_result('pass', tools=['skill:a']), _result('pass', tools=['skill:b', 'skill:a'])])

    assert one.messages == ['demo: no out.txt']
    assert two.tools == ['skill:a', 'skill:b']


# Result report: runs count and every transcript
def test_report_shows_runs_count_and_every_transcript(tmp_path):
    paths = [tmp_path / f't{n}.log' for n in (1, 2, 3)]
    combined = combine([_result('pass', transcript=paths[0]), _result('pass', transcript=paths[1]),
                        _result('fail', ['x'], transcript=paths[2])])

    report = write_report([combined], tmp_path / 'r.md').read_text()

    assert '| fail | 2/3 |' in report
    assert all(str(p) in report for p in paths)
