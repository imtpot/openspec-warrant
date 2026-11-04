# Tasks

Files this change reaches: `skills/warrant-setup/rules.yaml`,
`openspec/config.yaml`, `evals/fixtures/warrant-project/openspec/config.yaml`,
`evals/tests/test_kit.py`.

## 1. Rule

- [ ] 1.1 Write a failing kit test, then add the archive guidance entry to `rules.yaml` and its copies (specs: "Purpose after archive"); verify the kit and dogfood tests pass

## 2. Review

- [ ] 2.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 3. Verification

- [ ] 3.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 3.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 3.3 Run the setup scenarios on `claude` and `codex`; record each result
