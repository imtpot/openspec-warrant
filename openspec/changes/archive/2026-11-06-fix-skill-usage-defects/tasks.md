# Tasks

## 1. warrant-tdd

- [x] 1.1 Fail for the expected reason: add a phrase test to `evals/tests/test_kit.py` that the Red step sends a missing function, module or attribute under test to Green; see it fail, then edit `skills/warrant-tdd/SKILL.md` Red step 3 and see it pass
- [x] 1.2 Mutation check: add a phrase test that the Finish step applies, runs and reverts each mutation and shows red on the mutated code and green after the revert; see it fail, then edit the Finish step and see it pass
- [x] 1.3 Destructive verification (narrowed run): add a phrase test that Red step 2 points to the Destructive actions check of `warrant-verify`; see it fail, then add the sentence and see it pass

## 2. warrant-verify

- [x] 2.1 Fresh evidence only: add a phrase test that step 3 names the files the commands read and excludes recording results in OpenSpec artifacts; see it fail, then edit `skills/warrant-verify/SKILL.md` step 3 and see it pass
- [x] 2.2 Destructive verification: add a phrase test that step 2 covers every command including narrowed and diagnostic runs; see it fail, then edit step 2 and see it pass
- [x] 2.3 Development runs allowed, No guessed commands (project-contract): add a phrase test that step 1 forbids narrowed and diagnostic runs without a contract; see it fail, then edit step 1 and see it pass

## 3. Rules

- [x] 3.1 Test task per requirement: add a test that the tasks rules contain a rule asking for a task that names each requirement; see it fail, then add the rule to `skills/warrant-setup/rules.yaml` and see it pass
- [x] 3.2 Option ladder in the design: add a test that the design rule lists no change, existing project code, standard library or platform, installed dependency and new code in this order; see it fail, then edit the rule and see it pass
- [x] 3.3 Path after REVISE: extend `test_apply_guidance_gives_a_path_after_revise` to require asking the requester and stopping; see it fail, then edit the rule and see it pass
- [x] 3.4 Copy the `[warrant]` lines of `rules.yaml` into `openspec/config.yaml` and `evals/fixtures/warrant-project/openspec/config.yaml`; see `evals/tests/test_dogfood.py` pass

## 4. warrant-review

- [x] 4.1 Missing tasks: add a phrase test that Artifact mode blocks "a requirement that no task names"; see it fail, then edit `skills/warrant-review/SKILL.md` and see it pass
- [x] 4.2 Change selection: add a phrase test that Receive mode step 1 chooses the change as in Review mode step 2; see it fail, then edit step 1 and see it pass; check the file stays at or under 150 lines

## 5. warrant-setup and warrant-minimal-change

- [x] 5.1 No OpenSpec root: add a test that `skills/warrant-setup/SKILL.md` names `openspec init --tools agents` and has no `--profile`; see it fail, then edit step 2 and see it pass
- [x] 5.2 Install the rules: add a phrase test that step 4 looks first in the directory of the loaded `SKILL.md`; see it fail, then edit step 4 and see it pass; check the file stays at or under 150 lines
- [x] 5.3 Debt ledger (minimal-change): add a test that the ledger command excludes `.agents` and `.claude`; see it fail, then edit `skills/warrant-minimal-change/SKILL.md` and see it pass

## 6. Wording and evals

- [x] 6.1 Check every changed sentence in `skills/` with `writing-for-agents` and `asd-ste100`; rerun `uv run pytest evals/tests/test_kit.py` after any rewording
- [x] 6.2 Reinstall the skills with `npx skills add . -s warrant-setup warrant-minimal-change warrant-verify warrant-review warrant-tdd -a claude-code codex -y`
- [x] 6.3 Run `uv run python -m warrant_evals --agent claude --agent codex` from `evals/`; report each failing entry with the cause from its transcript
  Codex: 25 of 25 pass. Claude: 24 of 25 pass; `review-protected` fails with "Spec section reports untraced: free < 0", but the report excludes lines 13-14 ("The `free < 0` check at lines 13–14 counts as input validation") and the checker matched that sentence by substring. A checker defect, outside this change.

## 7. Review

- [x] 7.1 Check the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies

## 8. Verification

- [x] 8.1 Run `uv run pytest`
  Result: exit 0, 322 passed in 118.15s (0:01:58)
- [x] 8.2 Run `openspec validate --all --strict`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
