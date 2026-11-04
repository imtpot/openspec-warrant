# Spec Delta

## ADDED Requirements

### Requirement: Artifact review scenario checks

The evals SHALL include an artifact review scenario whose checker fails unless
the report names each planted flaw and ends with `Artifact review: REVISE`, and
a scenario on sound artifacts whose checker fails unless the report ends with
`Artifact review: PASS`.

#### Scenario: Missed compound requirement
- **WHEN** the report does not name the compound requirement
- **THEN** the checker fails and names the missing finding
