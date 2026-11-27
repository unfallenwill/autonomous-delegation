# Autonomous Delegation

A Claude Code Skill that hands a task to a background Supervisor and keeps your main conversation free.

Autonomous Delegation changes who owns a task, not the standard of the work. You state the outcome once; Main freezes it as a revisioned contract, launches exactly one background Supervisor, and returns your turn. The Supervisor runs the management loop with Executor agents, verifies each acceptance criterion against the real deliverable, and keeps you posted as the work proceeds: progress, the decisions behind it, and the problems that come up.

**Status:** revised for progress reporting. Statically checked for files, references, frontmatter, and ZIP integrity. Runtime capabilities and message routing were probed in a live Claude Code session, and the full flow was run end-to-end twice on small smoke-test tasks. The second, which used an earlier wording of the Supervisor's reports, confirmed that Executors report to the Supervisor live; the final wording has not been run end-to-end. See [Evaluation](#evaluation).

## Start in under a minute

Install globally for Claude Code:

```bash
npx skills add unfallenwill/autonomous-delegation --agent claude-code --global
```

Start a new Claude Code session, then hand off a task:

```
/autonomous-delegation Split session handling out of src/auth/login.ts, add unit tests for the new module, and keep the public API unchanged.
```

Main records the contract, launches the Supervisor, tells you it was launched, and ends the turn. Keep working while the Supervisor manages and verifies the task.

## Contents

