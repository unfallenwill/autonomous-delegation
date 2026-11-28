# Autonomous Delegation

A Claude Code Skill that hands a task to a background Supervisor and keeps your main conversation free.

Autonomous Delegation changes who owns a task, not the standard of the work. You state the outcome once; Main freezes it as a revisioned contract, launches exactly one background Supervisor, and returns your turn. The Supervisor runs the management loop with Executor agents, checks each mandatory acceptance criterion against the actual deliverable, and keeps you posted as the work proceeds: progress, the decisions behind it, and the problems that come up.

**Status:** The owner uses the skill in production environments and in daily development tasks. In the owner's assessment, the results are good and beyond what the owner expected. That is the owner's account of their own use, not a measurement, and it is not written up under `evals/`. The written record under `evals/` is separate and covers less: two small real tasks run end to end under the earlier rule-based wording, and, for the current wording (each role is given its stance in place of the scattered judgment rules), single-role probes but no recorded real-task run. See [The cognitive frame](#the-cognitive-frame) and [Evaluation](#evaluation).

## Start in under a minute

Install globally for Claude Code (the Skills CLI needs Node.js 22.20 or later):

```bash
npx skills add unfallenwill/autonomous-delegation --agent claude-code --global
```

Start a new Claude Code session, then hand off a task:

```
/autonomous-delegation Split session handling out of src/auth/login.ts, add unit tests for the new module, and keep the public API unchanged.
```

Main freezes the contract at revision 1, launches the Supervisor, and ends the turn. Keep working while the Supervisor manages and verifies the task.

Other ways to install, and what to do if the skill does not show up: [Installation](#installation).

## Contents

- [Start in under a minute](#start-in-under-a-minute)
- [Why use it](#why-use-it)
- [Installation](#installation)
- [Usage](#usage)
- [How it works](#how-it-works)
  - [The cognitive frame](#the-cognitive-frame)
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
- **Executors do the work.** A single active writer by default; additional agents only for independent work or verification, with write boundaries that do not overlap.
- **Independent acceptance.** The Supervisor checks each mandatory criterion itself. An agent exit, a test summary, or a completion notification is not acceptance.
- **Reporting you can follow.** Executors report to the Supervisor at each checkpoint. The Supervisor keeps you posted with what it checked and decided, and with the Executor decisions and problems worth knowing. Reports are tied to events by default, not to time, and are not raw transcripts.
- **Honest degradation.** If the Supervisor cannot launch Executors, the task is reported blocked. If no background launch is possible, the skill explains why and asks for your explicit approval before any different workflow. If no live message channel exists, reports travel in the handback. It never changes the workflow silently, and never pretends a live report was delivered.
- **What it costs.** A Supervisor that checks the work is a second agent. On the two small tasks written up under `evals/`, the chain cost the most of the three ways tried, with no measurable gain in quality or in success. See [Evaluation](#evaluation).

## Installation

### With the Skills CLI (recommended)

The Skills CLI requires Node.js 22.20 or later.

Install globally for Claude Code:

```bash
npx skills add unfallenwill/autonomous-delegation --agent claude-code --global
```

Install at project scope instead, and choose the agents as prompted:

```bash
npx skills add unfallenwill/autonomous-delegation
```

Other useful commands:

```bash
npx skills add unfallenwill/autonomous-delegation --list    # list the skills in the repository without installing
npx skills list                                             # list installed project skills
npx skills list -g                                          # list global installs
npx skills update                                           # update installed skills
npx skills update --global                                  # update global installs
```

The CLI symlinks the skill into each selected agent's skills directory by default; `--copy` copies the files instead. For Claude Code those directories are `.claude/skills/` at project scope and `~/.claude/skills/` at global scope.

### Manual installation

Clone directly into the Claude Code skills directory:

```bash
git clone https://github.com/unfallenwill/autonomous-delegation.git ~/.claude/skills/autonomous-delegation
```

To update a clone, run `git pull` inside that directory.

Or install from the repository's source archive into `~/.claude/skills/` (personal) or `.claude/skills/` (project). The archive extracts to `autonomous-delegation-main/`; rename it to `autonomous-delegation/`:

```bash
mkdir -p ~/.claude/skills
curl -L https://github.com/unfallenwill/autonomous-delegation/archive/refs/heads/main.zip -o autonomous-delegation-main.zip
unzip autonomous-delegation-main.zip
mv autonomous-delegation-main ~/.claude/skills/autonomous-delegation
```

To update an archive install, download it again and replace the directory.

Keep the directory name `autonomous-delegation`: it matches the skill's `name`, and the command you type is `/autonomous-delegation`. If an older install with the same name exists, move it aside first so stale protocol documents are not loaded.

### Confirm the skill loaded

Claude Code picks up skill changes within the current session, except in bare mode. After you add or edit the skill under `~/.claude/skills/`, the project `.claude/skills/`, or a `.claude/skills/` inside an `--add-dir` directory, open `/skills` and check that `autonomous-delegation` is listed. If a new skill does not appear, run `/reload-skills`.

The skill sets `disable-model-invocation: true`, so Claude does not invoke it on its own. Invoke it explicitly with `/autonomous-delegation`.

To remove the skill, delete its directory, or run `npx skills remove`.

## Usage

Pass the task as the argument. State the outcome, the constraints and what must be true at the end: Main turns it into a frozen task contract, launches one background Supervisor, and returns the turn.

### 1. Hand off a whole feature

```
/autonomous-delegation Split session handling out of src/auth/login.ts, add unit tests for the new module, and keep the public API unchanged.
```

Main freezes the contract at revision 1, launches the Supervisor, and ends the turn. The Supervisor confirms that it has taken over, launches an Executor, reports as the work proceeds, checks the result against the contract, and reports the verified outcome, a blocker, or a decision outside its authority.

### 2. Delegate the task you have already discussed

```
/autonomous-delegation
```

With no argument, Main reuses the task specification from the current conversation instead of asking you to restate it. If the request is materially ambiguous, Main resolves only what would make delegation unsafe, then proceeds.

### 3. Keep working while it runs

```
/autonomous-delegation Audit the repo for unhandled promise rejections and fix them with tests.
```

Then continue the conversation. Main stays free for unrelated requests and passes on the Supervisor's reports: what changed, what was decided and why, and what problems came up. You are asked only for decisions outside the delegated authority.

You can ask for status at any time. A status question is not an instruction to take over execution. To see which agents are running, or to stop one, use `/tasks`.

### 4. Say what you want to hear about

```
/autonomous-delegation Migrate the payment service to the new client library and keep the tests green. Report at each module.
```

Anything you say about reporting is carried into the task contract: it sets the Executor checkpoints and the points at which the Supervisor reports to Main, which passes the report on to you. Executors report at those points and whenever they make a notable decision or hit a problem; the Supervisor reports after each verification round. Decision requests, blockers and the final report are always sent.

## How it works

![Overview: Main writes the task contract, launches one background Supervisor and sends it its agent ID, then stays out of the work and asks you only for decisions it is not allowed to make. The Supervisor orders the Executor, receives its progress, decisions and problems, checks each acceptance criterion itself, and reports its judgment to Main.](assets/architecture-overview.svg)

<details>
<summary>Full diagram: the verification loop, lifecycle states and the handback</summary>

![Control and information flow: the user states intent to Main; Main freezes a revisioned task contract and launches exactly one background Supervisor, sends it its own agent ID, then stops routine execution, review, and supervision; the Supervisor issues execution orders to one active-writer Executor, independently verifies each mandatory acceptance criterion in the VERIFYING state, and resumes the same Executor on failure; Executors report progress, decisions and problems to the Supervisor only, and the Supervisor reports its own checks and decisions plus the Executor news worth knowing to Main; the Supervisor's final report reaches Main as its handback.](assets/architecture.svg)

</details>

### Roles

| Role | Owns | Must not |
|---|---|---|
| **Main** | User intent, task contract, delegation, decisions beyond delegated authority, user-facing communication | Perform routine execution, review, or supervision after launch |
| **Supervisor** | End-to-end task management, Executor selection, interventions, independent acceptance, reporting | Redefine the contract, perform the primary implementation itself, return routine management to Main |
| **Executor** | Implementation choices within scope, execution, progress updates to the Supervisor, self-checks, deliverables and evidence | Change the contract, declare overall acceptance, report to Main or ask it for decisions |

Main authors the contract, freezes it at revision 1, and is the only role that can amend it, to reflect your authority; an amendment increments the revision. The Supervisor delegates the primary work to an Executor and steps in on evidence, not on a difference of taste, saying what must hold and leaving the how to the Executor.

### The cognitive frame

Each role is first told how it weighs things, and why. The text states a situation and what matters in it. It gives no prohibition and no step; what follows from it is the role's to work out. The steps and the facts about the runtime that a role could not work out for itself stay where they were.

| Weight | Reason |
|---|---|
| Delivery over appearance: a result that has been verified, not progress that looks like progress | Nobody checks behind the user. They know the work only through reports. |
| Autonomy over asking: a decision that is yours is not passed upward | A question hands the task back. The user delegated to be free of it. |
| Trust over progress: one mistake costs more than one step gains | Autonomy rests on trust. Once lost, every step is watched. |
| Judgment over relay: a report carries the reporter's own assessment | A report passed on as it came makes the user do the judging. |
| Not pretending to know: what has not been checked is said to be a belief, not a fact | A guess passed on as a fact closes off the remedy: the user could still act on a doubt, but cannot undo a fact they trusted. |
| Respecting reality: when what is found contradicts a judgment, the finding wins | A judgment is only a tool for getting the work done. Holding on to one that the facts have passed gains nothing. |

Trust pulls toward caution and autonomy toward deciding alone. They are ordered this way: autonomy inside what was authorized, caution at its edge. Inside it the user has already decided, by authorizing. Where a choice would change the scope, the cost or something that cannot be undone, the user has not, and the role stops and asks. Authorization is not exemption: inside the boundary the role is still answerable for what its choices cost.

| Role | Holds |
|---|---|
| **Supervisor** | All six |
| **Main** | All but delivery: checking the deliverable is the Supervisor's work |
| **Executor** | All but judgment: comparing an account with the facts is the Supervisor's work |

The meaning, the reasons and the ordering were agreed with the owner on 2026-11-28. The record, with what to look for on real work, is in [`evals/cognitive-frame.md`](evals/cognitive-frame.md).

### Verification loop

1. Main launches exactly one background Supervisor with a complete TASK_ASSIGNMENT and the absolute paths to the protocol files, then sends it its own agent ID.
2. The Supervisor takes ownership, launches an Executor with an EXECUTION_ORDER, and works from the Executor's results.
3. In the VERIFYING state, the Supervisor checks each mandatory acceptance criterion against the actual deliverable, using tools or a separate verifier rather than the Executor's assertion. A required check that is unavailable, or that cannot be finished within bounds, is unknown.
4. On a failed check, the Supervisor resumes the same Executor with the concrete failed checks, then rechecks. After two consecutive correction rounds with no measurable improvement, it does not conclude that nothing is left: it diagnoses the stall itself in bounded, read-only steps, and stops as BLOCKED or FAILED only if the diagnosis yields nothing.
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
| `DISPATCHED` | Runtime confirmed Supervisor launch; ownership not yet confirmed |
| `RUNNING` | Supervisor accepted; execution or local correction is proceeding |
| `VERIFYING` | Supervisor is independently checking the deliverable |
| `WAITING_DECISION` | A specific decision is pending; unaffected work may proceed |
| `BLOCKED` | No viable authorized progress now; checkpoint and prerequisite recorded; resumable |
| `CANCELLING` | Stop requested but child shutdown not yet confirmed |
| `COMPLETED` | All mandatory acceptance criteria independently verified; terminal |
| `FAILED` | No viable path under current contract/resource bounds; terminal for this run |
| `CANCELLED` | Relevant child execution confirmed stopped; terminal for this run |
| `UNKNOWN` | Observability lost or runtime state unclear; reconcile before acting |

Runtime task status reflects execution, not contract acceptance. A completion notification, an agent exit, or a passing test run alone does not make a task COMPLETED.

### Handback

The final or blocked report reaches Main as the Supervisor's handback. If SendMessage or an equivalent live channel is unavailable, everything due to Main travels in it, and intermediate progress and decision requests may be delayed until then. Undelivered critical information is recorded as undelivered and is never claimed as delivered. An Executor also writes its result to an agreed location, so a report that the runtime drops can still be read. If a running child cannot be safely stopped or reconciled, the correct report is UNKNOWN, not a clean handback.

## Skill metadata and repository layout

`SKILL.md` is the Main entry point; the Markdown files under `references/` are normative, and the Claude Code adapter among them maps their intent onto the actual runtime. At run time Main reads `SKILL.md` and the five files under `references/`, the Supervisor reads the same five files from the absolute paths in its launch prompt, and an Executor reads none of them: it receives only the task contract and its execution instructions. Together the six skill files are about 5,400 words, by the count in `evals/manual-audit.md`.

| Frontmatter field | Value | Effect |
|---|---|---|
| `name` | `autonomous-delegation` | Command name: `/autonomous-delegation` |
| `description` | Summarizes delegation and when to use it | Human- and tool-facing metadata |
| `disable-model-invocation` | `true` | Manual invocation only; Claude does not auto-load the skill |
| `argument-hint` | `[task or current conversation objective]` | Autocomplete hint for the task argument |

The task text arrives as `$ARGUMENTS`. There is deliberately no `context: fork`: Main must write the task assignment in its own conversation, so the skill cannot run in a forked context.

```
autonomous-delegation/
├── SKILL.md                       # Main entry point: dispatch and event handling
├── references/                    # Normative protocols
│   ├── role-protocol.md           # Role table, the Supervisor's stance, structure
│   ├── control-protocol.md        # Supervisor entry and management loop
│   ├── communication-protocol.md  # Message types, the Executor's instruction
│   ├── lifecycle-protocol.md      # States and transitions
│   └── claude-code.md             # Runtime adapter
├── assets/                        # The two diagrams in this README
│   ├── architecture-overview.svg
│   └── architecture.svg
├── evals/                         # Not read at run time: the record behind the wording
│   ├── README.md                  # How a probe is run and read
│   ├── scenarios.md               # The judgment situations
│   ├── cognitive-frame.md
│   ├── manual-audit.md
│   ├── stance-draft.md
│   ├── audit/                     # Scripts and listings for the manual audit
│   ├── conditions/                # A copy of the skill that a probe reads instead
│   └── results/                   # Write-ups, and one file per run in 2026-11-28-runs/
├── README.md                      # For people deciding whether and how to install (this file)
├── LICENSE
└── .gitignore
```

`README.md` is for humans deciding whether and how to install the skill. `SKILL.md` is what Claude loads when the skill is invoked; it stays short and points at the protocol files. No file in the skill refers to `evals/`, so nothing under it is read at run time.

## Requirements

- **Claude Code** with the Agent tool, able to launch **background (non-blocking) subagents**.
- **Subagent nesting** at least two layers deep (Main → Supervisor → Executor). Claude Code allows three by default; `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` sets the limit.
- **SendMessage** (or an equivalent live channel) for progress and decisions during a run. Without it, the skill uses handback.
- No additional permissions, hooks, MCP servers, or settings changes are required or made by this skill.

If the Supervisor itself cannot launch Executors, because it lacks the Agent tool or enough nesting depth, it reports a blocker. If a background launch is unavailable, Main explains that and asks for your explicit approval before any different workflow; it never falls back to a foreground launch silently. If the live channel is unavailable, the skill falls back to handback. Capabilities vary by Claude Code version, tool set, permissions, and mode, so verify the tools actually exposed in the current session rather than inferring them from a version number.

## Compatibility and limitations

- **Claude Code first.** The only adapter in this repository targets Claude Code. The Skills CLI can install the skill for other agents, but the control protocol depends on background subagents and agent messaging, so compatibility beyond Claude Code is not claimed.
- **A prompting protocol, not an enforced state machine.** Claude Code does not enforce these roles, transitions, or message types; runtime compliance cannot be guaranteed.
- **Manual by design.** `disable-model-invocation: true` keeps the skill out of automatic selection. `context: fork` is intentionally not used.
- **Runtime interrupts still apply.** Tool or permission prompts can interrupt Main; the protocol cannot suppress them.
- **Reports interrupt Main too.** Each report to Main starts a Main turn that relays it to you, which is why reports are tied to events rather than to time by default. In each of the two chain runs written up under `evals/`, three reports reached Main. An earlier revision of this file also records two earlier smoke tests, which have no write-up under `evals/`: six reports to Main in about ten minutes, and five in about eighteen. The first of them still used an earlier routing in which Executors also messaged Main. If you want fewer reports, or timed instead, say so in the task: the contract then sets the reporting points, and decision requests, blockers and the final report are always sent.
- **The runtime can lose a child's report, and agents cannot always wait.** In the Claude Code build tested, a named Supervisor waiting on a nested call never received the Executor's final report, and a named Executor reports to Main instead of handing its report back. The skill therefore launches the Supervisor and its Executors unnamed, has Executors write results to an agreed location, and treats a missing report as unknown, never as completion. A Supervisor cannot idle while an Executor runs: it keeps working in bounded steps until the result arrives. An unnamed Supervisor is not told its own address, so Main sends it its agent ID right after launch, and Executors report to the Supervisor through that ID.
- **Cancellation is not rollback.** A cancelled run reports residual changes and does not erase them without authorization.
- **Frontmatter portability.** `argument-hint` and `disable-model-invocation` are Claude Code fields; the portable Agent Skills specification allows only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`.
- **Validation status.** What is written up under `evals/`, all on one model, is small: two real tasks under the rule-based wording, and single-role probes of the current wording. Nothing there records a real-task run of the current wording, a real sizeable task, an exercised correction loop or a second model. The two-round convergence default is a design choice, not an experimentally validated optimum. See [Evaluation](#evaluation).

## Evaluation

### What the record shows

The four results below are written up under [`evals/`](evals/README.md) and were run on one model. The current wording was developed on the `cognitive-framing` branch and fast-forwarded into `main`; the write-ups call it the branch or the philosophy condition.

- **Real tasks, rule-based wording.** Two small real tasks were run end to end by the chain (a Supervisor and one Executor): splitting session handling out of a module, and implementing a pricing specification. The pricing task ran from the files committed at 4c6042b; the split task ran with two corrections to the protocol that were not yet committed. Neither produced a false completion. Every run passed on the first attempt, so the correction loop was not exercised. See `evals/results/2026-11-27-live-run-1.md` and `evals/results/2026-11-27-pricing-task.md`.
- **Against working without the skill.** Each task was also done, once each, by one agent given the contract and by one agent given one sentence. All three ways met each task. On the pricing task, scored by 41 hidden tests, all three scored full marks. The chain cost the most (its Executor's token count is not visible from Main), with no measurable gain in quality or in success. See `evals/results/2026-11-27-baseline-vs-chain.md` and `evals/results/2026-11-27-pricing-task.md`.
- **Single-role probes.** Each of the fifteen situations in [`evals/scenarios.md`](evals/scenarios.md) was run once under the rule-based wording at 4c6042b, once under an earlier stance wording (`evals/conditions/reduced/`), and once with no protocol at all. The core judgment was the same with no protocol as with it, and the earlier stance wording lost no behaviour that held under the rules. With no protocol the behaviour changed in nine situations. Under the rule-based wording, fourteen of the fifteen matched the expected behaviour; in the fifteenth, M1, what Main should do is still an open decision. See `evals/results/2026-11-27-screen-current.md`, `evals/results/2026-11-27-reduced-vs-current.md` and `evals/results/2026-11-27-none.md`.
- **Stability and reach, current wording.** Seven of the fifteen situations were run three times under the current wording and three times under the rule-based wording at 4c6042b (42 runs), and four situations that no rule addresses directly were run twice under each (16 runs). The intended behaviour appeared in every one of the 58 valid runs, under both wordings. So on these situations the stance wording is as stable as the rules, and it carries into situations that no rule addresses; it was not shown to be more stable or to reach further. No run of the other eight situations under the current wording is recorded. A probe is a table-top exercise: it shows what an agent says it would do, not what it does in a live run. See [`evals/results/2026-11-28-stability-and-reach.md`](evals/results/2026-11-28-stability-and-reach.md).
- **Not written up under `evals/`.** The first revision of this file said the package had been statically checked for files, references, frontmatter and ZIP integrity. Nothing under `evals/` describes that check.

### How to evaluate a change

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
| Stability across runs | The same situation, run many times, lands on the intended behaviour about as often from one batch to the next, and more often than under the rule-based protocol |

The last row is the measure for the cognitive frame. The frame is there for consistency from one run to the next, so a single run cannot show whether it works.

Suggested smoke test: in a temporary directory, delegate a simple verifiable file-generation task and check the real invocation records of both agent layers; send an unrelated request to Main during execution; then simulate an unpassable acceptance check, a missing message channel, and a cancellation. Cross-check message sources, revisions, and states against the trace. Run tests only in approved directories.

[`evals/README.md`](evals/README.md) describes how a single-role probe is run, classified and recorded.

## Contributing

Contributions are welcome through GitHub issues and pull requests. The files under `references/` are normative: keep them internally consistent, update the Claude Code adapter when runtime behavior changes, and explain in the pull request any change to role boundaries, acceptance rules, or message types. `evals/README.md` describes how a change to the judgment text is checked with single-role probes. There is no separate CONTRIBUTING file or automated test suite yet.

## License

MIT License. Copyright (c) 2026 treadonsnow. See [LICENSE](LICENSE).
