# Spec Delta

## MODIFIED Requirements

### Requirement: EARS findings

WHEN the review skill reviews a change's artifacts, the review skill SHALL
report each requirement that has more than one `SHALL` or is not written in an
EARS pattern as a blocking finding naming the requirement.

#### Scenario: Compound requirement
- **WHEN** a requirement reads "... SHALL raise an error and SHALL NOT print output"
- **THEN** the report names that requirement as blocking

#### Scenario: Two clauses in rule order
- **WHEN** a requirement reads "WHERE the CLI runs in machine mode, WHEN a value cannot be serialized, the report command SHALL exit with code 2."
- **THEN** the report raises no EARS finding for it

### Requirement: Removed protection

The review skill SHALL report the removal of any code that
`warrant-minimal-change` protects as a blocking Standards finding.

#### Scenario: Dropped input check
- **WHEN** the diff deletes a check of user input
- **THEN** the Standards section lists the deletion as blocking
