# Tasks

Files this change reaches: `skills/warrant-setup/` (`rules.yaml` added,
`schema/` removed, `SKILL.md`), `skills/warrant-design/` (removed),
`skills/warrant-minimal-change/SKILL.md`, `evals/warrant_evals/` (`checks.py`,
`runner.py`, `scenarios.py`), `evals/tests/`, `evals/fixtures/` (setup fixtures,
`warrant-project`, `setup-upgrade` added, design fixtures removed),
`evals/scenarios/`, `docs/design.md`, `README.md`, `AGENTS.md`,
`openspec/config.yaml`, `openspec/schemas/` (removed).

## 1. Rules file

- [x] 1.1 Write a failing kit test: every entry in `skills/warrant-setup/rules.yaml` starts with `[warrant] `, and the file holds rules for proposal, specs, design and tasks and apply and archive guidance (specs: warrant-rules "Marked entries"); verify it fails
- [x] 1.2 Write `rules.yaml` from the schema's warrant additions plus the glossary rule and apply guidance naming `warrant-tdd`, `warrant-minimal-change` and `warrant-verify`; verify the kit test passes and, in a scratch project with the rules merged, `openspec instructions <artifact> --json` shows each rule and `openspec instructions apply --json` shows the guidance (specs: warrant-rules content requirements)

## 2. warrant-setup

- [x] 2.1 Extend the setup checker and its unit tests: `[warrant] ` rules present for the four artifacts and apply guidance present, `schema` and non-warrant lines unchanged, old `[warrant] ` entries replaced (specs: warrant-setup "Install the rules", "Keep the project's configuration", "Replace warrant entries on upgrade"); verify the tests pass
- [x] 2.2 Rewrite `skills/warrant-setup/SKILL.md`: version 1.16 or later, find `rules.yaml`, merge by marker, verify through `openspec instructions`, report the OpenSpec skills command for the installed version (specs: warrant-setup); remove `schema/`; verify the kit tests pass
- [x] 2.3 Add project rules to the `existing-contract` fixture, add the `setup-upgrade` fixture and scenario, and update the setup scenario expectations; verify the setup scenarios with `--agent claude`

## 3. Remove the schema and warrant-design

- [x] 3.1 Replace the schema in the `warrant-project` fixture by `schema: spec-driven` plus the shipped rules, replace the schema dogfood test by a rules-equality test, and remove `openspec/schemas/warrant/` after this repository runs its own setup (task 5.1); verify `uv run pytest`
- [x] 3.2 Remove `skills/warrant-design/`, the design scenarios, fixtures, checkers and their tests, and `warrant-design` from `AGENTS.md`, `README.md`, `docs/design.md` and `test_dogfood.py`; verify `git grep warrant-design` finds only archived changes and this change

## 4. Smaller removals and additions

- [x] 4.1 Remove the not-applicable mechanism from the runner, loader and tests (specs: behavioral-evals removed requirement); verify `uv run pytest`
- [x] 4.2 Add the no-leftover-files rule to `warrant-minimal-change` and the untracked-file check to the minimal-change checker with a unit test (specs: minimal-change "No leftover files", behavioral-evals "Leftover file check"); verify the tests pass

## 5. This repository and documentation

- [x] 5.1 Switch this repository to `schema: spec-driven` and merge the shipped rules into its `openspec/config.yaml` following the new setup steps; replace `openspec schema validate warrant` in the `AGENTS.md` contract with a check that the rules are rendered; verify `openspec instructions specs --json` shows the `[warrant] ` rules
- [x] 5.2 Update `docs/design.md` (architecture, map, drift, order of work) and `README.md` (what it ships, install, migration from the schema); verify every command in both runs as written

## 6. Review

- [x] 6.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 7. Verification

- [ ] 7.1 Run each command of this repository's contract and record its result
- [ ] 7.2 Run every eval scenario on `claude`, `codex` and `copilot`; record pass, fail or not run per entry and update the README agent table
