"""Prepare an eval workspace: commit the fixture and install the skills under test."""

import subprocess
from pathlib import Path

GIT_IDENTITY = ['-c', 'user.name=warrant-evals', '-c', 'user.email=evals@invalid']


def _run(args: list[str], cwd: Path) -> None:
    subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)


def prepare_workspace(workspace: Path, source: Path) -> None:
    """Install `source` skills, then commit, so `git diff` shows only the agent's changes."""
    _run(['git', 'init', '-q'], workspace)
    _run(['skills', 'add', str(source), '-a', 'claude-code', 'codex', '-y'], workspace)
    _run(['git', 'add', '-A'], workspace)
    _run(['git', *GIT_IDENTITY, 'commit', '-q', '-m', 'fixture'], workspace)
