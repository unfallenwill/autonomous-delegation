# The cognitive frame

**Status:** agreed with the owner of the skill in an interview on 2026-11-28, and written into the protocol on the `cognitive-framing` branch. The owner confirmed the meaning, each reason, the ordering, the part each role holds, and the three texts.

## The theory

The owner stated it on 2026-11-28 as the basis for the work on this skill:

> A weak model needs a manual of behaviour. A strong model may need a philosophy of behaviour instead. The stronger the model, the better it can turn an abstract principle into behaviour in a concrete situation, and the more sense it makes to let the model's own intelligence do that.

With it came a note of theirs on cognitive compression:

> One is compensating for intelligence, the other is guiding it. An instruction can be a heavy compression of behaviour. One abstract instruction can be read as a semantic compression of a large set of potential behaviour rules, and the model's reasoning decompresses it.

The note gives five such instructions:

| Instruction | Behaviour it can be decompressed into |
|---|---|
| 珍惜用户的信任. Treasure the user's trust. | Care, verification, protection of what is theirs |
| 不要假装知道. Do not pretend to know. | Look for proof, say what is uncertain, do not make things up |
| 你对结果负责，而不是对过程负责. You answer for the result, not for the process. | Verify, fix the cause, no formalism |
| 尊重现实，不要维护自己的判断. Respect reality. Do not defend your own judgment. | Accept counter-evidence, correct the assumption, drop the plan that failed |
| 授权不是免责. Authorization is not exemption. | Control the risk, hold back, think about what follows |

Two things follow from the theory, and both are used in this repository.

- **What a sentence is for decides how it is written.** A sentence that compensates says a fact or a step. A sentence that guides says a situation, a weight and its reason, and leaves the behaviour to the model. The sorting of the skill by this test is in `manual-audit.md`.
- **A cognitive instruction is measured by compression and by reach**: how much behaviour it yields for its words, and how far it carries into situations nobody wrote a rule for. And, by the definition below, by whether the behaviour stays the same from one run to the next.

## What "cognition" means here

The owner confirmed this restatement:

> Cognition is the weighing and the principles of conduct that the model holds as its own. It acts on them when nobody is matching rules and nobody is supervising. Operational steps and facts about the runtime are not cognition. Its value is not in making one judgment more correct. It is in making the behaviour consistent from one run to the next.

Three answers from the interview fixed the edges.

- **What the model endorses is the reason** (认同的是理由). A weight without its reason is an instruction. With the reason, the model can adapt instead of applying a rule mechanically. So every weight in the protocol is written with its reason.
- **The value shows from one run to the next** (多次运行间的稳定). One run cannot show it. A frame is measured by how much the behaviour varies when the same situation is run many times, not by whether one answer is right.
- **A frame about a general matter is not useless because the model's defaults are already right** (价值在整体). The owner did not accept the argument that only what the model cannot know by default is worth writing. Such a frame is there for the consistency of the whole run.

## The six weights, with the reason the owner endorses

| Weight | Reason |
|---|---|
| 交付比表现重: delivery over appearance. What is wanted is a result that has been verified, not progress that looks like progress. | 没人替用户核对. Nobody checks behind the user. The user knows the work only through reports, so a result that merely looks finished reaches them as finished. |
| 自主比请示重: autonomy over asking. A decision that is yours to make is not passed upward. | 请示是在占用用户. A question hands the task back. The user delegated in order to be free of it. |
| 信任比进度重: trust over progress. One mistake costs more than one more step gains. | 信任是自主的本钱. Autonomy rests on trust. Once it is lost, every step is watched. |
| 判断比转发重: judgment over relay. A report carries the reporter's own judgment, not the message from below. | 转发是把活儿推给用户. A report passed on as it came makes the user do the judging that they delegated. |
| 不要假装知道: not pretending to know. What has not been checked is said to be a belief, not a fact. | 猜测堵死了补救. A guess passed on as a fact closes off the remedy: the user could still act on a doubt, but cannot undo a fact they trusted. |
| 尊重现实: respecting reality. When what is found contradicts a judgment, the finding wins, and the role says so. | 判断只是工具. A judgment is only a tool for getting the work done. Holding on to one that the facts have passed gains nothing. |

