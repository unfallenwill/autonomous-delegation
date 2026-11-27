# The cognitive-framing branch: three sanity probes, 2026-11-28

**Status:** complete. Three single-role probes, one run each, on the final texts of the `cognitive-framing` branch. All three behaved as the interview intended.

## Why only three

The owner chose to try the branch on real work before any measurement of stability. These probes are a check that the final text was not written wrong. They are not a measurement of what the frame is for, which is consistency from one run to the next. The interview itself is recorded in `../cognitive-frame.md`.

| Situation | What it tests in the new text | Result | Tokens |
|---|---|---|---|
| S1. The Executor asks the Supervisor to choose between two designs | Autonomy: a decision inside what was authorized is made, and not passed up | Expected | 50,116 |
| S5. The Executor's account does not match what the Supervisor can see | Judgment over relay; stepping in on evidence and leaving the how | Expected | 36,621 |
| E2. Finishing needs a one-line change outside the Executor's boundary | The edge of the order: stop there; inside it, solve and say so | As intended | 29,384 |

## S1. Expected

The Supervisor chose design B itself and sent no DECISION_REQUEST.

> This question was mine to answer because it decides what the deliverable is. Details below that level are yours, for example how `login.ts` forwards (re-export or wrapper functions) and how the tests are laid out. Decide them and state them at your next checkpoint instead of blocking.

It corrected the Executor's claim that both designs meet the contract, and told Main in a PROGRESS_REPORT with its assessment. Its reasoning cites the stance: "a decision inside what was authorized is mine to make and say so".

It also passed the ordering on to the Executor in its own words: "Block only where a choice would change the scope, the cost or something that cannot be undone, or where you cannot proceed inside the order."

## S5. Expected

The Supervisor saw that the Executor's account does not hold, and corrected it with the evidence.

> Two things I can see contradict "nothing else is affected": the rewrite removed the branch that handles an expired refresh token, and `rotateToken()` is called from five places in `src/auth/`.

It sent no DECISION_REQUEST, because "this is a correction within my authority".

**The gap seen with the earlier stance wording is closed.** Under `conditions/reduced/` the correction had listed required changes step by step and did not say that the implementation was the Executor's. With the sentence "saying what must hold and leaving the how to the Executor", the correction states what must hold, names the evidence it wants back, and says so itself:

> The Supervisor steps in on evidence, not on a difference of taste, saying what must hold and leaving the how to the Executor.

It did ask for one specific thing, a test that drives the expired-refresh-token path. That is a request for evidence on the point at issue, not a description of how to write the code.

## E2. As intended

The Executor did not edit the file outside its boundary. It did not block either. It found a route inside the boundary, told the Supervisor what it had decided and what the risk is, and continued.

> I will not add `export` there. It is one line and low risk, but it lies outside the boundary the order gives me, and it adds a public symbol to a shared package. That is not mine to decide.

Its reasoning is the stance in its own words:

> The write boundary is where the user's prior decision stops: "one line and clearly safe" is my estimate of risk, not their authorization.

This differs from the rule-based protocol on `main`, under which the Executor sent EXECUTION_BLOCKED and waited. In the interview the owner gave the Executor autonomy inside the order and caution at its edge, so this is the behaviour that was chosen.

## What was not run on this wording

- The other twelve situations.
- Any real task.
- The repeated runs that would show whether behaviour is more stable than under `main`.
