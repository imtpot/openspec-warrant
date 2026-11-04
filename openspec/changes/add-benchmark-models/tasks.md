# Tasks

Files this change reaches: `evals/warrant_evals/benchmark.py`,
`evals/tests/test_benchmark.py`, `README.md`.

## 1. Model option

- [ ] 1.1 Write failing tests, then add `--model` (specs: "Model selection"); verify the tests pass
- [ ] 1.2 Document `--model` in `README.md`

## 2. Review

- [ ] 2.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 3. Verification

- [ ] 3.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 3.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 3.3 Run the implement task on `claude:sonnet` and `claude:haiku` in all arms, three runs each; record the results
