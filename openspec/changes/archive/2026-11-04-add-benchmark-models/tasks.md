# Tasks

Files this change reaches: `evals/warrant_evals/benchmark.py`,
`evals/tests/test_benchmark.py`, `README.md`.

## 1. Model option

- [x] 1.1 Write failing tests, then add `--model` (specs: "Model selection"); verify the tests pass
- [x] 1.2 Document `--model` in `README.md`

## 2. Review

- [x] 2.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 3. Verification

- [x] 3.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 198 passed in 92.36s
- [x] 3.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 12 passed, 0 failed (12 items)
- [x] 3.3 Run the implement task on `claude:sonnet` and `claude:haiku` in all arms, three runs each; record the results
  Result: exit 0, fault detection bare/openspec/warrant: Sonnet 0.75/0.79/0.83, Haiku 0.79/0.67/0.75 (warrant on Haiku after the fixture followed warrant's rules); every arm 11 of 11 acceptance
