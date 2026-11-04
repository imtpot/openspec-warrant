# Design

## Decisions

### 1. Two requests in one session

A first run asked to plan and implement in one request. `openspec-propose`
in OpenSpec 1.16 forbids implementation in the same response ("even if the
initial request asks for it"), so agents that followed OpenSpec closely
stopped after planning: warrant on Sonnet in two of three runs, plain OpenSpec
in one. A `[warrant]` rule that unconfirmed assumptions do not block
requested work did not change this and was dropped: warrant does not override
OpenSpec's planning boundary (principle 1). The task now sends the plan
request and, in the same session, an implement request, as a person would.
The second request also gives implementation a context already filled by
planning, which a later sub-agent comparison needs.

### 2. One run loop for all tasks

The benchmark runs every task through one loop that sends each prompt in
turn, so single-prompt tasks are the one-step case. Tokens are summed over the
steps; the report is the text of all steps.

### 3. Continuing a session

Claude Code continues the latest session in the workspace with `--continue`.
`codex exec resume --last` has no `-s` flag, so the sandbox mode moves to
`-c sandbox_mode="workspace-write"`.
