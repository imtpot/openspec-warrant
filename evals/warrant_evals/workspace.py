"""Prepare an eval workspace: commit the fixture and install the skills under test."""

import subprocess
from collections.abc import Sequence
from pathlib import Path

GIT_IDENTITY = ['-c', 'user.name=warrant-evals', '-c', 'user.email=evals@invalid']


def _run(args: list[str], cwd: Path) -> None:
    subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)


CACHE = Path.home() / '.cache' / 'warrant-evals'


def openspec_skills() -> Path:
    """The OpenSpec workflow skills for the installed CLI version, cloned once into a cache."""
    version = subprocess.run(['openspec', '--version'], capture_output=True, text=True, check=True).stdout.strip()
    clone = CACHE / f'openspec-{version}'
    if not clone.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        url = 'https://github.com/Fission-AI/OpenSpec'
        _run(['git', 'clone', '-q', '--depth', '1', '--branch', f'v{version}', url, str(clone)], CACHE)
    return clone / 'skills'


def prepare_workspace(workspace: Path, source: Path, extra: Sequence[Path] = ()) -> None:
    """Install `source` and `extra` skills, then commit, so `git diff` shows only the agent's changes."""
    _run(['git', 'init', '-q'], workspace)
    for skills in (source, *extra):
        _run(['skills', 'add', str(skills), '-a', 'claude-code', 'codex', '-y'], workspace)
    commit_fixture(workspace)


def commit_fixture(workspace: Path) -> None:
    """Commit the workspace as it is, so `git diff` shows only the agent's changes."""
    if not (workspace / '.git').exists():
        _run(['git', 'init', '-q'], workspace)
    _run(['git', 'add', '-A'], workspace)
    _run(['git', *GIT_IDENTITY, 'commit', '-q', '-m', 'fixture'], workspace)
