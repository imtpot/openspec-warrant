# openspec-warrant

Agent-neutral OpenSpec extension: the `warrant` schema and the `warrant-*`
skills. Skills live in `skills/<name>/SKILL.md`; the behavioral evals live in
`evals/`. Plan changes with OpenSpec in `openspec/`.

Skills are written from scratch. Upstream skill sets are inspiration only; do
not copy their text.

## Development setup

Installed skills are not tracked. Install them before working on a change:

```sh
npx skills add https://github.com/Fission-AI/OpenSpec/tree/v1.16.0/skills -a claude-code codex -y
npx skills add . -s warrant-setup warrant-minimal-change warrant-verify warrant-review warrant-tdd -a claude-code codex -y
```

Run the second command again after editing anything under `skills/`.

## Warrant contract

### Verification

- tests: `uv run pytest`
- openspec: `openspec validate --all --strict`

### Destructive actions

- `git push`
- `gh release`

### Glossary

none

### Decision records

none
