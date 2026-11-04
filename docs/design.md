# openspec-warrant design

## Problem

Coding agents working on real projects fail in four recurring ways:

1. They write requirements that read two ways, and build what they guessed.
2. They grow a change past what was asked: options, wrappers and abstractions
   nobody needs.
3. They report work as done, fixed or passing without running anything.
4. They decide open questions themselves and present the result as settled.

OpenSpec gives the work a shape (proposal → specs → design → tasks → apply →
verify → archive), but its default schema and skills do not prevent these
failures. Skill sets that address them (obra/superpowers, mattpocock/skills,
DietrichGebert/ponytail) each assume their own layout, tools and agent, overlap
with each other and with OpenSpec, and cannot be edited without losing updates.

## Goal

One agent-neutral extension of OpenSpec that removes the four failures in any
project, installed with the `skills` CLI, with no project, language or agent
assumptions in the skills themselves.

The name: every requirement is unambiguous, every changed line is **warranted**
by a requirement, and every completion claim is **warranted** by evidence.

## Non-goals

- Replacing or wrapping OpenSpec's own workflow skills.
- Owning the process: warrant adds rules to OpenSpec's steps, it does not add
  steps of its own.
- Supporting agents that cannot be evaluated headless.

## Principles

These are the rules every part of warrant follows. The `warrant-kit` spec makes
them checkable.

1. **Extend OpenSpec, do not duplicate it.** Where an OpenSpec skill already
   covers a step, warrant adds rules to that step through artifact `rules`
   and `operations.apply.guidance` in the project configuration, not through a parallel skill.
   A warrant skill exists only for work no OpenSpec skill does.
2. **Route through OpenSpec's own mechanisms.** `rules` carry the artifact
   rules; `warrant-setup` writes apply guidance that points to the warrant
   skills; nothing relies on agent-specific hooks or commands.
3. **Project facts come only from the contract.** Commands, destructive
   actions, glossary, decision records and standards are declared once in the
   `## Warrant contract` section of `AGENTS.md`.
4. **One rule, one place.** A rule lives in `rules.yaml` or in one skill, and
   other parts refer to it by name.
5. **Spend the reader's tokens carefully.** Short skills, short replies a busy
   person understands in one read, a closing line with what was skipped, not
   checked or risky, and skill descriptions that say only when to use the skill.
   (Ponytail: "Lower cost and latency are a side effect.")
6. **Agent-neutral.** No skill names an agent, an agent's tools or sub-agents.
7. **Evidence over claims, also for warrant itself.** Every skill has behavioral
   eval scenarios that pass on Claude Code, Codex and GitHub Copilot CLI.
   Checkers test behavior, not wording, and the harness stays small.

## Architecture

```
target project
├── AGENTS.md                ## Warrant contract  ← project facts (principle 3)
├── openspec/config.yaml     schema: spec-driven; [warrant] rules (EARS, assumptions,
│                            option ladder, review and verification tasks, glossary)
│                            and apply guidance → warrant skills
└── .agents/skills/          openspec-* (dependency) + warrant-* (this kit)
```

| Part | Owns | Does not own |
|---|---|---|
| warrant rules (`rules.yaml`) | what artifacts must contain: EARS requirements, assumptions, the option ladder, review and verification tasks, glossary terms; apply guidance | how code is written or checked |
| `warrant-setup` | merging the rules into the project configuration and creating the contract | anything at change time |
| `warrant-minimal-change` | how much code a change may add; `shortcut:` markers | choosing tasks |
| `warrant-tdd` | how one requirement is implemented test first | choosing or checking off tasks |
| `warrant-verify` | running the contract's commands before any completion claim | deciding what to verify beyond the contract |
| `warrant-review` | Standards (declared standards, protected code, correctness and security of connected code), Evidence, and receiving review comments | spec conformance |

## Map against OpenSpec skills

