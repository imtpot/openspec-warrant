# Tasks

## 1. Repeated runs

- [ ] 1.1 Add tests to `evals/tests/test_runner.py` with the fake agent writer: `run_evals(..., runs=3)` runs the agent three times in three separate workspaces and returns one result per scenario and agent with `runs == 3`, transcripts `<scenario>-<agent>-1.log` to `-3.log` and three workspaces when kept (Repeated runs: Three runs); without `runs` each scenario runs once and its transcript keeps the name `<scenario>-<agent>.log` (Repeated runs: Default)
- [ ] 1.2 Add tests for `combine`: two passes and one fail give `fail`, `passed == 2` and the failed run's messages prefixed `run 3: ` (Entry status from runs: One of three fails); three `not run` results without transcripts give `not run` with the reason and an empty `transcripts` list (Entry status from runs: Agent not installed); a `not run` and a `pass` give `not run` (Entry status from runs: Not run and pass); a single result keeps its messages unprefixed
- [ ] 1.3 Add a test to `evals/tests/test_runner.py` that `write_report` on a combined entry of three runs shows `2/3` and all three transcript paths (Result report); update `test_report_lists_every_entry_with_transcript` to the combined fields
- [ ] 1.4 In `evals/warrant_evals/runner.py`, add `number: int | None = None` to `_run_one` for the transcript name, `runs` to `run_evals` (number passed only when `runs > 1`), `combine`, the fields `passed`, `runs`, `transcripts` and `workspaces` on `Result`, and the Runs column and transcript list in `write_report`, per design.md Decision 1; verify 1.1 to 1.3 and the existing runner tests pass
- [ ] 1.5 Add `--runs` to `evals/warrant_evals/__main__.py` with a type function that rejects values below 1, and pass it to `run_evals`; extend `evals/tests/test_cli.py`: the fake `run_evals` receives `runs == 3` for `--runs 3` and `runs == 1` without the option (Repeated runs: Default), and `--runs 0` raises `SystemExit` with code 2 before `run_evals` is called (Invalid run count: Zero runs)
- [ ] 1.6 Verify `uv run pytest evals/tests/test_benchmark.py` passes unchanged, including the test that expects `two-bare-1-fake.log`

## 2. Scenario suite and exit code

- [ ] 2.1 Add tests to `evals/tests/test_cli.py`: a scenario file without `suite` loads as `regression` (Scenario suite: No suite field); `suite = "regresion"` raises `ValueError` naming the file and `regresion` (Unknown scenario suite: Misspelled suite)
- [ ] 2.2 Add `suite` to `Scenario` and `Result`, read and validate it in `evals/warrant_evals/scenarios.py`, and copy it into each `Result` in `runner.py`; verify 2.1 passes
- [ ] 2.3 Add tests: `main` returns 0 when only a capability entry fails (Capability entries and the exit code: Failed capability scenario) and 1 when a regression entry fails (Exit code by suite: Failed regression scenario); the report has a Suite column and ends with `regression: 2/3` and `capability: 1/1` for that mix (Result report: Totals per suite); the existing Mixed results test still passes
- [ ] 2.4 Implement the Suite column and totals in `write_report` and the exit rule in `__main__.main`; verify 2.3 passes

## 3. Judge

- [ ] 3.1 Create `evals/tests/test_judge.py`, which imports `ask`, `calibrate` and `main` by name from `warrant_evals.judge` and replaces `subprocess.run` and `shutil.which` in that module: the command is `claude -p --model sonnet --tools "" --setting-sources project,local --no-session-persistence --output-format json -- <prompt>` run in a temporary directory, and the prompt holds the description and the text inside `<report>` tags (Judge call: Judge command); a `result` of `Yes\nThe report names it.` gives `('yes', ...)`; `no` and `unknown` map likewise
- [ ] 3.2 Add failure tests: no `claude` on PATH gives `('unknown', 'claude not installed')` (Judge failure: No claude CLI); a non-zero exit, a timeout, output that is not JSON, and a `result` whose first word is not a verdict each give `unknown` with a reason
- [ ] 3.3 Create `evals/warrant_evals/judge.py` with `JUDGE_MODEL`, `ask(description, text)` and the rubric prompt from design.md Decision 3; verify 3.1 and 3.2 pass
- [ ] 3.4 Add tests for `calibrate` with a fake `ask`: three cases with a `yes` verdict on a `no` label give `agreement: 2/3` and a line naming that case, its verdict and reason (Judge calibration: One disagreement); an `unknown` verdict on a `yes` label is a disagreement (Judge calibration: Unknown verdict); `main(path, ask=<fake>)` on a temporary calibration file prints the same output and returns 0; `main` on a missing path and on a file that is not valid TOML raises `SystemExit` with a message naming the path (Calibration file failure: Missing file)
- [ ] 3.5 Implement `calibrate`, `main` and the `__main__` block in `judge.py` per design.md Decision 5; verify 3.4 passes

