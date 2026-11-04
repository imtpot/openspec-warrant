---
name: warrant-setup
description: Use when the user asks to set up, install or upgrade openspec-warrant in a project that uses OpenSpec 1.16 or later.
license: MIT
---

# Set up openspec-warrant

Add warrant's rules to the project's OpenSpec configuration and declare the
project contract that the other `warrant-*` skills read. Run the steps in order.
Stop at the first step that says stop, and write nothing after it.

## 1. Check the OpenSpec CLI version

Run `openspec --version`.

- If the version is older than `1.16.0`, stop. Report the installed version and
  that warrant needs OpenSpec 1.16 or later. Do not write any file.

## 2. Check for an OpenSpec root

Run `openspec list --json` and read `root`. OpenSpec searches parent
directories, so it can report the root of an enclosing repository.

- If `root` is `null`, or `root.path` is not this project's top directory (the
  output of `git rev-parse --show-toplevel`, or the current directory outside
  git), stop. Tell the user to run `openspec init` in this project first. Do
  not write any file and do not run `openspec init` yourself.

## 3. Find the shipped rules

The rules ship next to this skill as `rules.yaml`. Use the first that exists:

1. `.agents/skills/warrant-setup/rules.yaml` (project install)
2. `~/.agents/skills/warrant-setup/rules.yaml` (global install)

- If neither exists, stop. Report both paths and suggest reinstalling with
  `npx skills add imtpot/openspec-warrant`.

## 4. Merge the rules into `openspec/config.yaml`

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

Then verify:

- `openspec list --json` prints no warning about `rules` or `operations`.
- The number of list entries that start with `[warrant] ` in
  `openspec/config.yaml` equals the number of list entries in `rules.yaml`.

If either check fails, report the problem and stop.

## 5. Create the project contract

Open the root `AGENTS.md`.

- If it already contains a `## Warrant contract` section, leave the file
  unchanged and go to step 6.
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

## 6. Report

Report what you did: rules added or replaced, contract created or unchanged.
Then print this command with the installed OpenSpec version, which installs the
OpenSpec workflow skills for that release:

```sh
npx skills add https://github.com/Fission-AI/OpenSpec/tree/v<installed version>/skills
```

Do not run it yourself.
