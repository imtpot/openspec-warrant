# Tasks

Files this change reaches: `evals/warrant_evals/runner.py`,
`evals/tests/test_runner.py`, `README.md`, `openspec/config.yaml`,
`openspec/specs/behavioral-evals/spec.md` (Purpose).

## 1. Runner

- [x] 1.1 Change the tests: the agent list is exactly claude, codex and copilot (spec: "Supported agents"); the prompt-flag test covers copilot only; remove the headless-denial test (removed requirement); keep the missing-CLI test (spec: "Agent CLI unavailable"); verify the agent-list test fails
- [x] 1.2 Remove the agy agent, `AGY_SETTINGS`, `COMMAND_DENIED` and its branch from `runner.py`, and the `json` import if unused; verify `uv run pytest` passes

## 2. Documentation

- [x] 2.1 Remove agy from the README table and add a note that agy discovers the skills and the contract but is not evaluated until its headless permission rules work (#548); remove agy from the `context` in `openspec/config.yaml` and from the Purpose of `openspec/specs/behavioral-evals/spec.md`; verify `git grep -i agy` outside `openspec/changes/archive` finds only the README note, this change and the main-spec requirements that this change's delta replaces at archive

## 3. Review

- [x] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [x] 4.1 Run `uv run pytest` and record its result. Result: `90 passed`, exit code 0
- [x] 4.2 Run `openspec validate --all --strict` and record its result. Result: `Totals: 8 passed, 0 failed`, exit code 0
- [x] 4.3 Run `openspec schema validate warrant` and record its result. Result: `Schema 'warrant' is valid`, exit code 0
