## Why

The skills are in use in another project, and a review of `577421a` found
instructions that an agent cannot follow as written, or that lead it to act
against the specs:

- `warrant-tdd` sends a test that fails because the function under test does
  not exist yet to "fix the test", while production code may change only in
  Green. The mutation check says "red and green as in step 2", but a test that
  catches a mutation passes on the current code, which step 2 reads as
  "behavior already exists".
- `warrant-verify` says to run the commands again after any file change, so
  writing `Result:` lines into `tasks.md` restarts verification. Without a
  contract it allows "diagnostic" runs of the commands the contract would
  declare. It checks Destructive actions only for verification commands, so a
  narrowed run in `warrant-tdd` is never checked.
- The artifact review blocks a requirement without a test task, but no rule
  asks the planner for one. After `REVISE` the apply guidance loops with no
  exit when a finding needs the requester's decision. The design rule names the
  option ladder of a skill the planner may not have loaded.
- `warrant-setup` tells the user to run `openspec init --profile core`, which
  overrides a global `custom` profile and drops the `verify` workflow the Spec
  axis needs. It finds `rules.yaml` only under `.agents/`, so an agent-specific
  install stops at step 4.
- The shortcut ledger lists the skill's own examples from a tracked
  `.claude/skills/` copy. Receive mode has no rule for which OpenSpec change
  its requirements come from.

## Why code is needed

The defects are in the text of `skills/*/SKILL.md` and
`skills/warrant-setup/rules.yaml`; no configuration or documentation outside
them changes what an agent reads.

## What Changes

- `warrant-tdd`: a failure because the code under test does not exist yet is
  the missing behavior. The mutation check applies each mutation temporarily,
  runs the tests, and reverts it; a new test must fail on the mutation and
  pass after the revert. Narrowed runs follow the Destructive actions check.
- `warrant-verify`: "the files under verification" are the files the commands
  read; recording results in OpenSpec artifacts or the report is not a change.
  Without a contract, no test, lint, type-check or build command runs at all.
  The Destructive actions check covers every command the agent runs.
- `rules.yaml`: a tasks rule asks for a test task per requirement that names
  it. The REVISE guidance stops and asks the requester when a blocking finding
  needs a decision. The design rule lists the ladder rungs itself.
- `warrant-review`: Artifact mode defines a test task as one that names the
  requirement. Receive mode chooses the change as Review mode step 2 does.
- `warrant-setup`: the missing-root message names
  `openspec init --tools agents` without `--profile`. Rules are first looked up
  next to the loaded `SKILL.md`.
- `warrant-minimal-change`: the ledger command also excludes `.claude`.
- The kit tests in `evals/tests/test_kit.py` check each new wording.

## Out of scope

This change fixes skill text; it does not change the eval harness, the
benchmark or the README.

- The checker defects found in the same review (success-claim clauses, exit
  code of the full run, the red/green false pass, substring terms).
- Benchmark scoring over stderr and its timeout handling.
- README claims and numbers.
- Leftover `[warrant]` entries of lists a newer `rules.yaml` drops, the
  overlap of the `warrant-tdd` and `warrant-minimal-change` descriptions, and
  contract handling in `warrant-minimal-change`.
- New eval scenarios for the specs that have none.

## Assumptions

- The requester wants every listed defect fixed in one change, and the eval
  scenarios of all five skills run before archive. Owner: requester (confirmed).
- `openspec init --tools agents` without `--profile` uses the global profile;
  when that profile lacks `verify` or selects no workflow, step 3's existing
  note tells the user how to add it. Owner: requester (confirmed).
- The artifact review counts a task as the requirement's test task when the
  task names the requirement; the tasks rule also asks that task to write the
  tests, which the review cannot check from text alone. Owner: requester
  (confirmed).
- An agent that loads a skill knows the directory of its `SKILL.md`, so setup
  looks for `rules.yaml` there first. This replaces the archived
  `add-warrant-core` decision that only the `.agents` paths fixed by the
  `skills` CLI are searched; those paths stay as fallbacks. Owner: requester
  (confirmed).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `test-first`: Fail for the expected reason (missing code under test);
  Mutation check (how red and green are shown).
- `verification-evidence`: Fresh evidence only (which files count);
  Destructive verification (every command); Development runs allowed (only
  with a contract).
- `warrant-rules`: Option ladder in the design (rungs listed); Path after
  REVISE (requester decision); new Test task per requirement.
- `warrant-setup`: No OpenSpec root (command without `--profile`); Install the
  rules (rules next to the loaded skill).
- `project-contract`: No guessed commands (no narrowed or diagnostic run
  either).
- `code-review`: Missing tasks (test task defined); Change selection (Receive
  mode).

## Impact

- `skills/warrant-tdd/SKILL.md`, `skills/warrant-verify/SKILL.md`,
  `skills/warrant-review/SKILL.md`, `skills/warrant-setup/SKILL.md`,
  `skills/warrant-setup/rules.yaml`, `skills/warrant-minimal-change/SKILL.md`.
- `openspec/config.yaml` and `evals/fixtures/warrant-project/openspec/config.yaml`,
  which must carry the shipped rules (`test_dogfood.py`).
- `evals/tests/test_kit.py`.
- Projects already set up get the new rules when they run `warrant-setup` again.
