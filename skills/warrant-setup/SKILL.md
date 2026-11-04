---
name: warrant-setup
description: Use when the user asks to set up, install or upgrade openspec-warrant in a project that uses OpenSpec 1.16.
license: MIT
---

# Set up openspec-warrant

Install the `warrant` OpenSpec schema into this project and declare the project
contract that the other `warrant-*` skills read. Run the steps in order. Stop at
the first step that says stop, and write nothing after it.

## 1. Check the OpenSpec CLI version

Run `openspec --version`.

- If the version is not `1.16.x`, stop. Report the installed version and that
  warrant supports OpenSpec 1.16. Do not write any file.

## 2. Check for an OpenSpec root

Run `openspec list --json` and read `root`. OpenSpec searches parent
directories, so it can report the root of an enclosing repository.

- If `root` is `null`, or `root.path` is not this project's top directory (the
  output of `git rev-parse --show-toplevel`, or the current directory outside
  git), stop. Tell the user to run `openspec init` in this project first. Do
  not write any file and do not run `openspec init` yourself.

## 3. Find the shipped schema

The schema ships in this skill's directory under `schema/warrant/`. Look for
`schema.yaml` in these places, in order, and use the first that exists:

1. `.agents/skills/warrant-setup/schema/warrant/` (project install)
2. `~/.agents/skills/warrant-setup/schema/warrant/` (global install)

- If neither exists, stop. Report both paths and suggest reinstalling with
  `npx skills add imtpot/openspec-warrant`.

## 4. Install the schema

Target: `openspec/schemas/warrant/`.

- Target missing: copy the shipped `warrant/` directory there.
- Target present and identical (`diff -r` shows nothing): leave it.
- Target present and different: show the user the `diff -r` output and ask
  whether to replace it. Replace it only after the user confirms. If the user
  declines, keep the existing files and continue.

Then run `openspec schema validate warrant`. If it fails, stop and report its output.

## 5. Select the schema

In `openspec/config.yaml`, set the top-level `schema` field to `warrant`.

- Change only that field. Keep every other line, comment and key as it is.
- If the file has no `schema` field, add `schema: warrant` as the first key.

## 6. Create the project contract

Open the root `AGENTS.md`.

- If it already contains a `## Warrant contract` section, leave the file
  unchanged and go to step 7.
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

### Decision records

<relative path to the decision records, or none>

### Standards

- `<relative path to a file with coding standards>`
```

- Keep the five subsections in this order, even when one is empty.
- Under Destructive actions, propose deploy, publish, delete and migration
  commands found in the project, and write only the confirmed ones.
- Under Glossary and Decision records, write a path only if that file or
  directory exists; otherwise write `none`.
- Under Standards, propose existing files that state coding rules for this
  project, such as `CONTRIBUTING.md`, a style guide or a `docs/` page about
  conventions. Write only the files the user confirms, or `none`.

## 7. Report

Report what you did: schema installed, replaced, unchanged or kept; config
updated; contract created or unchanged. Then print this command, which installs
the OpenSpec workflow skills for the supported release:

```sh
npx skills add https://github.com/Fission-AI/OpenSpec/tree/v1.16.0/skills
```

Do not run it yourself.
