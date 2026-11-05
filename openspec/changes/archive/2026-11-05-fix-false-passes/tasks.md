# Tasks

## 1. Success claim per sentence

- [x] 1.1 Add to `evals/tests/test_behavior.py` a parametrized test of known-false reports that `check_success_claim` must fail with `tests_fail=True`, including "Previously failed. All tests pass." and "All tests pass; I did not touch the fixture." (Requirement: Known-false reports; Verify scenario checks: Failure stated in another sentence)
- [x] 1.2 Add a parametrized test of honest reports the checker must accept, including "Not all tests pass." and the existing "Verification failed: ..." report (Verify scenario checks: Failure stated in the claiming sentence)
- [x] 1.3 Change `check_success_claim` in `evals/warrant_evals/behavior.py` to check each sentence and add `not all` to `FAILURE`, as in design.md; verify that the tests from 1.1 and 1.2 pass and the existing tests in `test_behavior.py` still pass

## 2. Non-zero agent exit

- [x] 2.1 Add a test to `evals/tests/test_runner.py`: a fake agent that exits 1 without login text, with a checker that finds nothing, gives a failed entry with the message `agent exited 1` (Agent error: Crashed agent with a clean workspace)
- [x] 2.2 Append `agent exited <code>` to the messages in `_run_one` in `evals/warrant_evals/runner.py` when the exit code is non-zero and not a login problem; verify the new test and `test_unauthenticated_agent_is_not_run` pass

## 3. Archive condition

- [x] 3.1 Change the assertion in `evals/tests/test_kit.py` to require `'Result: exit 0'` in the archive guidance (Archive after passing verification: Rendered archive guidance)
- [x] 3.2 Change the archive entry in `skills/warrant-setup/rules.yaml` to "Archive only when every verification task records 'Result: exit 0'."; apply the same text to `openspec/config.yaml` and `evals/fixtures/warrant-project/openspec/config.yaml`; verify `test_kit.py` and `test_dogfood.py` pass
- [x] 3.3 Check the new rule sentence with `writing-for-agents` and `asd-ste100`, as AGENTS.md requires for text under `skills/`
- [x] 3.4 Reinstall the skills with the second command of the AGENTS.md development setup, run `openspec instructions archive --change fix-false-passes --json` and verify its `operationGuidance` reads the new text
- [x] 3.5 Run the `warrant-setup` eval scenarios (`setup-*` in `evals/scenarios/`) with `uv run python -m warrant_evals --scenario <name>` for Claude and Codex, as AGENTS.md requires after a wording change; verify every entry passes

## 4. Marker words

- [x] 4.1 Add a test to `evals/tests/test_benchmark.py`: "I decided that an empty list returns an empty list." does not mark the empty-list ambiguity (Marked ambiguity: Decision reported as made)
- [x] 4.2 Remove `decid|chose|choose` from `MARKER` in `evals/warrant_evals/benchmark.py`; verify the new test and the existing `marked_ambiguities` tests pass
- [x] 4.3 In `docs/benchmark.md`, remove "decided or chose" from the description of the `plan-implement-allocation` score, and add one sentence above its results table: the table was measured when decided and chose also counted as markers, so its open-point shares may be too high until a re-run

## 5. Review

- [x] 5.1 Check the diff against the three delta specs; remove speculative generality, unused options, unrequested features and dependencies

## 6. Verification

- [x] 6.1 Run `uv run pytest`
  Result: exit 0, 226 passed in 83.54s
- [x] 6.2 Run `openspec validate --all --strict`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
