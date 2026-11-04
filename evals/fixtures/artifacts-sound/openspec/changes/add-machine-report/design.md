# Design

## Decisions

### 1. JSON on stdout

Machine mode prints one JSON document to stdout, as decision 0001 requires;
`json.dumps` from the standard library covers it, so no dependency is added.
