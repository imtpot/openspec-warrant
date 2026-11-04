# Spec Delta

## Purpose

Prints the report rows in a machine-readable form for CI.

## ADDED Requirements

### Requirement: Machine mode

WHEN machine mode is requested, the report command SHALL print every row in one JSON document on stdout.

#### Scenario: Two rows
- **WHEN** machine mode is requested for two rows
- **THEN** one JSON document with both rows is printed

### Requirement: Unserializable value

IF a row value cannot be serialized to JSON, THEN the report command SHALL raise an error before printing anything.

#### Scenario: Bad value
- **WHEN** a row value cannot be serialized
- **THEN** an error is raised and nothing is printed
