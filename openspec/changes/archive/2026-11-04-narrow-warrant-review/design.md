# Design

## Context

See proposal.md. Eval workspaces get only the warrant skills today, installed
from this repository with `skills add <repo>`.

## Decisions

### 1. OpenSpec skills cached per version

Option ladder: the `skills` CLI already installs from a local directory, so the
runner clones `Fission-AI/OpenSpec` at tag `v<openspec --version>` once into
`~/.cache/warrant-evals/openspec-<version>/` and installs from
`<cache>/skills` in every workspace. Rejected: `skills add` with the GitHub URL
per workspace, which clones the repository once per scenario and agent.

### 2. Review skill wording

The Spec axis step says "run the openspec-verify-change workflow for the
change" by skill name, the way warrant skills already refer to each other. The
untraced-line check stays the skill's own step.

### 3. Fixture bug in connected code

`setup-common.sh` writes `app/cli.py` calling `check(args.needed, args.free)`
while `check` takes `(free, needed)`. The checker looks for `cli.py` and one of
"swap", "order" or "reversed" in the Standards section.

## Risks / Trade-offs

- [The cache goes stale if a tag is moved] → Tags are not moved in
  Fission-AI/OpenSpec; deleting the cache directory refreshes it.
