# Tasks

Files this change reaches: `skills/warrant-review/SKILL.md`,
`evals/warrant_evals/workspace.py`, `evals/warrant_evals/__main__.py`,
`evals/tests/test_workspace.py`, `evals/fixtures/review-branch/setup-common.sh`,
`evals/scenarios/review-branch.toml`, `evals/scenarios/review-named-base.toml`,
`docs/design.md`, `README.md`.

## 1. Workspaces with OpenSpec skills

- [ ] 1.1 Write a failing test: preparing a workspace with an extra skills source installs its skills next to the source's (specs: behavioral-evals "OpenSpec skills in workspaces"); then add the cached OpenSpec clone and the extra source to `prepare_workspace` and `__main__`; verify the test passes and a real prepared workspace contains `.agents/skills/openspec-verify-change/SKILL.md`

## 2. Review skill

- [ ] 2.1 Rewrite the review mode of `skills/warrant-review/SKILL.md`: Spec axis from openspec-verify-change plus untraced lines, verify-change missing, connected code on the Standards axis, axes in separate contexts with the fallback sentence (specs: code-review); verify the kit tests pass and the skill stays under 150 lines

## 3. Review evals

- [ ] 3.1 Add the swapped call to `setup-common.sh` and the connected-code term to the review scenarios' Standards expectations (specs: behavioral-evals "Connected-code check"); verify the checker unit tests still pass and the five review scenarios pass with `--agent claude`

## 4. Documentation

- [ ] 4.1 Update the `warrant-review` rows in `docs/design.md` and the README description; verify the kit design test passes

## 5. Review

- [ ] 5.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 6. Verification

- [ ] 6.1 Run `uv run pytest` and record its result
- [ ] 6.2 Run `openspec validate --all --strict` and record its result
- [ ] 6.3 Run the review and receive scenarios on `claude`, `codex` and `copilot`; record each result and update the README agent table
