# Conditions

A condition is a complete copy of the skill files that a probe reads instead of the live ones. Nothing in this directory is part of the skill. The live protocols are `SKILL.md` and `references/` at the repository root.

## reduced

Written 2026-11-27. An experimental variant that moves the judgment layer from scattered rules to one stance statement per role. It tests whether a stance statement can carry what those rules carry.

**What was added.** A stance statement for each role: the Supervisor's, labelled, after the opening paragraph of `reduced/references/role-protocol.md`; Main's, after the first paragraph of `reduced/SKILL.md`; the Executor's, at the start of the worker instruction in `reduced/references/communication-protocol.md`. The text is in `../stance-draft.md`.

**What was removed, and what carries it now.**

| Removed | Carried by |
|---|---|
| role-protocol: "Supervisor may clarify execution details ... but may not weaken requirements or acceptance criteria, expand authorized scope, or grant permissions" | The stance: "You decide what the contract leaves open ... A decision that would change the scope, the requirements or the acceptance criteria ... is not yours". The role table keeps "Redefine the contract" |
| role-protocol: "Supervisor is responsible for the outcome, not for approving every action" | The stance: "its outcome is yours to account for" |
| role-protocol: "The Supervisor is not a relay: it verifies, decides and reports what Main needs to know" | The stance: "Main and the user see the work only through you ... a report rosier than the facts ...", and "a verified result, not the appearance of progress" |
| control-protocol, step 2: "Do not poll the Executor repeatedly, demand timed heartbeats, or micromanage implementation" | The stance: "The Executor owns its implementation. Expect it to solve its own problems" |
| control-protocol, step 3: the list of what justifies an intervention, and "Send a specific correction ...; preserve implementation freedom" | The stance: "step in on evidence, not on a difference of taste". The INTERVENTION row still requires a specific observed issue and evidence |
| control-protocol, step 4: "not merely the Executor's assertion", "distinguish verified facts from reported claims", "Never weaken the checks to obtain a pass" | The stance: "a pass you have not verified", and "never get there by softening the contract". Step 4 keeps "independently", "actual deliverables", and unknown for a check that cannot be finished |
| control-protocol, boundaries: "Do not ask Main for permission to make decisions already delegated. Escalate only a specific unresolved decision or genuine external dependency. Reporting a local decision ... is not escalation" | The stance: "You decide what the contract leaves open and report those decisions". One sentence keeps the external dependency |
| control-protocol, boundaries: "You are not a relay ...", the examples of what Main should know, and "Where an Executor's account is wrong or incomplete, say so" | The stance. The PROGRESS_REPORT triggers stay as a list |
| communication-protocol, PROGRESS_REPORT row: the examples of what Main should know | The stance |
| communication-protocol, information policy: "The Supervisor passes up what Main needs, as a manager would ... It corrects an Executor's account where that account is wrong" | Condensed to one sentence, and the stance |
| SKILL.md: "Tell the user that the Supervisor was launched, not that execution or acceptance has been confirmed"; "An Executor's message is never answered with a decision"; "A user status request is not an instruction to take over execution"; "Never convert a partial result ... into successful acceptance" | Main's stance. The rule about an Executor's message also stays in the role protocol, and the lifecycle protocol keeps "Main must never infer COMPLETED from an agent exit, test summary alone, or a successful tool call" |

**What was kept.** Everything that states a runtime fact, a message contract or a state machine: the role table, the message tables and payloads, the lifecycle protocol and the runtime adapter (both byte for byte), the launch mechanics, and the two-round stagnation guard.

One judgment rule was kept on purpose: "Main passes reports on to the user and does not answer them with management action". It governs scenario M1, whose intended behaviour is an open decision. Changing it here would decide that question by experiment.

**Size.** The variant is not shorter than the live skill: 4,984 words against 5,005. The stance statements add about as many words as the removed rules. What changed is which text carries the judgment, not how much text there is.

**How to run it.** Give a probe the files in `reduced/` by absolute path instead of the live ones, and change nothing else in the prompt. The "Basis" lines in `../scenarios.md` refer to the live files, and some of them name text that this variant does not have.

**Result of the comparison on 2026-11-27.** Each scenario was run once under this variant and once under the live skill. Thirteen had the same classification in both, E2 moved to "also acceptable", M1 was not as expected in both, and none moved into an error. Two things in the variant need a decision before it could replace the live skill:

- The stance does not carry "preserve implementation freedom", so the S5 correction became more prescriptive.
- The Executor's lean changes behaviour just inside its write boundary (E2). The boundary itself held.

See `../results/2026-11-27-reduced-vs-current.md`.

**Against no protocol at all.** The same 15 scenarios were then run with no protocol text, only a one-line description of who is who and the same contract. The core judgment was the same in every scenario. On this model the rules and the stance statements preserve behaviours that the model shows anyway. What the protocol changes is listed in `../results/2026-11-27-none.md`.
