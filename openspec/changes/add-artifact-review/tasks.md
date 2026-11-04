# Tasks

Files this change reaches: `skills/warrant-review/SKILL.md`,
`skills/warrant-setup/rules.yaml`, `openspec/config.yaml`,
`evals/fixtures/warrant-project/openspec/config.yaml`,
`evals/fixtures/artifacts-flawed/`, `evals/fixtures/artifacts-sound/`,
`evals/scenarios/artifact-review-*.toml`, `evals/warrant_evals/checks.py`,
`evals/tests/test_artifact_check.py`, `docs/design.md`, `README.md`.

## 1. Fixtures

- [x] 1.1 Add `artifacts-flawed` (an OpenSpec change with a compound requirement, a design that chooses YAML against the recorded JSON decision `docs/decisions/0001-use-json.md`, an output path the proposal does not mention, and tasks without a verification group) and `artifacts-sound` (the same change without the flaws); verify `openspec validate` passes structurally on both

## 2. Checker

- [x] 2.1 Write failing tests, then implement the artifact-review checker: each planted flaw named, the last report line equal to the expected verdict, no file changed (specs: behavioral-evals "Artifact review scenario checks"); verify the tests pass

## 3. Skill and guidance

- [x] 3.1 Add the artifact mode to `skills/warrant-review/SKILL.md` (specs: code-review artifact requirements); verify the kit tests pass and the skill stays under 150 lines
- [x] 3.2 Add the artifact-review entry to the apply guidance in `rules.yaml` and its copies (specs: warrant-rules "Artifact review before apply"); verify the dogfood rules test passes and `openspec instructions apply --json` shows it

## 4. Scenarios and documentation

- [x] 4.1 Add `artifact-review-flawed` and `artifact-review-sound`; update `docs/design.md` and `README.md`; verify both scenarios with `--agent claude`

## 5. Review

- [x] 5.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 6. Verification

- [x] 6.1 Run `uv run pytest` and record its result. Result: `147 passed`, exit 0
- [x] 6.2 Run `openspec validate --all --strict` and record its result. Result: `Totals: 10 passed, 0 failed`, exit 0
- [ ] 6.3 Run both artifact scenarios on `claude`, `codex` and `copilot`; record each result and update the README agent table
