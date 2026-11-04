"""Compare no kit, plain OpenSpec and OpenSpec plus warrant on the same tasks.

Run: uv run python -m warrant_evals.benchmark --agent claude --runs 3
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from warrant_evals.checks import _missing
from warrant_evals.contract import parse_contract
from warrant_evals.runner import AGENTS, Agent, Scenario, _run_one
from warrant_evals.workspace import commit_fixture, openspec_skills, prepare_workspace

REPO = Path(__file__).resolve().parents[2]
TASKS = REPO / 'evals' / 'benchmark'
RULES_FILE = REPO / 'skills' / 'warrant-setup' / 'rules.yaml'
ARMS = ['bare', 'openspec', 'warrant']
CODEX_TOKENS = re.compile(r'tokens used\s*\n\s*([\d,]+)')
CONTRACT_SECTION = re.compile(r'^## Warrant contract\s*$.*?(?=^## |\Z)', re.M | re.S)
# Counts tests run and tests failed or errored, so that "no tests" differs from "all passed".
COUNT_TESTS = (
    'import json, sys, unittest\n'
    'suite = unittest.defaultTestLoader.discover(sys.argv[1], top_level_dir=".")\n'
    'result = unittest.TestResult()\n'
    'suite.run(result)\n'
    'print(json.dumps([result.testsRun, len(result.failures) + len(result.errors)]))\n'
)
TEST_TIMEOUT = 120


@dataclass
class Run:
    task: str
    agent: str
    arm: str
    scores: dict[str, float | None] = field(default_factory=dict)
    number: int = 1
    # Faults the agent's tests let through, or planted problems the report missed.
    missed: list[str] = field(default_factory=list)
    workspace: Path | None = None


def bench_agents(usage_file: Path) -> list[Agent]:
    """The eval agents; Claude reports usage as JSON and runs without user settings."""
    commands = {a.name: list(a.command) for a in AGENTS}
    claude = commands['claude']
    claude[claude.index('-p') + 1:claude.index('-p') + 1] = ['--output-format', 'json', '--setting-sources', 'project,local']
    return [Agent(name, command) for name, command in commands.items()]


def tokens(agent: str, stdout: str, usage_file: Path) -> int | None:
    """All input (including cache) plus output tokens as the agent reports them."""
    if agent == 'claude':
        try:
            data = json.loads(stdout)
        except ValueError:
            return None
        # `usage` covers only the main context; `modelUsage` adds every sub-agent.
        if isinstance(data, dict) and data.get('modelUsage'):
            keys = ['inputTokens', 'cacheCreationInputTokens', 'cacheReadInputTokens', 'outputTokens']
            return sum(m.get(key, 0) for m in data['modelUsage'].values() for key in keys)
        usage = data.get('usage') if isinstance(data, dict) else None
        if not usage:
            return None
        keys = ['input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens', 'output_tokens']
        return sum(usage.get(key, 0) for key in keys)
    if agent == 'codex':
        match = CODEX_TOKENS.search(stdout)
        return int(match.group(1).replace(',', '')) if match else None
    return None


def report_text(agent: str, stdout: str) -> str:
    if agent == 'claude':
        try:
            return json.loads(stdout)['result']
        except (ValueError, KeyError, TypeError):
            return stdout
    return stdout


def contract_as_text(agents_md: str) -> str:
    """Replace the Warrant contract with plain text naming the same commands and standards."""
    contract = parse_contract(agents_md)
    if contract is None:
        return agents_md
    lines = ['## Verification', '']
    lines += [f'- {name}: `{command}`' for name, command in contract.verification]
    if contract.standards:
        lines += ['', 'Coding standards: ' + ', '.join(f'`{path}`' for path in contract.standards)]
    return CONTRACT_SECTION.sub('\n'.join(lines) + '\n\n', agents_md).rstrip('\n') + '\n'


def prepare_arm(workspace: Path, arm: str) -> None:
    agents_md = workspace / 'AGENTS.md'
    if arm == 'warrant':
        config = workspace / 'openspec' / 'config.yaml'
        config.write_text(config.read_text().rstrip('\n') + '\n\n' + RULES_FILE.read_text())
        prepare_workspace(workspace, REPO, extra=[openspec_skills()])
        return
    agents_md.write_text(contract_as_text(agents_md.read_text()))
    if arm == 'openspec':
        prepare_workspace(workspace, openspec_skills())
    else:
        commit_fixture(workspace)


def _count_tests(workspace: Path, directory: str) -> tuple[int, int]:
    # A fresh bytecode cache per run: a swapped module of the same size within
    # one second would otherwise run from stale bytecode.
    with tempfile.TemporaryDirectory() as cache:
        env = {**os.environ, 'PYTHONPYCACHEPREFIX': cache, 'PYTHONDONTWRITEBYTECODE': '1'}
        done = subprocess.run(
            [sys.executable, '-c', COUNT_TESTS, directory], cwd=workspace, env=env,
            capture_output=True, text=True, timeout=TEST_TIMEOUT, check=False,
        )
    try:
        run, failed = json.loads(done.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return 0, 0
    return run, failed


def fault_detection(workspace: Path, hidden: Path, module: str, tests: str = 'tests') -> tuple[float | None, list[str]]:
    """Share of faulty implementations the agent's tests reject, and the faults they let through.

    The share is None when the tests reject the reference implementation.
    """
    target = workspace / module
    original = target.read_text() if target.exists() else None
    try:
        target.write_text((hidden / 'reference.py').read_text())
        run, failed = _count_tests(workspace, tests)
        faults = sorted((hidden / 'faults').glob('*.py'))
        if run == 0:
            return 0.0, [f.name for f in faults]
        if failed:
            return None, []
        missed = []
        for fault in faults:
            target.write_text(fault.read_text())
            if not _count_tests(workspace, tests)[1]:
                missed.append(fault.name)
        return 1 - len(missed) / len(faults), missed
    finally:
        if original is None:
            target.unlink(missing_ok=True)
        else:
            target.write_text(original)


def acceptance(workspace: Path, hidden: Path) -> int:
    """Hidden acceptance tests that pass against the agent's implementation."""
    copy = workspace / 'acceptance'
    shutil.copytree(hidden / 'acceptance', copy)
    (copy / '__init__.py').touch()
    try:
        run, failed = _count_tests(workspace, 'acceptance')
    finally:
        shutil.rmtree(copy)
    return run - failed


