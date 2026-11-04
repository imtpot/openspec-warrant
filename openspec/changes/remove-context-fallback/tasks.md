# Tasks

Files this change reaches: `skills/warrant-review/SKILL.md`,
`evals/tests/test_kit.py`, `docs/design.md`.

## 1. Kit test

- [ ] 1.1 Replace the fallback test with a test that no skill contains "If you cannot start a separate context", and see it fail (specs: warrant-kit "Fresh context with a fallback" removed); verify it passes after 2.1

## 2. Skill and documentation

- [ ] 2.1 Remove both fallback sentences from `warrant-review` (specs: code-review "Axes in fresh contexts", "Artifact review in a sub-agent"); verify the kit tests pass
- [ ] 2.2 Update principle 6 in `docs/design.md`; verify the kit tests pass

## 3. Review

- [ ] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [ ] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.3 Run the review and artifact-review scenarios on `claude`, `codex` and `copilot`; record each result
