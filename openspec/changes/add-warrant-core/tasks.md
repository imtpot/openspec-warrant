# Tasks

Files this change creates: `pyproject.toml`, `LICENSE`, `README.md`, `AGENTS.md`,
`.gitignore`, `skills/warrant-setup/` (with `schema/warrant/`),
`skills/warrant-minimal-change/SKILL.md`, `skills/warrant-verify/SKILL.md`,
`evals/warrant_evals/`, `evals/tests/`, `evals/fixtures/`, `evals/scenarios/`.

## 1. Repository scaffold

- [x] 1.1 Add `pyproject.toml` (Python 3.12+, `pytest` as the only dev dependency, `evals` as the test path), MIT `LICENSE` for imtpot, `.gitignore` for `.venv/` and eval output; verify `uv sync` succeeds and `uv run pytest` exits with code 5 (no tests collected yet)
- [x] 1.2 Add `AGENTS.md` with this repository's own `## Warrant contract` (Verification: `uv run pytest`, `openspec validate --all --strict`; `openspec schema validate warrant` is added when this repository switches to the warrant schema, see Workflow follow-up; Destructive actions: `git push`, `gh release`; Glossary: none; Decision records: none); verify by reading the four subsections in order

## 2. Contract parser and artifact checkers

- [x] 2.1 Write failing tests in `evals/tests/` for the contract parser: four subsections in order, verification bullets with backticked commands, `none` locations, missing section, empty Verification list (specs: project-contract); verify they fail
- [x] 2.2 Implement the parser in `evals/warrant_evals/contract.py` with the standard library; verify the 2.1 tests pass
- [x] 2.3 Write failing tests with recorded spec files for the requirement checker: missing EARS keyword, two `SHALL`, `WHERE` before an environment state, valid requirements of each of the five patterns (specs: warrant-schema, behavioral-evals "Propose scenario checks"); verify they fail
- [x] 2.4 Implement the requirement checker and the Assumptions-section check; verify the 2.3 tests pass and each failure message quotes the requirement name
- [x] 2.5 Write failing tests, then implement the success-claim checker (final report versus failing fixture test) and the duplicate-helper checker (new function names versus fixture helpers) (specs: behavioral-evals "Verify scenario checks", "Minimal-change scenario checks"); verify the tests pass

## 3. Eval runner

- [x] 3.1 Write failing tests with a fake agent script for: one entry per scenario and agent, agent filter, separate temporary directory per run with the repository fixture unchanged, missing agent marked not run, 15-minute timeout (lowered by a test parameter) marked timeout, report with transcript paths (specs: behavioral-evals); verify they fail
- [x] 3.2 Implement `evals/warrant_evals/runner.py` and the agent command table in restricted modes, never with a permission-bypass flag (`claude -p --permission-mode acceptEdits --allowedTools`, `codex exec -s workspace-write`, `copilot -p -s --allow-tool`, `agy -p --mode accept-edits --sandbox`), taking each flag from the CLI's `--help`; verify the 3.1 tests pass
- [x] 3.3 Add the workspace preparation step: copy fixture, `git init`, `skills add <repo> -a claude-code codex -y`, commit; verify with a test that an installed skill exists in `.agents/skills/` with its Claude link and that `git status` is clean (the test installs a demo skill, because the warrant skills are written in groups 5–7)

- [x] 3.4 Add the command line `uv run python -m warrant_evals [--scenario NAME]... [--agent NAME]... [--keep]` and a loader for `evals/scenarios/*.toml` (fixture, prompt, checker name, checker parameters); it writes `evals/out/report.md` and exits non-zero when an entry fails (specs: behavioral-evals "Agent filter", "Result report"); verify with tests for the loader, an unknown checker name and the agent filter

## 4. Warrant schema

