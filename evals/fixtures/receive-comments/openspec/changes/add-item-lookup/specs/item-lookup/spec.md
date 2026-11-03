# Spec Delta

## Purpose

Tells a calling script, through the exit code, whether an item exists.

## ADDED Requirements

### Requirement: Known item

WHEN the item exists, the lookup command SHALL exit with code 0.

#### Scenario: Existing item
- **WHEN** the lookup runs for an existing item
- **THEN** the exit code is 0

### Requirement: Unknown item

IF the item does not exist, THEN the lookup command SHALL exit with code 2.

#### Scenario: Missing item
- **WHEN** the lookup runs for an item that does not exist
- **THEN** the exit code is 2
