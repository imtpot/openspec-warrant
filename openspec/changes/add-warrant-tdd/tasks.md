# Tasks

Files this change reaches: `skills/warrant-tdd/SKILL.md`,
`evals/warrant_evals/checks.py`, `evals/tests/`, `evals/fixtures/tdd-project/`,
`evals/fixtures/tdd-no-tests/`, `evals/fixtures/tdd-direct/`, `evals/scenarios/`,
`evals/tests/test_dogfood.py`, `README.md`, `AGENTS.md` (setup command).

## 1. Fixtures

- [ ] 1.1 Add `tdd-project`, `tdd-no-tests` and `tdd-direct` as described in design decision 4; verify each fixture's tests pass and each contract parses

## 2. Checker

- [ ] 2.1 Write failing tests, then implement the TDD checker: every expected scenario named in an added test name or comment (normalized), a failing line before a passing line per red-green scenario in the transcript, an "already" report and unchanged code for present behavior, a narrowed command matching a pattern, the full tests command in the transcript (specs: test-first "A test per scenario", "Test names its scenario", "Behavior already present", "Narrowed test command", "Red and green evidence", "Full verification at the end"; behavioral-evals "TDD scenario checks"); verify the tests pass

## 3. warrant-tdd skill

- [ ] 3.1 Write `skills/warrant-tdd/SKILL.md` (specs: test-first); verify it stays under 150 lines and names no agent-specific tool

## 4. Scenarios

- [ ] 4.1 Add `tdd-change` (tdd-project), `tdd-no-tests` (specs: "No tests command") and `tdd-direct` (specs: "Scenarios without a change": the transcript lists scenarios and a test is added); verify each with `--agent claude`

## 5. Documentation

- [ ] 5.1 Add `warrant-tdd` to the README skill list, the `AGENTS.md` setup command and `SKILLS` in `test_dogfood.py`, and state in the README that evals check the TDD report, not the runs themselves; verify the setup command runs as written

## 6. Review

- [ ] 6.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 7. Verification

- [ ] 7.1 Run `uv run pytest` and record its result
- [ ] 7.2 Run `openspec validate --all --strict` and record its result
- [ ] 7.3 Run `openspec schema validate warrant` and record its result
- [ ] 7.4 Run the TDD scenarios on `claude`, `codex` and `copilot`; record pass, fail or not run with the reason, and update the README agent table
