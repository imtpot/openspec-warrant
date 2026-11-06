"""Load eval scenarios from `evals/scenarios/*.toml`."""

import tomllib
from collections.abc import Callable, Mapping
from pathlib import Path

from warrant_evals.runner import Check, Scenario

CheckerFactory = Callable[[dict], Check]
SUITES = ('regression', 'capability')


def load_scenarios(directory: Path, checkers: Mapping[str, CheckerFactory]) -> list[Scenario]:
    """Each file names a fixture under `../fixtures/`, a prompt and a checker."""
    scenarios = []
    for path in sorted(directory.glob('*.toml')):
        data = tomllib.loads(path.read_text())
        if data['checker'] not in checkers:
            raise ValueError(f'{path.name}: unknown checker {data["checker"]}')
        if (suite := data.get('suite', 'regression')) not in SUITES:
            raise ValueError(f'{path.name}: unknown suite {suite}')
        scenarios.append(Scenario(
            name=path.stem,
            fixture=directory.parent / 'fixtures' / data['fixture'],
            prompt=data['prompt'],
            check=checkers[data['checker']](data.get('params', {})),
            path=data.get('path', []),
            setup=data.get('setup'),
            loaded=data.get('loaded', []),
            record=data.get('record', []),
            suite=suite,
        ))
    return scenarios
