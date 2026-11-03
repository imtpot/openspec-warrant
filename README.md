# openspec-warrant

An agent-neutral extension of [OpenSpec](https://github.com/Fission-AI/OpenSpec)
1.16. Every requirement is unambiguous, every changed line is warranted by a
requirement, and every completion claim is warranted by verification evidence.

It ships:

- the `warrant` OpenSpec schema: EARS requirements with one outcome each, an
  Assumptions section in every proposal, a design that records which simpler
  option failed, and review and verification groups at the end of every task list;
- `warrant-setup`: installs the schema and creates the project contract;
- `warrant-minimal-change`: the smallest complete change, `shortcut:` markers
  and a shortcut ledger;
- `warrant-verify`: no completion claim without running the project's
  verification commands and reading their output;
- `warrant-review`: reviews a diff along three separate axes - Spec (the
  OpenSpec change), Standards (the project's declared standards) and Evidence
  (the contract's verification) - and addresses review comments by checking
  each one before acting on it.

Community extension; not affiliated with Fission-AI or the OpenSpec project.

## Install

Requirements: OpenSpec CLI 1.16 and an OpenSpec root (`openspec init`).

```sh
npx skills add imtpot/openspec-warrant
```

Then ask your agent to run the `warrant-setup` skill. It installs the schema
into `openspec/schemas/warrant/`, sets `schema: warrant` in
`openspec/config.yaml`, proposes a contract for `AGENTS.md` and prints the
command that installs the OpenSpec workflow skills for 1.16:

```sh
npx skills add https://github.com/Fission-AI/OpenSpec/tree/v1.16.0/skills
```

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

### Decision records

none

### Standards

- `CONTRIBUTING.md`
```

- **Verification**: `- <name>: \`<exact command>\``, one per line.
- **Destructive actions**: commands or prefixes an agent runs only with approval.
- **Glossary**, **Decision records**: a relative path or `none`.
- **Standards** (optional, last): files with coding standards that
  `warrant-review` checks, as backticked paths, or `none`. A missing
  subsection means `none`.

## Supported agents

Results of the eval scenarios (11 per agent) for openspec-warrant 0.1, run on
2026-11-04 with each agent in a restricted permission mode.

| Agent | Pass | Not pass | Notes |
|---|---|---|---|
| Claude Code 2.1 | 11 | 0 | `verify-no-contract` passed after the `warrant-verify` description began to cover any test run; it failed once before that change |
| Codex 0.166 | 10 | 1 not run | `setup-wrong-version` is not applicable: Codex runs commands in a login shell that resets `PATH`, so the fixture's fake CLI is hidden |
| GitHub Copilot CLI 1.0 | 10 | 1 fail | `verify-no-contract`: Copilot does not load `warrant-verify` when the project has no contract, and reports the work as complete without verification |
| Antigravity CLI (agy) 1.4 | 6 | 5 not run | Headless agy denies commands that its permission rules do not match and does not name the command; see [#548](https://github.com/google-antigravity/antigravity-cli/issues/548) and [#565](https://github.com/google-antigravity/antigravity-cli/issues/565). Every scenario that agy completed passed |

All four agents discover the skills in `.agents/skills/` and read the contract
from `AGENTS.md` (`discovery` scenario).

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

## Inspired by

The skills are written from scratch. Their ideas come from:

- [EARS](https://alistairmavin.com/ears/) - Easy Approach to Requirements Syntax
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) - the
  smallest complete change and `shortcut:` markers
- [obra/superpowers](https://github.com/obra/superpowers) - verification before completion
- [mattpocock/skills](https://github.com/mattpocock/skills) - small, composable skills

## License

MIT
