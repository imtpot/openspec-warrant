# Tasks

Files this change reaches: `evals/tests/test_kit.py`, `skills/*/SKILL.md`
(description lines only), `docs/design.md`.

## 1. Kit tests

- [ ] 1.1 Write `evals/tests/test_kit.py` with one parametrized test per requirement of `warrant-kit` (agent-neutral text, size, description start, license, eval coverage, design map), each failure naming the skill and the reason; verify the description test fails for the skills whose description summarizes a workflow and the other tests pass

## 2. Descriptions

- [ ] 2.1 Rewrite each failing description to say only when to use the skill, starting with "Use when" or "Use before"; reinstall the skills with the `AGENTS.md` setup command; verify `test_kit.py` and `test_dogfood.py` pass

## 3. Review

- [ ] 3.1 Review the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies the specs do not require

## 4. Verification

- [ ] 4.1 Run `uv run pytest` and record its result
- [ ] 4.2 Run `openspec validate --all --strict` and record its result
- [ ] 4.3 Run `openspec schema validate warrant` and record its result
