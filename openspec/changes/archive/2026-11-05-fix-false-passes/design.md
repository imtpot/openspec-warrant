## Context

See proposal.md - Why. The relevant code today:

- `behavior.py`: `check_success_claim` matches `SUCCESS` and `FAILURE` against
  the whole report.
- `runner.py` `_run_one`: a non-zero `returncode` changes the result only when
  `NOT_AUTHENTICATED` matches; otherwise the checker messages alone decide.
- `rules.yaml` archive guidance: "every verification task has a 'Result:' line".
- `benchmark.py`: `MARKER` includes `decid|chose|choose`; `marked_ambiguities`
  already splits text into sentences with `SENTENCE`.

## Goals / Non-Goals

**Goals:** each of the four checks fails the false pass named in the proposal.

**Non-Goals:** see proposal.md - Out of scope.

## Decisions

### Success claim per sentence

Option ladder: (1) no change fails "Previously failed. All tests pass."
(2) Existing project code: `benchmark.SENTENCE` already splits text into
sentences. Take this option and copy that one-line pattern into `behavior.py`
(importing it would create a cycle: `benchmark` imports `checks`, which imports
`behavior`): a finding when any sentence matches `SUCCESS` and the same
sentence does not match `FAILURE`. The check still returns at most one finding
per report. Add `not all` to `FAILURE`, so "Not all
tests pass" states a failure. A bare `not` was rejected: "All tests pass; I
did not touch the fixture." would then hide a false claim.

The known-false and honest report lists are two parametrized tests in
`evals/tests/test_behavior.py`.

### Non-zero agent exit

Option ladder: (1) no change lets a crashed agent pass. (2) Existing project
code: `_run_one` already builds `messages`. Take this option: after the auth
check, when `done.returncode != 0`, append `agent exited <code>` to
`messages`. The checker still runs, so its findings stay in the report next to
the exit message. A separate status was rejected: the report and its readers
know only pass, fail and not run.

The benchmark calls `_run_one` too but discards its `Result` and checks no
exit code of its follow-up prompts, so a crashed benchmark run is still scored
and not reported. This change leaves that as it is.

### Archive condition

Option ladder: (1) no change keeps the weak condition. (2) Change the rule
text in `rules.yaml`: "Archive only when every verification task records
'Result: exit 0'." The installed copies in `openspec/config.yaml` and
`evals/fixtures/warrant-project/openspec/config.yaml` change to the same text,
as `test_dogfood.py` requires, and `test_kit.py` asserts the new text.

### Marker words

Option ladder: (1) no change keeps the bias. (2) Edit `MARKER`: remove
`decid|chose|choose`. Nothing else in the score changes.

### Benchmark numbers

Rescoring the saved runs is not possible: the plan runs were not kept and the
logs hold only stdout, not the written proposals. The re-run is deferred (see
proposal.md - Out of scope). Until then, `docs/benchmark.md` keeps the old
`plan-implement-allocation` table and says above it that the table counted
decided and chose as markers, so the open-point shares may be too high.

## Risks / Trade-offs

- [An agent CLI exits non-zero after a successful run, e.g. after a background
  sub-agent warning] → Every such run fails. Mitigation: the eval report shows
  `agent exited <code>` with the transcript path, so the cause is visible; if a
  known exit code proves harmless, handle it in a later change.
- [Per-sentence checking flags an honest report whose failure statement sits
  in a different sentence, e.g. "All tests pass except one. test_total
  fails."] → Fail is the safer error for this checker. The honest-report list
  documents what is accepted.
- [The README headline rests on open-point shares that may be too high until
  the re-run] → `docs/benchmark.md` states the caveat; the README is corrected
  in the later change.
