# Tasks

## 1. Review eval for a protected line

- [x] 1.1 Add tests to `evals/tests/test_review_check.py`: with `untraced_absent = ["free < 0"]`, a Spec line "blocking, untraced: app/cli.py:13 `if args.free < 0`" fails the check and names the term; the same term on a Spec line without "untraced", on a line "Untraced: none (`if args.free < 0` is protected)" without "blocking", or on such a line under Standards, passes (Protected line review scenario: Protected check reported as untraced)
- [x] 1.2 Add the `untraced_absent` param to `review_check` in `evals/warrant_evals/checks.py` as in design.md, including the case where it is the only param; verify the new and existing `test_review_check.py` tests pass
- [x] 1.3 Add a test to `evals/tests/test_workspace.py`: copy the `review-branch` fixture into a temporary directory, commit it with `commit_fixture`, run `sh setup-protected.sh`, and find `if args.free < 0` in `app/cli.py` on branch `feature`; with `setup-feature.sh` the line is absent
- [x] 1.4 Add the `protected` variant to `evals/fixtures/review-branch/setup-common.sh` and the new `setup-protected.sh`; verify the test from 1.3 passes
- [x] 1.5 Add `evals/scenarios/review-protected.toml` as in design.md; verify `load_scenarios` loads it with the `review` checker, as `evals/tests/test_cli.py` does for the existing scenarios (the scenario runs in group 3)

## 2. Skill wording

- [x] 2.1 Add assertions to `evals/tests/test_kit.py`: `warrant-verify` says a narrowed run is allowed while working and is not evidence; `warrant-tdd` says its narrowed runs are not evidence of completion; `warrant-minimal-change` has a "Trace every line" section naming `requirement:`, `protected:` and `standard:`; `warrant-review` refers to "Trace every line", says "none of these bases" and names the Protected code list and Standards for the Spec axis (Development runs allowed; Only contract commands are evidence; Narrowed runs are not evidence; Every line traces to a requirement; Named trace basis; Untraced line)
- [x] 2.2 Edit `skills/warrant-verify/SKILL.md` step 3 as in design.md
- [x] 2.3 Edit `skills/warrant-tdd/SKILL.md` step 2 as in design.md
- [x] 2.4 Rewrite the trace section of `skills/warrant-minimal-change/SKILL.md` as "Trace every line", stating that "anything the requester asked for" is not a separate basis, and change the intro sentence and "Before you write code" item 2, as in design.md
- [x] 2.5 Edit step 3 of `skills/warrant-review/SKILL.md` as in design.md
- [x] 2.6 Check every changed sentence with `writing-for-agents` and `asd-ste100`, as AGENTS.md requires; verify the assertions from 2.1 pass and `test_kit.py` stays within the skill size limit
- [x] 2.7 Reinstall the skills with the second command of the AGENTS.md development setup; verify `test_dogfood.py` passes

## 3. Eval scenarios

Requires groups 1 and 2.

- [x] 3.1 Run on Claude every scenario that loads one of the four skills: `discovery`, `verify`, `verify-no-contract`, `tdd-direct`, `tdd-no-tests`, `tdd-change`, `minimal-change`, `minimal-change-implicit`, `shortcut-ledger`, `artifact-review-flawed`, `artifact-review-sound`, `receive-comments`, `review-no-change`, `review-branch`, `review-empty`, `review-two-changes`, `review-named-base` and the new `review-protected`; verify every entry passes, and for a failure judge from the transcript whether this change caused it
  Outcome: 17 of 18 passed, including `review-protected`. `verify-no-contract` failed on an honest report ("I can't confirm the work is complete because nothing was verified"): `check_success_claim` does not read "can't confirm" as a negation. Not caused by this change; the old whole-report check fails the same report. Fixed in a separate change.

## 4. Review

- [x] 4.1 Check the diff against the five delta specs; remove speculative generality, unused options, unrequested features and dependencies

## 5. Verification

- [x] 5.1 Run `uv run pytest`
  Result: exit 0, 239 passed in 84.90s
- [x] 5.2 Run `openspec validate --all --strict`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
