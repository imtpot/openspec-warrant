# Tasks

Files this change reaches: `evals/warrant_evals/benchmark.py`,
`evals/tests/test_benchmark.py`, `evals/benchmark/`, `README.md`,
`docs/design.md`.

## 1. Scoring

- [x] 1.1 Write failing tests, then implement token parsing for Claude and Codex with not measured when absent (specs: "Token usage", "Missing usage"); verify the tests pass
- [x] 1.2 Write failing tests, then implement fault detection, acceptance count and added lines (specs: "Implement task scores", "Invalid agent tests"); verify the tests pass
- [x] 1.3 Write failing tests, then implement the review score (specs: "Review task score"); verify the tests pass
- [x] 1.4 Write failing tests, then implement the summary table (specs: "Summary table"); verify the tests pass

## 2. Arms and command

- [x] 2.1 Write failing tests, then implement the baseline and warrant arm preparation (specs: "Three arms", "Baseline arms", "Warrant arm", "No user settings for Claude"); verify the tests pass
- [x] 2.2 Add the command line with `--task`, `--agent` and `--runs`; verify a test runs it with a fake agent

## 3. Tasks

- [x] 3.1 Add the implement task fixture, hidden tests, reference and faulty implementations; verify the reference passes the hidden tests and every faulty implementation fails them
- [x] 3.2 Add the review task with a fixture whose planted problems need the spec, the standards or code outside the diff
- [x] 3.3 Document the benchmark in `README.md` and `docs/design.md`

## 4. Review

- [x] 4.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 5. Verification

- [x] 5.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 180 passed in 79.20s
- [x] 5.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 10 passed, 0 failed (10 items)
- [x] 5.3 Run the benchmark on `claude`; record the results
  Result: exit 0, implement-proration, 3 runs: fault detection bare 0.75, openspec 0.92, warrant 0.67 (with sub-agent rules); every arm passed 11 of 11 acceptance tests. review-export, 1 run: every arm named 6 of 6 problems. The README gets the table after warrant-tdd tests the boundaries its requirements state
