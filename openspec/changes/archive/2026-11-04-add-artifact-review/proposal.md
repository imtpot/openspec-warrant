# Proposal

## Why

warrant's artifact rules are advice: an agent can still write a compound
requirement, leave a decision unconfirmed and unlisted, or skip the
verification tasks, and nothing notices before code is written. The trial runs
showed all three. anvil reviews the artifacts in a fresh context before
implementation; with fresh contexts now allowed, warrant can do the same
without a new artifact. The review also gives the contract's Decision records
subsection a reader again: a new decision that contradicts a recorded one is
caught before it is built.

## What Changes

- `warrant-review` gains an artifact mode: it reviews a change's proposal,
  specs, design and tasks against warrant's rules and the project's recorded
  decisions, in a separate fresh context, without changing files.
- The artifact review ends with one line CI can parse: `Artifact review: PASS`
  or `Artifact review: REVISE`.
- warrant's apply guidance asks for an artifact review before the first task
  and to continue only after `PASS`.
- Two eval scenarios: flawed artifacts must get `REVISE` with the flaws named;
  sound artifacts must get `PASS`.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `code-review`: the artifact mode.
- `warrant-rules`: apply guidance asks for the artifact review.
- `behavioral-evals`: artifact review scenarios.

## Impact

`skills/warrant-review/SKILL.md`, `skills/warrant-setup/rules.yaml`, this
repository's `openspec/config.yaml` and the `warrant-project` fixture
configuration (rules copies), new fixtures, scenarios and a checker in
`evals/`, `docs/design.md`, `README.md`.

## Why code is needed

OpenSpec has no review step for artifacts, and `openspec validate` checks
structure, not warrant's rules; the review skill and the guidance must change.

## Out of scope

This change adds an artifact review; it does not add a new artifact, block
apply mechanically, or count review rounds.

Features and options deliberately left out:

- A review artifact file in the change (anvil's `review.md`).
- A limit on review rounds; the requester decides when to stop.
- Cross-model review.

## Assumptions

Confirmed by the requester: fresh contexts may be used; take anvil's artifact
review without an agent-specific mechanism.

- The artifact review lives in `warrant-review`, not in a new skill, and writes
  no file. Owner: requester (decided while the requester was away).
- The verdict line is the last line of the report, exactly `Artifact review:
  PASS` or `Artifact review: REVISE`. Owner: requester (decided while the
  requester was away).
- Recorded decisions are read from the contract's Decision records location
  and from the `design.md` files of archived changes. Owner: requester
  (decided while the requester was away).
