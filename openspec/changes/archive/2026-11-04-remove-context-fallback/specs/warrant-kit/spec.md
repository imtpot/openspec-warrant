# Spec Delta

## REMOVED Requirements

### Requirement: Fresh context with a fallback

**Reason**: Every supported agent starts sub-agents, so the fallback sentence
describes a case that does not occur and costs tokens on every load.
**Migration**: Remove sentences that start with "If you cannot start a
separate context"; ask for the fresh context only.
