# Proposal

## Why

`warrant-setup` installs the OpenSpec CLI and runs `openspec init` after the
user confirms. A global install changes the user's machine, depends on the
operating system and package manager, and Codex's sandbox cannot run init
because it cannot write `.agents/`. The README now gives the manual commands,
and the user runs them once. The skill also sits at its 150-line limit.

## What Changes

- Setup no longer installs the CLI or runs `openspec init`. When either is
  missing, it stops and names the commands: `npm install -g
  @fission-ai/openspec@latest` (or `brew install openspec`) and
  `openspec init --tools agents --profile core`.
- Setup keeps linking the OpenSpec skills into agent skills directories and
  reporting a missing `openspec-verify-change`.
- The `setup-init-confirmed` scenario goes.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `warrant-setup`: stop and name the install and init commands.

## Impact

`skills/warrant-setup/SKILL.md`, setup scenarios, `README.md`.

## Why code is needed

Only the skill text and scenario files change.

## Out of scope

This change narrows setup; it keeps the skill links and the verify note.

Features and options deliberately left out:

- Running the commands after confirmation.

## Assumptions

Confirmed by the requester: leave installing OpenSpec and `openspec init` to
the user and the README; keep the links and the verify note in the skill. No
other decision is open.
