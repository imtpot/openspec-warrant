## MODIFIED Requirements

### Requirement: No guessed commands

IF a warrant skill runs in a project whose `AGENTS.md` has no warrant contract,
THEN the skill SHALL run no command that the contract would declare.

#### Scenario: Verify without contract runs nothing
- **WHEN** `warrant-verify` runs in a project without the contract
- **THEN** it runs no verification command

#### Scenario: No diagnostic run without contract
- **WHEN** the project has no warrant contract
- **THEN** the agent runs no narrowed or diagnostic test, lint, type-check or build command
