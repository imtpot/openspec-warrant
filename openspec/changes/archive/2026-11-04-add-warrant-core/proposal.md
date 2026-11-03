# Proposal

## Why

OpenSpec's `spec-driven` workflow lets an agent write ambiguous requirements,
grow a change past what was asked, and report work as done without evidence.
Project rules in `openspec/config.yaml` reduce this, but they are advisory, they
cannot change templates, operation guidance exists only for apply and archive,
and every project must re-invent and copy them. A trial run on a real project
showed the gaps: compound requirements, `WHERE` used for an environment state,
and nine unconfirmed decisions reported as "no open questions".

Third-party skill sets cover parts of this (EARS notation, minimal changes,
verification before completion), but they assume their own file layouts and
tools, they overlap, and they cannot be edited without losing updates. A single
agent-neutral extension that ships the schema, the skills and the project
contract together removes these compromises.

## What Changes

- Add the `warrant` OpenSpec schema, derived from `spec-driven` 1.16. Its
  templates and instructions require EARS requirements, an Assumptions section
  in the proposal, a design that records which simpler option failed, and
  review and verification task groups in every task list.
- Define the project contract: a fixed-heading section in the target project's
  `AGENTS.md` that declares verification commands, destructive actions, the
  glossary location and the decision-record location. Skills read project
  specifics only from this contract.
- Add the `warrant-setup` skill: it installs the schema into the target
  project, selects it in `openspec/config.yaml`, creates the contract section
  and reports the OpenSpec skills command that matches the installed CLI.
- Add the `warrant-minimal-change` skill: the smallest complete change, with
  every changed line traced to a requirement and every deliberate limitation
  marked with a `shortcut:` comment; it can also list those comments as a debt
  ledger.
- Add the `warrant-verify` skill: no completion claim without running the
  contract's verification commands and reading their output; checks that
  cannot run are reported as not run.
- Add behavioral evals: fixture projects, scenarios and an artifact checker,
  run headless against Claude Code, Codex, GitHub Copilot CLI and agy.
- Publish as a GitHub repository under MIT, installable with
  `npx skills add <owner>/openspec-warrant`.

Why code is necessary: `openspec/config.yaml` cannot change templates or add
operation guidance for propose and verify, and the `skills` CLI distributes
skills but not schemas. Copying rules between projects is what this change
replaces.

## Out of scope

This change delivers the schema, the contract, three skills and their evals; it
does not wrap or replace OpenSpec's own workflow skills.

Features and options deliberately left out:

- Skills for TDD, diagnosis, design and code review (planned for a later change).
- A lightweight schema variant without `design.md`; `design.md` is already
  conditional in `spec-driven`.
- Wrappers around `openspec-propose`, `openspec-apply-change` or other OpenSpec
  workflow skills; projects install those from Fission-AI/OpenSpec.
- Support for OpenSpec versions other than 1.16.
- Agents other than the four named above.
- Running the evals in CI.

## Capabilities

### New Capabilities
- `warrant-schema`: the artifacts, templates and instructions of the `warrant`
  OpenSpec schema.
- `project-contract`: the contract section a target project declares and how
  warrant skills read it.
- `warrant-setup`: installing the schema and the contract into a target project.
- `minimal-change`: the behavior of the `warrant-minimal-change` skill.
- `verification-evidence`: the behavior of the `warrant-verify` skill.
- `behavioral-evals`: the fixtures, scenarios, checker and agent runners that
  test the skills and the schema.

### Modified Capabilities
None.

## Impact

- New repository layout: `skills/<skill-name>/SKILL.md` for the three skills,
  the schema files inside the `warrant-setup` skill directory, and `evals/`.
- Dependencies of target projects: OpenSpec CLI 1.16 and the `skills` CLI.
- Dependencies for running evals: authenticated local installs of Claude Code,
  Codex, GitHub Copilot CLI and agy.

## Open questions

Confirmed by the requester: the GitHub owner is `imtpot`
(`npx skills add imtpot/openspec-warrant`); the project contract is a section
of `AGENTS.md`; the eval checker and runners use Python with `uv`; evals run
manually on a developer machine, not in CI.

Assumptions not yet confirmed by the requester:

1. Copilot CLI and agy read `AGENTS.md` and discover skills in `.agents/skills/`.
   Copilot documents `.agents/skills/`; the rest comes from third-party sources
   and is verified by an eval smoke test. Owner: implementer.
2. An agent running `warrant-setup` can locate the files shipped next to its
   `SKILL.md` for both project and global (`-g`) installs. Owner: implementer;
   resolved in design.
