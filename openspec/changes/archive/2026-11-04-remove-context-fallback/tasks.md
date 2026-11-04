# Tasks

Files this change reaches: `skills/warrant-review/SKILL.md`,
`evals/tests/test_kit.py`, `docs/design.md`.

## 1. Kit test

- [x] 1.1 Replace the fallback test with a test that no skill contains "If you cannot start a separate context", and see it fail (specs: warrant-kit "Fresh context with a fallback" removed); verify it passes after 2.1

## 2. Skill and documentation

- [x] 2.1 Remove both fallback sentences from `warrant-review` (specs: code-review "Axes in fresh contexts", "Artifact review in a sub-agent"); verify the kit tests pass
- [x] 2.2 Update principle 6 in `docs/design.md`; verify the kit tests pass

## 3. Review

- [x] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [x] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 147 passed, 5 skipped in 73.44s (dogfood tests skip in a worktree without installed skills)
- [x] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 10 passed, 0 failed (10 items)
- [x] 4.3 Run the review and artifact-review scenarios on `claude` and `codex`; record each result
  Result: exit 0, 14 of 14 pass (7 scenarios x claude, codex)
