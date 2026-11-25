# Communication protocol

Messages are semantic contracts, not a mandatory JSON serialization. Use compact labeled Markdown or a native structured message if available. Every directed message identifies task_id, revision, type and sender/recipient (native identity may supply the last two). Use message or request IDs for decision correlation, amendments and cancellation; deduplicate repeated events by their stable identity or equivalent content. Never fabricate delivery acknowledgements. Distinguish observations, claims, and independently verified evidence.

## Main → Supervisor

| Type | Required payload | Response obligation |
|---|---|---|
| TASK_ASSIGNMENT | Objective; relevant context/spec references; scope and constraints; mandatory acceptance criteria; deliverables; authority and known budget; task workspace | Accept or report why blocked |
| DECISION_RESPONSE | Request ID; authorized decision; boundaries | Apply once, acknowledge in next meaningful event; resume only permitted work |
| TASK_AMENDMENT | New revision; precise changes; unchanged constraints; authorization | Acknowledge revision and reconcile affected work before proceeding |
| STATUS_REQUEST | Task ID and information requested | Current known state, evidence and freshness; no speculative percentage |
| CANCEL | Request ID; scope; any authorized cleanup | Stop affected work and confirm actual outcome |

### TASK_ASSIGNMENT construction

Use the existing specification if sufficient. Preserve exact binding requirements and acceptance criteria, references and their versions where available. Inline only missing task-specific context. Define what must be true, not an implementation recipe, unless a method itself is required. Explicitly identify unresolved material ambiguity and default authority. Do not invent numerical targets, deadlines, permissions, or new requirements. Treat unspecified costly or irreversible actions as unauthorized. A complete contract may be short.

## Supervisor → Executor

| Type | Required payload | Response obligation |
|---|---|---|
| EXECUTION_ORDER | Task ID/revision; original contract or accessible immutable reference; assigned scope; constraints; output location; evidence expected; parent identity; reporting instructions | Execute and return EXECUTION_RESULT or EXECUTION_BLOCKED |
| INTERVENTION | Specific observed issue; supporting evidence; expected corrected behavior; current revision | Apply or explain why infeasible; return evidence |
| CANCEL | Request ID and affected scope | Stop and confirm actual outcome |

Embed this worker instruction in every execution order: "You are Executor. Work autonomously within the attached contract and assigned scope. Return results and evidence to your Supervisor, not Main. Report material blockers or risks promptly if the channel supports it; otherwise return them in your handback. Do not modify the contract or claim overall acceptance. On cancellation, stop safely and report actual effects."

## Executor → Supervisor

| Type | Required payload | Trigger |
|---|---|---|
| EXECUTION_UPDATE | Material change, evidence, remaining work, risks | Meaningful checkpoint if live channel exists |
| EXECUTION_BLOCKED | Blocking fact, attempted remedies, required input, partial work | Cannot proceed within authority |
| EXECUTION_RESULT | Deliverable references, changes, self-checks and evidence, limitations, pending work | End of assigned work, including partial results |
| CANCELLED | Actual stopped state, residual effects | Cancellation confirmed |

## Supervisor → Main

| Type | Required payload | Trigger / response |
|---|---|---|
| TASK_ACCEPTED | Scope confirmed; execution status; child ID if launched | Once, optional live notification; no reply |
| PROGRESS_REPORT | Material change, evidence reference, remaining work, risk if relevant | Only meaningful milestone or material risk; no reply |
| DECISION_REQUEST | Request ID; issue; why outside authority; viable options and consequences; recommendation; what can continue | Decision required; pause affected work only |
| STATUS_REPORT | State, last verified progress and freshness, outstanding work | In response to request; no reply |
| AMENDMENT_ACK | Revision, affected work, reconciliation status | On amendment; no reply |
| TASK_COMPLETED | Outcome, deliverables, acceptance results/evidence, residual limitations | All mandatory checks passed; no reply |
| TASK_BLOCKED | Blocker, attempts, unmet checks, partial deliverables, exact prerequisite and recovery handle | No viable current path or decision delivery unavailable; actionable reply only |
| TASK_FAILED | Reason, evidence, unmet checks, partial deliverables, remaining risk | Terminal failure; no reply |
| CANCELLED | Confirmed stopped work, residual effects, partial deliverables | Cancellation confirmed; no reply |

## Information policy

Send the minimum sufficient information at each boundary. Executor reports execution facts to Supervisor; Supervisor turns them into verified milestones, decisions and outcomes for Main. Do not forward raw transcripts, routine failures, every retry, speculative progress estimates, or secrets. Prefer stable, accessible artifact paths, commit IDs, check outputs or other evidence references. Include enough detail to locate and understand the evidence; a reference alone is not proof.

Use event-driven, one-way informational notifications. Do not send a message just because time elapsed. Do not require acknowledgement of progress or terminal reports. A decision request is not permission; only an explicit authorized response permits the affected action. If the live channel is unavailable, use the final handback and record undelivered critical information; never claim that Main received an event merely because it was written locally.

On stale or duplicate messages, reconcile against the current revision and active run identity. Do not accept stale results as evidence of a new contract without checking them. A final report must be self-contained even if all prior notifications were lost.
