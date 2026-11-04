# Tasks

Files this change reaches: `skills/warrant-setup/rules.yaml`,
`openspec/config.yaml`, `evals/fixtures/warrant-project/openspec/config.yaml`,
`evals/tests/test_kit.py`, `README.md`, `docs/design.md`.

## 1. Rules

- [x] 1.1 Write failing kit tests for the sub-agent, verify-before-check-off and independent-group rules, then change `rules.yaml` and its copies (specs: "Sub-agent per task group", "Verify before checking off", "Independent task groups", "Smaller model for settled groups"); verify the kit and dogfood tests pass

## 2. Documentation

- [x] 2.1 Update `README.md` and `docs/design.md`; verify the kit tests pass

## 3. Review

- [x] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [x] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 201 passed in 81.71s (0:01:21)
- [x] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
- [x] 4.3 Run the setup scenarios on `claude` and `codex`; record each result
  Result: exit 0, 12 of 12 pass (6 setup scenarios x claude, codex)
- [x] 4.4 Run the plan-implement benchmark task in the warrant arm on Opus three times; record the models its sub-agents used, the scores and the cost against warrant without sub-agents
  Result: exit 0, 3 runs: open points 1.00, acceptance 6 of 6, faults 1.00, 15 lines; sub-agents ran on Sonnet in every run; $2.08 per run against $2.30 without sub-agents
