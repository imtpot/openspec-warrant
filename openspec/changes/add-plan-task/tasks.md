# Tasks

Files this change reaches: `evals/warrant_evals/benchmark.py`,
`evals/tests/test_benchmark.py`, `evals/benchmark/plan-implement-allocation.toml`,
`evals/benchmark/plan-implement-allocation/`, `README.md`.

## 1. Scoring

- [ ] 1.1 Write failing tests, then count faults per reference-passing test (specs: "Invalid agent tests", "Fault caught by a reference-passing test"); verify the tests pass
- [ ] 1.2 Write failing tests, then score marked ambiguities (specs: "Marked ambiguity"); verify the tests pass
- [ ] 1.3 Write failing tests, then score plan-implement runs (specs: "Plan-implement task scores"); verify the tests pass

## 2. Task

- [ ] 2.1 Add the allocation fixture, reference, faults and acceptance tests; verify the reference passes and every fault fails an acceptance test

## 3. Documentation

- [ ] 3.1 Describe the task in `README.md`

## 4. Review

- [ ] 4.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 5. Verification

- [ ] 5.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 5.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 5.3 Run the task on `claude` (Opus) and `claude:sonnet` in all arms, three runs each; record the results