## 4. Described items in the checks

- [ ] 4.1 Create `evals/tests/conftest.py` with an autouse fixture that sets `warrant_evals.judge.ask` to a fake returning `('no', 'judge off in tests')` (Checker tests: Offline test run); verify the whole suite passes, including `test_judge.py`
- [ ] 4.2 Add tests to `evals/tests/test_review_check.py`, overriding the fake per test: a described Spec finding whose terms miss and whose judge answers `yes` gives no missing finding, and the judge received only the Spec section's text (Judged review findings: Synonym the terms miss); a term match makes no judge call (Term found); a plain list group with no match gives the missing finding with no judge call (Finding without description); an `unknown` verdict gives `Spec section lacks: <first term> (judge: unknown, <reason>)` (Unknown verdict)
- [ ] 4.3 Add tests to `evals/tests/test_benchmark.py`: `review_score` counts a described problem as named on `yes` (Judged review problems: Problem named in other words), as missed with `(judge: unknown, ...)` in `missed` and in the `run_list` output on `unknown` (Judged review problems: Judge unsure), and the existing two-of-three test still passes
- [ ] 4.4 Extend `_missing` in `evals/warrant_evals/checks.py` to accept `{ terms, description }` items and call `judge.ask` through the module at call time; verify 4.2 and 4.3 pass

## 5. Descriptions

- [ ] 5.1 Add a description to each Spec and Standards group of `evals/scenarios/review-branch.toml` and `review-named-base.toml`, to the Spec group of `review-protected.toml`, and to the Standards group of `review-no-change.toml`, written from the `review-branch` fixture and the scenario's setup script; keep the terms, the evidence groups and the `review-no-change` Spec item unchanged
- [ ] 5.2 Add a description to each planted problem of `evals/benchmark/review-refund.toml` and `evals/benchmark/review-export.toml`, written from each task's fixture and setup; keep the terms unchanged
- [ ] 5.3 Create `evals/judge/calibration.toml` with about 20 cases per design.md Decision 5, using the descriptions from 5.1 and 5.2: report excerpts from eval transcripts labeled `yes` or `no`, and written `no` cases that mention the code without reporting the defect
- [ ] 5.4 Add a test to `evals/tests/test_cli.py` that loads every scenario and benchmark task and checks that each described item has a non-empty `description` and at least one term, and that every calibration case has a name, description, text and a `yes` or `no` label; verify the existing `review-protected` load tests still pass with the conftest fake

## 6. Documentation

- [ ] 6.1 Update the Evals section of `docs/benchmark.md`: `--runs N` and `k/N`, the per-run transcript names, `suite` with the exit rule and the totals, described items and the judge (model, no tools, the calibration command, `unknown`, `claude` needed for Codex runs too); update the Benchmark section for the judged review problems

## 7. Eval runs

- [ ] 7.1 Run `uv run python -m warrant_evals.judge`; record the agreement line and each disagreement here. If a `no` case gets `yes`, revise the rubric or the model and run again before 7.2
  Result:
- [ ] 7.2 Run `uv run python -m warrant_evals --agent claude --agent codex --scenario review-branch --scenario review-protected --runs 2`; verify the report shows `k/2` per entry, the Suite column and the totals; read the transcript of every finding the judge decided and record whether each verdict is right
- [ ] 7.3 Run `uv run python -m warrant_evals.benchmark --agent claude --arm warrant --runs 1 --task review-refund --task review-export`; verify the run list shows judged and missed problems as expected

## 8. Review

- [ ] 8.1 Check the diff against the delta specs; remove speculative generality, unused options, unrequested features and dependencies

## 9. Verification

- [ ] 9.1 Run `uv run pytest`
  Result:
- [ ] 9.2 Run `openspec validate --all --strict`
  Result:
