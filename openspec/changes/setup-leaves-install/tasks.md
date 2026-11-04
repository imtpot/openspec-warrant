# Tasks

Files this change reaches: `skills/warrant-setup/SKILL.md`,
`evals/scenarios/setup-init-confirmed.toml`, `README.md`.

## 1. Skill and scenarios

- [ ] 1.1 Remove `setup-init-confirmed`, then make steps 1 and 2 of `warrant-setup` stop and name the commands (specs: "No OpenSpec root", "Unsupported OpenSpec version"); verify the kit tests pass
- [ ] 1.2 Update the install list in `README.md`

## 2. Review

- [ ] 2.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 3. Verification

- [ ] 3.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 3.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 3.3 Run every setup scenario on `claude` and `codex`; record each result
