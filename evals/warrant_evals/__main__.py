"""Command line: run eval scenarios against agent CLIs and write a report."""

import argparse
import functools
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

from warrant_evals.runner import AGENTS, run_evals, write_report
from warrant_evals.scenarios import CheckerFactory, load_scenarios
from warrant_evals.workspace import prepare_workspace

REPO = Path(__file__).resolve().parents[2]


def main(argv: Sequence[str] | None = None, checkers: Mapping[str, CheckerFactory] | None = None) -> int:
    if checkers is None:
        from warrant_evals.checks import CHECKERS as checkers
    parser = argparse.ArgumentParser(prog='warrant_evals')
    parser.add_argument('--scenario', action='append', help='run only these scenarios')
    parser.add_argument('--agent', action='append', help='run only these agents')
    parser.add_argument('--keep', action='store_true', help='keep workspaces under the output directory')
    parser.add_argument('--scenarios', type=Path, default=REPO / 'evals' / 'scenarios')
    parser.add_argument('--out', type=Path, default=REPO / 'evals' / 'out')
    args = parser.parse_args(argv)

    scenarios = [
        s for s in load_scenarios(args.scenarios, checkers)
        if not args.scenario or s.name in args.scenario
    ]
    results = run_evals(
        scenarios, AGENTS, args.out, only=args.agent, keep=args.keep,
        prepare=functools.partial(prepare_workspace, source=REPO),
    )
    print(write_report(results, args.out / 'report.md').read_text())
    return 1 if any(r.status == 'fail' for r in results) else 0


if __name__ == '__main__':
    sys.exit(main())
