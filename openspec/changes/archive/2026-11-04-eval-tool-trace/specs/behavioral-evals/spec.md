# Spec Delta

## ADDED Requirements

### Requirement: Loaded skills

The eval runner SHALL record the skills each run loaded, from Claude Code's
tool calls and from Codex's reads of `.agents/skills/<name>/SKILL.md`.

#### Scenario: Claude loads a skill
- **WHEN** Claude's stream shows a `Skill` tool call for `warrant-verify`
- **THEN** the run's loaded skills include `warrant-verify`

### Requirement: Required skill load

IF a scenario lists `loaded` skills and a run loads none of a listed skill,
THEN the eval runner SHALL fail the run with a message naming that skill.

#### Scenario: Skill not loaded
- **WHEN** `minimal-change-implicit` requires `warrant-minimal-change` and the run never loads it
- **THEN** the run fails with "skill not loaded: warrant-minimal-change"

### Requirement: Claude report text

WHEN Claude runs with streamed output, the eval runner SHALL pass the final
result text to the checker.

#### Scenario: Streamed run
- **WHEN** the stream ends with a result event whose text is "Done."
- **THEN** the checker receives "Done."