def added_lines(workspace: Path) -> int:
    """Lines the agent added outside tests and OpenSpec artifacts, against the fixture commit."""
    git = lambda *args: subprocess.run(['git', *args], cwd=workspace, capture_output=True, text=True, check=True).stdout  # noqa: E731
    root = git('rev-list', '--max-parents=0', 'HEAD').split()[0]
    git('add', '-A')
    numstat = git('diff', '--cached', '--numstat', root, '--', '.', ':!tests', ':!openspec', ':!acceptance')
    return sum(int(line.split('\t')[0]) for line in numstat.splitlines() if line.split('\t')[0].isdigit())


def review_score(report: str, problems: list[list[str]]) -> tuple[float, list[str]]:
    """Share of planted problems the report names, and the first term of each missed one."""
    missed = _missing(report, problems)
    return 1 - len(missed) / len(problems), missed


def summary(runs: Sequence[Run]) -> str:
    """Mean of each score per task, agent and arm; `(k)` is the number of runs that measured it."""
    keys = sorted({key for run in runs for key in run.scores})
    groups: dict[tuple[str, str, str], list[Run]] = {}
    for run in sorted(runs, key=lambda r: (r.task, r.agent, ARMS.index(r.arm))):
        groups.setdefault((run.task, run.agent, run.arm), []).append(run)
    lines = ['| Task | Agent | Arm | Runs | ' + ' | '.join(keys) + ' |', '|---' * (4 + len(keys)) + '|']
    for (task, agent, arm), group in groups.items():
        cells = []
        for key in keys:
            values = [r.scores[key] for r in group if r.scores.get(key) is not None]
            mean = sum(values) / len(values) if values else None
            if mean is None:
                cells.append('n/a')
            elif key == 'tokens' or key.endswith('_count'):
                cells.append(f'{round(mean)} ({len(values)})')
            else:
                cells.append(f'{mean:.2f} ({len(values)})')
        lines.append(f'| {task} | {agent} | {arm} | {len(group)} | ' + ' | '.join(cells) + ' |')
    return '\n'.join(lines) + '\n'


