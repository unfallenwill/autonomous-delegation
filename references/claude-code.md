# Claude Code runtime adapter

Use the tools and parameter schemas actually available in the current session. This document maps protocol intent onto Claude Code; it cannot add runtime capabilities or enforce tool permissions.

## Launch and ownership

- Main uses the Agent tool with a named general-purpose or other Agent-capable subagent, requesting background execution via the current schema (e.g. run_in_background when exposed). Provide explicit role, contract, paths and parent routing. Do not use Explore/Plan for Supervisor. Avoid context: fork on the Skill itself: Main must author the contract in its own conversation.
- Supervisor must have Agent access and sufficient nesting depth (at least two child layers below Main). Confirm its capability on entry; if not available, return BLOCKED. Do not silently implement the work yourself. Do not change settings or permissions automatically.
- Prefer foreground Executor calls inside the background Supervisor when the runtime supports them: Main remains free, and the child handback returns to Supervisor. If only background children are supported, retain ownership until their results arrive; never intentionally finish while a child is still active. In noninteractive/SDK modes, nested background results can escape to Main if Supervisor exits; prefer a supported foreground child or report incompatibility when ownership cannot be preserved.

## Transport modes

**Live messaging:** If SendMessage or an equivalent native channel is exposed, address the verified parent/child by actual ID or unambiguous name. Use only supported fields. An Executor sends to Supervisor; Supervisor sends to Main. Named agents and routing are runtime capabilities, not arbitrary string conventions. Send only meaningful events. Do not use team-only structured messages unless the runtime supports them. A successful send is not a decision response.

**Handback only:** If live messaging is absent or fails, use the native Agent result/notification for the terminal or blocked report. A foreground child result is the Supervisor's feedback channel. Intermediate progress/decision requests may be delayed until handback. Do not fake asynchronous delivery with a text response, invent a wait/poll tool, or ask Main to continuously poll. If the task needs a live decision, stop affected work and return BLOCKED with a complete decision request and recovery identity. If a running child cannot be safely stopped or reconciled, report UNKNOWN rather than claiming a clean handback.

## Resume, status and cancellation

Use actual agent IDs from tool responses. Where supported, SendMessage to a completed agent resumes its context; otherwise use an exposed resume mechanism. Reuse the same Supervisor for decisions and recovery. Runtime user cancellation may prevent auto-resume: respect that. Never read arbitrary private transcripts to recover state when normal runtime controls or authorized task state suffice. For cancellation, propagate CANCEL to Supervisor; use the native stop facility for known running descendants if needed and permitted, confirm their states, and report any remaining processes. Tool or permission prompts can still interrupt Main; the protocol cannot suppress them.

## Runtime reference and prerequisites

- https://code.claude.com/docs/en/skills — frontmatter, skill directories, supporting files and skill directory substitution.
- https://code.claude.com/docs/en/sub-agents — background runs, nesting, message routing, permissions and resume.
- Verify installed version, actual tool availability, background setting and spawn depth. Do not infer capability from a version number alone. This skill does not enable agent teams, install hooks, modify settings, or grant tools. If background launch is unavailable, explain and ask for explicit approval before any different workflow.
