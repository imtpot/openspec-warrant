# Spec Delta

## Purpose

Defines the `warrant-design` skill: an interview that settles open design
decisions before an OpenSpec change is proposed, and records agreed terms and
decisions where the project keeps them.

## ADDED Requirements

### Requirement: One question per message

WHEN the design skill needs a decision from the user, the design skill SHALL ask
exactly one question in that message.

#### Scenario: Several open decisions
- **WHEN** a request leaves three decisions open
- **THEN** the first message asks about one of them only

### Requirement: Options and recommendation

WHEN the design skill asks a question, the design skill SHALL give the options it
sees and mark one as recommended with a reason.

#### Scenario: Output format question
- **WHEN** the skill asks whether output is JSON or YAML
- **THEN** the message lists both and names one as recommended, with the reason

### Requirement: Look up facts instead of asking

The design skill SHALL take facts that the project's code, configuration or
documentation contains from those files instead of asking the user.

#### Scenario: Language version in configuration
- **WHEN** `pyproject.toml` declares the supported Python versions
- **THEN** the skill does not ask the user which Python versions to support

### Requirement: Record an agreed term

WHEN the user and the design skill agree on the meaning of a term, the design
skill SHALL add the term and its meaning to the glossary file named in the
contract.

#### Scenario: New term
- **WHEN** the user confirms that "headroom" means free quota after reservations
- **THEN** the glossary file contains "headroom" with that meaning

### Requirement: Record an agreed decision

WHEN the user confirms a design decision, the design skill SHALL write it to
the contract's decision-records location with its context, the decision and its
consequences.

#### Scenario: Decision in a directory
- **WHEN** the decision-records location is `docs/decisions/` holding `0001-use-json.md`
- **THEN** the skill writes `docs/decisions/0002-<slug>.md` with context, decision and consequences

### Requirement: No location declared

WHILE the contract names `none` for the glossary or the decision records, the
design skill SHALL create no file for that kind of record.

#### Scenario: Decision records none
- **WHEN** the contract's Decision records subsection reads `none`
- **THEN** no decision file is created

### Requirement: Records without a location

WHILE the contract names `none` for the glossary or the decision records, the
design skill SHALL list the agreed records of that kind in its summary.

#### Scenario: Summary lists decisions
- **WHEN** the contract's Decision records subsection reads `none` and two decisions were agreed
- **THEN** the summary lists both decisions

### Requirement: Conflicting term

IF the user uses a term with a meaning that differs from its glossary entry,
THEN the design skill SHALL quote the glossary definition and ask which meaning
applies.

#### Scenario: Quota means two things
- **WHEN** the glossary defines "quota" as a project limit and the user uses it for free capacity
- **THEN** the skill quotes the glossary definition and asks which meaning applies

### Requirement: Existing records unchanged

The design skill SHALL leave existing glossary entries and decision records
unchanged.

#### Scenario: Term already defined
- **WHEN** the glossary already defines a term the interview discusses
- **THEN** the existing entry stays as it is

### Requirement: Ready for a proposal

WHEN the scope fits one sentence, the open design decisions are settled and the
acceptance criteria are concrete, the design skill SHALL summarize the decisions
and suggest running `openspec-propose`.

#### Scenario: Converged interview
- **WHEN** the user has confirmed scope, decisions and acceptance criteria
- **THEN** the summary lists the decisions and names `openspec-propose`

### Requirement: Remaining decisions as assumptions

IF the interview ends while decisions are still open, THEN the design skill
SHALL list each open decision as an assumption with an owner in its summary.

#### Scenario: User stops early
- **WHEN** the user ends the interview with one decision unanswered
- **THEN** the summary lists that decision as an assumption with an owner

### Requirement: No change created

The design skill SHALL create no OpenSpec change and write no proposal.

#### Scenario: End of interview
- **WHEN** the interview ends
- **THEN** `openspec/changes/` contains no new change
