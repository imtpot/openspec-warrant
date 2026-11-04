# Tasks

Files this change reaches: `skills/warrant-setup/rules.yaml`,
`openspec/config.yaml`, `evals/fixtures/warrant-project/openspec/config.yaml`,
`evals/tests/test_kit.py`, `docs/design.md`.

## 1. Rules

- [x] 1.1 Write a failing kit test for the result format, then replace the not-run tasks rule with the result format rule and update the archive guidance in `rules.yaml` and its copies (specs: warrant-rules "Verification result format"); verify the kit and dogfood tests pass

## 2. Documentation

- [x] 2.1 Update principle 5, the drift list and the order of work in `docs/design.md`; verify the kit design test passes

## 3. Review

- [x] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [ ] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 4.3 Run the setup-fresh, setup-upgrade and propose scenarios on `claude`, `codex` and `copilot`; record each result
