---
name: warrant-design
description: Settle open design decisions with the user before an OpenSpec change is proposed - one question at a time with a recommended answer, recording agreed terms in the glossary and agreed decisions in the decision records. Use when the user wants to design, plan, discuss or think through a feature before proposing it.
license: MIT
---

# Design interview

Settle the decisions a request leaves open before anyone writes a proposal. A
decision the user did not confirm is an assumption; this interview exists so
that few remain.

Read the `## Warrant contract` section of the root `AGENTS.md` first. If it is
missing, tell the user to run `warrant-setup` and stop. Note the `### Glossary`
and `### Decision records` locations; either may be `none`.

## Before the first question

1. Read the request and the code, configuration and documentation it touches.
2. Read the glossary, if the contract names one, and the existing decision
   records. Do not re-open a recorded decision unless the user asks.
3. List the open decisions: anything that changes scope, externally visible
   behavior, compatibility or acceptance criteria.
4. Remove every item you can answer from the project's files (a supported
   language version, an existing command, a configured path). Do not ask the
   user for facts the project already states.

## Asking

- Ask exactly one question per message.
- Start with the decision that others depend on.
- Give the options you see as a short list, mark one **recommended**, and say
  why in one line.
- Then stop and wait for the answer.

## Terms

When the user uses a term:

- It is in the glossary with a different meaning: quote the glossary
  definition word for word and ask which meaning applies. Do not guess, and
  record nothing that uses the term until the user answers.
- It is new and the user confirms its meaning: add it to the glossary right
  away, in the glossary's own format (a table row in a table, a
  `- **term**: meaning` bullet otherwise).
- Never change or remove an existing glossary entry.

## Decisions

The request itself is not a confirmation. A decision is confirmed when the
user answers your question about it, or states explicitly that it is agreed.
When the user confirms a decision, record it right away:

- **Directory** location: a new file `NNNN-<slug>.md`, `NNNN` one above the
  highest existing number (`0001` when there is none), with:

  ```markdown
  # <decision in a few words>

  ## Context

  ## Decision

  ## Consequences
  ```

- **File** location: append the same three sections under a
  `## <decision in a few words>` heading.
- Never change an existing decision record.

If the contract names `none` for the glossary or the decision records, create
no file for that kind of record; keep the agreed items for the summary.

## Ending

The interview is done when the scope fits one sentence, the open decisions are
settled and the acceptance criteria are concrete. Then write a summary:

- scope in one sentence,
- confirmed decisions and terms (with the files you wrote them to, or the
  items themselves when the location is `none`),
- acceptance criteria,
- remaining assumptions: every decision still open, each with an owner who can
  confirm it.

Suggest running `openspec-propose` with this summary. Do not create the
OpenSpec change and do not write the proposal yourself.

If the user ends the interview early, write the same summary; every unanswered
decision goes under remaining assumptions.
