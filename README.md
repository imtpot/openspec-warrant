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
  verification commands and reading their output.

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
Keep the four subsections in this order.

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
```

- **Verification**: `- <name>: \`<exact command>\``, one per line.
- **Destructive actions**: commands or prefixes an agent runs only with approval.
- **Glossary**, **Decision records**: a relative path or `none`.

## Supported agents

| Agent | Skill and contract discovery |
|---|---|
| Claude Code | not run |
| Codex | not run |
| GitHub Copilot CLI | not run |
| Antigravity CLI (agy) | not run |

The column shows the result of the `discovery` eval scenario.

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
