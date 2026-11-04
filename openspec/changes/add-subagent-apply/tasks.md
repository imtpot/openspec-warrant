# Tasks

Files this change reaches: `skills/warrant-setup/rules.yaml`,
`openspec/config.yaml`, `evals/fixtures/warrant-project/openspec/config.yaml`,
`evals/tests/test_kit.py`, `README.md`, `docs/design.md`.

## 1. Rules

- [ ] 1.1 Write failing kit tests for the sub-agent, verify-before-check-off and independent-group rules, then change `rules.yaml` and its copies (specs: "Apply guidance", "Sub-agent per task group", "Verify before checking off", "Independent task groups"); verify the kit and dogfood tests pass

## 2. Documentation

- [ ] 2.1 Update `README.md` and `docs/design.md`; verify the kit tests pass

## 3. Review

- [ ] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [ ] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.3 Run the setup scenarios on `claude` and `codex`; record each result
- [ ] 4.4 Run the implement benchmark task on `claude` and `codex` before and after this change; record tokens and scores in `README.md`
