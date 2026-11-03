"""Run eval scenarios headless against agent CLIs in isolated workspaces."""

import os
import re
import shutil
import subprocess
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from warrant_evals.requirements import Finding

TIMEOUT_SECONDS = 15 * 60
NOT_AUTHENTICATED = re.compile(r'log ?in|authenticat|sign in|api key|unauthori[sz]ed', re.I)


@dataclass
class Agent:
    name: str
    # `{prompt}` marks where the prompt goes; without it the prompt is appended.
    command: list[str]

    def argv(self, prompt: str) -> list[str]:
        if '{prompt}' in self.command:
            return [prompt if part == '{prompt}' else part for part in self.command]
        return [*self.command, prompt]


# Restricted modes only: agents may edit files in the workspace and run the
# shell commands below. Flags are taken from each CLI's --help.
CLAUDE_TOOLS = [
    'Bash(openspec *)', 'Bash(uv run *)', 'Bash(make *)', 'Bash(diff *)',
    'Bash(cp *)', 'Bash(mkdir *)', 'Bash(git status*)', 'Bash(git diff*)',
    'Bash(git grep*)', 'Bash(git log*)', 'Bash(git rev-parse*)',
]
COPILOT_TOOLS = [
    'write', 'shell(openspec:*)', 'shell(uv:*)', 'shell(make:*)', 'shell(diff:*)',
    'shell(cp:*)', 'shell(mkdir:*)', 'shell(git:*)',
]
AGENTS = [
    Agent('claude', ['claude', '-p', '--permission-mode', 'acceptEdits', '--allowedTools', *CLAUDE_TOOLS, '--', '{prompt}']),
    Agent('codex', ['codex', 'exec', '-s', 'workspace-write']),
    Agent('copilot', ['copilot', '-p', '{prompt}', '-s', '--allow-tool', *COPILOT_TOOLS, '--deny-tool', 'shell(git push)']),
    Agent('agy', ['agy', '-p', '--mode', 'accept-edits', '--sandbox']),
]

Check = Callable[[Path, str], list[Finding]]


@dataclass
class Scenario:
    name: str
    fixture: Path
    prompt: str
    check: Check
    # Workspace-relative directories put first on PATH, e.g. for a fake CLI.
    path: list[str] = field(default_factory=list)


@dataclass
class Result:
    scenario: str
    agent: str
    status: str  # pass, fail or not run
    messages: list[str] = field(default_factory=list)
    transcript: Path | None = None
    workspace: Path | None = None


def _workspace(root: Path, scenario: Scenario, agent: Agent) -> Path:
    workspace = Path(tempfile.mkdtemp(prefix=f'{scenario.name}-{agent.name}-', dir=root))
    shutil.copytree(scenario.fixture, workspace, dirs_exist_ok=True)
    return workspace


def _run_one(
    scenario: Scenario, agent: Agent, out_dir: Path, workspaces: Path,
    prepare: Callable[[Path], None], timeout: float,
) -> Result:
    if shutil.which(agent.command[0]) is None:
        return Result(scenario.name, agent.name, 'not run', [f'{agent.command[0]} not installed'])
    workspace = _workspace(workspaces, scenario, agent)
    prepare(workspace)
    transcript = out_dir / f'{scenario.name}-{agent.name}.log'
    env = dict(os.environ)
    env['PATH'] = os.pathsep.join([*(str(workspace / d) for d in scenario.path), env['PATH']])
    try:
        done = subprocess.run(
            agent.argv(scenario.prompt), cwd=workspace, capture_output=True,
            text=True, timeout=timeout, check=False, env=env,
        )
    except subprocess.TimeoutExpired as expired:
        transcript.write_text(f'{expired.stdout or ""}{expired.stderr or ""}')
        return Result(scenario.name, agent.name, 'fail', ['timeout'], transcript, workspace)
    output = done.stdout + done.stderr
    transcript.write_text(output)
    if done.returncode != 0 and NOT_AUTHENTICATED.search(output):
        return Result(scenario.name, agent.name, 'not run', ['not authenticated'], transcript, workspace)
    messages = [f'{f.requirement}: {f.message}' for f in scenario.check(workspace, done.stdout)]
    status = 'fail' if messages else 'pass'
    return Result(scenario.name, agent.name, status, messages, transcript, workspace)


def run_evals(
    scenarios: Sequence[Scenario], agents: Sequence[Agent], out_dir: Path, *,
    only: Sequence[str] | None = None, prepare: Callable[[Path], None],
    timeout: float = TIMEOUT_SECONDS, keep: bool = False,
) -> list[Result]:
    out_dir.mkdir(parents=True, exist_ok=True)
    selected = [agent for agent in agents if not only or agent.name in only]
    if keep:
        # Kept workspaces stay outside any repository, like the temporary ones,
        # so tools that search parent directories find nothing but the fixture.
        workspaces = Path(tempfile.mkdtemp(prefix='warrant-evals-'))
        return [
            _run_one(s, a, out_dir, workspaces, prepare, timeout)
            for s in scenarios for a in selected
        ]
    with tempfile.TemporaryDirectory(prefix='warrant-evals-') as tmp:
        return [
            _run_one(s, a, out_dir, Path(tmp), prepare, timeout)
            for s in scenarios for a in selected
        ]


def write_report(results: Sequence[Result], path: Path) -> Path:
    lines = ['| Scenario | Agent | Status | Messages | Transcript | Workspace |', '|---|---|---|---|---|---|']
    lines += [
        f'| {r.scenario} | {r.agent} | {r.status} | {"; ".join(r.messages)} | {r.transcript or ""} '
        f'| {r.workspace if r.workspace and r.workspace.exists() else ""} |'
        for r in results
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(lines) + '\n')
    return path
