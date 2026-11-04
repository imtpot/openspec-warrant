# Tasks

Files this change reaches: `skills/warrant-minimal-change/SKILL.md`,
`evals/scenarios/minimal-change-implicit.toml`.

## 1. Skill

- [ ] 1.1 Change "Never remove" to "Never leave out or remove" and add accessibility of user interfaces (specs: minimal-change "Protected code"); verify the kit tests pass

## 2. Scenario

- [ ] 2.1 Add `minimal-change-implicit` with the minimal-change prompt minus the skill name (specs: behavioral-evals "Minimal change without naming the skill"); verify the scenario tests pass

## 3. Review

- [ ] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [ ] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.3 Run `minimal-change` and `minimal-change-implicit` on `claude` and `codex`; record each result
