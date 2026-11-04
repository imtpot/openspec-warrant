# Tasks

Files this change reaches: `skills/warrant-setup/SKILL.md`,
`evals/scenarios/setup-no-openspec.toml`, `evals/scenarios/setup-wrong-version.toml`,
`evals/scenarios/setup-init-confirmed.toml`, `README.md`.

## 1. Scenarios

- [x] 1.1 Expect the init and install commands in the stop scenarios and add `setup-init-confirmed` (specs: "No OpenSpec root", "Unsupported OpenSpec version", "Confirmed install and init"); verify the scenario tests pass

## 2. Skill

- [x] 2.1 Rewrite steps 1, 2 and 7 of `warrant-setup` and add the skills step (specs: all of this change); verify the kit tests pass

## 3. Documentation

- [x] 3.1 Update the install section of `README.md`

## 4. Review

- [x] 4.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 5. Verification

- [x] 5.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 200 passed, 5 skipped in 84.81s (0:01:24) (dogfood tests skip in a worktree without installed skills)
- [x] 5.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
- [x] 5.3 Run every setup scenario on `claude` and `codex`; record each result
  Result: exit 0, 14 of 14 (7 setup scenarios x claude, codex) after the checker accepted a setup that creates the OpenSpec root
