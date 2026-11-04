# Spec Delta

## ADDED Requirements

### Requirement: Artifact mode changes no file

WHILE the review skill reviews a change's artifacts, the review skill SHALL
leave every file unchanged.

#### Scenario: Flawed artifacts
- **WHEN** the artifact review finds flaws
- **THEN** `git status` is the same before and after

### Requirement: EARS findings

WHEN the review skill reviews a change's artifacts, the review skill SHALL
report each requirement that does not use exactly one EARS pattern with one
`SHALL` as a blocking finding naming the requirement.

#### Scenario: Compound requirement
- **WHEN** a requirement reads "... SHALL raise an error and SHALL NOT print output"
- **THEN** the report names that requirement as blocking

### Requirement: Missing tasks

WHEN the review skill reviews a change's artifacts, the review skill SHALL
report a task list without a test task for a requirement, or without a
verification group, as a blocking finding.

#### Scenario: No verification group
- **WHEN** `tasks.md` has no verification tasks
- **THEN** the report names the missing verification group as blocking

### Requirement: Contradicted decision

WHEN the review skill reviews a change's artifacts, the review skill SHALL
report a design decision that contradicts a recorded decision as a blocking
finding quoting both.

#### Scenario: Output format already decided
- **WHEN** a recorded decision says machine output is JSON and the design chooses YAML
- **THEN** the report quotes both decisions and marks the conflict as blocking

### Requirement: Unlisted assumption

WHEN the review skill reviews a change's artifacts, the review skill SHALL
report a decision that the specs or design present as settled, and that the
proposal lists neither as confirmed nor under Assumptions, as a blocking finding.

#### Scenario: Unconfirmed output path
- **WHEN** the design fixes an output path that the proposal never mentions
- **THEN** the report names the decision as an unlisted assumption

### Requirement: Artifact review in a fresh context

The review skill SHALL review the artifacts in a separate, fresh context that
receives the artifact files and not the conversation that produced them.

#### Scenario: Agent without separate contexts
- **WHEN** the agent cannot start a separate context
- **THEN** the skill re-reads the artifact files from disk and reviews them as written, ignoring its own earlier reasoning

### Requirement: Verdict line

WHEN the artifact review ends, the review skill SHALL end its report with the
line `Artifact review: REVISE` if any blocking finding exists and
`Artifact review: PASS` otherwise.

#### Scenario: Blocking finding
- **WHEN** the review reports one blocking finding
- **THEN** the last line of the report is `Artifact review: REVISE`
