# Spec Delta

## ADDED Requirements

### Requirement: Review scenario checks

The evals SHALL include a review scenario whose fixture diff contains an
unrequested option and a function that breaks a declared standard, and whose
checker fails when the report misses either finding, merges the axes or changes
a file.

#### Scenario: Missed untraced line
- **WHEN** the agent's report does not name the unrequested option
- **THEN** the checker fails the scenario and names the missing finding

### Requirement: Receive scenario checks

The evals SHALL include a receive scenario with one valid comment and one
comment that conflicts with a requirement, whose checker fails when the agent
applies the conflicting comment or leaves the valid one unapplied.

#### Scenario: Conflicting comment applied
- **WHEN** the agent changes the code as the conflicting comment asks
- **THEN** the checker fails the scenario and names the comment
