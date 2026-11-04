# Tasks

Files this change reaches: `evals/warrant_evals/benchmark.py`,
`evals/tests/test_benchmark.py`, `evals/benchmark/plan-implement-allocation.toml`,
`evals/benchmark/plan-implement-allocation/`, `README.md`.

## 1. Scoring

- [x] 1.1 Write failing tests, then count faults per reference-passing test (specs: "Invalid agent tests", "Fault caught by a reference-passing test"); verify the tests pass
- [x] 1.2 Write failing tests, then score marked ambiguities (specs: "Marked ambiguity"); verify the tests pass
- [x] 1.3 Write failing tests, then score plan-implement runs (specs: "Plan-implement task scores"); verify the tests pass

- [x] 1.4 Write failing tests, then send several prompts in one session (specs: "Prompts in one session"); verify the tests pass

## 2. Task

- [x] 2.1 Add the allocation fixture, reference, faults and acceptance tests; verify the reference passes and every fault fails an acceptance test

## 3. Documentation

- [x] 3.1 Describe the task in `README.md`

## 4. Review

- [x] 4.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 5. Verification

- [x] 5.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 198 passed in 92.36s
- [x] 5.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 12 passed, 0 failed (12 items)
- [x] 5.3 Run the task on `claude` (Opus) and `claude:sonnet` in all arms, three runs each; record the results
  Result: exit 0, open points marked bare/openspec/warrant: Opus 0.00/0.22/1.00, Sonnet 0.22/0.67/1.00, Haiku 0.00/0.11/1.00; every arm 6 of 6 acceptance; see README
