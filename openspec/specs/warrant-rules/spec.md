# warrant-rules Specification

## Purpose
Defines the artifact rules and operation guidance that warrant adds to a
project's `openspec/config.yaml`, on top of OpenSpec's own `spec-driven` schema.

## Requirements

### Requirement: Marked entries

The warrant rules and guidance SHALL start each of their entries with `[warrant] `.

#### Scenario: Project config after setup
- **WHEN** setup has written the rules
- **THEN** every entry that warrant added starts with `[warrant] `

### Requirement: Assumptions in the proposal

The warrant proposal rules SHALL require an Assumptions section that lists each
decision the requester has not confirmed, with an owner.

#### Scenario: Rendered proposal instructions
- **WHEN** `openspec instructions proposal --json` runs in a project after setup
- **THEN** its `rules` contain the Assumptions rule

### Requirement: Why code is needed

The warrant proposal rules SHALL require a statement of why configuration, an
existing tool or a documentation change cannot meet the need.

#### Scenario: Rendered proposal rule
- **WHEN** `openspec instructions proposal --json` runs after setup
- **THEN** its `rules` contain the "why code is needed" rule

### Requirement: EARS requirements

The warrant specs rules SHALL require one EARS pattern per requirement, WHERE
only for options, an IF/THEN requirement for each real failure, and a trace to
the request or an assumption.

#### Scenario: Rendered specs rules
- **WHEN** `openspec instructions specs --json` runs after setup
- **THEN** its `rules` contain the EARS, WHERE, IF/THEN and trace rules

### Requirement: No rule OpenSpec already gives

The warrant rules SHALL contain no rule that OpenSpec's own spec guidance
already gives, such as one `SHALL` per requirement or observable outcomes.

#### Scenario: One-SHALL rule
- **WHEN** OpenSpec's `writing-specs` guidance asks for one `SHALL` per requirement
- **THEN** `rules.yaml` has no rule about the number of `SHALL` per requirement

### Requirement: Option ladder in the design

The warrant design rules SHALL require recording the first option that fully
works, in the order existing code or tool, standard library, installed
dependency, new code, with the reason each earlier option failed.

#### Scenario: Rendered design rule
- **WHEN** `openspec instructions design --json` runs after setup
- **THEN** its `rules` contain the option-ladder rule

### Requirement: Review and verification tasks

The warrant tasks rules SHALL require a review group followed by a verification
group with one task per contract verification command, and a checks-not-run
record.

#### Scenario: Rendered tasks rules
- **WHEN** `openspec instructions tasks --json` runs after setup
- **THEN** its `rules` contain the review, verification and not-run rules

### Requirement: Glossary terms

The warrant proposal and specs rules SHALL require using the terms of the
glossary named in the contract and adding a new term to it once the requester
confirms its meaning.

#### Scenario: Rendered glossary rule
- **WHEN** `openspec instructions specs --json` runs after setup
- **THEN** its `rules` contain the glossary rule

### Requirement: Apply guidance

The warrant apply guidance SHALL direct the agent to follow `warrant-tdd`,
`warrant-minimal-change` and `warrant-verify`.

#### Scenario: Rendered apply guidance
- **WHEN** `openspec instructions apply --json` runs for a change after setup
- **THEN** its `operationGuidance` names the three skills

### Requirement: Artifact review before apply

The warrant apply guidance SHALL ask for a `warrant-review` artifact review
before the first task and for implementation only after `Artifact review: PASS`.

#### Scenario: Rendered apply guidance
- **WHEN** `openspec instructions apply --json` runs for a change after setup
- **THEN** its `operationGuidance` asks for the artifact review before the first task

### Requirement: Verification result format

The warrant tasks rules SHALL require each verification task to record its
result on its own line as `Result: exit <code>, <result line>` or
`Result: not run, <reason>`.

#### Scenario: Rendered tasks rule
- **WHEN** `openspec instructions tasks --json` runs after setup
- **THEN** its `rules` contain the result format

### Requirement: Sub-agent per task group

The warrant apply guidance SHALL direct the agent to implement each task group
in a separate, fresh context that receives the group's tasks, their
requirement names and the paths of the change's artifacts.

#### Scenario: Rendered sub-agent guidance
- **WHEN** `openspec instructions apply --json` runs for a change after setup
- **THEN** its `operationGuidance` asks for a fresh context per task group

### Requirement: Verify before checking off

The warrant apply guidance SHALL direct the orchestrating agent to run
`warrant-verify` after a sub-agent reports and to check off the group's tasks
only when every verification command exited with 0.

#### Scenario: Group finished
- **WHEN** a sub-agent reports a finished group
- **THEN** the guidance asks the orchestrating agent to verify before checking off

### Requirement: Independent task groups

The warrant tasks rules SHALL require each implementation group to be
implementable from the artifacts and the code without another group's
unfinished work.

#### Scenario: Rendered tasks rule
- **WHEN** `openspec instructions tasks --json` runs after setup
- **THEN** its `rules` ask for independent task groups

### Requirement: Smaller model for settled groups

WHERE the agent can choose a sub-agent's model, the warrant apply guidance
SHALL direct it to give a task group whose requirements and design leave
nothing open to a smaller, faster model, and every other group to the
session's model.

#### Scenario: Settled group
- **WHEN** a task group's requirements and design leave no point open
- **THEN** the guidance asks for a smaller, faster model for its sub-agent

### Requirement: Path after REVISE

WHEN the artifact review ends with `Artifact review: REVISE`, the warrant apply
guidance SHALL direct the agent to revise the artifacts and run the artifact
review again.

#### Scenario: Blocking finding
- **WHEN** the artifact review reports a requirement without a test task
- **THEN** the guidance asks to revise the tasks and review again before the first task
