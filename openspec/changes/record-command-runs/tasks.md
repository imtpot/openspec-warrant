# Tasks

## 1. Recorder

- [x] 1.1 Add tests in a new `evals/tests/test_record.py` that install shims for a fake tool in a temporary git workspace and run them: a failing run piped through `tail` is logged with its non-zero exit; a nested run is logged twice; arguments with spaces, environment variables, stdout, stderr, stdin and the exit code pass through unchanged; `state` changes when a file changes and not otherwise; the log is not in `git status`; with a read-only log directory the tool still runs, its exit code passes through and one warning goes to stderr; a missing real tool exits 127 (Recorded command runs: Piped failing test, Nested run, Tool behavior unchanged; Recorder failure: Read-only log directory)
- [x] 1.2 Add `evals/warrant_evals/record.py` with the shim entry point, `install_shims(workspace, tools) -> dict` (the env changes), `recorded_runs(workspace)` and `workspace_state(workspace)`, as in design.md; verify the tests from 1.1 pass

## 2. Runner and scenarios

- [x] 2.1 Add a test to `evals/tests/test_runner.py`: a scenario with `record = ["<fake tool>"]` whose agent script runs the tool leaves one logged run in the workspace, and a scenario without `record` leaves no log
- [x] 2.2 Add `record: list[str]` to `Scenario`, read it in `load_scenarios`, and install the shims in `_run_one` before the agent starts; verify the test from 2.1 and the existing runner tests pass

## 3. Fact checks

- [x] 3.1 Add tests to `evals/tests/test_tdd_check.py` with a written log: a red then green run covering the scenario's test on different states passes, for a test named `test_<scenario>` run by id and for a test under a `# <Requirement>: <Scenario>` comment run by module; only green runs fail with the scenario name; red and green on the same state fail; a `discover` run does not cover a test; a `-k` run with part of the function name covers it; a full run on an earlier state fails with "full verification not run on the final files"; an empty log (no run) fails the same way; a workspace without a log keeps today's results (Recorded red and green: all three scenarios; Recorded full verification)
- [x] 3.2 Add tests to `evals/tests/test_verify_propose_checks.py`: with a log, a `make test` run on the final state passes, an edit after it or no run fails (Recorded full verification: Edit after the full run, Full run never made)
- [x] 3.3 Add the fact checks to `tdd_check` and `verify_check` in `evals/warrant_evals/checks.py`, as in design.md; verify the tests from 3.1 and 3.2 and the existing checker tests pass

## 4. Scenarios

- [x] 4.1 Add `record` to `tdd-change.toml` and `tdd-direct.toml`, and `record` and `full` to `verify.toml`, as in design.md; verify `load_scenarios` loads them
- [x] 4.2 Run `uv run python -m warrant_evals --agent claude --scenario tdd-change --scenario tdd-direct --scenario verify`; verify every entry passes, and for a failure judge from the transcript and the run log whether the checker or the agent is wrong
  Outcome: tdd-change, tdd-direct and verify pass on Claude. The logs show a failing then passing run of each scenario test on changed files, a full run on the final files, and the nested `python3` run under `make test`.

- [x] 4.3 In `docs/benchmark.md`, replace "they cannot prove that each run happened" with what the recorded runs now prove for the TDD and verify scenarios, and that Codex runs cannot record

## 5. Review

- [x] 5.1 Check the diff against the delta spec; remove speculative generality, unused options, unrequested features and dependencies

## 6. Verification

- [x] 6.1 Run `uv run pytest`
  Result: exit 0, 307 passed in 127.91s (0:02:07)
- [x] 6.2 Run `openspec validate --all --strict`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
