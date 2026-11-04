# Spec Delta

## MODIFIED Requirements

### Requirement: Supported agents

The eval runner SHALL run each scenario headless with Claude Code and Codex
when no agent filter is given.

#### Scenario: Full run
- **WHEN** the user runs the evals without an agent filter
- **THEN** the results contain one entry per scenario for Claude Code and for Codex

## ADDED Requirements

### Requirement: Copilot on request

WHERE the agent filter names `copilot`, the eval runner SHALL run the scenarios
with GitHub Copilot CLI.

#### Scenario: Copilot selected
- **WHEN** the user runs the evals with the filter `copilot`
- **THEN** the results contain entries for Copilot only
