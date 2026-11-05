## ADDED Requirements

### Requirement: Run log outside the workspace

WHERE a scenario lists tools to record, the eval runner SHALL keep the shims and
the run log in a directory next to the workspace, outside the workspace.

#### Scenario: Codex sandbox
- **WHEN** Codex runs a recorded tool under `workspace-write`, which keeps `.git` read-only
- **THEN** the run is logged

#### Scenario: Agent's view
- **WHEN** the agent lists or searches the workspace files
- **THEN** neither the shims nor the log appear
