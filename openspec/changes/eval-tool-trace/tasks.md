# Tasks

Files this change reaches: `evals/warrant_evals/runner.py`,
`evals/warrant_evals/scenarios.py`, `evals/warrant_evals/benchmark.py`,
`evals/tests/test_runner.py`, `evals/tests/test_benchmark.py`,
`evals/scenarios/minimal-change-implicit.toml`,
`evals/scenarios/verify-no-contract.toml`, `docs/benchmark.md`.

## 1. Runner

- [ ] 1.1 Write failing tests, then parse Claude's stream into report text and tool calls and Codex's output into skill reads (specs: "Loaded skills", "Claude report text"); verify the tests pass
- [ ] 1.2 Write failing tests, then fail runs that miss a required skill and list loaded skills in the report (specs: "Required skill load"); verify the tests pass
- [ ] 1.3 Keep the benchmark's Claude command on JSON output; verify the benchmark tests pass

## 2. Scenarios and documentation

- [ ] 2.1 Require `warrant-minimal-change` in `minimal-change-implicit` and `warrant-verify` in `verify-no-contract`; describe `loaded` in `docs/benchmark.md`

## 3. Review

- [ ] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [ ] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.3 Run every eval scenario on `claude` and `codex`; record each result