| OpenSpec skill | What it does | What warrant adds, and where |
|---|---|---|
| `openspec-explore` | interview before a change: one question at a time, a recommendation, facts looked up, decisions kept in the conversation | nothing separate; glossary use is an artifact rule for proposal and specs |
| `openspec-propose`, `-new-change`, `-continue-change`, `-ff-change` | write the artifacts | the `[warrant] ` artifact rules |
| `openspec-apply-change` | pick tasks, implement, check off | apply guidance routing to `warrant-tdd`, `warrant-minimal-change`, `warrant-verify` |
| `openspec-verify-change` | completeness, correctness (requirements and scenario coverage), coherence against artifacts; runs nothing | `warrant-verify` runs the commands; `warrant-review` covers standards and code outside the spec |
| `openspec-archive-change`, `-sync-specs`, `-update-change` | finish and sync | nothing |

OpenSpec's own spec guidance (`docs/writing-specs.md`) already asks for one
`SHALL` per requirement, observable outcomes and failure cases, so warrant's
rules add only EARS patterns, WHERE versus WHILE, IF/THEN for real failures,
traceability and the glossary.

## Related work

[anvil](https://github.com/jikkujoyce/openspec-schemas/tree/main/schemas/anvil)
is a community OpenSpec schema with the closest goals: an adversarial review of
the artifacts before any code, a test plan that maps every scenario to a named
test, red-green-refactor tasks and a `verify` artifact with a `DECISION:` line
that CI can parse. It forks the workflow into seven artifacts and relies on
sub-agents or a second model for the review. warrant stays on `spec-driven`,
adds no artifacts and names no agent, and adds what anvil lacks: EARS,
assumptions, minimal change, the project contract and evals on three agents.

Ideas from anvil worth taking, without an agent-specific mechanism: a review of
the artifacts before implementation, verification results in a line CI can
parse, and a bound on review rounds.

## Current state and drift

Built: the artifact rules, the contract, `warrant-setup`, `warrant-minimal-change`,
`warrant-tdd`, `warrant-verify` and `warrant-review`, with eval scenarios on
three agents. The schema fork and `warrant-design` were removed because they
duplicated OpenSpec (principle 1).

Remaining drift:

- `warrant-review`'s Spec axis duplicates `openspec-verify-change` (principle 1),
  and it misses correctness and security in connected code (Ponytail review).
- No brevity rule or closing "skipped / not checked / risk" line (principle 5).
- The contract's Decision records subsection is no longer read by any skill
  (principle 4).

## Success criteria

- A project goes from `openspec init` to warrant in one `npx skills add` and
  one `warrant-setup` run.
- Every principle above that can be checked mechanically has a test in
  `uv run pytest`.
- Every skill's scenarios pass on Claude Code, Codex and Copilot CLI, with each
  remaining failure explained in the README.

## Order of work

1. Done: `warrant-kit` spec with tests; rules instead of the schema fork, with
   apply guidance; `warrant-design` removed.
2. Narrow `warrant-review` to what `openspec-verify-change` does not do.
3. Economy: brevity and the closing line; decide on the Decision records subsection.
4. From anvil: an artifact review before implementation and verification
   results CI can parse.
5. Next skills only where no OpenSpec skill covers the work (`warrant-diagnose`).

## Sources

Ideas come from, and are written anew rather than copied:

- [OpenSpec](https://github.com/Fission-AI/OpenSpec): workflow, schemas,
  project configuration.
- [obra/superpowers](https://github.com/obra/superpowers): evidence before
  claims, test first, receiving review, "description = when to use".
- [mattpocock/skills](https://github.com/mattpocock/skills): small composable
  skills, two-axis review, glossary, decision records used sparingly.
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail): the
  option ladder, `shortcut:` markers, short replies and fewer tokens.
- [EARS](https://alistairmavin.com/ears/): requirement syntax.
- [anvil](https://github.com/jikkujoyce/openspec-schemas/tree/main/schemas/anvil):
  see Related work.
