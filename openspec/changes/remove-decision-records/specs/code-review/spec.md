# Spec Delta

## MODIFIED Requirements

### Requirement: Contradicted decision

WHEN the review skill reviews a change's artifacts, the review skill SHALL
report a design decision that contradicts a decision in `design.md` of an
archived change as a blocking finding quoting both.

#### Scenario: Output format already decided
- **WHEN** an archived change's design says machine output is JSON and the design chooses YAML
- **THEN** the report quotes both decisions and marks the conflict as blocking
