# openspec-warrant

OpenSpec rules and skills that make coding agents surface open questions, test boundaries and prove their claims.

openspec-warrant extends [OpenSpec](https://github.com/Fission-AI/OpenSpec)
1.16 and later for any coding agent. In a benchmark on Claude Code, every
warrant run listed all the points a request left open, where plain OpenSpec
listed 11 to 67% and an agent without a kit almost none, with code half the
size and tests that catch as many faults. Every requirement is unambiguous,
every changed line is warranted by a requirement, and every completion claim
is warranted by verification evidence.

Community extension; not affiliated with Fission-AI or the OpenSpec project.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Project contract](#project-contract)
- [Supported agents](#supported-agents)
- [Results](#results)
- [Contributing](#contributing)
- [Thanks](#thanks)
- [License](#license)

## Background

Agents decide what a request leaves open without saying so, test the examples
they were shown rather than the rules, and report success they never checked.
OpenSpec gives a change a proposal, specs, a design and tasks; warrant adds
rules to those artifacts and skills for the code that follows:

| Step | OpenSpec | warrant adds |
|---|---|---|
| Propose | proposal, specs, design, tasks | EARS requirements, an Assumptions section with owners, "Why code is needed", "Out of scope", the simplest option that works, Review and Verification task groups |
| Before code | | `warrant-review` reviews the artifacts in a sub-agent and ends with `Artifact review: PASS` or `REVISE` |
| Apply | implements tasks | each task group in a fresh sub-agent with `warrant-tdd` (requirement scenarios and the boundaries they state, then a mutation check) and `warrant-minimal-change` (the smallest complete change) |
| Done | | `warrant-verify`: the project's verification commands, run and read, before any claim |
| Review | `openspec-verify-change` | `warrant-review` on a diff: Spec, Standards and Evidence axes in separate sub-agents |

warrant adds rules to OpenSpec's `spec-driven` schema instead of forking it,
so OpenSpec updates reach you unchanged. The principles behind it are in
[docs/design.md](docs/design.md).

## Install

```sh
npm install -g @fission-ai/openspec@latest   # or: brew install openspec
openspec config set profile custom
openspec config set workflows '["propose","explore","apply","update","sync","archive","verify"]'
openspec init --tools agents --profile custom   # in a project with openspec/: openspec update
npx skills add imtpot/openspec-warrant
```

The two `config set` commands add the `verify` workflow, which the Spec axis
of `warrant-review` uses, to OpenSpec's default ones. They replace your global
workflow list for every project: if you already chose workflows, add `verify`
with `openspec config profile` instead.

`openspec init --tools agents` writes the OpenSpec workflow skills to
`.agents/skills/`, where any agent can load them. Then ask your agent to run
the `warrant-setup` skill. With your confirmation where it proposes something,
it:

1. links the OpenSpec skills into each agent skills directory the project
   already has, such as `.claude/skills/`;
2. adds warrant's rules, each marked `[warrant] `, to `openspec/config.yaml`
   and keeps your own entries;
3. proposes an OpenSpec `context` when yours is empty and a contract for
   `AGENTS.md`.

If the OpenSpec CLI or the OpenSpec root is missing, `warrant-setup` stops and
names the command. Run it again after updating the kit: it replaces only the
`[warrant] ` entries.

### Dependencies

- Node.js 22.12 or later for the OpenSpec CLI and `npx skills`.

## Usage

Work with OpenSpec as usual; warrant's rules and apply guidance come with it.
Ask in plain words, for example:

```text
Plan the weekly digest email as an OpenSpec change.
Implement the change add-weekly-digest.
Review this branch before merge.
Address the review comments in review.md.
Show me the shortcut ledger.
```

Plan in one request and implement in the next: OpenSpec's propose workflow
stops after planning. To spend less, plan with a strong model and run apply in
a new session on a cheaper one; with warrant, Claude Haiku matched Claude Opus
on the benchmark's plan-and-implement task at a twelfth of the cost.

## Project contract

The skills read project facts only from this section of the root `AGENTS.md`.
`warrant-setup` proposes it from your build files; keep the subsections in
this order.

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

- **Verification**: one `- <name>: \`<exact command>\`` per line.
- **Destructive actions**: commands or prefixes an agent runs only with your
  approval. Empty when there are none.
- **Glossary**: a relative path or `none`.
- **Standards** (optional): files with coding rules that `warrant-review`
  checks, or `none`.

## Supported agents

| Agent | Eval scenarios passed |
|---|---|
| Claude Code 2.1 | 24 of 24 |
| Codex 0.166 | 24 of 24 |

The skills name no agent, so other agents can load them from `.agents/skills/`;
only Claude Code and Codex are evaluated. How the evals run:
[docs/benchmark.md](docs/benchmark.md#evals).

## Results

Claude Code, three runs per cell, plan a request and then implement it:

| Model | Arm | Open points listed | Faults caught | Lines added | Cost per run |
|---|---|---|---|---|---|
| Opus 5.5 | plain OpenSpec | 22% | 100% | 40 | $1.39 |
| | warrant | 100% | 100% | 19 | $2.30 |
| Sonnet 5.5 | plain OpenSpec | 67% | 100% | 29 | $0.57 |
| | warrant | 100% | 100% | 20 | $0.75 |
| Haiku 5.5 | plain OpenSpec | 11% | 100% | 34 | $0.04 |
| | warrant | 100% | 100% | 18 | $0.19 |

Every arm passed all hidden acceptance tests. Method, all arms and the other
tasks: [docs/benchmark.md](docs/benchmark.md).

## Contributing

Questions and bug reports go to
[GitHub issues](https://github.com/imtpot/openspec-warrant/issues); pull
requests are welcome. Every change goes through OpenSpec in `openspec/`, and
[AGENTS.md](AGENTS.md) lists the development setup and the verification
commands:

```sh
uv run pytest
openspec validate --all --strict
```

A change to a skill's wording is a change to its behavior: run the eval
scenarios of every skill it touches, as described in
[docs/benchmark.md](docs/benchmark.md#evals).

## Thanks

The skills are written from scratch. Their ideas come from:

- [EARS](https://alistairmavin.com/ears/), the Easy Approach to Requirements Syntax
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail): the
  smallest complete change, `shortcut:` markers and benchmarking against a
  baseline
- [obra/superpowers](https://github.com/obra/superpowers): verification before
  completion and the mutation check
- [mattpocock/skills](https://github.com/mattpocock/skills): small, composable
  skills and independent expected values in tests

## License

[MIT](LICENSE) © imtpot