- [Start in under a minute](#start-in-under-a-minute)
- [Why use it](#why-use-it)
- [Installation](#installation)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Skill metadata and repository layout](#skill-metadata-and-repository-layout)
- [Requirements](#requirements)
- [Compatibility and limitations](#compatibility-and-limitations)
- [Evaluation](#evaluation)
- [Contributing](#contributing)
- [License](#license)

## Why use it

Long-running work in a single conversation competes with everything else you want to do. This skill separates ownership from execution:

- **One Supervisor per task.** Main delegates once and does not run the task, review it, or supervise it afterwards.
- **A Supervisor that judges, not one that forwards.** Executors report to the Supervisor only. What reaches Main is the Supervisor's own report: independent checks, decisions about correction, and the Executor decisions and problems worth knowing.
- **Executors do the work.** A single active writer by default; additional agents only for independent work or verification with disjoint write boundaries.
- **Independent acceptance.** The Supervisor checks each mandatory criterion itself. An agent exit, a test summary, or a completion notification is not acceptance.
- **Reporting you can follow.** Executors report to the Supervisor at each checkpoint. The Supervisor keeps you posted with what it checked and decided and with the Executor decisions and problems worth knowing. Reports are event-driven by default, not timed heartbeats or raw transcripts.
- **Honest degradation.** If the runtime lacks background agents or a live message channel, the skill falls back to handback or reports a blocker. It never pretends a live report was delivered.

## Installation

### With the Skills CLI (recommended)

The Skills CLI requires Node.js 22.20 or later.

Install globally for Claude Code:

```bash
npx skills add unfallenwill/autonomous-delegation --agent claude-code --global
```

Install at project scope and choose agents as prompted:

```bash
npx skills add unfallenwill/autonomous-delegation
```

Useful variants:

```bash
npx skills add unfallenwill/autonomous-delegation --list    # list the repo's skills without installing
npx skills add unfallenwill/autonomous-delegation --all     # all skills, all agents, no prompts
npx skills list                                             # list installed project skills
npx skills list --global                                    # list global installs
npx skills update                                           # update installed skills
npx skills update --global                                  # update global installs
```

The CLI symlinks the skill into each selected agent directory by default; `--copy` copies the files instead. For Claude Code the targets are `.claude/skills/` at project scope and `~/.claude/skills/` at global scope.

### Manual installation

Clone directly into the Claude Code skills directory:

```bash
git clone https://github.com/unfallenwill/autonomous-delegation.git ~/.claude/skills/autonomous-delegation
```

Or install from the repository source archive into `~/.claude/skills/` (personal) or `.claude/skills/` (project). The archive extracts to `autonomous-delegation-main/`; rename it to `autonomous-delegation/`:

```bash
mkdir -p ~/.claude/skills
curl -L https://github.com/unfallenwill/autonomous-delegation/archive/refs/heads/main.zip -o autonomous-delegation-main.zip
unzip autonomous-delegation-main.zip
mv autonomous-delegation-main ~/.claude/skills/autonomous-delegation
```

If an older install with the same name exists, move it aside first so stale protocol documents are not loaded.

### Confirm the skill loaded

Claude Code picks up skill changes automatically within the current session, except in bare mode. Add or edit the skill under `~/.claude/skills/`, the project `.claude/skills/`, or a `.claude/skills/` inside an `--add-dir` directory, then open `/skills` to confirm `autonomous-delegation` is listed. If a new skill does not appear, run `/reload-skills`.

The skill sets `disable-model-invocation: true`, so Claude does not invoke it on its own. Invoke it explicitly with `/autonomous-delegation`.

## Usage

Pass the task as the argument. Main turns it into a frozen task contract, launches one background Supervisor, and returns the turn.

### 1. Hand off a whole feature

```
/autonomous-delegation Split session handling out of src/auth/login.ts, add unit tests for the new module, and keep the public API unchanged.
```

Main records the contract at revision 1, launches the Supervisor, and tells you it was launched. The Supervisor tells you when it takes over, spawns an Executor, reports as the work proceeds, checks the result against the contract, and reports the verified outcome, a blocker, or a decision outside its authority.

### 2. Delegate the task you have already discussed

```
/autonomous-delegation
```

With no argument, Main reuses the task specification from the current conversation instead of asking you to restate it. If the request is materially ambiguous, Main resolves only what would make delegation unsafe, then proceeds.

### 3. Keep working while it runs

```
/autonomous-delegation Audit the repo for unhandled promise rejections and fix them with tests.
```

Then continue the conversation. Main stays free for unrelated requests and passes on the progress reports: what changed, what was decided and why, and what problems came up. You are asked only for decisions outside the delegated authority.

You can ask for status at any time. A status question is not an instruction to take over execution. To see which agents are running or to stop one, use `/tasks`.

### 4. Say what you want to hear about

```
/autonomous-delegation Migrate the payment service to the new client library and keep the tests green. Report at each module.
```

Anything you say about reporting is carried into the task contract: it sets the Executor checkpoints and the points at which the Supervisor reports to you. Executors report at those points and whenever they make a notable decision or hit a problem; the Supervisor reports after each verification round. Decision requests, blockers and the final report are always sent.

## How it works

![Overview: Main writes the task contract, launches one background Supervisor and sends it its agent ID, then stays out of the work and asks you only for decisions it is not allowed to make. The Supervisor orders the Executor, receives its progress, decisions and problems, checks each acceptance criterion itself, and reports its judgment to Main.](assets/architecture-overview.svg)

<details>
<summary>Full diagram: the verification loop, lifecycle states and the handback</summary>

![Control and information flow: the user states intent to Main; Main freezes a revisioned task contract and launches exactly one background Supervisor, sends it its own agent ID, then stops routine execution, review, and supervision; the Supervisor issues execution orders to one active-writer Executor, independently verifies each mandatory acceptance criterion in the VERIFYING state, and resumes the same Executor on failure; Executors report progress, decisions and problems to the Supervisor only, and the Supervisor reports its own checks and decisions plus the Executor news worth knowing to Main; the Supervisor's final report reaches Main as its handback.](assets/architecture.svg)

</details>

### Roles

| Role | Owns | Must not |
|---|---|---|
| **Main** | User intent, the task contract, delegation, decisions beyond delegated authority, user-facing communication | Perform routine execution, review, or supervision after launch |
| **Supervisor** | End-to-end task management, Executor selection, interventions, independent acceptance, reporting | Redefine the contract, do the primary implementation, return routine management to Main |
| **Executor** | Implementation within scope, progress updates, self-checks, deliverables and evidence | Change the contract, claim overall acceptance, report to Main or ask it for decisions |

Main authors the contract and freezes it at revision 1; only Main can issue an amendment that increments the revision. The Supervisor may clarify execution details and derive verification checks but may not weaken requirements, expand scope, or grant permissions.

### Verification loop

1. Main launches exactly one background Supervisor with a complete TASK_ASSIGNMENT and the absolute paths to the protocol files, then sends it its own agent ID.
2. The Supervisor takes ownership, launches an Executor with an EXECUTION_ORDER, and works from the Executor's results.
3. In the VERIFYING state, the Supervisor checks each mandatory acceptance criterion against the actual deliverable, using tools or a separate verifier rather than the Executor's assertion.
4. On failure, the Supervisor resumes the same Executor with the concrete failed checks, then rechecks. After two consecutive correction rounds with no measurable improvement, it reassesses and stops as BLOCKED or FAILED if no credible new approach exists.
5. Only independently verified criteria yield COMPLETED. Unknown is not pass. Silence is not evidence of completion, failure, or cancellation.

### Progress reporting

1. Executors report to the Supervisor at the checkpoints named in their execution order and whenever they make a notable decision or hit a problem. Each update covers what changed, what was decided and why, and what went wrong and what was done about it.
2. Executors do not report to Main. Main hears from the Supervisor, as a report from a manager rather than a relay: the Executor decisions and problems worth knowing, what the Supervisor checked and found, the decisions it made about correcting, resuming or replacing an Executor, and what remains.
3. The Supervisor reports when it takes over, when an Executor update raises something you should know (a risk, a decision that affects scope or the deliverable, a problem that changes the plan), after each Executor return, after each intervention, after each management decision, at each point you named and at each state change.
4. Main passes these reports on to you in a few sentences.

The one exception is an Executor that cannot reach its Supervisor. It then sends to Main instead and says so, and the message is informational only.

By default reports are tied to events rather than to time, and each report to Main starts a Main turn. That is why Executors report to the Supervisor and only the Supervisor's reports reach Main.

### Lifecycle states

Supervisor-owned states:

| State | Meaning |
|---|---|
| `DISPATCHED` | Supervisor launch confirmed; ownership not yet confirmed |
| `RUNNING` | Supervisor accepted; execution or local correction proceeding |
| `VERIFYING` | Supervisor is independently checking the deliverable |
| `WAITING_DECISION` | A specific decision is pending; unaffected work may continue |
| `BLOCKED` | No viable authorized progress now; checkpoint and prerequisite recorded; resumable |
| `CANCELLING` | Stop requested but child shutdown not yet confirmed |
| `COMPLETED` | All mandatory acceptance criteria independently verified; terminal |
| `FAILED` | No viable path under the current contract or resource bounds; terminal for this run |
| `CANCELLED` | Relevant child execution confirmed stopped; terminal for this run |
| `UNKNOWN` | Observability lost or runtime state unclear; reconcile before acting |

Runtime task status reflects execution, not contract acceptance. A completion notification, an agent exit, or a passing test run alone does not make a task COMPLETED.

### Handback

The final or blocked report reaches Main as the Supervisor's handback. If SendMessage or an equivalent live channel is unavailable, everything due to Main travels in it, and intermediate progress and decision requests may be delayed until then. Undelivered critical information is recorded as undelivered and is never claimed as delivered. An Executor also writes its result to an agreed location, so a report that the runtime drops can still be read. If a running child cannot be safely stopped or reconciled, the correct report is UNKNOWN, not a clean handback.

## Skill metadata and repository layout

`SKILL.md` is the Main entry point; the Markdown files under `references/` are normative, and the Claude Code adapter maps their intent onto the actual runtime. The Supervisor loads all protocols itself from the absolute paths in Main's launch prompt; Executors receive only the task contract and execution instructions.

| Frontmatter field | Value | Effect |
|---|---|---|
| `name` | `autonomous-delegation` | Command name: `/autonomous-delegation` |
| `description` | Summarizes delegation and when to use it | Human- and tool-facing metadata |
| `disable-model-invocation` | `true` | Manual invocation only; Claude does not auto-load the skill |
| `argument-hint` | `[task or current conversation objective]` | Autocomplete hint for the task argument |

The task text arrives as `$ARGUMENTS`. There is deliberately no `context: fork`: Main must write the task assignment in its own conversation, so the skill cannot run in a forked context.

```
autonomous-delegation/
├── SKILL.md              # Main entry point: dispatch and event handling
├── references/           # Normative protocols
│   ├── role-protocol.md
│   ├── control-protocol.md
│   ├── communication-protocol.md
│   ├── lifecycle-protocol.md
│   └── claude-code.md    # Runtime adapter
├── assets/
│   ├── architecture-overview.svg
│   └── architecture.svg
├── README.md             # Human documentation (this file)
└── LICENSE
```

`README.md` is for humans deciding whether and how to install the skill. `SKILL.md` is what Claude loads when the skill is invoked; it stays short and points at the protocol files.

## Requirements

- **Claude Code** with the Agent tool, able to launch **background (non-blocking) subagents**.
- **Subagent nesting** deep enough for Main → Supervisor → Executor (at least two layers below Main).
- **SendMessage** (or an equivalent live channel) for progress and decisions during a run. Without it, the skill uses handback.
- No additional permissions, hooks, MCP servers, or settings changes are required or made by this skill.

If background or nested execution is unavailable, the skill reports a blocker instead of silently changing the workflow. If the live channel is unavailable, it falls back to handback. Capabilities vary by Claude Code version, tool set, permissions, and mode, so verify the tools actually exposed in the current session rather than inferring them from a version number.

## Compatibility and limitations

- **Claude Code first.** The only adapter in this repository targets Claude Code. The Skills CLI can install the skill for other agents, but the control protocol depends on background subagents and agent messaging, so compatibility beyond Claude Code is not claimed.
- **A prompting protocol, not an enforced state machine.** Claude Code does not enforce these roles, transitions, or message types; runtime compliance cannot be guaranteed.
- **Manual by design.** `disable-model-invocation: true` keeps the skill out of automatic selection. `context: fork` is intentionally not used.
- **Runtime interrupts still apply.** Tool or permission prompts can interrupt Main; the protocol cannot suppress them.
- **Reports interrupt Main too.** Each report to Main starts a Main turn that relays it to you. That is why reports are tied to events rather than to time by default. If you want fewer, or timed instead, say so in the task; the contract then sets the reporting points, and decision requests, blockers and the final report are always sent. In the first smoke test, which used an earlier routing in which Executors also messaged Main, a task that took under a minute of real work produced six reports to Main over about ten minutes. In the second, with Executors reporting only to the Supervisor, five reports reached Main over about eighteen minutes.
- **The runtime can lose a child's report, and agents cannot always wait.** In the Claude Code build tested, a named Supervisor waiting on a nested call never received the Executor's final report, and a named Executor reports to Main instead of handing its report back. The skill therefore launches the Supervisor and its Executors unnamed, has Executors write results to an agreed location, and treats a missing report as unknown, never as completion. A Supervisor cannot idle while an Executor runs: it keeps working in bounded steps until the result arrives. An unnamed Supervisor is not told its own address, so Main sends it its agent ID right after launch, and Executors report to the Supervisor through that ID.
- **Cancellation is not rollback.** A cancelled run reports residual changes and does not erase them without authorization.
- **Frontmatter portability.** `argument-hint` and `disable-model-invocation` are Claude Code fields; the portable Agent Skills specification allows only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`.
- **Validation status.** The package has been statically checked, and its runtime assumptions (nesting, background launch, message routing, child handback) were probed in a live Claude Code session. The full flow was then run end-to-end twice on small smoke-test tasks. In the second run every Executor update reached the Supervisor live and the handback reached it too, while Main received only the Supervisor's reports. That run used an earlier wording in which the Supervisor relayed each update; the final wording, in which it reports its own judgment, has not been run end-to-end. The correction loop has not been exercised either, because both runs passed first time. Nothing has been run on a real, sizeable task. The two-round convergence default is a design choice, not an experimentally validated optimum.

## Evaluation

Compare against a baseline without the skill using the same specification, model, initial environment, acceptance method, and permissions. No degradation in quality is the gate; Main's release behavior and protocol compliance are the primary metrics.

| Check | Pass criterion |
|---|---|
| Main's control flow | Ends the turn after confirming background launch; no routine task-advancing tool calls |
| Role boundaries | The Supervisor actually launches Executors; Main does not do the substantive work itself |
| Contract fidelity | The original specification is preserved; no unauthorized downgrade or expansion |
| Information routing | Executors report to the Supervisor only; Main receives the Supervisor's reports and its final report |
| Progress reporting | Executor updates reach the Supervisor at the required points; the Supervisor's reports state what it checked, decided and found |
| Response obligation | Informational reports do not trigger replies or extra management loops |
| Independent acceptance | Independent check evidence exists; unknown or failed is never labeled COMPLETED |
| Exception handling | Honest degradation when no channel exists; blocking, cancellation, and recovery do not duplicate active tasks |
| Cost and quality | Records total tokens, elapsed time, acceptance pass rate, Main tokens, Main's first-release latency, and intervention count |

Suggested smoke test: in a temporary directory, delegate a simple verifiable file-generation task and check the real invocation records of both agent layers; send an unrelated request to Main during execution; then simulate an unpassable acceptance check, a missing message channel, and a cancellation. Cross-check message sources, revisions, and states against the trace. Run tests only in approved directories.

This package has been statically checked for files, references, frontmatter, and ZIP integrity, its runtime assumptions were probed in a live Claude Code session, and the full flow was run end-to-end on two small smoke-test tasks, the second with an earlier wording of the Supervisor's reports. The two-round convergence default in the verification loop is an adjustable design default, not an experimentally validated optimum.

## Contributing

Contributions are welcome through GitHub issues and pull requests. The files under `references/` are normative: keep them internally consistent, update the Claude Code adapter when runtime behavior changes, and explain in the pull request any change to role boundaries, acceptance rules, or message types. There is no separate CONTRIBUTING file or automated test suite yet.

## License

MIT License. Copyright (c) 2026 treadonsnow. See [LICENSE](LICENSE).
