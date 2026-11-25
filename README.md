# Autonomous Delegation v2

A protocol-oriented Skill for Claude Code. It changes the workflow, control flow, and information flow rather than re-teaching the model how to write code or tests. Main writes the task assignment and delegates to a background Supervisor; the Supervisor delegates to Executors, supervises, and independently verifies; Main only receives information worth knowing.

## Installation

### With the Skills CLI (recommended)

Install globally for Claude Code:

```bash
npx skills add unfallenwill/autonomous-delegation --agent claude-code --global
```

Or install at project level for every detected agent (Claude Code, Cursor, Codex, and others):

```bash
npx skills add unfallenwill/autonomous-delegation
```

Useful variants:

```bash
npx skills add unfallenwill/autonomous-delegation --list          # inspect the repo's skills first
npx skills add unfallenwill/autonomous-delegation --all           # every skill, every detected agent
npx skills list                                                  # verify what is installed
npx skills update                                                # pull later updates
```

The CLI symlinks (or copies, with `--copy`) the skill into each agent's skills directory — for Claude Code, `~/.claude/skills/` globally or `.claude/skills/` per project.

### Manual installation

Clone straight into the Claude Code skills directory:

```bash
git clone https://github.com/unfallenwill/autonomous-delegation.git ~/.claude/skills/autonomous-delegation
```

Or, from the release ZIP, extract the `autonomous-delegation/` directory into `~/.claude/skills/` (personal) or `.claude/skills/` (project). If an older version with the same name exists, back it up and move it away first to avoid stale documents.

```bash
mkdir -p ~/.claude/skills
unzip autonomous-delegation-v2.zip -d ~/.claude/skills/
```

### Requirements

Requires a Claude Code build whose Agent tool supports background (non-blocking) subagents, plus `SendMessage` for live reporting. Without them the skill degrades to handback or reports a blocker instead of silently changing the workflow.

Start a new session (or run `/skills` to confirm it is loaded). The skill is triggered manually by default; there is no `context: fork`, because the task assignment must be written by Main. It defaults to one Supervisor and one active Executor, with justified parallelism allowed.

## Usage

Pass the task as the argument. Main turns it into a frozen task contract, launches one background Supervisor, and returns the turn.

### 1. Hand off a whole feature

```
/autonomous-delegation Split session handling out of src/auth/login.ts, add unit tests for the new module, and keep the public API unchanged.
```

Main records the contract at revision 1, launches the Supervisor, and tells you it was launched. The Supervisor spawns an Executor, checks the result against the contract, and reports back only for a verified outcome, a blocker, or a decision outside its authority.

### 2. Delegate the task you have already discussed

```
/autonomous-delegation
```

With no argument, Main reuses the task specification from the current conversation instead of asking you to restate it. If the request is materially ambiguous, Main resolves only what would make delegation unsafe, then proceeds.

### 3. Keep working while it runs

```
/autonomous-delegation Audit the repo for unhandled promise rejections and fix them with tests.
```

Then simply continue the conversation. Main stays free for unrelated requests, the Supervisor manages and verifies the Executor, and you stay out of the loop until something needs you. You can also ask for status at any time; a status question is not an instruction to take over execution.

## Protocol layout

`SKILL.md` is the Main entry point. The role, control, communication, and lifecycle protocols under `references/` are normative documents; the Claude Code adapter is only responsible for mapping the protocols onto the actual runtime. The Supervisor loads the protocols itself from the absolute paths given in Main's launch prompt; Executors receive only the necessary task contract and execution instructions.

## Runtime limitations

Claude Code documentation supports nested and background execution and SendMessage, but the capabilities actually available vary by version, tool set, permissions, and mode. When no live message channel exists, fall back to handback; never claim that live reporting happened. When background or nested execution is unavailable, report the blocker instead of silently changing the workflow. A Skill is a prompting protocol, not an enforced state machine, so runtime compliance cannot be guaranteed. No additional permissions, hooks, or MCP servers are configured.

## Evaluation (for human/trace inspection, not auto-loaded)

Compare against a baseline without the Skill using the same specification, model, initial environment, acceptance method, and permissions. No degradation in quality is the gate; Main's release and protocol compliance are the primary metrics.

| Check | Pass criterion |
|---|---|
| Main's control flow | Ends the turn after confirming background launch; no routine task-advancing tool calls |
| Role boundaries | The Supervisor actually launches Executors; Main does not do the substantive work itself |
| Contract fidelity | The original specification is preserved; no unauthorized downgrade or expansion |
| Information routing | Executors report to the Supervisor; Main receives only necessary events |
| Response obligation | Informational reports do not trigger replies or extra management loops |
| Independent acceptance | Independent check evidence exists; unknown or failed is never labeled COMPLETED |
| Exception handling | Honest degradation when no channel exists; blocking, cancellation, and recovery do not duplicate active tasks |
| Cost and quality | Records total tokens, elapsed time, acceptance pass rate, Main tokens, Main's first-release latency, and intervention count |

Suggested smoke test: in a temporary directory, delegate a simple verifiable file-generation task and check the real invocation records of both agent layers; send an unrelated request to Main during execution; then simulate an unpassable acceptance check, a missing message channel, and a cancellation. Cross-check message sources, revisions, and states against the trace. Run tests only in approved directories.

This package has been statically checked for files, references, frontmatter, and ZIP integrity; it has not been tested end-to-end in a real Claude Code session. The default convergence threshold above (re-evaluate after two consecutive rounds without progress) is an adjustable design default, not an experimentally validated optimum.
