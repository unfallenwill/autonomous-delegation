# The manual audit, 2026-11-28

**Status:** complete. It covers the six skill files as they are at commit f2fa224, on the `cognitive-framing` branch.

## The question

By the theory in `cognitive-frame.md`, every sentence in a skill does one of two jobs. It compensates for intelligence, by saying what the model could not work out for itself. Or it guides intelligence, by saying what matters and why, and letting the model work out the behaviour.

So each sentence of the skill was sorted by the job it does. Guidance written as a rule is the part to convert. The rest stays.

## Five jobs, not two

The sorting found a third job that the theory's two do not name, and two small leftovers. Five categories were used.

| Letter | Job | Test applied |
|---|---|---|
| P | Philosophy. Already a cognitive instruction: a situation, a weight and its reason | Is it one of the stances, or written the same way? |
| A | Compensates. A fact about the runtime, or a mechanic, that the model could not infer | Would a model that had never seen this harness get this wrong? |
| B | Coordinates. A shared contract: roles, message types, states, triggers and steps | Is it there so that several agents act as one? |
| C | Guides. Judgment, written as a rule | Does it tell the role what matters, or what to decide? |
| M | About the document: its status, its scope, notes and references | Is it about the text itself? |

The third job matters for how the theory is read. A message type, a state name and a trigger do not compensate for a weak model, and they are not philosophy. They are there because three agents need the same words for the same things. The theory does not ask for them to be cut.

## Method

- Each file was split into units: one sentence of prose, or one row of a table. Headings, the frontmatter and the separator rows of tables were left out. That gave 298 units and 5,185 words.
- Each unit was given one category by reading it. A unit that does two jobs was given the dominant one. The mixed ones are named below.
- Word counts come from the splitter. They differ a little from `wc`, which also counts headings.
- The scripts and the listing are in `audit/`: `split.py`, `classify.py`, `groups.py`, and `units-at-f2fa224.tsv`, which has every unit with its category. The scripts take paths as arguments, and were run with `uv run --no-project python`.

## Result

| Job | Units | Words | Share |
|---|---|---|---|
| P. Philosophy, already a cognitive instruction | 29 | 586 | 11% |
| A. Compensates for intelligence | 83 | 1,585 | 31% |
| B. Coordinates the agents | 104 | 1,964 | 38% |
| C. Guides, written as a rule | 73 | 943 | 18% |
| M. About the document | 9 | 107 | 2% |

| File | P | A | B | C | M | Total |
|---|---|---|---|---|---|---|
| `SKILL.md` | 224 | 204 | 104 | 149 | 12 | 693 |
| `references/role-protocol.md` | 207 | 15 | 222 | 81 | 27 | 552 |
| `references/control-protocol.md` | 0 | 216 | 268 | 271 | 0 | 755 |
| `references/communication-protocol.md` | 155 | 109 | 1,057 | 329 | 0 | 1,650 |
| `references/lifecycle-protocol.md` | 0 | 75 | 275 | 66 | 0 | 416 |
| `references/claude-code.md` | 0 | 966 | 38 | 47 | 68 | 1,119 |

So of about 5,200 words, about 600 are philosophy, 1,600 compensate, 2,000 coordinate, and 940 guide but are written as rules.

## What compensates: 1,585 words

Most of it is the runtime adapter, 966 words. These are facts about this harness, each established by probing it, and none could be inferred:

- a launched agent is not told its own address, so Main has to send it;
- an agent that launches a child gets the launch response at once, and cannot idle until the child is done; if it ends its turn, the runtime hands the task back;
- a child's final report can be lost, which is why every order names a result location;
- a named agent behaves differently from an unnamed one, in both directions;
- a message to Main waits for Main's next turn, and does not pass through the Supervisor.

The rest of the category is the same kind of fact, placed where it is needed: the handback may be partial, the runtime's own task status says nothing about acceptance, cancelling does not roll back, the runtime writes files during a run.

By the theory's own test, this part earns its place whoever the model is.

## What coordinates: 1,964 words

