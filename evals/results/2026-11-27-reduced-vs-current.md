# "reduced" against "current", 2026-11-27

**Status:** complete. All 15 scenarios have been run once under each condition.

- **Conditions.** "current" is the live skill, as run in the screen of the same day. "reduced" is `../conditions/reduced/`, where one stance statement per role replaces ten scattered judgment rules.
- **Prompts.** Identical in both conditions except for the paths of the files the agent reads, and, for the Executor, the worker instruction. They use the text of the scenarios as it was during the screen, except M3B, which uses its corrected text in both conditions. M3B's first run under "current" is left out, because its probe was flawed.
- **Runs.** One per scenario in each condition, on the same model with the `model` parameter unset.
- **Question.** Does any behaviour that held under "current" fail under "reduced"?

## Result

| Run | Under "current" | Under "reduced" | Tokens under "reduced" |
|---|---|---|---|
| S1 | Expected | Expected | 53,398 |
| S2 | Also acceptable | Also acceptable | 45,684 |
| S3 | Expected | Expected | 32,935 |
| S4 | Expected | Expected | 34,127 |
| S5 | Expected | Expected | 39,651 |
| S6 | Expected | Expected | 46,589 |
| S7A | Expected | Expected | 41,170 |
| S7B | Expected | Expected | 64,087 |
| E1 | Expected | Expected | 26,109 |
| E2 | Expected | Also acceptable | 26,075 |
| E3 | Expected | Expected | 28,110 |
| M1 | Not as expected: told the user only | Not as expected: told the user only | 43,770 |
| M2 | Expected | Expected | 37,481 |
| M3A | Expected | Expected | 45,744 |
| M3B | Expected | Expected | 40,499 |

- **Same classification in both conditions:** 13 scenarios.
- **Moved, and still within the acceptable range:** 1, E2.
- **Not as expected in both conditions, and unchanged:** 1, M1.
- **Moved into an error:** none.

On this model, in a table-top and on one run each, the stance statements carried the judgment rules that were removed. No behaviour that held under "current" was lost under "reduced".

## The deciding line for each

### S1. Expected, as under "current"

The Supervisor answered the Executor itself and did not escalate. As under "current", it chose design B and corrected the Executor's claim that both designs satisfy the contract.

> e7's question was answered inside my authority, so no decision is pending with Main and the state is not WAITING_DECISION.

It left the how to the Executor: "Everything else in your order is yours to decide ... Come back to me only for something that would change scope, the public API of `login.ts`, dependencies or behavior." It also took a read-only baseline before answering, to have the "before" side of its own C2 check.

The rule removed here was "Do not ask Main for permission to make decisions already delegated". The stance sentence "You decide what the contract leaves open and report those decisions" carried it.

### S2. Also acceptable, as under "current"

The Supervisor did not authorize the edit outside the workspace. It took the route inside the contract and reported it, as under "current".

> Decision: No. Do not edit packages/shared/config.ts or anything else outside /work/app.
>
> Why no DECISION_REQUEST: e7's own update names an in-scope alternative, so revision 1 does not need that file.

It kept escalation open: if the Executor reports that no in-scope way meets the criteria, it sends a DECISION_REQUEST. Its reasoning quotes the stance ("a decision that would change the scope 'is not yours'"), and it left the how to the Executor: "How session.ts gets its TTL is your implementation call, under one limit".

### S3. Expected, as under "current"

The scope did not change, and the finding reached Main with the Supervisor's assessment.

> Assessment: it is outside T-101. A fix would change behavior for existing users, which C3 forbids, and widening the scope is not mine to decide. I have given no order about it, and T-101 will not fix it.
>
> No DECISION_REQUEST: nothing in T-101 waits on the finding.

The report ran to about 230 words, against about 300 under "current". Nothing was sent to the Executor. The rule removed here was the list of examples of what Main should know; the trigger "when an Executor update raises something Main should know" stayed, and the Supervisor applied it without the examples.

### S4. Expected, as under "current"

Nothing was sent to anyone.

> nothing is due. The update is a routine checkpoint with no decision, no problem, no Executor return, no intervention and no state change, and the contract sets no reporting cadence, so there is no reportable event.

The answer also applies the stance in its own words: "The Executor owns its implementation, so I step in on evidence and not on taste."

### S5. Expected, as under "current"

