# Tasks

Files this change reaches: `skills/warrant-setup/SKILL.md`,
`evals/scenarios/setup-init-confirmed.toml`, `README.md`.

## 1. Skill and scenarios

- [x] 1.1 Remove `setup-init-confirmed`, then make steps 1 and 2 of `warrant-setup` stop and name the commands (specs: "No OpenSpec root", "Unsupported OpenSpec version"); verify the kit tests pass
- [x] 1.2 Update the install list in `README.md`

## 2. Review

- [x] 2.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 3. Verification

- [x] 3.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 201 passed, 5 skipped in 85.80s (dogfood tests skip in a worktree without installed skills)
- [x] 3.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
- [x] 3.3 Run every setup scenario on `claude` and `codex`; record each result
  Result: exit 0, 12 of 12 (6 setup scenarios x claude, codex)
