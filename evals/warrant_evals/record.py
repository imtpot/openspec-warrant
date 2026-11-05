"""Record runs of named tools in an eval workspace through pass-through shims on PATH."""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from collections.abc import Sequence
from pathlib import Path

# The shim runs this module with the harness's interpreter, so a `python3` shim does not call itself.
SHIM = '#!{python}\nimport sys\nsys.path.insert(0, {root!r})\nfrom warrant_evals.record import main\nmain()\n'


def run_log(workspace: Path) -> Path:
    """Where the shims log the runs of a workspace."""
    return workspace.parent / f'{workspace.name}.warrant' / 'runs.jsonl'


def install_shims(workspace: Path, tools: Sequence[str], path: str) -> dict[str, str]:
    """Write a shim per tool and an empty log; return the environment changes that activate them on `path`."""
    log = run_log(workspace)
    bin_dir = log.parent / 'bin'
    bin_dir.mkdir(parents=True, exist_ok=True)
    shim = SHIM.format(python=sys.executable, root=str(Path(__file__).resolve().parents[1]))
    for tool in tools:
        (bin_dir / tool).write_text(shim)
        (bin_dir / tool).chmod(0o755)
    log.write_text('')
    return {'PATH': f'{bin_dir}{os.pathsep}{path}', 'WARRANT_RUN_LOG': str(log),
            'WARRANT_WORKSPACE': str(workspace), 'WARRANT_REAL_PATH': path}


def workspace_state(workspace: Path) -> str:
    """SHA-256 over the path and content of every tracked and untracked, not ignored, file."""
    listed = subprocess.run(
        ['git', 'ls-files', '-c', '-o', '--exclude-standard', '-z'],
        cwd=workspace, capture_output=True, check=True,
    ).stdout
    digest = hashlib.sha256()
    # Sorted and deduplicated, so the hash is the same before and after `git add -A`.
    for name in sorted(set(listed.split(b'\0')) - {b''}):
        file = workspace / os.fsdecode(name)
        if file.is_file():
            data = file.read_bytes()
            digest.update(name + b'\0' + str(len(data)).encode() + b'\0' + data)
    return digest.hexdigest()


def recorded_runs(workspace: Path) -> list[dict]:
    """The logged runs in start order."""
    lines = run_log(workspace).read_text().splitlines()
    return sorted((json.loads(line) for line in lines), key=lambda run: run['seq'])


def main() -> None:
    """Shim entry point: run the real tool unchanged, log the run, exit with its exit code."""
    tool, args = Path(sys.argv[0]).name, sys.argv[1:]
    real = shutil.which(tool, path=os.environ['WARRANT_REAL_PATH'])
    if real is None:
        print(f'{tool}: command not found', file=sys.stderr)
        sys.exit(127)
    log = Path(os.environ['WARRANT_RUN_LOG'])
    state = workspace_state(Path(os.environ['WARRANT_WORKSPACE']))
    seq = time.time_ns()
    code = subprocess.run([real, *args]).returncode
    if code < 0:
        code = 128 - code  # killed by a signal: exit as a shell does
    run = {'seq': seq, 'tool': tool, 'args': args, 'cwd': os.getcwd(), 'exit': code, 'state': state}
    try:
        with log.open('a') as file:
            file.write(json.dumps(run) + '\n')
    except OSError as error:
        print(f'warrant recorder: run of {tool} not logged: {error}', file=sys.stderr)
    sys.exit(code)
