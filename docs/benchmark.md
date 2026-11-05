# Evals and benchmark

warrant's claims are checked twice: evals show that agents follow each skill,
and the benchmark shows whether following them helps.

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

The report is written to `evals/out/report.md`. Its Loaded column lists the
skills each run loaded and the sub-agents it started: Claude Code runs with
`--output-format stream-json --verbose`, so its tool calls are visible, and a
Codex run counts a skill as loaded when it reads its `SKILL.md`. A scenario's
`loaded` list names skills the agent must load by itself because the prompt
names none; a run that does not load them fails.

Evals see an agent's final report, not the commands it ran. TDD scenarios
therefore check the report (a failing result before a passing one, the
narrowed and full test commands) together with the tests and code in the
workspace; they cannot prove that each run happened.

Global agent configuration (user-level skills and plugins) also loads during
evals and can change the results; run evals with it disabled.

## Benchmark

The benchmark runs the same tasks in three arms on each agent: `bare` (no
skills), `openspec` (OpenSpec skills) and `warrant` (OpenSpec skills plus
warrant's skills, rules and contract). In `bare` and `openspec`, `AGENTS.md`
names the verification commands as plain text. Claude runs with
`--setting-sources project,local`, so user plugins stay out of every arm.

- `implement-proration`: implement a ready OpenSpec change in an existing
  billing module. Scores: hidden acceptance tests passed (of 11), the share of
  8 faulty implementations that the agent's own tests reject (3 of them break
  a requirement that no example scenario shows), and non-test lines added.
- `plan-implement-allocation`: plan a short request as an OpenSpec change,
  then, in the same session, implement it (two prompts, because OpenSpec's
  propose workflow stops after planning). The request leaves three things open:
  percentages that do not add up to 100, where leftover cents go, and an empty
  list or a zero percentage. Scores: the share of these the agent marks as
  assumed or open (in a proposal's Assumptions, or in a sentence that says
  assume, question, confirm, unclear or ambiguous), hidden
  acceptance tests on the unambiguous behavior (of 6), and the share of 6
  faulty implementations its tests reject. A fault counts as caught when a
  test that passes on the reference implementation fails on it, so tests that
  settle an open point differently are ignored.
- `review-export`: review a branch with 6 planted problems that need the
  spec, the standards or code outside the diff. Score: the share of problems
  the report names.
- `review-refund`: review a branch whose 6 planted problems show only against
  the spec, the standards or a caller outside the diff, while the branch's
  tests pass. On Opus, Sonnet and Haiku every arm named nearly all of them, so
  the review tasks check that a review misses nothing rather than separate
  the arms; that needs a diff of realistic size.
- Every run records the tokens the agent reports. Compare tokens between arms
  of one agent, not between agents.
- Claude runs with `--output-format stream-json`. The score reads every message
  of a run, not only the last: a headless Claude session can end with a short
  note after background sub-agents finish.

```sh
uv run python -m warrant_evals.benchmark --agent claude --runs 3
uv run python -m warrant_evals.benchmark --agent claude --model claude=sonnet --arm warrant
```

`--model <agent>=<model>` runs that agent with another model; its rows read
`<agent>:<model>`. `--arm` and `--task` limit the run.

The table is written to `evals/out/benchmark/benchmark.md`; `(k)` after a mean
is the number of runs that measured it. `runs.md` lists, per run, the faults
the agent's tests let through or the problems its review missed; with `--keep`
it also names each run's kept workspace.

Results on Claude Code, three runs per cell, 2026-11-04. Faults are the share
of faulty implementations the agent's own tests reject.

`plan-implement-allocation` (plan, then implement in the same session). This
table was measured when decided and chose also counted as markers, so its
open-point shares may be too high until a re-run:

| Model | Arm | Open points marked | Acceptance | Faults | Lines added | Cost per run |
|---|---|---|---|---|---|---|
| Opus 5.5 | `bare` | 0.00 | 6 of 6 | 1.00 | 37 | $1.13 |
| | `openspec` | 0.22 | 6 of 6 | 1.00 | 40 | $1.39 |
| | `warrant` | 1.00 | 6 of 6 | 1.00 | 19 | $2.30 |
| Sonnet 5.5 | `bare` | 0.22 | 6 of 6 | 0.83 | 31 | $0.36 |
| | `openspec` | 0.67 | 6 of 6 | 1.00 | 29 | $0.57 |
| | `warrant` | 1.00 | 6 of 6 | 1.00 | 20 | $0.75 |
| Haiku 5.5 | `bare` | 0.00 | 6 of 6 | 1.00 | 31 | $0.03 |
| | `openspec` | 0.11 | 6 of 6 | 1.00 | 34 | $0.04 |
| | `warrant` | 1.00 | 6 of 6 | 1.00 | 18 | $0.19 |

`implement-proration` (implement a ready change):

| Model | `bare` | `openspec` | `warrant` |
|---|---|---|---|
| Opus 5.5 | 0.75 | 0.92 | 0.96 |
| Sonnet 5.5 | 0.75 | 0.79 | 0.83 |
| Haiku 5.5 | 0.79 | 0.67 | 0.75 |

Every arm writes correct code. warrant's clear gain is in planning: on every
model, every warrant run named all three points the request left open, while
plain OpenSpec named 11 to 67% and no kit almost none (by the old marker list;
see the note above the table). warrant also adds about
half as many lines. Its tests catch faults about as well as plain OpenSpec's,
after `warrant-tdd` started testing the boundaries a requirement states but no
scenario shows (before: 0.67 on Opus). warrant costs 1.3 to 1.7 times plain
OpenSpec on Opus and Sonnet. On `review-export`, every arm named all 6 planted
problems in a single Opus run, so that task does not separate the arms yet.

## Spending less

warrant's apply guidance implements each task group in a fresh sub-agent and,
where the agent can choose its model, gives a group whose requirements and
design leave nothing open to a smaller, faster model. On Opus, with
`plan-implement-allocation`, the agent chose Sonnet for its sub-agents in
every run: same scores, fewer lines added (15 against 19) and about 10% lower
cost ($2.08 against $2.30 per run). Most of the remaining cost is the
orchestrating agent, which carries the planning conversation.

The larger saving is yours to make: plan with a strong model, then start a new
session on a cheaper model for apply. With warrant, Haiku matched Opus on that
task (every open point marked by the old marker list, 6 of 6 acceptance, every fault caught) at $0.19
against $2.30 per run; on `implement-proration` its tests caught fewer faults
(0.75 against 0.96).

Codex can set a sub-agent's model, but this was not measured: the benchmark
ran Claude Code only, and a reported Codex regression makes sub-agents inherit
the parent's model.
