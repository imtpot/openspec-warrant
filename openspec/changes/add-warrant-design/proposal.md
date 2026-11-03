# Proposal

## Why

The warrant schema makes unconfirmed decisions visible as assumptions, but only
after a proposal is written. The trial run that led to warrant ended with nine
decisions an agent made alone. The cheaper fix is earlier: settle the open
design decisions with the requester before the proposal, one at a time, and
keep the agreed terms and decisions where the project already keeps them.

## What Changes

- Add the `warrant-design` skill: an interview that settles open design
  decisions before an OpenSpec change is proposed.
  - One question per message, with options and a recommended answer.
  - Facts the project already contains (code, configuration, documentation)
    are looked up, not asked.
  - An agreed term goes into the glossary file named in the contract; an agreed
    decision goes into the contract's decision records, as soon as it is agreed.
  - A term that conflicts with the glossary is called out with the glossary's
    definition.
  - When the scope fits one sentence and the acceptance criteria are concrete,
    the skill summarizes decisions and remaining assumptions and suggests
    `openspec-propose`; it does not create the change.
- Add design eval scenarios.

## Capabilities

### New Capabilities
- `design-interview`: the behavior of the `warrant-design` skill.

### Modified Capabilities
- `behavioral-evals`: design scenarios join the eval set.

## Impact

New `skills/warrant-design/SKILL.md`; new checkers, fixtures and scenarios in
`evals/`; `README.md` and the `AGENTS.md` development setup command. No change
to the schema or the contract format.

## Why code is needed

No configuration or existing tool runs a design interview against a project's
glossary and decision records; the OpenSpec explore skill does not record terms
or decisions and does not stop at one question.

## Out of scope

This change adds the interview skill; it does not write proposals, create
OpenSpec changes or change the contract format.

Features and options deliberately left out:

- Creating the OpenSpec change or drafting the proposal.
- A batch mode that asks all questions at once.
- Creating a glossary or decision-record location the contract does not name.
- Rewriting existing glossary entries or decision records.

## Assumptions

Confirmed by the requester: `warrant-design` is the next v2 skill; it records
agreed terms in the glossary and agreed decisions in the decision records
during the interview; it asks one question at a time with a recommended answer;
it suggests `openspec-propose` and does not write the proposal; a decision in a
directory location becomes `NNNN-<slug>.md` numbered after the highest existing
one, and in a file location an appended section; a decision record has context,
decision and consequences; decisions still open at the end are listed as
assumptions with an owner.

None.
