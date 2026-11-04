# Tasks

Files this change reaches: `evals/warrant_evals/runner.py`,
`evals/tests/test_runner.py`, `README.md`, `docs/design.md`,
`openspec/config.yaml`.

## 1. Runner

- [x] 1.1 Change the supported-agents test to Claude Code and Codex and see it fail, then remove the Copilot command and allowlist (specs: "Supported agents"); verify the tests pass

## 2. Documentation

- [x] 2.1 Update `README.md`, `docs/design.md` and the context in `openspec/config.yaml`; verify the kit tests pass

## 3. Review

- [x] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [x] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 152 passed in 74.62s
- [x] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 10 passed, 0 failed (10 items)
