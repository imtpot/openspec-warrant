# Tasks

Files this change reaches: `skills/warrant-setup/SKILL.md`,
`skills/warrant-setup/rules.yaml`, `openspec/config.yaml`,
`evals/fixtures/warrant-project/openspec/config.yaml`,
`skills/warrant-minimal-change/SKILL.md`, `skills/warrant-tdd/SKILL.md`,
`skills/warrant-verify/SKILL.md`, `skills/warrant-review/SKILL.md`,
`evals/tests/test_kit.py`.

## 1. Meaning changes

- [x] 1.1 Write failing kit tests for the REVISE path and check-off after passing verification, then change the apply guidance in `rules.yaml` and its copies (specs: warrant-rules "Verify before checking off", "Path after REVISE"); verify the kit and dogfood tests pass
- [x] 1.2 Point `warrant-review` to the EARS rule, the protected list and line tracing in their sources (specs: code-review "EARS findings", "Removed protection"); verify the kit tests pass
- [x] 1.3 Add the empty Destructive actions form to `warrant-setup` and "continue" to `warrant-tdd` (specs: warrant-setup "No confirmed destructive actions", test-first "Scenarios without a change"); verify the kit tests pass

## 2. Wording

- [x] 2.1 Apply the audit's wording fixes to all five skills and `rules.yaml`; check each file with `ste-lint.py`; verify the kit tests pass

## 3. Review

- [x] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [x] 4.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 204 passed in 82.55s (0:01:22)
- [x] 4.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
- [x] 4.3 Run every eval scenario on `claude` and `codex`; record each result
  Result: exit 0, 24 of 24 on claude and codex after the EARS and empty-range fixes (first run: codex missed the EARS finding in a project without warrant rules, claude paraphrased "nothing to review", one claude timeout; all three pass on rerun)
- [x] 4.4 Run `implement-proration` and `plan-implement-allocation` in the warrant arm on Opus, three runs each; record the scores against the earlier results
  Result: exit 0, implement-proration faults 0.96 (before 0.96); plan-implement open points 1.00, acceptance 6 of 6, faults 1.00 (before the same)
