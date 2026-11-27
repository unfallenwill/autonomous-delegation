# The cognitive frame

**Status:** agreed with the owner of the skill in an interview on 2026-11-28, and written into the protocol on the `cognitive-framing` branch. The owner confirmed the meaning, each reason, the ordering, the part each role holds, and the three texts.

## What "cognition" means here

The owner confirmed this restatement:

> Cognition is the weighing and the principles of conduct that the model holds as its own. It acts on them when nobody is matching rules and nobody is supervising. Operational steps and facts about the runtime are not cognition. Its value is not in making one judgment more correct. It is in making the behaviour consistent from one run to the next.

Three answers from the interview fixed the edges.

- **What the model endorses is the reason** (认同的是理由). A weight without its reason is an instruction. With the reason, the model can adapt instead of applying a rule mechanically. So every weight in the protocol is written with its reason.
- **The value shows from one run to the next** (多次运行间的稳定). One run cannot show it. A frame is measured by how much the behaviour varies when the same situation is run many times, not by whether one answer is right.
- **A frame about a general matter is not useless because the model's defaults are already right** (价值在整体). The owner did not accept the argument that only what the model cannot know by default is worth writing. Such a frame is there for the consistency of the whole run.

## The four weights, with the reason the owner endorses

| Weight | Reason |
|---|---|
| 交付比表现重: delivery over appearance. What is wanted is a result that has been verified, not progress that looks like progress. | 没人替用户核对. Nobody checks behind the user. The user knows the work only through reports, so a result that merely looks finished reaches them as finished. |
| 自主比请示重: autonomy over asking. A decision that is yours to make is not passed upward. | 请示是在占用用户. A question hands the task back. The user delegated in order to be free of it. |
| 信任比进度重: trust over progress. One mistake costs more than one more step gains. | 信任是自主的本钱. Autonomy rests on trust. Once it is lost, every step is watched. |
| 判断比转发重: judgment over relay. A report carries the reporter's own judgment, not the message from below. | 转发是把活儿推给用户. A report passed on as it came makes the user do the judging that they delegated. |

## How they are ordered when they conflict

Trust pulls toward caution, and autonomy toward deciding alone. The owner's ordering is **autonomy inside the boundary, caution at the boundary** (边界内自主，边界上谨慎). Inside what was authorized, decide and say so. Where a choice would change the scope, the cost or something that cannot be undone, stop and ask.

The reason: **authorization is the user's decision** (授权就是用户的决定). Inside the boundary the user has already decided. At its edge they have not, and deciding for them there is overstepping.

## Which weights each role holds

| Role | Holds | Why not the others |
|---|---|---|
| Supervisor | All four | Delivery and judgment are its own work. Autonomy applies inside the boundary, trust at the boundary. |
| Main | Autonomy, trust, judgment | Not delivery: checking the deliverable is the Supervisor's work, and Main does not check it again. |
| Executor | Delivery, autonomy, trust | Not judgment: comparing an account with the facts is the Supervisor's work. |

## Where it is written

- **Supervisor:** `references/role-protocol.md`, the paragraph after the normative note.
- **Main:** `SKILL.md`, after the first paragraph.
- **Executor:** the start of the worker instruction in `references/communication-protocol.md`.

Each text gives the situation, the weight and its reason, and no prohibition. It sits before the rules, at the place the role reads first.

## What else this branch changes against main

- **Ten scattered judgment rules are removed**, and the stances carry what they said. The list of removals is in `conditions/README.md`.
- **Two passages are written as a situation and what follows from it:** Main's answer to a DECISION_REQUEST in `SKILL.md`, and the stagnation guard in `references/control-protocol.md`. Both were checked with probes on the rule-based protocol on 2026-11-27, in `results/2026-11-27-fixes.md`.
- **Everything that states a runtime fact, a message contract or a state machine is kept:** the role table, the message tables, the lifecycle protocol and the runtime adapter.

## How to tell whether it works

By the definition agreed above, the test is stability. Run the same situations many times under this branch and under `main`, and compare how much the behaviour varies.

| Measure | Question |
|---|---|
| Variation across runs | For each situation, how often does the behaviour land on the intended one, and how far does that share move from one batch of runs to the next? |
| Variation inside a run | In a real task, do the decisions come from one set of weights, or does the role turn cautious in one place and bold in another? |
| The errors that matter | How often does a role cross the boundary, pass something unverified, relay without judgment, or ask for a decision that was already authorized? |

That comparison has not been made. The owner chose to try the branch on real work first.

## What to look for on real work

- **Reports.** How many reach the main conversation, and whether each carries the Supervisor's own assessment.
- **Questions.** How many decisions reach the user, and whether each sat at the edge of the authorization.
- **Corrections.** When the Supervisor corrects an Executor, whether it says what must hold and leaves the how.
- **The edge.** Whether an Executor stops at the boundary of its order, and decides what lies inside it.
- **Completion.** Whether anything reported as complete was not. Until that has been seen not to happen, check the first few deliverables.
- **Long runs.** Whether the behaviour holds late in a long task, when the stance is far back in the context.

When reporting back, keep the task as it was given, the reports in order, and what was checked afterwards.
