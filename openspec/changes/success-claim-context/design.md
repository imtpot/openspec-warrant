## Context

See proposal.md - Why. `check_success_claim` skips a sentence that matches
`FAILURE` or `DENIAL` and otherwise fails on any `SUCCESS` match.

## Goals / Non-Goals

**Goals:** a success phrase that a qualifier in its own clause governs is not a
claim; every false report in the tests, and the realistic false reports below,
stay rejected.

**Non-Goals:** see proposal.md - Out of scope.

## Decisions

### Qualifier before the claim, in its clause

This replaces two archived decisions:

- `accept-denied-claims`: "Add a pattern `DENIAL` next to `FAILURE` ... skip a
  sentence that matches it". The closed phrase list missed the next honest
  report.
- `fix-false-passes`: "A bare `not` was rejected: 'All tests pass; I did not
  touch the fixture.' would then hide a false claim." A bare "not" now counts,
  but only in the claim's own clause and before the claim, so that sentence and
  its mirror "I did not touch the fixture; all tests pass." stay claims.

Option ladder: (1) no change keeps failing honest reports. (2) Existing code:
keep the per-sentence split and `FAILURE`; replace `DENIAL` with

- `QUALIFIER = n['’]t\b|\b(not|no|never|cannot|unable|without|until|unless|only|whether|if|proof|evidence)\b`
- `CLAUSE = [;:,—–]|\s--?\s|\b(and|but|so)\b`

(both case-insensitive). A sentence is a claim when it does not match
`FAILURE` and some `SUCCESS` match in it has no `QUALIFIER` match in the text
between the last `CLAUSE` boundary before it and the match itself.

A first version read the whole text before the match. The artifact review
showed it accepted realistic false reports for this fixture ("No regressions:
all tests pass.", "I did not change behavior; all tests pass.", "Without any
behavior change, the work is complete."). The clause limit rejects all of them.

This also rejects "I can't confirm lint, but all tests pass.", which the
`accept-denied-claims` design accepted as a risk: the checker is stricter
there.

Checked before writing this design: 17 false reports (the 5 in the tests, the
mirror case, and 11 from the review) are rejected; 19 honest reports (the
tests, both real reports, and one sentence per qualifier word) are accepted.

## Risks / Trade-offs

- [This softens "Fail is the safer error for this checker" from the archived
  `fix-false-passes` design further than `accept-denied-claims` did] → The
  softening is limited to a qualifier in the claim's own clause; a false claim
  must put the qualifier right in front of itself to pass.
- [A false claim with a qualifier in its own clause, e.g. "Only now all tests
  pass." or "No doubt the work is complete."] → Accepted
  (proposal.md - Assumptions). No other check of the verify scenarios catches
  it: `verify-no-contract` checks with its `.tests-ran` marker that no test ran,
  not that the report is true, and `verify` has no marker.
