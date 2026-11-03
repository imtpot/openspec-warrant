# Spec Delta

## MODIFIED Requirements

### Requirement: Supported agents

The eval runner SHALL run each scenario headless with Claude Code, Codex and
GitHub Copilot CLI.

#### Scenario: Full run
- **WHEN** the user runs the evals without an agent filter
- **THEN** the results contain one entry per scenario and agent

## ADDED Requirements

### Requirement: Agent CLI unavailable

IF an agent CLI is not installed or not authenticated, THEN the eval runner
SHALL mark that agent's entries as not run with the reason and continue with the
other agents.

#### Scenario: Missing Copilot CLI
- **WHEN** `copilot` is not on PATH
- **THEN** Copilot entries are marked not run and the other agents still run

## REMOVED Requirements

### Requirement: Agent not available
**Reason**: Its only scenario used agy; the same behavior moves to "Agent CLI unavailable" with a scenario for a supported agent.
**Migration**: None; the behavior is unchanged.

### Requirement: Command denied in headless mode
**Reason**: Only agy produced headless permission denials, and agy is no longer evaluated.
**Migration**: None; a run that an agent cannot complete now reads as fail.
