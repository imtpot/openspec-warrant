# Spec Delta

## ADDED Requirements

### Requirement: Draft the OpenSpec context

WHILE `context` in `openspec/config.yaml` is missing or empty, the setup skill
SHALL propose a context of at most 10 lines with only those constraints from
the project's own documents that an agent cannot infer from the code.

#### Scenario: Constraint in the README
- **WHEN** the README states that all user-facing text is German
- **THEN** setup proposes a context line with that constraint

#### Scenario: Discoverable facts
- **WHEN** the project has a `Makefile` with a `test` target
- **THEN** the proposed context names neither the test command nor the build tool

### Requirement: Write only confirmed context

WHEN the user confirms lines of the proposed context, the setup skill SHALL
write only those lines as `context` and keep every other key and comment.

#### Scenario: User confirms none
- **WHEN** the user confirms no line
- **THEN** `openspec/config.yaml` has no `context` value

### Requirement: Keep existing context

WHILE `context` in `openspec/config.yaml` is not empty, the setup skill SHALL
leave it unchanged.

#### Scenario: Context written by the team
- **WHEN** `context` already holds the team's text
- **THEN** after setup OpenSpec renders the same context