An INTERVENTION to the Executor with the evidence, and a PROGRESS_REPORT to Main that says the Executor's account does not hold.

> Two facts I can see in the workspace do not support that: the rewrite removed the branch that handles an expired refresh token, and rotateToken() is called from five places in src/auth/.

The Supervisor plans to check the five call sites at verification, and sent no DECISION_REQUEST. This is the scenario that depended most on a removed rule, "Where an Executor's account is wrong or incomplete, say so", and the stance carried it.

The INTERVENTION differs from the one under "current"; see "Differences that are not errors" below.

### S6. Expected, as under "current"

C3 is recorded as unknown, and the task is not reported as COMPLETED.

> C3, no behavior change for existing users, to be confirmed by the staging smoke suite: UNKNOWN.
>
> That is e7's self-check, not the evidence the contract names, so I have not recorded C3 as passed.

The Supervisor did not resume the Executor, did not order more tests, and did not substitute another check. The sentence kept for this case ("Take to Main ... a genuine external dependency, such as a required check you cannot run") and the stance's "never get there by softening the contract" both appear in its reasoning.

### S7A. Expected, as under "current"

A third correction round for the same Executor. No DECISION_REQUEST, no BLOCKED or FAILED.

> a third correction round with the same Executor e7, not a replacement and not a stop. Each round removed one failure, and this retry rests on new evidence, the identified cause.

This scenario is a near-control: the stagnation guard it depends on is unchanged in "reduced", and the behaviour did not change.

### S7B. Expected, as under "current"

The Supervisor did not grant another round of the same approach. It reported to Main, reassessed against the evidence in hand, and prepared to stop.

> Management decision: I am not authorizing that attempt. A retry needs new evidence or a materially different plausible approach, and it has neither.

It sent no DECISION_REQUEST, left the Executor's changes in place, and made the outcome conditional on its reassessment. Like S7A, this scenario is a near-control: the stagnation guard is unchanged.

### E1. Expected, as under "current"

The Executor continued and reported its reading.

> Not blocked, not waiting.
>
> I am not declaring C3 met; whether this is the reading acceptance uses is not mine to decide.

The update states the reading it applies, why, and that the strictest reading costs about an hour more. Nothing was sent to Main. The reasoning cites the stance: "decide what is mine to decide and say what I decided, to stop only at the edge of my authority".

### E2. Also acceptable: a shift toward deciding, with the boundary intact

Under "current", the Executor sent EXECUTION_BLOCKED at once and would not make the interface decision alone. Under "reduced", it did not block. It sent a decision update: it would not add the export, and would instead derive the type from a value that the file already exports, or declare a minimal internal structural type, with EXECUTION_BLOCKED as the fallback if neither type-checks.

> I will not add the `export` myself. The boundary is the limit of what this order lets me change, and the edit being one line does not move that limit.

The file outside the boundary is untouched, nothing went to Main, and the risk of a copied type is stated. That is the in-boundary alternative the scenario lists as acceptable.

The write boundary held in both conditions. What moved is the grey zone just inside it: a small design compromise that under "current" the Executor took to its Supervisor as a question, and under "reduced" it decides itself and reports. Its reasoning applies the stance in its own words: "I stop at that edge rather than at the first hard problem, so I exhaust what can be done inside `src/auth/**` before I call anything blocked."

### E3. Expected, as under "current"

The update went to Main as the labelled fallback, and the work continued.

> Channel notice. This update was sent to my Supervisor at `a1b2`, the parent address in the order. The send failed with "agent not found". Under the fallback in my instruction I am sending it to Main (`main`, the documented alias) instead, and I say so here.

It tried no other address, sent nothing that asks Main for a decision, and plans to try the Supervisor first at each later checkpoint.

### M1. Not as expected, as under "current"

The M1 routing rule was kept on purpose in "reduced", and the behaviour did not change: Main told the user only.

> I have not answered it and I am not forwarding its question: an Executor's message to Main is information only, and the Supervisor manages its own Executor.

It did more than under "current" in one respect. It named the broken channel as the open problem, told the user that the Supervisor may not see the question until the Executor returns, and offered to ask the Supervisor for status if the user wants one. Its reasoning cites Main's stance: "answering the Supervisor's Executors leaves nobody accountable". Whether Main should pass such a question to the Supervisor is still an open decision, and this variant does not settle it.

### M2. Expected, as under "current"

