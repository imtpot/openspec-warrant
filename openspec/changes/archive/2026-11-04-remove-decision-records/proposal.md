# Proposal

## Why

The contract's `### Decision records` subsection points to a separate decision
log such as an ADR directory. In OpenSpec, each change's `design.md` already
records its decisions, and the archive keeps them, so a second location
duplicates OpenSpec (principle 1). Only the artifact review reads the
subsection, and it already falls back to archived `design.md` files. Every
setup asks the user one more question for it.

## What Changes

- The contract has the subsections Verification, Destructive actions, Glossary
  and the optional Standards.
- `warrant-setup` no longer writes or asks for Decision records.
- The artifact review takes recorded decisions only from `design.md` of
  archived changes.
- **Compatibility**: a contract that still has `### Decision records` stays
  valid; skills ignore that subsection.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `project-contract`: four subsections; the old subsection is ignored.
- `warrant-setup`: skeleton without Decision records.
- `code-review`: recorded decisions come from archived changes.

## Impact

`skills/warrant-setup/SKILL.md`, `skills/warrant-review/SKILL.md`,
`evals/warrant_evals/contract.py`, contract tests, fixture `AGENTS.md` files,
the `artifacts-*` fixtures, `README.md`, `AGENTS.md`, `docs/design.md`.

## Why code is needed

The contract parser in the evals must accept the shorter contract, and the
artifact fixtures must record their decision in an archived change.

## Out of scope

This change removes one contract subsection; it does not change how the review
judges a contradiction.

Features and options deliberately left out:

- A migration step in `warrant-setup` that deletes the old subsection; an
  ignored subsection does no harm.
- Reading ADR directories found by search.

## Assumptions

Confirmed by the requester: remove the Decision records subsection.

- A contract that still contains the subsection stays valid and the subsection
  is ignored. Owner: requester (decided while the requester was away).
