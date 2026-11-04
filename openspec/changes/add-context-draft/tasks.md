# Tasks

Files this change reaches: `skills/warrant-setup/SKILL.md`,
`evals/warrant_evals/openspec_rules.py`, `evals/warrant_evals/checks.py`,
`evals/tests/test_setup_check.py`, `evals/scenarios/setup-fresh.toml`,
`evals/scenarios/setup-upgrade.toml`, `evals/fixtures/fresh-project/`,
`evals/fixtures/setup-upgrade/openspec/config.yaml`, `README.md`,
`docs/design.md`.

## 1. Checker

- [ ] 1.1 Write failing tests, then let the setup checker read the rendered context and check expected terms, absent contract commands and an unchanged context (specs: behavioral-evals "Context checks"); verify the tests pass

## 2. Skill

- [ ] 2.1 Add the context step to `warrant-setup` (specs: warrant-setup "Draft the OpenSpec context", "Write only confirmed context", "Keep existing context"); verify the kit tests pass

## 3. Scenarios and documentation

- [ ] 3.1 Add a German-text constraint to the `fresh-project` README and a team context to the `setup-upgrade` fixture; set the scenario params and prompts; verify the scenario tests pass
- [ ] 3.2 Update `README.md` and `docs/design.md`; verify the kit tests pass

## 4. Review

- [ ] 4.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 5. Verification

- [ ] 5.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 5.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 5.3 Run every setup scenario on `claude`, `codex` and `copilot`; record each result
