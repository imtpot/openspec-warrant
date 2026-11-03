# Tasks

Files this change reaches: `evals/warrant_evals/contract.py`,
`evals/warrant_evals/runner.py`, `evals/warrant_evals/scenarios.py`,
`evals/warrant_evals/checks.py`, `evals/tests/`, `evals/fixtures/` (new review
and receive fixtures, `fresh-project` gains `CONTRIBUTING.md`),
`evals/scenarios/`, `skills/warrant-setup/SKILL.md`,
`skills/warrant-review/SKILL.md`, `README.md`, `AGENTS.md` (development setup
command), `openspec/schemas/warrant/` (unchanged; dogfood test must stay green).

## 1. Contract Standards subsection

- [x] 1.1 Write failing parser tests: five subsections in order, Standards with two backticked paths, Standards `none`, contract without Standards reads as empty standards, Standards before Decision records rejected (specs: project-contract "Contract section and headings", "Standards entries", "Missing Standards subsection"); verify they fail
- [x] 1.2 Make `Standards` an optional last subsection in `contract.py` and add `Contract.standards`; verify the 1.1 tests and all earlier contract tests pass

## 2. Scenario setup script

- [x] 2.1 Write a failing runner test: a scenario with `setup = "setup.sh"` runs that fixture script in the workspace after preparation, and the loader reads the field; verify it fails
- [x] 2.2 Add `Scenario.setup` to the runner and loader; verify the 2.1 test passes

## 3. warrant-setup writes Standards

- [x] 3.1 Add `CONTRIBUTING.md` with one coding rule to the `fresh-project` fixture and extend the setup checker with an expected Standards path; verify the checker unit tests cover present and missing Standards
- [x] 3.2 Update `skills/warrant-setup/SKILL.md`: propose standards files, write the confirmed ones under `### Standards`, or `none` (specs: warrant-setup "Create the contract skeleton"); verify the file stays under 150 lines
- [x] 3.3 Update `setup-fresh` to expect `CONTRIBUTING.md` under Standards; verify with `--agent claude --scenario setup-fresh`

## 4. warrant-review skill

- [x] 4.1 Write `skills/warrant-review/SKILL.md` with review mode (range commands, change selection, Spec, Standards and Evidence axes, finding format, no file changes) and receive mode (classify first, reject conflicts and false claims, ask on unclear comments, verify at the end) (specs: code-review); verify it stays under 150 lines and names no agent-specific tool

## 5. Review evals

- [x] 5.1 Add the `review-branch` fixture: OpenSpec change with three requirements (one implemented and tested, one implemented without test, one not implemented), `docs/standards.md` listed under Standards, and a setup script that creates `origin` and a feature branch whose commit adds an unrequested option, a function that breaks the naming rule, an unused parameter and the removal of an input check; verify `setup.sh` runs in a scratch copy and `git log` shows the branch
- [x] 5.2 Write failing checker tests for the review checker with recorded reports: findings in the right sections, merged axes, missing finding, changed files (specs: behavioral-evals "Review scenario checks"); then implement the checker; verify the tests pass
- [x] 5.3 Add scenarios `review-branch` (default range), `review-named-base` (base given as a tag), `review-empty` (no changes), `review-no-change` (no active OpenSpec change) and `review-two-changes` (asks which change) with checkers for their expected report lines (specs: code-review range, selection and empty-range requirements); verify each with `--agent claude`

## 6. Receive evals

- [x] 6.1 Add the `receive-comments` fixture: an OpenSpec change requiring exit code 2 for an unknown item, implementing code and tests, and `REVIEW.md` with four comments: valid, conflicting with the exit-code requirement, a false claim about a missing check, and an unclear one; verify the fixture tests pass
- [x] 6.2 Write failing checker tests, then implement the receive checker: valid comment applied, exit code still 2, the existing check unchanged, the unclear comment's code unchanged, classification of every comment and the verification command in the report (specs: code-review receive requirements, behavioral-evals "Receive scenario checks"); verify the tests pass
- [x] 6.3 Add the `receive-comments` scenario; verify with `--agent claude`

## 7. Documentation

- [x] 7.1 Update `README.md`: `warrant-review` in the skill list, Standards in the contract format, and the scenario count; update the `AGENTS.md` development setup command to install `warrant-review`; verify every command in both files runs as written

## 8. Review

- [x] 8.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 9. Verification

- [x] 9.1 Run `uv run pytest` and record its result. Result: `89 passed`, exit code 0
- [x] 9.2 Run `openspec validate --all --strict` and record its result. Result: `Totals: 7 passed, 0 failed`, exit code 0
- [x] 9.3 Run `openspec schema validate warrant` and record its result. Result: `Schema 'warrant' is valid`, exit code 0
- [ ] 9.4 Run the new and changed scenarios on `claude`, `codex`, `copilot` and `agy`; record pass, fail or not run with the reason per entry, and update the README agent table
