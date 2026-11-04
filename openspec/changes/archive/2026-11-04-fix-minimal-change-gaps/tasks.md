# Tasks

Files this change reaches: `skills/warrant-minimal-change/SKILL.md`,
`evals/scenarios/minimal-change-implicit.toml`.

## 1. Skill

- [x] 1.1 Change "Never remove" to "Never leave out or remove" and add accessibility of user interfaces (specs: minimal-change "Protected code"); verify the kit tests pass

## 2. Scenario

- [x] 2.1 Add `minimal-change-implicit` with the minimal-change prompt minus the skill name (specs: behavioral-evals "Minimal change without naming the skill"); verify the scenario tests pass

## 3. Review

- [x] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [x] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 175 passed, 5 skipped in 76.69s (0:01:16) (dogfood tests skip in a worktree without installed skills)
- [x] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
- [x] 4.3 Run `minimal-change` and `minimal-change-implicit` on `claude` and `codex`; record each result
  Result: exit 0, 4 of 4 pass; Codex loaded the skill unprompted, Claude's text output does not show whether it did
