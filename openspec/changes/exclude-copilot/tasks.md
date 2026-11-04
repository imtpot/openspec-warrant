# Tasks

Files this change reaches: `evals/warrant_evals/runner.py`,
`evals/warrant_evals/__main__.py`, `evals/tests/test_runner.py`,
`evals/tests/test_cli.py`, `README.md`, `docs/design.md`,
`openspec/config.yaml`.

## 1. Default agents

- [ ] 1.1 Write failing tests, then run Claude Code and Codex without a filter and Copilot only when named (specs: "Supported agents", "Copilot on request"); verify the tests pass

## 2. Documentation

- [ ] 2.1 Update `README.md`, `docs/design.md` and the context in `openspec/config.yaml`; verify the kit tests pass

## 3. Review

- [ ] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [ ] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
