# Spec Delta

## MODIFIED Requirements

### Requirement: Supported agents

The eval runner SHALL run each scenario headless with Claude Code and Codex.

#### Scenario: Full run
- **WHEN** the user runs the evals without an agent filter
- **THEN** the results contain one entry per scenario and agent

### Requirement: Agent CLI unavailable

IF an agent CLI is not installed or not authenticated, THEN the eval runner
SHALL mark that agent's entries as not run with the reason and continue with the
other agents.

#### Scenario: Missing Copilot CLI
- **WHEN** `codex` is not on PATH
- **THEN** Codex entries are marked not run and the other agents still run
