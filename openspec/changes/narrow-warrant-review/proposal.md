# Proposal

## Why

`warrant-review` checks on its Spec axis whether each requirement is
implemented and tested, which `openspec-verify-change` already does
(Completeness, Correctness, Coherence). That duplicates OpenSpec (kit
principle 1). Meanwhile the review misses what Ponytail's review checks: bugs
and security problems in the code connected to the diff, such as callers of a
changed function. With fresh contexts allowed, the Spec and Standards axes can
also run independently, as mattpocock/skills' two-axis review does.

## What Changes

- The Spec axis runs the `openspec-verify-change` workflow for the change and
  reports its findings, then adds only what that workflow lacks: added lines
  that serve no requirement.
- The Standards axis adds correctness and security of the connected code:
  callers and callees of changed functions are read, not only the diff.
- The Spec and Standards axes each run in a separate, fresh context, with a
  fallback when none is available.
- Eval workspaces get the OpenSpec workflow skills for the installed OpenSpec
  version, because the review now uses one of them.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `code-review`: Spec axis delegated to `openspec-verify-change`; connected
  code on the Standards axis; axes in separate contexts.
- `behavioral-evals`: workspaces carry the OpenSpec skills; the review scenario
  checks a bug in connected code.

## Impact

`skills/warrant-review/SKILL.md`, `evals/warrant_evals/workspace.py`,
`evals/warrant_evals/__main__.py`, `evals/fixtures/review-branch/setup-common.sh`,
`evals/scenarios/review-*.toml`, `docs/design.md`, `README.md`.

## Why code is needed

The review skill's text and the eval workspace preparation must change; no
configuration covers either.

## Out of scope

This change narrows and extends `warrant-review`; it does not add a review of
artifacts before implementation, which follows in its own change.

Features and options deliberately left out:

- A load or performance axis (Ponytail review); no supported project needs it yet.
- Keeping warrant's own requirement and test checks next to verify-change's.

## Assumptions

Confirmed by the requester: delegate the Spec axis to OpenSpec where it
covers it; use fresh contexts with a fallback.

- verify-change's severities are kept as reported (CRITICAL, WARNING,
  SUGGESTION) instead of being mapped to blocking and non-blocking; an untested
  scenario is therefore a WARNING, not blocking. Owner: requester (decided
  while the requester was away).
- If `openspec-verify-change` is not installed, the review reports the Spec
  axis as not run and names the `skills add` command from `warrant-setup`
  instead of checking requirements itself. Owner: requester (decided while the
  requester was away).
- Eval workspaces fetch the OpenSpec skills once per OpenSpec version from
  GitHub and reuse a local cache. Owner: requester (decided while the requester
  was away).
