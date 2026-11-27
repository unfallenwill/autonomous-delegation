# A harder task, three ways, with hidden tests, 2026-11-27

**Status:** complete. All three runs are scored. All three scored full marks on the hidden tests, and the chain cost the most.

One run of each. One run each can show that a difference exists. It cannot show that there is none.

## The task

Implement the print order pricing specified in `docs/PRICING.md`, in `src/billing/pricing.js`, with unit tests. The document has eleven rules, a list of invalid orders and a required shape for the returned object. What makes it harder than the first task is that the rules interact:

- the volume discount starts at exactly 100 sheets and again at 500;
- a double-sided item with an odd page count needs one more sheet;
- both discounts are applied and only then is a line rounded, once, half up;
- the express surcharge is a quarter of the discounted line amount, and gets no discount itself;
- the minimum order charge is applied after the discounts and before the surcharge, and the surcharge ignores it;
- an empty order costs nothing.

The document gives three worked examples. It states every rule in plain words and gives a formula for the one that is easiest to get wrong.

The workspace is the first task's project with the document, an empty `src/billing/pricing.js` and a README entry added. Baseline commit 15c2465, a clean tree, 8 tests passing. Each run started from a clean clone.

## How quality is measured

The same way for all three runs, by tests the agents never saw:

- 41 tests in one file, covering about 770 orders: the three examples with the values the document states, each rule and each interaction above, the empty order, fields left out, and every kind of invalid order.
- The expected values are computed from the document in whole-number arithmetic.
- Only the properties the document names are compared, so that an extra property is not punished.
- Before any run, the tests passed 41 of 41 on a reference solution of mine, and failed on the empty stub.

