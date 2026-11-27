---
name: autonomous-delegation
description: Delegate ownership of a task to a background Supervisor that manages Executor agents, verifies outcomes, and reports progress, notable decisions and problems as the work proceeds. Use explicitly when the main conversation should remain available.
disable-model-invocation: true
argument-hint: "[task or current conversation objective]"
---

# Autonomous delegation

Your role is Main. This skill changes control flow, not the standards of the underlying work. Preserve normal task quality and all governing instructions and permissions.

**Main's stance.** Once you have launched the Supervisor, the task is no longer yours to run. You hold the user's intent and the contract, you speak for the user, and you pass on what the Supervisor reports. You made the Supervisor accountable for the outcome: reviewing the work behind it, answering its Executors or taking the task back leaves nobody accountable, and a status question from the user does not ask you to. After launch the user needs two things from you: decisions that were never delegated, and an honest account of where things stand. In that account, keep apart what the Supervisor verified and what it only reports. A launch is a handover, not a result.

## Dispatch

1. Read [role protocol](references/role-protocol.md), [control protocol](references/control-protocol.md), [communication protocol](references/communication-protocol.md), [lifecycle protocol](references/lifecycle-protocol.md), and [Claude Code adapter](references/claude-code.md). Resolve their paths against `${CLAUDE_SKILL_DIR}` (or the actual installed skill directory if not expanded).
2. Interpret `$ARGUMENTS` and the relevant conversation. Create the TASK_ASSIGNMENT defined in the communication protocol. Reuse an existing complete specification rather than rewriting it. Resolve only material ambiguities that prevent safe delegation. Freeze the initial contract at revision 1; preserve authoritative references and user decisions. Carry over what the user wants to hear about during the run as reporting wishes: progress checkpoints for Executors and the points at which the Supervisor reports to you.
3. Launch exactly one background, Agent-capable Supervisor for this task using the available Agent tool, and leave it unnamed (the adapter explains why). Include the full assignment (or immutable accessible contract reference), actual absolute paths to all five protocol files, the role SUPERVISOR, and the instruction to read them before acting. Do not assume the child sees this conversation or Skill. Do not use a foreground launch or delegate directly to an Executor as a silent fallback. Follow the adapter if the required runtime capability is unavailable.
4. On confirmed launch, send the Supervisor its own agent ID from the launch response as one SUPERVISOR_ADDRESS message: it cannot discover its own address, and its Executors report to it through that ID. If that send fails, tell the user that live reporting from Executors to the Supervisor is unavailable. Then retain the task ID, revision, Supervisor identity, scope/workspace and launch status in the conversation. End this turn immediately; do not wait, poll, review work, start a competing agent, or call any further tool to advance this task.

## Handle subsequent events

- Treat Supervisor and Executor messages using the communication and lifecycle protocols. Correlate the sender, task ID and revision before acting.
- For progress reports, tell the user briefly what changed, what was decided and why, and what problems came up and how they were handled. No reply is required, except that you send SUPERVISOR_ADDRESS again if the Supervisor says it has not arrived. Do not restart the management loop.
- For decisions outside the delegated authority, obtain user authorization if required, then return the decision or a versioned amendment to the existing Supervisor.
- On terminal reports, relay the verified outcome, deliverables and unresolved limitations.
- For recovery or cancellation, act through the existing Supervisor and the adapter. Do not duplicate a live task. A new unrelated user request may be handled normally, subject to workspace conflicts.
