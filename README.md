# openspec-warrant

An agent-neutral extension of [OpenSpec](https://github.com/Fission-AI/OpenSpec)
1.16 and later. Every requirement is unambiguous, every changed line is warranted by a
requirement, and every completion claim is warranted by verification evidence.

It ships:

- artifact rules for OpenSpec's `spec-driven` schema: EARS requirements with
  one outcome each, an Assumptions section in every proposal, a design that
  records which simpler option failed, review and verification groups at the
  end of every task list, and use of the project glossary; plus apply guidance
  that routes implementation to the warrant skills;
- `warrant-setup`: merges the rules into `openspec/config.yaml`, drafts an
  empty OpenSpec `context` from the project's documents and creates the
  project contract;
- `warrant-minimal-change`: the smallest complete change, `shortcut:` markers
  and a shortcut ledger;
- `warrant-tdd`: test first, one requirement scenario at a time - each new
  test seen failing before any code, tests named after their scenarios; task
  selection stays with the OpenSpec apply workflow;
- `warrant-verify`: no completion claim without running the project's
  verification commands and reading their output;
- `warrant-review`: reviews a change's artifacts before any code (ending with
  `Artifact review: PASS` or `REVISE`), and reviews a diff along three separate axes - Spec
  (`openspec-verify-change` plus lines no requirement asks for), Standards (the
  project's declared standards and bugs or security problems in connected
  code) and Evidence (the contract's verification) - and addresses review
  comments by checking each one before acting on it.

Community extension; not affiliated with Fission-AI or the OpenSpec project.

## Install

Requirements: OpenSpec CLI 1.16 or later and an OpenSpec root (`openspec init`).

```sh
npx skills add imtpot/openspec-warrant
```

Then ask your agent to run the `warrant-setup` skill. It adds warrant's rules,
each marked `[warrant] `, to the `rules` and `operations` lists in
`openspec/config.yaml` without touching your own entries or the `schema` field,
proposes a `context` when yours is empty (only constraints an agent cannot
infer from the code, written after you confirm them), proposes a contract for
`AGENTS.md` and prints the command that installs the OpenSpec workflow skills
for your OpenSpec version, for example:

```sh
npx skills add https://github.com/Fission-AI/OpenSpec/tree/v1.16.0/skills
```

Run `warrant-setup` again after updating the kit: it replaces only the
`[warrant] ` entries.

### Migrating from the warrant schema (0.5 and earlier)

Set `schema: spec-driven` in `openspec/config.yaml`, run `warrant-setup`, and
delete `openspec/schemas/warrant/` once no active change uses it (a change
records its schema in its `.openspec.yaml`). `warrant-design` is gone; use
`openspec-explore`.

## Project contract

The skills read project facts only from this section of the root `AGENTS.md`.
Keep the subsections in this order.

```markdown
## Warrant contract

### Verification

- tests: `make test`
- lint: `make lint`

### Destructive actions

- `make deploy`

### Glossary

docs/glossary.md

### Standards

- `CONTRIBUTING.md`
```

- **Verification**: `- <name>: \`<exact command>\``, one per line.
- **Destructive actions**: commands or prefixes an agent runs only with approval.
- **Glossary**: a relative path or `none`.
- **Standards** (optional, last): files with coding standards that
  `warrant-review` checks, as backticked paths, or `none`. A missing
  subsection means `none`.

## Supported agents

Results of the eval scenarios (23 per agent) for openspec-warrant 0.8, run on
2026-11-04 with each agent in a restricted permission mode.

| Agent | Pass | Not pass | Notes |
|---|---|---|---|
| Claude Code 2.1 | 23 | 0 | |
| Codex 0.166 | 23 | 0 | runs commands in a non-login shell (`-c allow_login_shell=false`) so a fixture's fake CLI stays on `PATH` |

Both agents discover the skills in `.agents/skills/` and read the contract from
`AGENTS.md` (`discovery` scenario). The skills name no agent, so other agents
can load them, but only Claude Code and Codex are evaluated.

Global agent configuration (user-level skills and plugins) also loads during
evals and can change the results; run evals with it disabled.

## Evals

Behavioral evals run the skills headless against each agent in a temporary
copy of a fixture project. Agents run in restricted modes, never with a
permission-bypass flag. Evals need authenticated agent CLIs and use model
quota, so they run manually, not in CI.

```sh
uv run pytest                                          # checker tests, no agent needed
uv run python -m warrant_evals --agent claude          # every scenario on one agent
uv run python -m warrant_evals --scenario verify --keep  # one scenario, keep its workspace
```

The report is written to `evals/out/report.md`.

Evals see an agent's final report, not the commands it ran. TDD scenarios
therefore check the report (a failing result before a passing one, the
narrowed and full test commands) together with the tests and code in the
workspace; they cannot prove that each run happened.

## Benchmark

The benchmark runs the same tasks in three arms on each agent: `bare` (no
skills), `openspec` (OpenSpec skills) and `warrant` (OpenSpec skills plus
warrant's skills, rules and contract). In `bare` and `openspec`, `AGENTS.md`
names the verification commands as plain text. Claude runs with
`--setting-sources project,local`, so user plugins stay out of every arm.

- `implement-split`: implement a ready OpenSpec change. Scores: hidden
  acceptance tests passed (of 8), the share of 7 faulty implementations that
  the agent's own tests reject, and non-test lines added.
- `review-branch`: review a branch with 6 planted problems. Score: the share
  of problems the report names.
- Every run records the tokens the agent reports. Compare tokens between arms
  of one agent, not between agents.

```sh
uv run python -m warrant_evals.benchmark --agent claude --runs 3
```

The table is written to `evals/out/benchmark/benchmark.md`; `(k)` after a mean
is the number of runs that measured it.

## Inspired by

The skills are written from scratch. Their ideas come from:

- [EARS](https://alistairmavin.com/ears/) - Easy Approach to Requirements Syntax
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) - the
  smallest complete change and `shortcut:` markers
- [obra/superpowers](https://github.com/obra/superpowers) - verification before completion
- [mattpocock/skills](https://github.com/mattpocock/skills) - small, composable skills

## License

MIT
