# openspec-warrant

Agent-neutral OpenSpec extension: rules for OpenSpec's `spec-driven` schema in
`skills/warrant-setup/rules.yaml` and the `warrant-*` skills in
`skills/<name>/SKILL.md`. The behavioral evals and the benchmark live in
`evals/`. Plan changes with OpenSpec in `openspec/`.

Skills are written from scratch. Upstream skill sets are inspiration only; do
not copy their text.

## Development setup

Installed skills are not tracked. Install them before working on a change:

```sh
npx skills add https://github.com/Fission-AI/OpenSpec/tree/v1.16.0/skills -a claude-code codex -y
npx skills add . -s warrant-setup warrant-minimal-change warrant-verify warrant-review warrant-tdd -a claude-code codex -y
npx skills add https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/productivity/writing-for-agents -a claude-code codex -y
npx skills add https://github.com/danyuchn/asd-ste100-skill/tree/a610dbdfb27366653798bcdd4cebe745c92e1ac5 -s asd-ste100 -a claude-code codex -y
```

Run the second command again after editing anything under `skills/`.

## Writing for agents

Text under `skills/` and this file are read by agents. Write and edit them with
`writing-for-agents`, then check the wording with `asd-ste100`. A wording change
is a behavior change: run the scenarios of every skill it touches.

## Warrant contract

### Verification

- tests: `uv run pytest`
- openspec: `openspec validate --all --strict`

### Destructive actions

- `git push`
- `gh release`

### Glossary

none
