# Tasks

Files this change reaches: `skills/warrant-tdd/SKILL.md`,
`evals/warrant_evals/benchmark.py`, `evals/tests/test_benchmark.py`,
`README.md`.

## 1. Benchmark

- [x] 1.1 Write a failing test, then add `--arm` (specs: benchmark "Arm filter"); verify the test passes

## 2. Skill

- [x] 2.1 Add boundary cases, independent expected values, boundary-only mocks and the mutation check to `warrant-tdd` (specs: test-first "Boundary cases from the requirement text", "Boundary cases in the report", "Independent expected values", "Mocks only at external boundaries", "Mutation check"); verify the kit tests pass

## 3. Documentation

- [x] 3.1 Rewrite principle 5 in `docs/design.md` (tokens buy quality) and record the benchmark results in `README.md`; verify the kit tests pass

## 4. Review

- [x] 4.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 5. Verification

- [x] 5.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 181 passed in 80.18s
- [x] 5.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
- [x] 5.3 Run the tdd scenarios on `claude` and `codex`; record each result
  Result: exit 0, 6 of 6 pass (tdd-change, tdd-direct, tdd-no-tests x claude, codex)
- [x] 5.4 Run the implement benchmark task in the warrant arm on `claude` three times; record fault detection and the faults missed
  Result: exit 0, fault detection 0.96 (runs: 8/8, 8/8, 7/8 missing after_period_negative.py); before 0.67; plain OpenSpec 0.92