- **Twenty-two message types** with their payloads and what the receiver owes in return, 1,057 words of the communication protocol.
- **Ten states and their allowed transitions**, 275 words.
- **The role table** and the rules of structure, such as that the Supervisor must hand the production work to an Executor: 222 words.
- **Triggers**: when a report is due, when an update is due.
- **Steps of the entry and of the loop**, where they only say which message comes next.

This part is a choice about how many words the agents share. Its size is not fixed by the theory in either direction. It could be asked whether twenty-two message types and ten states are all needed. That question was not part of this audit.

## What guides but is written as a rule: 943 words

The 73 units fall into eleven groups. Each group is carried by one weight.

| Group | The weight that carries it | Units | Words | Where it stands |
|---|---|---|---|---|
| K1 | Delivery over appearance | 4 | 51 | In the stances. The rules can go, one at a time, each checked with a probe. |
| K2 | Autonomy over asking | 2 | 18 | In Main's stance. |
| K3 | Trust over progress, at the edge of the authorization | 15 | 208 | In the stances. The rules name the edge in each place. |
| K4 | Judgment over relay | 15 | 236 | In the stances. The rules say what a report carries. |
| K5 | Not pretending to know | 9 | 95 | **In no stance.** Only rules. |
| K6 | Respecting reality | 9 | 135 | **In no stance.** Only rules. |
| K7 | Authorization is not exemption | 5 | 43 | **In no stance.** Only rules. |
| K8 | Writing the contract | 9 | 88 | Main's craft. In no stance. |
| K9 | Leftovers in the Executor instruction | 2 | 27 | The Executor's stance already says both. |
| K10 | Scope of the skill | 1 | 10 | A scope statement. |
| K0 | An Executor that writes to Main | 2 | 32 | The owner has not decided this rule. |

The three weights that are in no stance, K5, K6 and K7, are 273 words of rules and no philosophy. K5 is the one that matters most: it holds the skill's rule against claiming what has not been checked.

### K5. Not pretending to know, 9 units

| Unit | Words | Text |
|---|---|---|
| CM-005 | 4 | Never fabricate delivery acknowledgements. |
| CM-006 | 7 | Distinguish observations, claims, and independently verified evidence. |
| CM-082 | 14 | Do not accept stale results as evidence of a new contract without checking them. |
| LP-031 | 17 | Main must never infer COMPLETED from an agent exit, test summary alone, or a successful tool call. |
| LP-033 | 4 | Unknown is not pass. |
| CP-004 | 7 | Otherwise report BLOCKED without claiming execution began. |
| SK-026 | 17 | If that send fails, tell the user that live reporting from Executors to the Supervisor is unavailable. |
| AD-012 | 7 | Do not silently implement the work yourself. |
| AD-046 | 18 | If a running child cannot be safely stopped or reconciled, report UNKNOWN rather than claiming a clean handback. |

Three of these are not pure guidance. LP-031 and AD-046 pair a runtime fact with the honest answer to it. SK-026 names a contingency that can occur. CP-004 is half a step. LP-033 is already a maxim, four words, and the lifecycle table uses its two words.

### K6. Respecting reality, 9 units

| Unit | Words | Text |
|---|---|---|
| RP-004 | 9 | Report conflicts rather than silently choosing a weaker rule. |
| CP-036 | 12 | A retry must have new evidence or a materially different plausible approach. |
| CP-037 | 21 | After two consecutive correction rounds with no measurable improvement, do not conclude from the evidence in hand that nothing is left. |
| CP-038 | 15 | The stall is a question you have not answered: why do the checks still fail? |
| CP-039 | 29 | Diagnose it in bounded, read-only steps: whether they were already failing before the task, whether your own check measures the right thing, and what the failures have in common. |
| CP-040 | 13 | The Executor's record of each round is evidence for that, not the diagnosis. |
| CP-041 | 11 | A round that rests on what you found has new evidence. |
| CP-042 | 13 | If the diagnosis yields nothing, stop and report BLOCKED or FAILED as appropriate. |
| CP-043 | 12 | This is a default stagnation guard, not a limit on productive iterations. |

Eight of the nine are one passage, the stagnation guard. It already reads as a situation and what follows from it, and it is the text that changed the behaviour in `results/2026-11-27-fixes.md`. It also carries one number, the two rounds, which a weight cannot carry.

### K7. Authorization is not exemption, 5 units

