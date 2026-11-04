# Tasks

Files this change reaches: `evals/tests/test_kit.py`, `skills/*/SKILL.md`
(description lines only), `docs/design.md`.

## 1. Kit tests

- [x] 1.1 Write `evals/tests/test_kit.py` with one parametrized test per requirement of `warrant-kit` (agent-neutral text, size, description start, license, eval coverage, design map), each failure naming the skill and the reason; verify the description test fails for the skills whose description summarizes a workflow and the other tests pass

## 2. Descriptions

- [x] 2.1 Rewrite each failing description to say only when to use the skill, starting with "Use when" or "Use before"; reinstall the skills with the `AGENTS.md` setup command; verify `test_kit.py` and `test_dogfood.py` pass

## 3. Review

- [x] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [x] 4.1 Run `uv run pytest` and record its result. Result: `150 passed`, exit code 0
- [x] 4.2 Run `openspec validate --all --strict` and record its result. Result: `Totals: 10 passed, 0 failed`, exit code 0
- [x] 4.3 Run `openspec schema validate warrant` and record its result. Result: `Schema 'warrant' is valid`, exit code 0
- [x] 4.4 Run every eval scenario on `claude`, `codex` and `copilot`, because the rewritten descriptions decide when agents load the skills; record pass, fail or not run per entry and update the README agent table. Result: Claude 24/25 (`design-stop-early` lists open decisions without owners), Codex 25/25 (after running it with `allow_login_shell=false`), Copilot 24/25 (`minimal-change` leaves a stray file). Copilot's earlier `verify-no-contract` failure is gone with the new description. Two first-run Codex failures came from checkers bound to wording; they now anchor on requirement keywords and test ids, and the minimal-change checker no longer stages files
