# Proposal

## Why

An audit of the kit's agent-facing text with `writing-for-agents` and
`asd-ste100` found two contradictions and several gaps besides wording. The
artifact review blocks a requirement that "does not use exactly one EARS
pattern with one SHALL", while the rules allow two combined clauses. The
review's list of protected code lacks accessibility and requested behavior,
which `warrant-minimal-change` protects. An artifact review that ends with
REVISE gives the agent no next step. Tasks are checked off after verification
whether or not it passed. Setup defines no empty form for destructive actions.
Without a change, `warrant-tdd` lists scenarios to the user but does not say
whether to wait. The rest is wording: semicolons that join instructions,
prohibitions where a target works, sentences the model obeys by default,
meanings stated in two places, and terms without one name.

## What Changes

- `warrant-review` takes the EARS rule, the protected list and line tracing
  from their one source instead of restating them.
- Apply guidance: after `Artifact review: REVISE`, revise the artifacts and
  review again; check off a group's tasks only when every verification
  command exited with 0.
- `warrant-setup` leaves the Destructive actions list empty when the user
  confirms none.
- `warrant-tdd` continues after listing derived scenarios.
- Wording across all skills and rules: one instruction per sentence, positive
  targets, no restated or default instructions, named terms ("option ladder",
  "result line") and three verbs kept apart: verify (run the contract's
  commands), check (inspect), confirm (the requester agrees).

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `code-review`: EARS and protected code from their sources.
- `warrant-rules`: a path after REVISE; check off only after passing
  verification.
- `test-first`: continue after derived scenarios.
- `warrant-setup`: empty Destructive actions.

## Impact

All five `skills/*/SKILL.md`, `skills/warrant-setup/rules.yaml` and its
copies, kit tests.

## Why code is needed

Only skill text and rules change, and kit tests follow them.

## Out of scope

This change fixes the audited text; it changes no workflow step.

Features and options deliberately left out:

- Shorter descriptions for `warrant-review` and `warrant-setup`; their
  triggering is measured and works.
- A Review task group that runs `warrant-review` on the diff.

## Assumptions

Confirmed by the requester: apply the audit; keep descriptions; run every
scenario and the benchmark afterwards.

- Without a change, `warrant-tdd` lists the derived scenarios and continues
  without waiting. Owner: requester (decided while the requester was away).
- An empty Destructive actions list is an empty subsection. Owner: requester
  (decided while the requester was away).