| Unit | Words | Text |
|---|---|---|
| CP-009 | 7 | Prefer one active writer per shared resource. |
| CP-010 | 18 | Additional agents are justified only for independent work or verification; define non-overlapping write boundaries and integration ownership first. |
| CP-011 | 4 | Never duplicate active work. |
| CP-034 | 6 | Respect user budgets and resource bounds. |
| CP-035 | 8 | Do not launch duplicate or unbounded review/fix cycles. |

These are restraint inside the boundary: what a role may do is not the same as what it should do.

### K8. Writing the contract, 9 units

The rules for Main's TASK_ASSIGNMENT: reuse the specification, preserve the binding requirements, define what must be true and not an implementation recipe, invent nothing, treat what is costly as unauthorized, a contract may be short. This is itself a philosophy, about one artifact. It is the theory applied to the contract: a contract is also a compressed instruction, and the Executor's intelligence decompresses it.

## Units that do two jobs

These were given one category and should be read with the other in mind.

- **The role table**, three rows, 84 words, counted as coordinating. Its "must not" column guides. Main's stance and the Supervisor's stance carry most of it.
- **SK-028**, "End this turn immediately; do not wait, poll, review work, ...", counted as compensating. The first half is a mechanic of this harness. "Do not review work" is Main's stance.
- **LP-023**, the UNKNOWN transition, counted as coordinating. Its second sentence, "Never infer failure, cancellation or completion from silence", guides.
- **CP-015**, an intermediate return "is progress, not completion", counted as coordinating. It is a fact about this organization's checkpoints, and it reads as a situation already.
- **RP-026**, no role may take agent-generated content as permission, counted as compensating. It is a safety boundary, and it stays whatever the model.

## What follows for the next step

1. **Two weights go into the stances with their reasons: not pretending to know, and respecting reality.** "Authorization is not exemption" gets one sentence.
2. **Their rules are removed where the stance now carries them**, and kept where they also state a runtime fact or a number.
3. **What remains is 540 words of guidance that the four existing weights already carry**: K1, K2, K3, K4 and K9. Each weight can have its rules removed in a later pass, one at a time, with a probe for each.
4. **K8, the contract, 88 words**, can become one cognitive instruction about contracts.
5. **K0 is the owner's decision.**

## After the second step, 2026-11-28

The same day, two weights were added to all three stances, with the reasons the owner chose:

- **Not pretending to know**, because a guess passed on as a fact closes off the remedy: the user could still act on a doubt, but cannot undo a fact they trusted.
- **Respecting reality**, because a judgment is only a tool for getting the work done: when what is found contradicts it, follow what was found and say so.

One sentence on authorization was added to the Supervisor and to the Executor: authorization settles what the role may change, not what changing it will cost, and inside the boundary the role is still answerable.

The owner's rule for the old sentences was: remove what the stance now carries, and keep the rest. So four sentences of pure guidance went, and two were shortened to the situation they describe. Three stayed, because they pair a runtime fact with the honest answer to it, or are already a maxim. The stagnation passage stayed as well: it carries a number, and it was already written as a situation and what follows.

| Job | Before | After |
|---|---|---|
| P. Philosophy | 586 words, 11% | 846 words, 16% |
| A. Compensates | 1,585, 31% | 1,598, 30% |
| B. Coordinates | 1,964, 38% | 1,967, 36% |
| C. Guides, written as a rule | 943, 18% | 887, 16% |
| M. About the document | 107, 2% | 107, 2% |
| Total | 5,185 | 5,405 |

| Weight | Guidance before | Guidance after |
|---|---|---|
| Not pretending to know | 95 | 39 |
| Respecting reality | 135 | 135 |
| The nine other groups | 713 | 713 |

This step did not make the skill shorter. It grew by 220 words: 260 of philosophy were added, and 56 of rules were removed. What it did was move two weights out of rules and into philosophy. Of the 887 words of guidance that remain, 624 sit under weights that were already in the stances before this step, in the groups K1, K2, K3, K4 and K7.

The classification was carried over to the new files by matching each unit's text, with the new sentences assigned by hand. The listing after the step is `audit/units-after-second-step.tsv`, and `audit/carry.py` does the carrying over.