- [x] 4.1 Run `openspec schema fork spec-driven warrant` and move the result to `skills/warrant-setup/schema/warrant/`; verify the artifact graph matches `spec-driven` with `openspec status --json` in a scratch project
- [x] 4.2 Edit the proposal template and instruction: Assumptions section with owners, statement on configuration, existing tools and documentation as alternatives; verify by reading the rendered `openspec instructions proposal --json`
- [x] 4.3 Edit the specs instruction and template: one EARS pattern, one outcome per requirement, WHERE only for options, trace to request or assumption; verify the requirement checker passes on the template's example requirement
- [x] 4.4 Edit the design instruction: option ladder with the reason each earlier option failed; verify by reading the rendered instruction
- [x] 4.5 Edit the tasks template and instruction: review group, then verification group running each contract command, not-run reporting; verify by reading the rendered template
- [x] 4.6 Verify `openspec schema validate warrant` exits with code 0 in a scratch project that contains the schema

## 5. warrant-setup skill

- [x] 5.1 Add fixtures `fresh-project` (OpenSpec root, `AGENTS.md` without contract, a test command in its build file), `no-agents-md`, `no-openspec`, and `existing-contract`; verify each fixture's `openspec` state by command
- [x] 5.2 Write `skills/warrant-setup/SKILL.md`: version check, OpenSpec root check, schema lookup in project then global skill path, copy with diff-and-confirm on differences, `schema: warrant` with other config fields unchanged, contract skeleton, confirmed verification commands, final `skills add` command for Fission-AI/OpenSpec at `v1.16.0` (specs: warrant-setup); verify it stays under 150 lines
- [x] 5.3 Add a setup scenario and checker: schema files present, only `schema` changed in `config.yaml`, contract headings, second run leaves `AGENTS.md` unchanged, `no-openspec` and wrong-version cases write nothing; verify with `uv run python -m warrant_evals --scenario setup --agent claude`

## 6. warrant-minimal-change skill

- [x] 6.1 Add fixture `has-helper` with an existing helper and a task that the helper solves; verify the fixture tests pass
- [x] 6.2 Write `skills/warrant-minimal-change/SKILL.md`: option ladder, skipped features named, complete change, line-to-requirement trace inside an OpenSpec change, protected code, `shortcut:` marker, ledger mode with `git grep` and `no-trigger` tag (specs: minimal-change); verify it stays under 150 lines
- [x] 6.3 Add the minimal-change scenario and a ledger scenario (two markers, one without trigger; `git status` unchanged after the run); verify both with `--agent claude`

## 7. warrant-verify skill

- [x] 7.1 Add fixtures `failing-test` (contract with a test command and one failing test) and `no-contract`; verify the fixture test fails as intended
- [x] 7.2 Write `skills/warrant-verify/SKILL.md`: run every contract command before a claim, evidence per command, failure blocks the claim, not-run reporting, fresh evidence only, approval for destructive commands, missing contract and empty list handling (specs: verification-evidence, project-contract); verify it stays under 150 lines
- [ ] 7.3 Add the verify scenario and the propose scenario on `fresh-project` with the warrant schema installed; verify both with `--agent claude`

## 8. Discovery and documentation

- [ ] 8.1 Add the discovery smoke scenario: the agent lists the warrant skills and quotes a contract line; verify with `--agent claude`
- [ ] 8.2 Write `README.md`: purpose, install (`npx skills add imtpot/openspec-warrant`, then `warrant-setup`), contract format, supported agents with their smoke result, "Inspired by" links, "not affiliated with Fission-AI"; verify every command in it against the implementation

## 9. Review

- [ ] 9.1 Review the diff for speculative generality, unused options, unrequested features and new dependencies; remove what the specs do not require; verify `pyproject.toml` lists only `pytest` and every skill file is under 150 lines

## 10. Verification

- [ ] 10.1 Run `uv run pytest` and record the summary line
- [ ] 10.2 Run `openspec validate --all --strict` and record the result
- [ ] 10.3 Run `openspec schema validate warrant` in a scratch project with the schema installed and record the result
- [ ] 10.4 Run all scenarios for each of `claude`, `codex`, `copilot` and `agy`; record pass or fail per entry, and record an agent as not run with the reason when its CLI is missing or not authenticated

## Workflow follow-up

- Switch this repository to `schema: warrant` by running its own `warrant-setup`, then add `openspec schema validate warrant` to the contract's Verification list.
- Create the GitHub repository `imtpot/openspec-warrant` and push (requires explicit authorization).
- Archive the change.
