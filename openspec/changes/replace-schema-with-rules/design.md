# Design

## Context

See proposal.md - Why. Requirements are in `specs/`.

- OpenSpec 1.16 reads `rules.<artifact>` (lists of strings, injected into that
  artifact's instructions) and `operations.apply|archive.guidance` from
  `openspec/config.yaml` (OpenSpec `docs/customization.md`).
- The `skills` CLI ships a skill directory with any files next to `SKILL.md`;
  `warrant-setup` already finds its own files under `.agents/skills/` or
  `~/.agents/skills/`.

## Goals / Non-Goals

**Goals:**
- One source for warrant's artifact rules: a file shipped with `warrant-setup`.
- A project's own configuration survives every setup run.

**Non-Goals:**
- No code in target projects; the agent edits YAML by following the skill.

## Decisions

### 1. Rules shipped as `skills/warrant-setup/rules.yaml`

The file holds `rules:` (proposal, specs, design, tasks) and `operations:`
(apply, archive) exactly as they will appear in a project's configuration,
every entry starting with `[warrant] `. Option ladder: OpenSpec's `rules` and
`operations` meet the need; no schema, no new mechanism.

### 2. Merge by marker

Setup removes every list entry that starts with `[warrant] ` from the project's
`rules` and `operations` lists, then appends the shipped entries to the same
lists, creating a list only when it is missing. Everything else, including
`schema` and `context`, stays as it is. A second run with the same file
therefore changes nothing. Rejected: a separate include file; OpenSpec has no
include mechanism.

### 3. Verification of the merge

After editing, setup runs `openspec list --json` and reads its error output:
OpenSpec warns about `rules` or `operations` it cannot use ("must be an array of
strings, ignoring ..."). Setup also counts the `[warrant] ` entries in the
configuration against `rules.yaml`. Any warning or a different count is
reported as a failed setup. Rejected: `openspec instructions`, which needs an
existing change, so setup would have to create one in the project.

### 4. Minimum OpenSpec version 1.16

`operations` guidance exists from 1.16; rules alone would work on older
versions but without apply routing. Setup refuses older versions and accepts
newer ones.

### 5. Glossary as a rule, decisions in design.md

The glossary rule joins the proposal and specs rules. Decisions live in the
change's `design.md` (Decisions), as OpenSpec intends; nothing writes decision
records. The contract keeps its Decision records subsection for compatibility;
whether to drop it is left for a later change.

### 6. Evals

- Setup scenarios check the merged configuration instead of schema files; the
  `existing-contract` fixture gains project rules that must survive, and a new
  `setup-upgrade` fixture holds outdated `[warrant] ` entries that must be
  replaced.
- The `warrant-project` fixture (propose scenario) carries the shipped rules in
  its configuration; a dogfood test keeps them equal to `rules.yaml`.
- The minimal-change checker fails on any untracked file the task did not ask for.

## Risks / Trade-offs

- [An agent reformats the whole YAML file while merging] → The setup checker
  compares every non-warrant line before and after; the skill says to edit
  only the listed lists.
- [Rules are advisory, the schema's templates were not] → The propose scenario
  keeps checking Assumptions and EARS in real output on three agents.

## Migration Plan

A project on the `warrant` schema runs the new `warrant-setup`: it sets nothing
on `schema`, so the project sets `schema: spec-driven` itself and may delete
`openspec/schemas/warrant/`. Changes created with the old schema keep it in
their `.openspec.yaml`; they finish on it while the directory exists.