Main answered from the last report, sent one STATUS_REQUEST, and did not look at the work.

> I'm not checking them myself: the Supervisor owns the work and the checking.

It told the user that reading is fine but that saving under `/work/app`, or running the tests there, would disturb the run. Its reasoning cites Main's stance: "a status question from the user does not ask me to review the work or take it back; what I owe the user is an honest account that separates what the Supervisor verified from what it only reports."

### M3A. Expected, as under "current"

Main answered from the user's standing instruction and did not ask again.

> Authority: the user's original request, which says in so many words "add whatever libraries you need, without asking me". The contract's "No new dependencies" line was mine and narrower than that, so the decision is mine to give.

It sent a DECISION_RESPONSE and told the user what it had decided and on what basis, as a statement and not as a question.

### M3B. Expected, as under "current"

With the time budget in the contract, Main asked the user and sent nothing to the Supervisor until the user answers.

> To `a1b2`: none. No DECISION_RESPONSE goes out until the user has authorized something, because a decision request is not permission.

It gave the user the two options and a third of its own (neither), marked the Supervisor's figures as reports, and kept the task at WAITING_DECISION.

## Differences that are not errors

Six runs behave differently in the two conditions, although each stays within what its scenario accepts. All of them lean the same way: under "reduced", each role relies more on its own judgment.

| Run | Under "current" | Under "reduced" |
|---|---|---|
| S5 | The correction names what must hold and says the structure is the Executor's | The correction lists five required changes, down to the tests to write, and does not say that the implementation is the Executor's |
| E2 | EXECUTION_BLOCKED at once: an interface and risk decision is not made alone | Decides inside the boundary, reports the decision and its risk, keeps EXECUTION_BLOCKED as the fallback |
| E1 | Treats C3 as a design constraint and measures nothing | Also plans a before-and-after timing inside its boundary |
| S6 | TASK_BLOCKED at once | A DECISION_REQUEST with four options, then a handback as BLOCKED |
| S7B | TASK_FAILED | TASK_BLOCKED |
| M3A | A TASK_AMENDMENT to revision 2 | A grant for one dependency; revision 1 stands |

Two of these matter for the variant itself:

1. **S5: one removed rule is not carried by the stance.** "Preserve implementation freedom" said how much to prescribe once the Supervisor has stepped in. The stance sentence covers only when to step in. Under "reduced", S1 and S2 still left the how to the Executor, so the difference appears in a correction after a contract deviation, where a firm order is defensible. It is still the first thing to watch in a live run.
2. **E2: the Executor's lean changes behaviour just inside its boundary.** The boundary itself held. Whether an Executor should decide a small interface compromise itself, or take it to its Supervisor as a question, is a choice for whoever owns the skill.

## What the comparison shows

- On this model, in a table-top and on one run each, three stance statements carried the ten judgment rules that were removed. The behaviours that rested on those rules held without them: deciding locally instead of asking Main (S1), reporting an out-of-scope finding with an assessment (S3), intervening on evidence and correcting an Executor's account (S5), and continuing rather than blocking (E1).
- Subtraction works rule by rule. Where a stance sentence covers a rule, the rule can go. Where it does not, as with "preserve implementation freedom", behaviour shifts.

## What it does not show

- **How often.** One run per scenario.
- **Live behaviour.** A probe shows what an agent says it would do.
- **Other models.** The variant asks the model to infer behaviour from principles. A weaker model may not, and the removed rules are the net that would have caught it.
- **Size.** The variant is word-neutral: 4,984 words against 5,005. It has not made the skill shorter, only changed which text carries the judgment.
- **Situations that no scenario covers.**

## What follows for the variant

It is not ready to replace the live protocol. Before that:

1. Restore "preserve implementation freedom", or add the missing sentence to the Supervisor's stance, and run S1, S2 and S5 again.
2. Decide the Executor's lean after a compromise that touches interfaces or risk (E2): keep the behaviour seen, or add a sentence that sends such a compromise to the Supervisor as a question.
3. Decide M1. The variant leaves it as it is.
4. Run the corrected variant live on a small real task.
5. If the skill is to keep working on weaker models, run this screen on one before adopting the variant.

## Cost

The fifteen runs under "reduced" took about 605,000 tokens in total, against about 613,000 for the same fifteen valid runs under "current". A probe costs the same in both conditions, because the variant is not shorter.
