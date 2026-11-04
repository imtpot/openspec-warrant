# Tasks

Files this change reaches: `evals/warrant_evals/contract.py`,
`evals/tests/test_contract.py`, `evals/tests/test_setup_check.py`,
`evals/fixtures/*/AGENTS.md`, `evals/fixtures/artifacts-flawed/`,
`evals/fixtures/artifacts-sound/`, `evals/scenarios/artifact-review-flawed.toml`,
`skills/warrant-setup/SKILL.md`, `skills/warrant-review/SKILL.md`,
`README.md`, `AGENTS.md`, `docs/design.md`.

## 1. Contract parser

- [x] 1.1 Write failing tests, then let the parser accept three required subsections and ignore `### Decision records` (specs: project-contract "Contract section and headings", "Former Decision records subsection"); verify the contract tests pass

## 2. Skills

- [x] 2.1 Remove Decision records from the `warrant-setup` template and instructions (specs: warrant-setup "Create the contract skeleton"); verify the kit tests pass
- [x] 2.2 Take recorded decisions only from archived changes in `warrant-review` (specs: code-review "Contradicted decision"); verify the kit tests pass

## 3. Fixtures and documentation

- [x] 3.1 Remove the subsection from fixture contracts, move the JSON decision of the `artifacts-*` fixtures into an archived change and update the flawed scenario's expected finding; verify the scenario tests pass
- [x] 3.2 Update `README.md`, `AGENTS.md` and `docs/design.md`; verify the kit tests pass

## 4. Review

- [x] 4.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 5. Verification

- [x] 5.1 Run `uv run pytest` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, 144 passed, 5 skipped in 50.65s (dogfood tests skip in a worktree without installed skills)
- [x] 5.2 Run `openspec validate --all --strict` and record its result as `Result: exit <code>, <result line>`
  Result: exit 0, Totals: 10 passed, 0 failed (10 items)
- [x] 5.3 Run the setup and artifact-review scenarios on `claude`, `codex` and `copilot`; record each result
  Result: exit 0, 24 of 24 pass after the sound fixture listed its error decision; before that, Copilot rightly reported it as unlisted