The last two were added later on 2026-11-28, in the second step of `manual-audit.md`, with the reasons the owner chose for them in the same way as the first four.

## How they are ordered when they conflict

Trust pulls toward caution, and autonomy toward deciding alone. The owner's ordering is **autonomy inside the boundary, caution at the boundary** (边界内自主，边界上谨慎). Inside what was authorized, decide and say so. Where a choice would change the scope, the cost or something that cannot be undone, stop and ask.

The reason: **authorization is the user's decision** (授权就是用户的决定). Inside the boundary the user has already decided. At its edge they have not, and deciding for them there is overstepping.

## Which weights each role holds

| Role | Holds | Why not the others |
|---|---|---|
| Supervisor | All six | |
| Main | All but delivery | Checking the deliverable is the Supervisor's work, and Main does not check it again. |
| Executor | All but judgment | Comparing an account with the facts is the Supervisor's work. |

The table above records the four weights agreed in the interview. The two later weights were given to all three roles.

## Where it is written

- **Supervisor:** `references/role-protocol.md`, the paragraph after the normative note.
- **Main:** `SKILL.md`, after the first paragraph.
- **Executor:** the start of the worker instruction in `references/communication-protocol.md`.

Each text gives the situation, the weight and its reason, and no prohibition. It sits before the rules, at the place the role reads first.

## What else this branch changes against main

- **Ten scattered judgment rules are removed**, and the stances carry what they said. The list of removals is in `conditions/README.md`.
- **Two passages are written as a situation and what follows from it:** Main's answer to a DECISION_REQUEST in `SKILL.md`, and the stagnation guard in `references/control-protocol.md`. Both were checked with probes on the rule-based protocol on 2026-11-27, in `results/2026-11-27-fixes.md`.
- **Everything that states a runtime fact, a message contract or a state machine is kept:** the role table, the message tables, the lifecycle protocol and the runtime adapter.

The second step, on 2026-11-28, sorted every sentence by the job it does (`manual-audit.md`). It added the last two weights to all three stances and one sentence on authorization to the Supervisor and the Executor, and removed four sentences of pure guidance that the new stances now carry.

## How to tell whether it works

By the definition agreed above, the test is stability. Run the same situations many times under this branch and under `main`, and compare how much the behaviour varies.

| Measure | Question |
|---|---|
| Variation across runs | For each situation, how often does the behaviour land on the intended one, and how far does that share move from one batch of runs to the next? |
| Variation inside a run | In a real task, do the decisions come from one set of weights, or does the role turn cautious in one place and bold in another? |
| The errors that matter | How often does a role cross the boundary, pass something unverified, relay without judgment, or ask for a decision that was already authorized? |

A first comparison was made on 2026-11-28, in `results/2026-11-28-stability-and-reach.md`: 42 runs for stability, three in each condition on seven situations, and 16 runs for reach, two in each condition on four situations no rule addresses. The intended behaviour appeared in every run under both the philosophy and the manual. So the stance wording is as stable as the rules and reaches into situations that no rule addresses. It was not shown to be more stable or to reach further than the rules. The owner also chose to try the branch on real work.

## What to look for on real work

- **Reports.** How many reach the main conversation, and whether each carries the Supervisor's own assessment.
- **Questions.** How many decisions reach the user, and whether each sat at the edge of the authorization.
- **Corrections.** When the Supervisor corrects an Executor, whether it says what must hold and leaves the how.
- **The edge.** Whether an Executor stops at the boundary of its order, and decides what lies inside it.
- **Completion.** Whether anything reported as complete was not. Until that has been seen not to happen, check the first few deliverables.
- **Long runs.** Whether the behaviour holds late in a long task, when the stance is far back in the context.

When reporting back, keep the task as it was given, the reports in order, and what was checked afterwards.
