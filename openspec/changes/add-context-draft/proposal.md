# Proposal

## Why

OpenSpec injects `context` from `openspec/config.yaml` into every planning
request, but nothing fills it: `openspec init` leaves a commented example, and
a project that skips it plans without its non-obvious constraints. The
constraints usually already exist as prose in the project's README,
contributing guide or `AGENTS.md`, where an agent may not read them.

## What Changes

- `warrant-setup` drafts `context` when it is missing or empty: only
  constraints an agent cannot infer from the code, taken from the project's own
  documents, as the `openspec init` template asks.
- Setup shows the draft and writes only the lines the user confirms.
- A non-empty `context` stays unchanged.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `warrant-setup`: draft the OpenSpec context.
- `behavioral-evals`: setup checks for the drafted and the kept context.

## Impact

`skills/warrant-setup/SKILL.md`, `evals/warrant_evals/openspec_rules.py`,
`evals/warrant_evals/checks.py`, setup scenarios and fixtures, `README.md`,
`docs/design.md`.

## Why code is needed

The skill text carries the behavior; the checker must read the context as
OpenSpec renders it.

## Out of scope

Setup drafts `context` once; it does not keep it in sync with the project.

Features and options deliberately left out:

- Tech stack, layout and commands in `context`: an agent can infer them from
  the code, and the contract already holds the commands.
- Rewriting a non-empty `context`.

## Assumptions

Confirmed by the requester: setup drafts `context`, and writes only confirmed
lines.

- Draft only constraints an agent cannot infer from the code, following the
  `openspec init` 1.16 template rather than the older migration guide that
  lists the tech stack. Owner: requester (decided while the requester was away).
- Sources are the project's own documents: `README`, contributing guide,
  `AGENTS.md` outside the contract and `docs/`. Owner: requester (decided while
  the requester was away).
- The draft has at most 10 lines. Owner: requester (decided while the
  requester was away).
