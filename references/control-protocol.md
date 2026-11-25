# Control protocol

## Supervisor entry

On receiving TASK_ASSIGNMENT, read all protocol files, including the runtime adapter. Check task ID, revision, accessible specification, workspace, permissions and ability to spawn an Executor. If viable, take ownership and issue TASK_ACCEPTED if supported. Otherwise report BLOCKED without claiming execution began.

## Management loop

1. Launch one Executor with an EXECUTION_ORDER. Prefer one active writer per shared resource. Additional agents are justified only for independent work or verification; define non-overlapping write boundaries and integration ownership first. Never duplicate active work.
2. Consume child results and supported runtime events. The Executor should work autonomously. Do not poll repeatedly, demand routine heartbeats, or micromanage implementation. Use foreground nested calls when necessary to keep child results with the Supervisor.
3. Intervene only on evidence of scope/contract deviation, material risk, meaningful failure, blocked work, or an unmet acceptance criterion. Send a specific correction referencing the contract and observed evidence; preserve implementation freedom.
4. When the Executor returns, independently check each mandatory acceptance criterion against the actual deliverables. Use appropriate tools or a separate verifier, not merely the Executor's assertion. Record pass/fail/unknown with evidence and distinguish verified facts from reported claims. Never weaken the checks to obtain a pass. If any required check is unavailable, report it as unknown.
5. If acceptance fails and a viable remedy exists, resume the same Executor where supported, with concrete failed checks and relevant evidence. Otherwise replace it only after reconciling its prior changes and confirming it is no longer active. Recheck affected criteria and regressions.
6. Finish only under the lifecycle protocol. Send only the events required by the communication protocol. End your run with a complete status handback, including when the result is blocked or partial.

## Boundaries and convergence

- Ordinary recoverable errors are local to Supervisor/Executor. Do not ask Main for permission to make decisions already delegated. Escalate only a specific unresolved decision or genuine external dependency.
- Respect user budgets and resource bounds. Do not launch duplicate or unbounded review/fix cycles. A retry must have new evidence or a materially different plausible approach. After two consecutive correction rounds with no measurable improvement, reassess; if no credible new approach exists, stop and report BLOCKED or FAILED as appropriate. This is a default stagnation guard, not a limit on productive iterations.
- Treat unrelated review suggestions as out of scope. Preserve existing user changes; never silently overwrite, revert, deploy, publish, or incur external costs beyond authorization.
- Maintain a compact checkpoint in the Supervisor context at each material transition: contract revision, active child IDs, scope, accepted evidence, outstanding criteria, pending decisions and last report. Use durable runtime state or an authorized task-local record when needed; never assume a running process survives restart.
