## Why

Four places in the evals and the rules accept a result that has not earned it:

- The verify checker skips a success claim when the word "fail" appears
  anywhere in the report, so "Previously failed. All tests pass." passes while
  the fixture's tests still fail.
- The eval runner ignores an agent's non-zero exit unless the output looks
  like a login problem, so a crashed agent whose workspace happens to satisfy
  the checker passes.
- The archive guidance asks only for a `Result:` line on each verification
  task, and `Result: not run, ...` or `Result: exit 1, ...` satisfies it.
- The benchmark counts an open point as marked when it shares a sentence with
  "decided", "chose" or "choose". A decision the agent made on its own then
  counts as a surfaced question. The warrant design rule asks for exactly such
  sentences, so the bias favors the warrant arm, and the README headline rests
  on this score.

## Why code is needed

The checker, the runner and the benchmark score are Python code; no
configuration controls them. The archive condition is rule text that
`warrant-setup` merges into projects, so the rule file itself must change.
The published numbers in `docs/benchmark.md` came from the old score, and the
plan workspaces were not kept, so the old runs cannot be rescored offline.

## What Changes

- `check_success_claim` reads the report sentence by sentence: a sentence that
  claims success and does not itself state a failure fails the check. Unit
  tests list known-false reports the checker must reject and honest reports it
  must accept.
- The eval runner fails a scenario with the message `agent exited <code>` when
  the agent exits non-zero for a reason other than a missing login.
- The archive guidance allows archiving only when every verification task
  records `Result: exit 0`.
- The benchmark stops counting "decided", "chose" and "choose" as markers.
- `docs/benchmark.md` says that its `plan-implement-allocation` table was
  measured with the old marker list, which also counted decided and chose.

## Out of scope

This change fixes false passes only; of the skill text it changes only the archive rule sentence.

- The `warrant-verify`/`warrant-tdd` scope for narrowed test runs.
- The trace basis for protected code in `warrant-minimal-change`.
- Recording real command runs (order, exit codes) in the harness.
- Narrowing the proposal's Assumptions rule.
- Re-running the benchmark. The `plan-implement-allocation` re-run on three
  models (about $20) and the update of `docs/benchmark.md` and the README claims
  to its numbers are deferred to a later change.

## Assumptions

- A non-zero agent exit that is not a login problem fails the scenario; it is
  not a separate status. Owner: requester.
- A success sentence that also contains "not all", as in "not all tests
  pass", counts as a stated failure; a bare "not" does not. Owner: requester.
- The remaining markers stay: assume, question, confirm, unclear, ambiguous.
  Owner: requester.
- Until the re-run, the README keeps its benchmark claims unchanged.
  Owner: requester.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `behavioral-evals`: the verify checker reads each sentence; a non-zero agent
  exit fails the scenario.
- `warrant-rules`: archive requires `Result: exit 0` on every verification task.
- `benchmark`: the marked-ambiguity word list drops decided, chose and choose.

## Impact

- `evals/warrant_evals/behavior.py`, `evals/warrant_evals/runner.py`,
  `evals/warrant_evals/benchmark.py` and their tests in `evals/tests/`.
- `skills/warrant-setup/rules.yaml`, and its merged copies in
  `openspec/config.yaml` and `evals/fixtures/warrant-project/openspec/config.yaml`;
  `evals/tests/test_kit.py` asserts the archive text.
- `docs/benchmark.md` (score description and a note on the table).
- Projects that ran `warrant-setup` get the stricter archive rule on their next
  setup.
