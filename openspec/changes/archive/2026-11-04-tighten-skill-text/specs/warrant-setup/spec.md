# Spec Delta

## ADDED Requirements

### Requirement: No confirmed destructive actions

IF the user confirms no destructive action, THEN the setup skill SHALL leave
the Destructive actions subsection empty.

#### Scenario: Nothing confirmed
- **WHEN** setup proposes `make deploy` and the user confirms none
- **THEN** `### Destructive actions` has no entry
