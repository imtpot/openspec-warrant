## Why

`review-protected` failed on Codex 0.166 although the agent was right. It
reported the unrequested option as "Blocking, untraced — `app/cli.py:2–7,11,15–16`:
CLI dispatch, JSON output, and report formatting ...", and left the protected
check on lines 13–14 out, as the scenario wants. The scenario accepts only
"--json" or "JSON option" in the Spec section, so "JSON output" failed it.

## Why code is needed

The accepted terms live in `evals/scenarios/review-protected.toml`; the change
is one parameter value.

## What Changes

- The `spec` param of `review-protected` also accepts "JSON output".

## Out of scope

This change widens one term list; it does not change the review checker.

- Other scenarios' term lists.
- `review-branch`, which also accepts "cli.py" and passed on Codex.

## Assumptions

- "JSON output" names the unrequested option as clearly as "JSON option"; a
  report that names only the JSON output format without flagging it untraced
  would still pass, as with the existing terms. Owner: requester.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None: the scenario's checked behavior is the same; only its accepted wording
grows.

## Impact

- `evals/scenarios/review-protected.toml`.
