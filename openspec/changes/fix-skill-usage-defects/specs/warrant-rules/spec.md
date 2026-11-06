## ADDED Requirements

### Requirement: Test task per requirement

The warrant tasks rules SHALL require, for each requirement of the change, a
task that names the requirement and writes its tests.

#### Scenario: Rendered test-task rule
- **WHEN** `openspec instructions tasks --json` runs after setup
- **THEN** its `rules` contain the test-task rule

## MODIFIED Requirements

### Requirement: Option ladder in the design

The warrant design rules SHALL require recording the first option that fully
works, with the reason each earlier option failed, in an order written in the
rule itself: no change, existing project code, standard library or platform,
installed dependency, new code.

#### Scenario: Rendered design rule
- **WHEN** `openspec instructions design --json` runs after setup
- **THEN** its `rules` contain the option-ladder rule with all five options in order

### Requirement: Path after REVISE

WHEN the artifact review ends with `Artifact review: REVISE`, the warrant apply
guidance SHALL direct the agent to revise the artifacts and run the artifact
review again, and to ask the requester and stop before any task when a
blocking finding needs a decision only the requester can make.

#### Scenario: Blocking finding
- **WHEN** the artifact review reports a requirement without a test task
- **THEN** the guidance asks to revise the tasks and review again before the first task

#### Scenario: Unconfirmed decision
- **WHEN** a blocking finding is a conflict with an archived design that only the requester can resolve
- **THEN** the guidance asks the requester and stops before the first task
