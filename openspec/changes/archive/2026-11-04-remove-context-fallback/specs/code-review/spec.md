# Spec Delta

## REMOVED Requirements

### Requirement: Axes in separate contexts

**Reason**: Every supported agent starts sub-agents; the fallback is removed.
**Migration**: See "Axes in fresh contexts".

### Requirement: Artifact review in a fresh context

**Reason**: Every supported agent starts sub-agents; the fallback is removed.
**Migration**: See "Artifact review in a sub-agent".

## ADDED Requirements

### Requirement: Axes in fresh contexts

The review skill SHALL run the Spec axis and the Standards axis each in a
separate, fresh context.

#### Scenario: Branch review
- **WHEN** a branch is reviewed
- **THEN** each axis runs in its own fresh context and the report keeps their findings apart

### Requirement: Artifact review in a sub-agent

The review skill SHALL review the artifacts in a separate, fresh context that
receives the artifact files and not the conversation that produced them.

#### Scenario: Artifacts written in this conversation
- **WHEN** the agent wrote the artifacts earlier in the conversation
- **THEN** a fresh context reviews them from the files on disk
