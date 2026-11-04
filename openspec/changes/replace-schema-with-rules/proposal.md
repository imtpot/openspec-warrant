# Proposal

## Why

The `warrant` schema is a fork of OpenSpec's `spec-driven`: of its 429 lines
about 80 % are a copy of upstream text. The copy stops receiving OpenSpec's
improvements, pins warrant to one OpenSpec version and breaks the kit's first
principle ("extend OpenSpec, do not duplicate it", `docs/design.md`).
OpenSpec's own guidance is to start with `config.yaml` and fork only when
configuration is not enough; everything warrant adds to the artifacts is
instruction text, which `rules` carry. `warrant-design` duplicates
`openspec-explore` and contradicts it by writing files.

## What Changes

- **BREAKING**: remove the `warrant` schema. Projects stay on `spec-driven`.
- `warrant-setup` writes warrant's artifact rules and apply guidance into the
  project's `openspec/config.yaml`, merged with the project's own entries and
  marked so that a later setup replaces only warrant's entries.
- The rules carry what the schema carried: EARS requirements, one outcome per
  requirement, WHERE only for options, traceability, an Assumptions section,
  the option ladder, review and verification task groups, glossary use.
- **BREAKING**: remove `warrant-design`; the interview belongs to
  `openspec-explore`, and the glossary rule moves into the artifact rules.
- Remove the unused "scenario not applicable to an agent" mechanism.
- `warrant-minimal-change` forbids leftover temporary files in the change.

## Capabilities

### New Capabilities
- `warrant-rules`: the artifact rules and apply guidance warrant adds to a
  project's OpenSpec configuration.

### Modified Capabilities
- `warrant-setup`: installs rules and guidance instead of a schema; supports
  OpenSpec 1.16 and later.
- `behavioral-evals`: scenarios follow the removal of the schema and of
  `warrant-design`; the not-applicable mechanism goes.
- `minimal-change`: no leftover temporary files.
- `warrant-schema`: retired.
- `design-interview`: retired.

## Impact

`skills/warrant-setup/` (rules file replaces `schema/`), `skills/warrant-design/`
(removed), `skills/warrant-minimal-change/SKILL.md`, `evals/` (setup and propose
checkers, fixtures, design scenarios removed, runner), `docs/design.md`,
`README.md`, `AGENTS.md`, this repository's `openspec/config.yaml` and
`openspec/schemas/` (removed).

## Why code is needed

The rules must reach every target project's configuration and be updated
there without touching the project's own rules; only `warrant-setup` can do
that. The rest of the change deletes code.

## Out of scope

This change replaces the schema with configuration and removes duplicates; it
does not narrow `warrant-review`, which follows in its own change.

Features and options deliberately left out:

- Keeping the schema as an option next to the rules.
- Changing OpenSpec's templates.
- A replacement interview skill.

## Assumptions

Confirmed by the requester: replace the schema with rules written by
`warrant-setup`; remove `warrant-design`.

- warrant's rule and guidance entries start with `[warrant] ` so that setup can
  find and replace them. Owner: requester.
- Setup accepts OpenSpec 1.16 and later, because `operations` guidance exists
  from 1.16. Owner: requester.
- Agreed terms are added to the glossary by the agent writing the proposal or
  design, as an artifact rule; decision records stay in `design.md` (Decisions)
  and the contract's Decision records subsection is no longer read by any skill.
  Owner: requester.
