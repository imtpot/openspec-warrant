# Design

## Context

See proposal.md - Why. Requirements are in `specs/`.

- The contract already names the glossary (one file or `none`) and the decision
  records (a file, a directory or `none`); `warrant-design` adds no contract field.
- Evals run headless: nobody answers the skill's questions.

## Goals / Non-Goals

**Goals:**
- The interview ends with every decision either confirmed and recorded, or
  listed as an assumption with an owner.

**Non-Goals:**
- No glossary or decision-record format beyond what the specs and the
  assumptions in the proposal define.

## Decisions

### 1. Records written as soon as they are agreed

The skill writes a term or decision right after the user confirms it, not at the
end. An interview that stops early keeps what was agreed. Rejected: one write
at the end, because an interrupted session loses everything.

### 2. Decision record format

Directory location: new file `NNNN-<slug>.md`, `NNNN` one above the highest
existing number (`0001` when empty), with `# <decision>`, `## Context`,
`## Decision`, `## Consequences`. File location: the same three sections
appended under a `## <decision>` heading. Option ladder: no existing tool writes
decision records in a project-defined place; the format is the common ADR shape
in three headings, which a few lines of skill text describe.

### 3. Glossary entry format

The skill follows the existing glossary's format: a table row when the file is a
table, a `- **term**: meaning` bullet otherwise. Rejected: a fixed format, which
would break glossaries kept as a `| Term | Meaning |` table.

### 4. Evals in two shapes

- **First question**: the prompt gives a request that leaves decisions open and
  says nobody can answer; the agent must ask one question with a recommended
  option and stop. Checker: exactly one `?`-terminated sentence outside code in
  the transcript's last message, a word from {recommend, recommended}, no
  question about the fact stated in the fixture's `pyproject.toml`, no file
  changed.
- **Recording**: the prompt lists decisions and terms the user has already
  confirmed and asks to record them; checker: the glossary and decision files
  contain them, existing entries are byte-identical, no new OpenSpec change, and
  the transcript names `openspec-propose`.
- **Conflict**: the fixture glossary defines "quota" as a project limit, the
  prompt uses it for free capacity; checker: the transcript quotes the glossary
  definition.
- **No locations**: contract with `none` for both; checker: no file changed,
  transcript lists the confirmed terms and decisions.

## Risks / Trade-offs

- [Counting `?` misreads a question inside an option] → Count only sentences
  that end with `?` outside code spans and list items; checker unit tests cover
  options written as bullets.
- [Recording scenarios bypass the interview] → They test only the recording
  rules; the first-question scenario tests the interview's opening, and the
  multi-turn interview stays a manual check.
