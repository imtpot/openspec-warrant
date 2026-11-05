## Context

See proposal.md - Why. The texts involved:

- `skills/warrant-verify/SKILL.md` step 3: "Run each command in the
  Verification list, exactly as written, after your last change".
- `skills/warrant-tdd/SKILL.md` step 2: "Run only this test. Narrow the
  contract's tests command ..."; step 3 Finish runs the full verification.
- `skills/warrant-minimal-change/SKILL.md` "Protected code" list and
  "Trace lines to requirements" section.
- `skills/warrant-review/SKILL.md` step 3 traces lines "as
  `warrant-minimal-change` describes under "Trace lines to requirements"" and
  reports "a line that serves no requirement" as untraced.
- `evals/warrant_evals/checks.py` `review_check` only checks that expected
  terms appear per axis section; it cannot fail on a term that must not be
  reported.

## Goals / Non-Goals

**Goals:** an agent that follows all four skills meets no contradiction about
narrowed runs or protected lines; the review eval catches a protected line
reported as untraced.

**Non-Goals:** see proposal.md - Out of scope.

## Decisions

### Development runs in warrant-verify

Option ladder: (1) no change keeps the conflict. (2) Existing text: step 3
already defines evidence; add two sentences there, before "For each command,
record": a narrowed or diagnostic run is allowed while working; only the
Verification commands, exactly as written after the last change, are evidence.
The description (trigger) stays, so the skill still loads before the first
test run and the contract is read before any command.

### Narrowed runs in warrant-tdd

Option ladder: (1) no change leaves the TDD side silent. (2) Add one sentence
to step 2 item 2: the narrowed run shows this scenario only and is not
evidence that the work is complete. Step 3 Finish stays.

### Trace bases in warrant-minimal-change

This replaces part of Decision 2 of the archived `add-warrant-review` design
("for each added line in the diff, name the requirement it serves"), which
`narrow-warrant-review` Decision 2 kept. A line may now name a Protected code
item or a declared standard instead of a requirement, because the same skills
already require those lines (`warrant-minimal-change` "Protected code",
`warrant-review` Standards axis). The untraced check stays the skill's own step.

Option ladder: (1) no change keeps the conflict. (2) Rewrite the trace
section in place and rename it "Trace every line", since it no longer traces
only to requirements. The section lists the three bases with the label format
from proposal.md - Assumptions, keeps "Imports, test code and formatting count
for the line they support", and keeps the stop-and-report path for a needed
line with no basis. "Anything the requester asked for" is not a basis (see
Assumptions), and the section says so. The intro sentence ("each added or
changed line exists because the task or a requirement needs it") names the
three bases too. In "Before you write code" item 2, "Only the specs define what is
required" changes as proposal.md - Assumptions says, so the two sections agree.

### Untraced in warrant-review

Option ladder: (1) no change keeps reporting protected lines as untraced.
(2) Change step 3: the section name in the reference becomes "Trace every
line", "A line that serves no requirement" becomes "A line with none of these
bases", and one sentence tells the Spec-axis context to read the Protected code
list of `warrant-minimal-change` and the files under `### Standards` to check a
`protected:` or `standard:` basis. Step 2 already gives each axis context "only
its own step"; that step now names those inputs, so the Spec axis reads the
Standards files only to check a basis, not to report rule breaks.

### Review eval for a protected line

Option ladder: (1) no change: `review-branch` has no protected line, so the
eval cannot see the new behavior. (2) Existing project code:
`setup-common.sh` already builds variants from `VARIANT`; `review_check`
already splits the report into sections. Take this option:

- `setup-common.sh`: split the quoted `app/cli.py` heredoc after
  `args = parser.parse_args(argv)`; for `VARIANT=protected` only, write
  `    if args.free < 0:` and `        parser.error('free must not be negative')`
  between the two parts. New `setup-protected.sh` sets the variant like
  `setup-feature.sh`.
- `review_check`: a new optional param `untraced_absent`, a list of terms. The
  report is split into sections when any axis param or `untraced_absent` is
  set. For each term, the check fails when a line of the Spec section contains
  "untraced", "blocking" (any case) and the term; requiring "blocking" keeps a
  summary line such as "Untraced: none (`if args.free < 0` is protected)" from
  failing. Lines, not sentences, because review
  findings are one per line.
- `evals/scenarios/review-protected.toml`: the `review-branch` fixture,
  `setup-protected.sh`, the same prompt as `review-branch`, `spec = [["--json",
  "JSON option"]]` so the scenario still finds the unrequested option as
  untraced, and `untraced_absent = ["free < 0", "parser.error"]`. The other
  `review-branch` params are left out: their terms ("negative", "args.free")
  could now match text about the new check, and `review-branch` keeps covering
  them.

## Risks / Trade-offs

- [An agent labels a speculative line `protected:` to keep it] → The review's
  Standards axis still reports speculative generality, and the label names a
  concrete list item that a reviewer can check.
- [The `untraced_absent` check misses a finding that names the check without
  the word "untraced", spans two lines or writes `args.free<0`; it fails an
  honest line such as "`free < 0` is not untraced"] → Accepted: the skill's
  finding text is "untraced" with file and line, and a false failure shows in
  the transcript.
- [An agent traces the new check to the fixture's "Negative input"
  requirement, which is about `needed`] → The scenario still passes, as the
  check is not untraced; the eval does not check which basis is named.
- [Wording changes shift behavior in other scenarios] → Run every scenario of
  the four skills on Claude. Codex is not checked in this change (proposal.md -
  Out of scope).
