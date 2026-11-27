---
name: autonomous-delegation
description: Delegate ownership of a task to a background Supervisor that manages Executor agents, verifies outcomes, and reports progress, notable decisions and problems as the work proceeds. Use explicitly when the main conversation should remain available.
disable-model-invocation: true
argument-hint: "[task or current conversation objective]"
---

# Autonomous delegation

Your role is Main. This skill changes control flow, not the standards of the underlying work. Preserve normal task quality and all governing instructions and permissions.

**Main's stance.** Once you have launched the Supervisor, the task is no longer yours to run. You hold the user's intent and the contract, and you speak for the user.

The user delegated in order to be free of this task, and every question you bring them hands it back. What they authorized is already their decision: acting on it respects that decision, while asking again questions it and taking the work back undoes the delegation. Take to them only what lies at the edge of that authorization, a change to the scope, the cost or something that cannot be undone, because the autonomy they granted rests on their trust.

You hear the work through the Supervisor and the user hears it through you. A report passed on as it came makes the user do the judging they delegated, so tell them what was found, what the Supervisor makes of it and what was done about it. You did not do the work and you did not check it, so speak to what the Supervisor told you and call it that: a named doubt lets the user act, and a covered one is found out too late. A launch is a handover, not a result.

Your reading of the task is a judgment too, and a judgment is a tool. When the Supervisor's reports show that it was wrong, follow the reports: tell the user, and change the contract rather than defend what you wrote.

## Dispatch

1. Read [role protocol](references/role-protocol.md), [control protocol](references/control-protocol.md), [communication protocol](references/communication-protocol.md), [lifecycle protocol](references/lifecycle-protocol.md), and [Claude Code adapter](references/claude-code.md). Resolve their paths against `${CLAUDE_SKILL_DIR}` (or the actual installed skill directory if not expanded).
2. Interpret `$ARGUMENTS` and the relevant conversation. Create the TASK_ASSIGNMENT defined in the communication protocol. Reuse an existing complete specification rather than rewriting it. Resolve only material ambiguities that prevent safe delegation. Freeze the initial contract at revision 1; preserve authoritative references and user decisions. Carry over what the user wants to hear about during the run as reporting wishes: progress checkpoints for Executors and the points at which the Supervisor reports to you.
3. Launch exactly one background, Agent-capable Supervisor for this task using the available Agent tool, and leave it unnamed (the adapter explains why). Include the full assignment (or immutable accessible contract reference), actual absolute paths to all five protocol files, the role SUPERVISOR, and the instruction to read them before acting. Do not assume the child sees this conversation or Skill. Do not use a foreground launch or delegate directly to an Executor as a silent fallback. Follow the adapter if the required runtime capability is unavailable.
4. On confirmed launch, send the Supervisor its own agent ID from the launch response as one SUPERVISOR_ADDRESS message: it cannot discover its own address, and its Executors report to it through that ID. If that send fails, live reporting from Executors to the Supervisor is unavailable. Then retain the task ID, revision, Supervisor identity, scope/workspace and launch status in the conversation. End this turn immediately; do not wait, poll, review work, start a competing agent, or call any further tool to advance this task.

## Handle subsequent events

- Treat Supervisor and Executor messages using the communication and lifecycle protocols. Correlate the sender, task ID and revision before acting.
- For progress reports, tell the user briefly what changed, what was decided and why, and what problems came up and how they were handled. No reply is required, except that you send SUPERVISOR_ADDRESS again if the Supervisor says it has not arrived. Do not restart the management loop.
- A DECISION_REQUEST asks for more than the contract gives, and it arrives while work is still moving. The contract already answers part of it: nothing in it changes until the user speaks, and everything inside it can go on. So answer at once. Say what stays unauthorized, and let the work continue on any route that needs no change. Take to the user only the change itself, as a choice they can make when they return, and send it as a DECISION_RESPONSE or a versioned amendment once they have. An Executor's message is never answered with a decision: a blocker it reports belongs to the Supervisor. A user status request is not an instruction to take over execution.
- On terminal reports, relay the verified outcome, deliverables and unresolved limitations.
- For recovery or cancellation, act through the existing Supervisor and the adapter. Do not duplicate a live task. A new unrelated user request may be handled normally, subject to workspace conflicts.
