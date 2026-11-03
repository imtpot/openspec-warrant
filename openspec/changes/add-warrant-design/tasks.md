# Tasks

Files this change reaches: `skills/warrant-design/SKILL.md`,
`evals/warrant_evals/checks.py`, `evals/tests/`, `evals/fixtures/design-project/`,
`evals/fixtures/design-no-locations/`, `evals/scenarios/`, `evals/tests/test_dogfood.py`,
`README.md`, `AGENTS.md` (development setup command).

## 1. Fixtures

- [x] 1.1 Add `design-project`: `pyproject.toml` with `requires-python`, a table glossary at `docs/glossary.md` defining "quota" as a project limit, `docs/decisions/0001-use-json.md`, and a contract naming both; add `design-no-locations` with `none` for both; verify each contract parses with the contract parser

## 2. Checkers

- [x] 2.1 Write failing tests, then implement the first-question checker: exactly one question sentence outside code and list items, a recommendation word, no question about the Python version, no file changed (specs: "One question per message", "Options and recommendation", "Look up facts instead of asking"); verify the tests pass
- [x] 2.2 Write failing tests, then implement the recording checker: expected glossary rows and a new `0002-*.md` with Context, Decision and Consequences headings, existing glossary rows and `0001-use-json.md` unchanged, no new OpenSpec change, `openspec-propose` named; and the no-locations variant: no file changed, terms and decisions listed in the transcript (specs: "Record an agreed term", "Record an agreed decision", "Existing records unchanged", "Ready for a proposal", "No change created", "No location declared", "Records without a location"); verify the tests pass

## 3. warrant-design skill

- [x] 3.1 Write `skills/warrant-design/SKILL.md` (specs: design-interview); verify it stays under 150 lines and names no agent-specific tool

## 4. Scenarios

- [x] 4.1 Add scenarios `design-first-question`, `design-record`, `design-conflict` (specs: "Conflicting term") and `design-no-locations`, plus `design-stop-early` whose prompt ends the interview with one decision open and whose checker needs that decision listed as an assumption with an owner (specs: "Remaining decisions as assumptions"); verify each with `--agent claude`

## 5. Documentation

- [x] 5.1 Add `warrant-design` to the README skill list and to the `AGENTS.md` setup command, and to `SKILLS` in `test_dogfood.py`; verify the setup command runs as written

## 6. Review

- [x] 6.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 7. Verification

- [x] 7.1 Run `uv run pytest` and record its result. Result: `102 passed`, exit code 0
- [x] 7.2 Run `openspec validate --all --strict` and record its result. Result: `Totals: 8 passed, 0 failed`, exit code 0
- [x] 7.3 Run `openspec schema validate warrant` and record its result. Result: `Schema 'warrant' is valid`, exit code 0
- [x] 7.4 Run the design scenarios on `claude`, `codex` and `copilot`; record pass, fail or not run with the reason, and update the README agent table. Result: all five pass on Claude, Codex and Copilot. First run: Copilot `design-first-question` failed on checker wording (a closing "Which do you want?" counted as a second question; fixed in the checker, identical questions now count once), and Codex `design-conflict` failed for real (it recorded a decision from the request without confirmation and paraphrased the glossary); the skill now states that a request is not a confirmation and that the definition is quoted word for word, and the rerun of `design-conflict` and `design-record` passes on all three
