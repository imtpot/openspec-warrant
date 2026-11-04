# Tasks

Files this change reaches: `evals/warrant_evals/benchmark.py`,
`evals/tests/test_benchmark.py`, `evals/benchmark/`, `README.md`,
`docs/design.md`.

## 1. Scoring

- [ ] 1.1 Write failing tests, then implement token parsing for Claude, Codex and Copilot with not measured when absent (specs: "Token usage", "Missing usage"); verify the tests pass
- [ ] 1.2 Write failing tests, then implement fault detection, acceptance count and added lines (specs: "Implement task scores", "Invalid agent tests"); verify the tests pass
- [ ] 1.3 Write failing tests, then implement the review score (specs: "Review task score"); verify the tests pass
- [ ] 1.4 Write failing tests, then implement the summary table (specs: "Summary table"); verify the tests pass

## 2. Arms and command

- [ ] 2.1 Write failing tests, then implement the baseline and warrant arm preparation (specs: "Three arms", "Baseline arms", "Warrant arm", "No user settings for Claude"); verify the tests pass
- [ ] 2.2 Add the command line with `--task`, `--agent` and `--runs`; verify a test runs it with a fake agent

## 3. Tasks

- [ ] 3.1 Add the implement task fixture, hidden tests, reference and faulty implementations; verify the reference passes the hidden tests and every faulty implementation fails them
- [ ] 3.2 Add the review task with a fixture whose planted problems need the spec, the standards or code outside the diff
- [ ] 3.3 Document the benchmark in `README.md` and `docs/design.md`

## 4. Review

- [ ] 4.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 5. Verification

- [ ] 5.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 5.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 5.3 Run the benchmark on `claude`, `codex` and `copilot`; record the table in `README.md`
