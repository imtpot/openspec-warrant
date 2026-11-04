# Proposal

## Why

`warrant-setup` stops when the OpenSpec CLI is missing or old and when the
project has no OpenSpec root, and it only prints the command that installs the
OpenSpec workflow skills at a version tag. The user then runs three commands by
hand. OpenSpec 1.16 can do the skill part itself: `openspec init --tools agents`
writes the workflow skills to `.agents/skills/` for any agent, and `openspec
update` keeps them in step with the CLI. Agents that read only their own skills
directory need a link to each of these skills.

## What Changes

- A missing or old CLI: setup proposes an install command and runs it after the
  user confirms; without confirmation it stops as before.
- No OpenSpec root: setup proposes `openspec init --tools agents --profile
  core` and runs it after the user confirms; without confirmation it stops as
  before.
- Setup links every `.agents/skills/openspec-*` skill into each existing
  `.<agent>/skills/` directory that lacks it.
- Setup reports when `openspec-verify-change` is missing, because the Spec axis
  of `warrant-review` needs it.
- Setup no longer prints the `skills add` command for the OpenSpec skills.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `warrant-setup`: install OpenSpec and its skills with the user's
  confirmation.

## Impact

`skills/warrant-setup/SKILL.md`, setup scenarios, `README.md`.

## Why code is needed

Only the skill text and scenario files change.

## Out of scope

Setup installs OpenSpec and its skills for the project; it never changes the
user's global OpenSpec configuration.

Features and options deliberately left out:

- The `curl ... | sh` installer; a package manager is safer to run from an
  agent.
- Changing the global workflow profile to add `verify`.

## Assumptions

Confirmed by the requester: install OpenSpec from setup; use
`openspec init --tools agents`; link the skills for agents that need it.

- `--profile core`, because `--profile custom` installs no skill for a user
  whose global configuration selects no workflow (checked with an empty
  configuration). Owner: requester (decided while the requester was away).
- The install command follows the project's own tool pinning (`mise.toml`,
  `package.json`) when present, otherwise `npm install -g
  @fission-ai/openspec@latest` or `brew install openspec`. Owner: requester
  (decided while the requester was away).
