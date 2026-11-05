import os
import stat
import subprocess
from pathlib import Path

import pytest

from warrant_evals.record import install_shims, recorded_runs, run_log, workspace_state
from warrant_evals.workspace import commit_fixture


def _script(path: Path, body: str) -> Path:
    path.write_text(f'#!/bin/sh\n{body}\n')
    path.chmod(path.stat().st_mode | stat.S_IEXEC)
    return path


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    # A committed git workspace and a fake tool on PATH that echoes its input and exits with $FAKE_EXIT.
    tools = tmp_path / 'tools'
    tools.mkdir()
    _script(tools / 'fake', 'echo "args:$#:$1|$2"; echo "env:$FAKE_VAR" >&2; cat; exit ${FAKE_EXIT:-0}')
    _script(tools / 'outer', 'fake nested')
    monkeypatch.setenv('PATH', f'{tools}{os.pathsep}{os.environ["PATH"]}')
    ws = tmp_path / 'ws'
    ws.mkdir()
    (ws / 'README.md').write_text('fixture\n')
    commit_fixture(ws)
    return ws


def _shell(workspace: Path, env: dict[str, str], command: str, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(
        command, shell=True, cwd=workspace, env=os.environ | env, capture_output=True, text=True, **kwargs
    )


# Recorded command runs: Piped failing test
def test_piped_failing_run_is_logged_with_its_exit_code(workspace):
    env = install_shims(workspace, ['fake'], os.environ['PATH'])

    result = _shell(workspace, env, 'FAKE_EXIT=3 fake -m unittest 2>&1 | tail -1')

    assert result.returncode == 0
    [run] = recorded_runs(workspace)
    assert (run['tool'], run['args'], run['exit']) == ('fake', ['-m', 'unittest'], 3)


# Recorded command runs: Nested run
def test_nested_run_is_logged_twice(workspace):
    env = install_shims(workspace, ['outer', 'fake'], os.environ['PATH'])

    _shell(workspace, env, 'outer')

    assert [(run['tool'], run['args']) for run in recorded_runs(workspace)] == [('outer', []), ('fake', ['nested'])]


# Recorded command runs: Tool behavior unchanged
def test_arguments_environment_input_output_and_exit_code_pass_through(workspace):
    env = install_shims(workspace, ['fake'], os.environ['PATH'])

    result = _shell(workspace, env, "FAKE_EXIT=5 FAKE_VAR=v fake 'a b' c", input='from stdin\n')

    assert (result.returncode, result.stdout, result.stderr) == (5, 'args:2:a b|c\nfrom stdin\n', 'env:v\n')
    assert recorded_runs(workspace)[0]['args'] == ['a b', 'c']


# Recorder failure: Read-only log directory
def test_unwritable_log_still_runs_the_tool_and_warns_once(workspace):
    env = install_shims(workspace, ['fake'], os.environ['PATH'])
    Path(env['WARRANT_RUN_LOG']).chmod(0o444)

    result = _shell(workspace, env, 'FAKE_EXIT=4 fake x')

    assert (result.returncode, result.stdout) == (4, 'args:1:x|\n')
    [warning] = result.stderr.splitlines()[1:]
    assert result.stderr.startswith('env:\n') and 'warrant' in warning


# Recorded command runs: the workspace hash changes with a file change and not otherwise
def test_state_changes_only_when_a_file_changes(workspace):
    env = install_shims(workspace, ['fake'], os.environ['PATH'])

    _shell(workspace, env, 'fake')
    _shell(workspace, env, 'fake')
    (workspace / 'README.md').write_text('edited\n')
    _shell(workspace, env, 'fake')

    first, second, third = (run['state'] for run in recorded_runs(workspace))
    assert first == second != third == workspace_state(workspace)


# Recorded command runs: an untracked file counts, and `git add -A` does not change the hash
def test_state_covers_untracked_files_and_ignores_the_index(workspace):
    before = workspace_state(workspace)
    (workspace / 'new.txt').write_text('new\n')
    untracked = workspace_state(workspace)
    subprocess.run(['git', 'add', '-A'], cwd=workspace, check=True)

    assert before != untracked == workspace_state(workspace)


# Recorded command runs: ignored files do not count, a deleted tracked file does
def test_state_skips_ignored_and_deleted_files(workspace):
    (workspace / '.gitignore').write_text('*.log\n')
    before = workspace_state(workspace)
    (workspace / 'out.log').write_text('noise\n')
    assert workspace_state(workspace) == before

    (workspace / 'README.md').unlink()
    assert workspace_state(workspace) != before


# Run log outside the workspace: Agent's view
def test_log_starts_empty_next_to_the_workspace_and_not_in_it(workspace):
    env = install_shims(workspace, ['fake'], os.environ['PATH'])
    assert recorded_runs(workspace) == []

    _shell(workspace, env, 'fake')

    log = workspace.parent / 'ws.warrant' / 'runs.jsonl'
    assert run_log(workspace) == log and len(log.read_text().splitlines()) == 1
    assert (workspace.parent / 'ws.warrant' / 'bin' / 'fake').is_file()
    status = subprocess.run(['git', 'status', '--porcelain'], cwd=workspace, capture_output=True, text=True)
    assert status.stdout == ''
    assert sorted(path.name for path in workspace.rglob('*') if '.git' not in path.parts) == ['README.md']


# Run log outside the workspace: Codex sandbox
@pytest.mark.skipif(os.geteuid() == 0, reason='root writes to a read-only directory')
def test_run_is_logged_when_git_is_read_only(workspace):
    env = install_shims(workspace, ['fake'], os.environ['PATH'])
    git = workspace / '.git'
    subprocess.run(['chmod', '-R', 'a-w', git], check=True)
    try:
        result = _shell(workspace, env, 'fake x')
    finally:
        subprocess.run(['chmod', '-R', 'u+w', git], check=True)

    assert 'warrant recorder' not in result.stderr
    [run] = recorded_runs(workspace)
    assert run['args'] == ['x']


# Recorded command runs: the working directory of the run is logged
def test_run_logs_its_working_directory(workspace):
    env = install_shims(workspace, ['fake'], os.environ['PATH'])
    (workspace / 'sub').mkdir()

    _shell(workspace / 'sub', env, 'fake')

    assert Path(recorded_runs(workspace)[0]['cwd']).resolve() == (workspace / 'sub').resolve()


# Recorded command runs: a real tool missing from PATH exits 127 as in the shell
def test_missing_real_tool_exits_127(workspace):
    env = install_shims(workspace, ['nosuchtool'], os.environ['PATH'])

    result = _shell(workspace, env, 'nosuchtool')

    assert result.returncode == 127 and 'nosuchtool: command not found' in result.stderr


# Recorded command runs: the shim directory comes first on the PATH the caller passes
def test_shims_extend_the_given_path_not_the_process_path(workspace):
    env = install_shims(workspace, ['fake'], '/given/bin')

    bin_dir = str(Path(env['WARRANT_RUN_LOG']).parent / 'bin')
    assert env['PATH'] == f'{bin_dir}{os.pathsep}/given/bin'
    assert env['WARRANT_REAL_PATH'] == '/given/bin'


# Recorded command runs: a tool killed by a signal exits 128 + signal, as in a shell
def test_signal_killed_tool_exits_128_plus_signal_and_logs_it(workspace):
    tools = workspace.parent / 'tools'
    _script(tools / 'killed', 'kill -TERM $$')
    env = install_shims(workspace, ['killed'], os.environ['PATH'])

    result = _shell(workspace, env, 'killed')

    assert result.returncode == 143
    assert recorded_runs(workspace)[0]['exit'] == 143
