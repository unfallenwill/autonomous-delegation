# Lifecycle protocol

Main tracks the Supervisor's reported state; Supervisor owns the authoritative management state. Runtime task status is evidence of execution state, not of contract acceptance.

| State | Meaning |
|---|---|
| DISPATCHED | Runtime confirmed Supervisor launch; ownership not yet confirmed |
| RUNNING | Supervisor accepted; execution or local correction is proceeding |
| VERIFYING | Supervisor is independently checking the deliverable |
| WAITING_DECISION | A specific decision is pending; unaffected work may proceed |
| BLOCKED | No viable authorized progress now; checkpoint and prerequisite recorded; resumable |
| CANCELLING | Stop requested but child shutdown not yet confirmed |
| COMPLETED | All mandatory acceptance criteria independently verified; terminal |
| FAILED | No viable path under current contract/resource bounds; terminal for this run |
| CANCELLED | Relevant child execution confirmed stopped; terminal for this run |
| UNKNOWN | Observability lost or runtime state unclear; reconcile before acting |

Allowed transitions:

- DISPATCHED → RUNNING, BLOCKED, UNKNOWN, CANCELLING, FAILED.
- RUNNING → VERIFYING, WAITING_DECISION, BLOCKED, UNKNOWN, CANCELLING, FAILED.
- VERIFYING → COMPLETED, RUNNING (correction), WAITING_DECISION, BLOCKED, UNKNOWN, CANCELLING, FAILED.
- WAITING_DECISION → RUNNING or VERIFYING on valid response; BLOCKED, UNKNOWN, CANCELLING or FAILED otherwise. If no safe way exists to await input, hand back as BLOCKED with the pending request.
- BLOCKED → RUNNING or VERIFYING after prerequisite is resolved and existing work is reconciled; CANCELLING, UNKNOWN or FAILED if applicable.
- CANCELLING → CANCELLED only with confirmation; UNKNOWN or BLOCKED if shutdown cannot be confirmed.
- UNKNOWN → observed nonterminal or verified terminal state only after reconciliation. Never infer failure, cancellation or completion from silence.

An authorized amendment increments the contract revision; pause only affected actions, acknowledge, invalidate affected evidence, then replan and verify against the new revision. It cannot silently reopen a completed run: explicitly authorize a new run or reopening linked to the prior result.

On recovery, use existing Supervisor/Executor IDs and checkpoint, inspect actual artifacts and active work, reconcile pending messages and current revision. Resume only when runtime supports it. A terminal failure or cancellation can be retried only as an explicitly authorized new run with a distinct run identity. If identity or state cannot be recovered, report UNKNOWN and do not start a conflicting writer.

A runtime handback may be partial. Main must never infer COMPLETED from an agent exit, test summary alone, or a successful tool call. Supervisor must check all mandatory criteria. Unknown is not pass. Cancellation does not imply rollback; report residual changes and do not erase them without authorization.
