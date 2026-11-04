# Tasks

Files this change reaches: `evals/warrant_evals/runner.py`,
`evals/tests/test_runner.py`, `README.md`, `docs/design.md`,
`openspec/config.yaml`.

## 1. Runner

- [ ] 1.1 Change the supported-agents test to Claude Code and Codex and see it fail, then remove the Copilot command and allowlist (specs: "Supported agents"); verify the tests pass

## 2. Documentation

- [ ] 2.1 Update `README.md`, `docs/design.md` and the context in `openspec/config.yaml`; verify the kit tests pass

## 3. Review

- [ ] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [ ] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