They are kept in a folder with an unrelated name, `%TEMP%\ad-judge-9f3k\`, and run against a copy of the deliverable.

## The three conditions

| Condition | Protocol | What it was given |
|---|---|---|
| Single agent, one sentence | None | "Implement `quoteOrder` in `src/billing/pricing.js` according to `docs/PRICING.md`, with unit tests.", and the workspace path |
| Single agent, contract | None | The objective, the constraints and five criteria, and nothing else |
| Chain | The last committed version of the skill, 4c6042b, exported to a separate folder, without the two changes recorded in `2026-11-27-fixes.md` | The same objective, constraints and criteria as the contract run, in the form of a TASK_ASSIGNMENT, with a result location and the reporting rules |

The five criteria: C1 `npm test` passes; C2 the three examples give exactly the documented results; C3 every rule in the document is implemented as written, including the shape of the returned object, checked with cases derived from the document; C4 each invalid order throws a `PricingError`, and an empty order returns normally; C5 no file other than `src/billing/pricing.js` and new test files is modified.

For the chain, C3 says "not only with cases the Executor supplies". For the single agent with the contract, it says "not only with the examples in it".

## Result

| | Single agent, one sentence | Single agent, contract | Chain |
|---|---|---|---|
| Hidden tests | 41 of 41 | 41 of 41 | 41 of 41 |
| Own tests added | 91 | 151 | 125 |
| `npm test` | 99 of 99 | 159 of 159 | 133 of 133 |
| Files changed | `pricing.js`, a new test file, one line of `README.md` | `pricing.js` and a new test file | `pricing.js` and a new test file |
| Nothing committed, nothing added | Yes | Yes | Yes |
| Tokens | 100,321 | 161,698 | Supervisor 156,204; the Executor's figure is not visible from Main |
| Tool calls | 51 | 59 | Supervisor 66; the Executor's figure is not visible |
| Wall time | About 20 minutes | About 34 minutes | About 37 minutes |
| Messages to the user's conversation | 1 | 1 | 3 |
| Decisions asked of anyone | 0 | 0 | 0 |
| Correction rounds | Not applicable | Not applicable | 0 |
| Noticed that the volume discount is a cliff | Yes | No | No |

No run left a defect that the hidden tests could find, and none claimed more than it had done.

## The chain's run

| # | Message | When | What it carried |
|---|---|---|---|
| 1 | TASK_ACCEPTED | 23:21 | Scope confirmed; address received; its own entry checks; state RUNNING; one unnamed Executor being launched; the cases it intended to derive from the document |
| 2 | PROGRESS_REPORT | 23:51 | The Executor returned; the Supervisor's own checks pass C1 to C5; one management decision, taken locally; one boundary slip by the Executor, reported by the Executor itself; the README left alone; a terminal handback announced |
| 3 | TASK_COMPLETED, as the handback | about 23:52 | Outcome, deliverables with a hash for each file, the acceptance results, how the run went, four things for Main to know, the records |

- **What ran.** One Executor, launched at 23:22 and done at 23:51. It reported at all three default checkpoints. No replacement and no correction round.
- **One management decision, taken locally.** At the second checkpoint the Executor asked whether it should switch to `BigInt`. The Supervisor told it to keep its arithmetic in ordinary numbers, accepted its choices for inputs the document does not describe, and told it to leave `README.md` alone because of C5. Nothing was asked of Main. This was the only message the Supervisor sent the Executor.
- **What the Supervisor verified itself**, against the files as returned:
  - C1: `npm test`, 133 of 133.
  - C2: the three examples, with the documented objects.
  - C3: 56 cases it derived by hand from the document, among them both thresholds, rounding per line, half-up for both tiers in every bracket, the document's "21, not 22" case, the minimum charge at 199 and 200, the empty order, and the exact keys of the result and of each line. On top of that, 67,656 generated orders matched an exact rational reference that it wrote separately, with no difference. It also read the module rule by rule.
  - C4: 123 invalid orders in 12 groups.
  - C5: `git status --short` shows `pricing.js` modified and the new test file, and nothing else.
- **Nothing was found wrong with the Executor's work.** The independent check confirmed it. It did not add a defect that the Executor's own tests had missed.
- **One problem, reported by the Executor itself.** To filter one test output, it wrote a temporary log under the shell's temp folder, outside the workspace and the delegation folder, and deleted it in the same command. The Supervisor looked, found nothing left behind, and took no action. It also saw a directory `Temp\Temp` appear there for about a minute and could not say what created it. The directory is not there now, and I cannot say either.
- **For the user, outside the contract.** `README.md` still says the pricing is "Not implemented yet". It was left untouched because of C5.
- **Records.** The Executor's `result.md`, and a `supervisor` folder with its checkpoint, its verification script, its outputs, and the test run.

## What was checked independently, after each run

Run from the main conversation, on the final files of each workspace.

- The hidden tests: 41 of 41 for each of the three.
- `npm test`: 99 of 99, 159 of 159 and 133 of 133.
- `git status --short`: `pricing.js` modified and the new test file in each; `README.md` modified in the one-sentence run only. HEAD is still 15c2465 in all three, nothing is staged, there is no stash, and `package.json` is unchanged in all three.
- The chain's two files have the same SHA-256 values as the Supervisor recorded.
- The skill's own repository shows the same three entries as before the runs.

## What each run did on its own

**One sentence.** It wrote the rounding in whole-number arithmetic so that a tie cannot be missed. It cross-checked its implementation against a separate reference that works in exact fractions: 300,000 random orders and a sweep of 24,000 cases, with no disagreement. It ran its tests against 50 deliberately broken copies of the implementation; 49 made a test fail, and it explained why the fiftieth behaves identically. It removed "Not implemented yet" from the README.

It also noticed something that the document does not say. The volume discount is a cliff: at A4 black for a standard customer, 99 sheets cost 495 and 100 sheets cost 450. It implemented the document as written and raised the point.

**Contract.** It validated the whole order before pricing any of it. It derived cases for each rule, among them the document's own "21, not 22" case built as a real order. It applied 46 single-change errors to its implementation; 44 made a test fail, and it explained the two that do not. It cross-checked against a reference in exact fractions: the 4,076 orders its suite sends to `quoteOrder`, and 40,000 further random orders. It left the README alone because of C5, and said so.

**Chain.** The Executor's tests and the Supervisor's checks are described above. The Supervisor's verification was the same in kind as what the two single agents did on their own work: cases derived from the document, a separate reference in exact arithmetic, and a reading of the module.

All three chose the same where the document is silent: a value for `color` or `express` that is not a boolean is read by its truth value, because the document's list of invalid orders does not include it.

## What this shows

- **The harder task did not separate the three.** Every interaction that the hidden tests were built around was handled by all three. The Supervisor's independent check found nothing to correct.
- **The chain cost the most.** The Supervisor alone used about one and a half times the tokens of the cheapest single agent; the Executor's share is not included. It took nearly twice as long, and sent three messages where one carried the result.
- **The contract made the single agent slower and more thorough, not more correct.** It wrote 151 tests against 91, and used about 60 percent more tokens, for the same score.
- **The one observation that went beyond the task came from the run with the least instruction.** The cliff in the volume discount was raised only by the single agent given one sentence.

With the first task, the record now stands at two tasks and three ways of doing each. On both, all ways met the task, and the chain cost the most without a measurable gain in quality or in success.

## What it does not show

- **A difference that needs more than one run to appear.**
- **A task too large for one agent**, or one with a real trap that this model falls into. Both tasks here were exactly specified.
- **A different model in the Executor's seat.** All roles ran on the same model.
- **The correction loop.** Three chain runs have now passed on the first attempt.
- **The two protocol changes.** The chain ran with the skill as committed.

## Cost

100,321 tokens for the single agent with one sentence, 161,698 for the single agent with the contract, 156,204 for the chain's Supervisor. The Executor's figure is not visible from Main.
