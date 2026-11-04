# Tasks

Files this change reaches: `skills/warrant-tdd/SKILL.md`,
`evals/warrant_evals/benchmark.py`, `evals/tests/test_benchmark.py`,
`README.md`.

## 1. Benchmark

- [ ] 1.1 Write a failing test, then add `--arm` (specs: benchmark "Arm filter"); verify the test passes

## 2. Skill

- [ ] 2.1 Add boundary cases, independent expected values, boundary-only mocks and the mutation check to `warrant-tdd` (specs: test-first "Boundary cases from the requirement text", "Boundary cases in the report", "Independent expected values", "Mocks only at external boundaries", "Mutation check"); verify the kit tests pass

## 3. Review

- [ ] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [ ] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.3 Run the tdd scenarios on `claude` and `codex`; record each result
- [ ] 4.4 Run the implement benchmark task in the warrant arm on `claude` three times; record fault detection and the faults missed
