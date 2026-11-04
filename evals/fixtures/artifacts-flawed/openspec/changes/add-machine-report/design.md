# Design

## Decisions

### 1. YAML documents

Machine mode prints YAML, because it is easier to read in CI logs.

### 2. Output file

Machine mode writes the document to `reports/report.yaml` instead of stdout.
