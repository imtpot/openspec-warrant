# Spec Delta

## ADDED Requirements

### Requirement: Sub-agent per task group

The warrant apply guidance SHALL direct the agent to implement each task group
in a separate, fresh context that receives the group's tasks, their
requirement names and the paths of the change's artifacts.

#### Scenario: Rendered sub-agent guidance
- **WHEN** `openspec instructions apply --json` runs for a change after setup
- **THEN** its `operationGuidance` asks for a fresh context per task group

### Requirement: Verify before checking off

The warrant apply guidance SHALL direct the orchestrating agent to run
`warrant-verify` after a sub-agent reports and before it checks off the
group's tasks.

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
