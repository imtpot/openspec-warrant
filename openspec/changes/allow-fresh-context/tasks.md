# Tasks

Files this change reaches: `docs/design.md`, `evals/tests/test_kit.py`.

## 1. Kit test

- [x] 1.1 Remove "subagent" from the banned words and add a test: a skill that mentions a fresh or separate context or a sub-agent contains "If you cannot start a separate context" (specs: warrant-kit "Fresh context with a fallback"); verify the test fails on a temporary skill text without the sentence and passes on the current skills

## 2. Design

- [x] 2.1 Rewrite principle 6 in `docs/design.md`; verify the kit design test passes

## 3. Review

- [x] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [x] 4.1 Run `uv run pytest` and record its result. Result: `140 passed`, exit 0
- [x] 4.2 Run `openspec validate --all --strict` and record its result. Result: `Totals: 10 passed, 0 failed`, exit 0
