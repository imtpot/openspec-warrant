# Tasks

Files this change reaches: `skills/warrant-setup/SKILL.md`,
`evals/scenarios/setup-no-openspec.toml`, `evals/scenarios/setup-wrong-version.toml`,
`evals/scenarios/setup-init-confirmed.toml`, `README.md`.

## 1. Scenarios

- [ ] 1.1 Expect the init and install commands in the stop scenarios and add `setup-init-confirmed` (specs: "No OpenSpec root", "Unsupported OpenSpec version", "Confirmed install and init"); verify the scenario tests pass

## 2. Skill

- [ ] 2.1 Rewrite steps 1, 2 and 7 of `warrant-setup` and add the skills step (specs: all of this change); verify the kit tests pass

## 3. Documentation

- [ ] 3.1 Update the install section of `README.md`

## 4. Review

- [ ] 4.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 5. Verification

- [ ] 5.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 5.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 5.3 Run every setup scenario on `claude` and `codex`; record each result