def _score(task: dict, run: Run, workspace: Path, stdout: str, usage_file: Path) -> None:
    run.scores['tokens'] = tokens(run.agent, stdout, usage_file)
    if task['kind'] == 'implement':
        hidden = task['dir'] / 'hidden'
        run.scores['acceptance_count'] = acceptance(workspace, hidden)
        run.scores['faults'], run.missed = fault_detection(workspace, hidden, task['module'])
        run.scores['added_lines_count'] = added_lines(workspace)
    else:
        run.scores['problems'], run.missed = review_score(report_text(run.agent, stdout), task['problems'])


def run_list(runs: Sequence[Run]) -> str:
    """One row per run with what it missed and, with --keep, its workspace."""
    lines = ['| Task | Agent | Arm | Run | Missed | Workspace |', '|---|---|---|---|---|---|']
    lines += [
        f'| {r.task} | {r.agent} | {r.arm} | {r.number} | {", ".join(r.missed)} | {r.workspace or ""} |'
        for r in runs
    ]
    return '\n'.join(lines) + '\n'


def load_tasks(directory: Path = TASKS) -> list[dict]:
    tasks = []
    for path in sorted(directory.glob('*.toml')):
        task = tomllib.loads(path.read_text())
        task['name'] = path.stem
        task['dir'] = directory / path.stem
        task['fixture'] = (directory / task['fixture']).resolve()
        tasks.append(task)
    return tasks


def run_benchmark(
    tasks: Sequence[dict], agents: Sequence[str] | None, runs: int, out_dir: Path, keep: bool = False,
) -> list[Run]:
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix='warrant-bench-') as tmp:
        # Kept workspaces stay outside any repository, like the temporary ones.
        root = Path(tempfile.mkdtemp(prefix='warrant-bench-')) if keep else Path(tmp)
        for task in tasks:
            for arm in ARMS:
                for n in range(1, runs + 1):
                    usage_file = out_dir / f'{task["name"]}-{arm}-{n}.usage.json'
                    for agent in bench_agents(usage_file):
                        if agents and agent.name not in agents:
                            continue
                        run = Run(task['name'], agent.name, arm, number=n)

                        def check(workspace, stdout, run=run, usage_file=usage_file):
                            _score(task, run, workspace, stdout, usage_file)
                            run.workspace = workspace if keep else None
                            return []

                        scenario = Scenario(
                            f'{task["name"]}-{arm}-{n}', task['fixture'], task['prompt'], check,
                            path=task.get('path', []), setup=task.get('setup'),
                        )
                        _run_one(scenario, agent, out_dir, root, lambda w, arm=arm: prepare_arm(w, arm), 15 * 60)
                        results.append(run)
    return results


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog='warrant_evals.benchmark')
    parser.add_argument('--task', action='append', help='run only these tasks')
    parser.add_argument('--agent', action='append', help='run only these agents')
    parser.add_argument('--runs', type=int, default=3)
    parser.add_argument('--out', type=Path, default=REPO / 'evals' / 'out' / 'benchmark')
    parser.add_argument('--keep', action='store_true', help='keep workspaces and list them in runs.md')
    args = parser.parse_args(argv)
    tasks = [t for t in load_tasks() if not args.task or t['name'] in args.task]
    runs = run_benchmark(tasks, args.agent, args.runs, args.out, keep=args.keep)
    table = summary(runs)
    (args.out / 'benchmark.md').write_text(table)
    (args.out / 'runs.md').write_text(run_list(runs))
    print(table)
    return 0


if __name__ == '__main__':
    sys.exit(main())
