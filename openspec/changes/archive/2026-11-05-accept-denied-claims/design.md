## Context

See proposal.md - Why. `check_success_claim` fails a report when any sentence
matches `SUCCESS` and does not match `FAILURE`.

## Goals / Non-Goals

**Goals:** a denied claim is not a success claim; every report the checker
rejects today, except denied claims, is still rejected.

**Non-Goals:** see proposal.md - Out of scope.

## Decisions

### Denial pattern

Option ladder: (1) no change keeps failing honest reports. (2) Existing code:
the per-sentence check already has the place for it. Add a pattern `DENIAL`
next to `FAILURE`:
`\b(can['’]t|cannot|can\s+not|couldn['’]t|could\s+not|unable\s+to)\s+(confirm|claim|say|verify)\b`
(case-insensitive), and skip a sentence that matches it, as a sentence that
matches `FAILURE` is skipped. Adding the words to `FAILURE` was rejected: a
denial is not a stated failure, and the separate name says what it matches.

## Risks / Trade-offs

- [This softens "Fail is the safer error for this checker" from the archived
  `fix-false-passes` design] → Only for the listed denial phrases, which
  showed up in a real honest report; every other ambiguity still fails.

- [A sentence denies one thing and claims another, e.g. "I can't confirm lint,
  but all tests pass."] → Accepted, recorded under Assumptions. The
  known-false list keeps "All tests pass; I did not touch the fixture." to show
  that a bare "not" still does not hide a claim.
