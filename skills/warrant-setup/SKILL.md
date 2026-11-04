---
name: warrant-setup
description: Use when the user asks to set up, install or upgrade openspec-warrant in a project.
license: MIT
---

# Set up openspec-warrant

Add warrant's rules to the project's OpenSpec configuration and declare the
contract the `warrant-*` skills read. Run the steps in order. At a step that
says stop, write nothing.

## 1. Check the OpenSpec CLI

Run `openspec --version`.

- If the command is missing or older than `1.16.0`, stop. Report the installed
  version, that warrant needs 1.16 or later, and the install command
  `npm install -g @fission-ai/openspec@latest` (or `brew install openspec`).

## 2. Check for an OpenSpec root

Run `openspec list --json` and read `root`. OpenSpec searches parent
directories, so it can report the root of an enclosing repository.

The project's top directory is `git rev-parse --show-toplevel`, or the current
directory outside git.

- If `root` is `null`, or `root.path` is not this project's top directory,
  stop. Tell the user to run `openspec init --tools agents --profile core`,
  which also writes the OpenSpec skills to `.agents/skills/`, and then this
  skill again.

## 3. Link the OpenSpec skills

For each `.agents/skills/openspec-*` directory and each existing
`.<agent>/skills/` directory, create the missing link `.<agent>/skills/<skill>`
pointing to `../../.agents/skills/<skill>`. Keep every existing entry.

If `.agents/skills/openspec-verify-change` is missing, note for the report
that the Spec axis of `warrant-review` needs it and that `openspec config
profile`, then `openspec update`, adds it.

## 4. Find the shipped rules

The rules ship next to this skill as `rules.yaml`. Use the first that exists:

1. `.agents/skills/warrant-setup/rules.yaml` (project install)
2. `~/.agents/skills/warrant-setup/rules.yaml` (global install)

- If neither exists, stop. Report both paths and suggest reinstalling with
  `npx skills add imtpot/openspec-warrant`.

## 5. Merge the rules into `openspec/config.yaml`

`rules.yaml` holds the lists `rules.<artifact>` and
`operations.<operation>.guidance`. Every entry starts with `[warrant] `.

For each of these lists:

1. In `openspec/config.yaml`, remove every entry of that list that starts with
   `[warrant] `.
2. Append the shipped entries to the same list, each as one double-quoted line,
   exactly as in `rules.yaml`. Create the list, and its parent keys, only if it
   is missing.

Change nothing else: keep `schema`, `context`, comments, the project's own
entries and their order.

Then check:

- `openspec list --json` prints no warning about `rules` or `operations`.
- The number of list entries that start with `[warrant] ` in
  `openspec/config.yaml` equals the number of list entries in `rules.yaml`.

If either check fails, report the problem and stop.

## 6. Draft the OpenSpec context

OpenSpec injects `context` from `openspec/config.yaml` into every planning
request.

- If `context` has a value, leave it unchanged and go to step 7.

Otherwise, read the project's own documents: `README`, the contributing guide,
`AGENTS.md` outside the Warrant contract and `docs/`. Collect only constraints
that an agent cannot infer from the code, for example "All user-facing text is
German" or "Public APIs stay backwards compatible". Leave out the tech stack,
the directory layout, commands and general good practice.

Propose at most 10 lines to the user. Write only the lines the user confirms,
as a `context: |` block after `schema`, and keep every other key and comment.
If the user confirms none, or you found none, write no `context`.

## 7. Create the project contract

Open the root `AGENTS.md`.

- If it already contains a `## Warrant contract` section, leave the file
  unchanged and go to step 8.
- If the file does not exist, create it with only the contract section.
- Otherwise, append the contract section at the end and keep the existing
  content unchanged.

Before writing, find candidate verification commands in the project's own
configuration: build files (`Makefile`, `package.json` scripts, `pyproject.toml`,
`justfile`, `mise.toml` tasks, `Taskfile.yml`) and CI configuration. Propose the
commands you found to the user and write only the ones the user confirms. Do not
invent a command that the project does not define. If the user confirms none,
leave the Verification list empty.

Write the section in exactly this form:

```markdown
## Warrant contract

### Verification

- <name>: `<exact command>`

### Destructive actions

- `<command or command prefix that needs explicit approval>`

### Glossary

<relative path to the glossary, or none>

### Standards

- `<relative path to a file with coding standards>`
```

- Keep the four subsections in this order, even when one is empty.
- Under Destructive actions, propose deploy, publish, delete and migration
  commands found in the project, and write only the confirmed ones. If the
  user confirms none, leave the subsection empty.
- Under Glossary, write a path only if that file exists. Otherwise write
  `none`.
- Under Standards, propose existing files that state coding rules for this
  project, such as `CONTRIBUTING.md`, a style guide or a `docs/` page about
  conventions. Write only the files the user confirms, or `none`.

## 8. Report

Report what you did: skill links created, rules added or replaced, context written or kept, contract created or
unchanged, and the note from step 3 if there is one.
