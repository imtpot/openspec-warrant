---
name: warrant-minimal-change
description: Use when writing, fixing or refactoring code, and when the user asks for the shortcut ledger or the list of shortcut comments.
license: MIT
---

# Minimal change

A change is warranted line by line. Each added or changed line exists because
the task, a requirement, Protected code or a declared standard needs it. Be
economical with the solution and complete with its reach.

## Before you write code

1. List every place the change must reach: callers, tests, fixtures,
   configuration, exports, documentation that names the changed behavior.
2. If the work belongs to an OpenSpec change, read its specs. The specs define
   the required behavior. Protected code and the files under `### Standards` of
   the Warrant contract add what every change keeps.

## Option ladder

Go through these options in order and take the first that solves the whole
task:

1. **No change.** The behavior already exists, or a setting already provides it.
2. **Existing project code.** A function, module or pattern in this project
   already does it. Call it the way the surrounding code does.
3. **Standard library or platform.** Use it. If the project has its own wrapper
   for the same thing, use the wrapper.
4. **An installed dependency.** Use it. Write a few lines of code instead of
   adding a dependency for them.
5. **New code.** Write the least code that works and that a reader understands
   at a glance.

When you leave out a feature, option or variant that the request did not ask
for, name it in one line of your report, so the requester can ask for it.

## While you write

- Write only the code the task needs: no wrapper, abstraction, parameter,
  option, configuration or "for later" code beyond it. Deleting code beats
  adding code.
- Keep the structure the project already has: its layers, names and conventions.
- Fix a bug at its root, once, in the shared code.
- Update every caller, test, fixture and configuration that your change breaks,
  in the same change.
- When you move or merge code, keep its validation and error handling.
- Between two options of the same size, take the one that handles edge cases.
- Give new non-trivial logic (a branch, a loop, a parser) one small test.
- Delete every temporary, backup or scratch file you created before you report
  the change.

## Protected code

Keep these in new and existing code, even when leaving them out would make the
change smaller:

- validation at trust boundaries (user input, network input, file input),
- error handling that prevents data loss,
- security checks,
- accessibility of user interfaces,
- anything the requester asked for.

## Trace every line

When the work belongs to an OpenSpec change, review your diff before you report
completion. For each added line, name its basis:

- `requirement: <name>`: a requirement of the change,
- `protected: <item>`: an item of the Protected code list,
- `standard: <file>`: a rule in a file under `### Standards` of the Warrant
  contract.

"Anything the requester asked for" is not a basis of its own. Such a line
serves a requirement, or the specs are missing one. Imports, test code and
formatting count for the line they support. Remove every line that has no
basis. If the change needs a line that has no basis, stop and tell the user that
the specs are missing a requirement.

## Mark deliberate limitations

When you accept a known limitation, put a comment at that place in this form:

```
shortcut: <the limit>, <when to upgrade>
```

Example: `# shortcut: first 100 items only, paginate when a project exceeds 100`.
Always name the trigger for the upgrade. A shortcut without a trigger becomes
permanent without anyone deciding it.

## Shortcut ledger

When the user asks for the shortcut ledger, list the shortcuts without changing
any file:

1. Run `git grep -nE '(#|//|--|;|/\*) ?shortcut:' -- ':!.agents'`.
   This covers files tracked by git, skips installed skills (whose examples
   use the convention) and requires a comment prefix, so prose that only
   mentions the convention is not listed.
2. Print one line per hit:
   `<file>:<line> - limit: <the limit> - upgrade: <the trigger>`
3. Tag a line `no-trigger` when its comment names no upgrade trigger.
4. End with `<N> shortcuts, <M> without trigger.` If there are none, print
   `No shortcuts.`
