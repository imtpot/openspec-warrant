# Spec Delta

## MODIFIED Requirements

### Requirement: Verify before checking off

The warrant apply guidance SHALL direct the orchestrating agent to run
`warrant-verify` after a sub-agent reports and to check off the group's tasks
only when every verification command exited with 0.

#### Scenario: Group finished
- **WHEN** a sub-agent reports a finished group
- **THEN** the guidance asks the orchestrating agent to verify before checking off

## ADDED Requirements

### Requirement: Path after REVISE

WHEN the artifact review ends with `Artifact review: REVISE`, the warrant apply
guidance SHALL direct the agent to revise the artifacts and run the artifact
review again.

#### Scenario: Blocking finding
- **WHEN** the artifact review reports a requirement without a test task
- **THEN** the guidance asks to revise the tasks and review again before the first task
