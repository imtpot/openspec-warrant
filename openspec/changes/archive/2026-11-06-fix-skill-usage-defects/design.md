## Context

See proposal.md - Why. Every fix is a wording change in a skill or in
`rules.yaml`. `evals/tests/test_kit.py` already checks skill text by phrase
(for example `test_verify_allows_narrowed_runs_that_are_not_evidence`) and
limits each `SKILL.md` to 150 lines; `warrant-review` has 142.
`test_dogfood.py` requires `openspec/config.yaml` and
`evals/fixtures/warrant-project/openspec/config.yaml` to carry exactly the
shipped `[warrant]` lines. The skill text is written with `writing-for-agents`
and checked with `asd-ste100`, as `AGENTS.md` requires.

## Goals / Non-Goals

**Goals:** each instruction listed in the proposal can be followed as written
and agrees with its spec; the scenarios of all five skills and `propose` pass
on Claude Code and Codex after the change.

**Non-Goals:** see proposal.md - Out of scope.

## Decisions

Option ladder for every part: (1) no change leaves the defect; (2) existing
project code: the skills and `rules.yaml` are that code, so each part edits the
sentence that carries the defect, and adds a sentence only where none exists.
The rungs after (2) do not apply to instruction text.

### warrant-tdd

- Red, step 3: the first bullet becomes "It fails because the behavior, or the
  function, module or attribute under test, does not exist yet: go to Green."
  The second bullet names import and syntax errors "in the test".
- Red, step 2: add one sentence: check the narrowed command against
  Destructive actions as `warrant-verify` step 2 says. A pointer, so the rule
  stays in `warrant-verify`.
- Finish: replace "add one and run red and green as in step 2" with: apply the
  mutation, run the tests, revert it; for a mutation no test fails on, write a
  test, run it on the mutated code (red), revert, run it again (green). End
  with: the code has no mutation left.

### warrant-verify

- Step 1, no contract: "Run no test, lint, type-check or build command, not
  even a narrowed or diagnostic one." This closes the diagnostic run that step 3
  allows; the delta of "Development runs allowed" limits that requirement to a
  project with a contract. This narrows the archived
  `clarify-evidence-and-trace` decision that a narrowed or diagnostic run is
  allowed while working; "No guessed commands" already forbade those commands
  without a contract.
- Step 2: compare "every command you run in this project, including narrowed
  and diagnostic runs" with Destructive actions.
- Step 3: "If you change a file the commands read (code, tests, configuration)
  after a run, run the commands again. Recording results in OpenSpec artifacts
  or in your report is not such a change." The undefined "files under
  verification" goes.

### rules.yaml

- tasks: new rule "For each requirement, add a task that names the requirement
  and writes its tests." Placed before the Review/Verification rule so the
  rendered list reads in task-list order.
- design: "record the first option that fully works in this order: no change,
  existing project code, the standard library or platform, an installed
  dependency, new code". The pointer to `warrant-minimal-change` goes.
- apply: append to the REVISE rule: "If a blocking finding needs a decision
  only the requester can make, ask the requester and stop before the first
  task."
- Both config copies get the same lines.

### warrant-review

- Artifact mode: "a requirement that no task names" replaces "a requirement
  for which `tasks.md` has no test task". Naming is what the reviewer can check
  from text alone.
- Receive mode, step 1: "Choose the OpenSpec change as in Review mode step 2."
  One clause instead of repeating the four cases keeps the file under 150
  lines.

### warrant-setup

- Step 2: `openspec init --tools agents` without `--profile`. This replaces the
  `setup-installs-openspec` assumption "`--profile core`, because `--profile
  custom` installs no skill for a user whose global configuration selects no
  workflow": `--profile core` also overrides a global `custom` profile that
  selects `verify`, which the README's install steps create. Checked with
  OpenSpec 1.16 in a scratch repository: with no global configuration, init
  without `--profile` installs the core skills; with `custom` and no workflow,
  it installs none. In that case `openspec-verify-change` is missing, and the
  note of step 3 already names `openspec config profile`, then
  `openspec update`.
- Step 4: the first path is "`rules.yaml` in the directory of this `SKILL.md`";
  the `.agents` paths follow as fallbacks. This replaces part of Decision 2 of
  the archived `add-warrant-core` design ("Both paths are fixed by the `skills`
  CLI, not by the agent"): an install for one agent only, such as
  `npx skills add ... -a claude-code`, may create no `.agents/` directory, and
  the agent that loaded the skill knows where its `SKILL.md` lies. The
  `.agents` paths stay for an agent that does not.

### warrant-minimal-change

- Ledger: `-- ':(exclude,glob).*/skills/**'`, which skips the installed skills
  under `.agents/`, `.claude/` and any other agent directory without naming an
  agent (`test_skill_is_agent_neutral`). Checked in a scratch repository:
  hits under `.agents/skills/`, `.claude/skills/` and `.codex/skills/` are
  left out, `app/` and `.github/` stay.

### Tests

Each requirement gets a phrase test in `test_kit.py`, in the style of the
existing ones, with a `# <capability>: <requirement>` comment. The phrase tests
fail on the current text (red) and pass after the edit (green). Behavior is
checked by the eval scenarios.

## Risks / Trade-offs

- [A wording change shifts behavior a scenario checks] → All 25 scenarios run
  on both agents; a failure is judged from the transcript before any further
  wording change.
- [Projects already set up keep the old rules] → `warrant-setup` replaces the
  `[warrant]` entries when run again; the proposal's Impact says so.
- [Phrase tests pin wording] → Accepted, as with the existing kit tests; they
  catch a lost instruction, and the scenarios catch lost behavior.
