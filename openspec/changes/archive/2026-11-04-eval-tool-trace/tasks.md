# Tasks

Files this change reaches: `evals/warrant_evals/runner.py`,
`evals/warrant_evals/scenarios.py`, `evals/warrant_evals/benchmark.py`,
`evals/tests/test_runner.py`, `evals/tests/test_benchmark.py`,
`evals/scenarios/minimal-change-implicit.toml`,
`evals/scenarios/verify-no-contract.toml`, `docs/benchmark.md`.

## 1. Runner

- [x] 1.1 Write failing tests, then parse Claude's stream into report text and tool calls and Codex's output into skill reads (specs: "Loaded skills", "Claude report text"); verify the tests pass
- [x] 1.2 Write failing tests, then fail runs that miss a required skill and list loaded skills in the report (specs: "Required skill load"); verify the tests pass
- [x] 1.3 Keep the benchmark's Claude command on JSON output; verify the benchmark tests pass

## 2. Scenarios and documentation

- [x] 2.1 Require `warrant-minimal-change` in `minimal-change-implicit` and `warrant-verify` in `verify-no-contract`; describe `loaded` in `docs/benchmark.md`

## 3. Review

- [x] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [x] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 208 passed, 5 skipped in 86.54s (dogfood tests skip in a worktree without installed skills)
- [x] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
- [x] 4.3 Run every eval scenario on `claude` and `codex`; record each result
  Result: exit 0, 25 of 25 on claude and codex (before setup-init-confirmed was removed on main); both agents loaded warrant-minimal-change and warrant-verify by themselves in the implicit scenarios; Claude ran the review axes in general-purpose sub-agents; in `propose`, Claude loaded no skill at all and still passed
