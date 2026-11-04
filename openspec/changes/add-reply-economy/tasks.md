# Tasks

Files this change reaches: `skills/warrant-verify/SKILL.md`,
`skills/warrant-setup/rules.yaml`, `openspec/config.yaml`,
`evals/fixtures/warrant-project/openspec/config.yaml`,
`evals/warrant_evals/checks.py`, `evals/tests/test_verify_propose_checks.py`,
`evals/scenarios/verify.toml`, `evals/scenarios/verify-no-contract.toml`,
`evals/tests/test_kit.py`, `docs/design.md`.

## 1. Checker

- [ ] 1.1 Write failing tests, then let the verify checker require a last line starting with `Not checked:` (specs: behavioral-evals "Closing line check"); verify the tests pass

## 2. Skill and rules

- [ ] 2.1 Add the one-line-per-command report and the closing line to `warrant-verify` (specs: verification-evidence); verify the kit tests pass
- [ ] 2.2 Replace the not-run tasks rule with the result format rule and update the archive guidance in `rules.yaml` and its copies, with a kit test for the format (specs: warrant-rules "Verification result format"); verify the dogfood rules test passes

## 3. Documentation

- [ ] 3.1 Update principle 5 and the drift list in `docs/design.md`; verify the kit design test passes

## 4. Review

- [ ] 4.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 5. Verification

- [ ] 5.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
- [ ] 5.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
- [ ] 5.3 Run the verify, tdd and propose scenarios on `claude`, `codex` and `copilot`; record each result and update the README agent table
