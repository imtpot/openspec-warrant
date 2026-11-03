# Design

## Context

See proposal.md - Why. Requirements are in `specs/`.

Facts that shape the approach (checked on OpenSpec 1.16.0 and skills 1.7.4):

- `openspec schema fork spec-driven <name>` copies the built-in schema
  (`schema.yaml` plus `templates/`) into `openspec/schemas/<name>/`. A fork is a
  snapshot: `openspec update` never touches `openspec/schemas/`.
- Schema resolution order is project, user, package; `openspec schema which`
  reports the source.
- `skills add <path>` installs from a local directory (`sourceType: local`);
  `skills add <owner>/<repo>` discovers `skills/<name>/SKILL.md`.
- `skills` installs project skills into `.agents/skills/<name>/` and global
  skills into `~/.agents/skills/<name>/`, and links them for Claude Code.
- Headless entry points: `claude -p`, `codex exec`, `copilot -p` (with
  `-s` and `--allow-all-tools`), `agy -p` (with `--output-format` and
  `--dangerously-skip-permissions`). Flags are taken from each CLI's `--help`.

## Goals / Non-Goals

**Goals:**
- Every behavior lives in exactly one place: schema instructions for artifact
  content, skills for working practice, the contract for project facts.
- Skills are plain Markdown that any of the four agents can follow without
  agent-specific tools.

**Non-Goals:**
- No runtime code shipped to target projects; the only code is the eval harness.
- No automation of `skills add` for OpenSpec skills; setup prints the command.

## Decisions

### 1. Build the schema with `openspec schema fork`

Run `openspec schema fork spec-driven warrant` in this repository, then edit
the forked `schema.yaml` instructions and the four templates. The result is
committed under `skills/warrant-setup/schema/warrant/`.

Option ladder: an existing OpenSpec feature (fork) meets the need; writing the
schema from scratch would duplicate the upstream artifact graph and drift from
it. Rejected: `rules` in `openspec/config.yaml` only, because rules cannot
change templates and every target project would have to copy them.

### 2. Ship the schema inside the setup skill

The `skills` CLI copies a whole skill directory, so files placed next to
`warrant-setup/SKILL.md` reach the target project with the skill. The setup
instructions look for them in this order: `.agents/skills/warrant-setup/schema/`
(project install), then `~/.agents/skills/warrant-setup/schema/` (global
install), and stop with an error if neither exists. Both paths are fixed by the
`skills` CLI, not by the agent, so the lookup works for all four agents
(resolves proposal assumption 2).

Rejected: download the schema from GitHub at a release tag. It needs network
access, a second version pin and a tool such as `curl` on every machine.
Rejected: a separate `warrant-schema` skill holding only files. It is not a
skill an agent should ever trigger.

### 3. Contract as Markdown headings in `AGENTS.md`

Agents read `AGENTS.md` without being told; a fixed `## Warrant contract`
section with four `###` subsections and backticked commands is readable by
agents and parseable by the eval checker with a few lines of Python. Confirmed
by the requester.

Rejected: a YAML block inside `AGENTS.md`. It adds a format inside a format and
gives agents no advantage.

### 4. Three skills with narrow triggers

- `warrant-setup`: triggered only by an explicit request to set up warrant.
- `warrant-minimal-change`: triggered when writing or changing code; the debt
  ledger is a mode of this skill, not a fourth skill, because it reads the same
  `shortcut:` convention.
- `warrant-verify`: triggered before any completion claim.

Each `SKILL.md` stays under 150 lines. Descriptions name concrete triggers so
they do not compete with OpenSpec workflow skills.

### 5. Debt ledger via `git grep`

`git grep -nE '(#|//|--|;|/\*) ?shortcut:'` covers tracked files only and needs
no new tool. A comment prefix is required so prose that mentions the convention
is not listed.

### 6. Eval harness in Python with `uv`

Confirmed by the requester. Layout:

- `evals/fixtures/<name>/`: small git repositories with an OpenSpec root and a
  warrant contract.
- `evals/scenarios/<name>.toml`: fixture, prompt, checker name.
- `evals/warrant_evals/`: runner (`subprocess` with a 900 s timeout), agent
  command table, checkers, Markdown report writer.
- `evals/tests/`: checker unit tests with recorded artifacts; no agent needed.

The runner copies the fixture into a temporary directory, runs `git init`,
`openspec` and `skills add <repo path> -a claude-code codex -y`, then the
agent. Agents run in restricted modes, never with a flag that bypasses all
permissions: file edits are accepted, and shell access is limited to an
allowlist of the commands the skills and fixtures use (`openspec`, `uv run`,
`make`, `diff`, `cp`, `mkdir`, read-only `git`):

- Claude Code: `-p --permission-mode acceptEdits --allowedTools <list>`
- Codex: `exec -s workspace-write` (sandbox: writes only inside the workspace)
- Copilot CLI: `-p <prompt> -s --allow-tool write <shell list> --deny-tool 'shell(git push)'`
- agy: `-p --mode accept-edits --sandbox`

A command outside the allowlist is denied or waits for approval; a run that
waits ends at the timeout and is reported as such. Standard library only (`tomllib`, `subprocess`, `tempfile`, `re`);
`pytest` is the one dev dependency.

Rejected: an existing eval framework (for example `claude plugin eval`). It is
tied to one agent.

### 7. Checker rules, not model grading

Checkers are deterministic: EARS keyword at the start of the requirement text,
count of `SHALL`, `WHERE` followed by a state word list, presence of an
Assumptions heading, failing-test fixture versus the word set of a success
claim, and new `def`/`function` names versus fixture helpers. Rejected: a model
grading the artifacts, because results would vary between runs and cost more.

### 8. Repository layout and own contract

```
skills/warrant-setup/SKILL.md
skills/warrant-setup/schema/warrant/{schema.yaml,templates/*.md}
skills/warrant-minimal-change/SKILL.md
skills/warrant-verify/SKILL.md
evals/...
AGENTS.md            # contains this repo's own warrant contract
README.md, LICENSE (MIT), pyproject.toml
```

This repository keeps using `spec-driven` until the warrant schema exists, then
switches to `warrant` by running its own setup.

## Risks / Trade-offs

- [The fork drifts from upstream `spec-driven`] → Support only OpenSpec 1.16;
  setup refuses other versions; a new OpenSpec release means a new fork and a
  new warrant release.
- [Copilot CLI or agy do not discover `.agents/skills/` or `AGENTS.md`] → The
  discovery smoke scenario fails for that agent; the README states the agent as
  unsupported until fixed. No agent-specific workaround is added in this change.
- [Heuristic checkers give false results] → Each checker has unit tests with
  passing and failing recorded artifacts; the report quotes the matched text.
- [Eval runs are slow and cost model usage] → Agent filter and one scenario per
  run; evals are not part of `uv run pytest`.
- [Bypass flags would let an agent run any command] → Rejected: no run uses a
  bypass flag; restricted modes and a shell allowlist are used instead.
- [A restricted agent stalls on a command outside the allowlist] → The run ends
  at the timeout; the transcript shows the denied command, and the allowlist is
  extended only when a scenario needs it.
- [agy's sandbox has no command allowlist] → agy relies on `--sandbox` terminal
  restrictions; its results are read with that difference in mind.

## Migration Plan

New repository; nothing to migrate. Rollback is deleting the release tag.
Target projects adopt warrant in their own changes after v1 is published.
