# Three ways of doing the same task, 2026-11-27

**Status:** complete. One run of each, on the same task from the same baseline commit. One run each can show that a difference exists. It cannot show that there is none.

| Condition | Who did the work | What it was given |
|---|---|---|
| Chain | A Supervisor and one Executor under the live protocol | The contract: objective, constraints, three criteria, a result location, the reporting rules |
| Single agent with the contract | One agent, no protocol, no second party | The same objective, constraints and three criteria, written the way the skill teaches Main to write a contract, and nothing else |
| Single agent with one sentence | One agent, no protocol, no second party | "Split the session handling out of `src/auth/login.js` into its own module and add unit tests for it.", plus the workspace path |

The task: split session handling out of `src/auth/login.js` into a new `src/auth/session.js`, add unit tests for the new module, and keep the public API of `login.js` unchanged. The three criteria: C1 `npm test` passes; C2 the same eight export names with the same behavior; C3 the two existing test files unmodified and passing, and no other file modified. Each condition started from a clean copy of baseline commit 6efca1a.

## Result

| | Chain | Single agent, contract | Single agent, one sentence |
|---|---|---|---|
| Outcome | COMPLETED on the first attempt | All three criteria hold on the first attempt | C1 and C2 hold. C3 holds except that `README.md` was updated, which no one had told it not to do |
| False completion | None | None | None |
| Tokens | Supervisor 179,198; the Executor's figure is not visible from Main | 81,555 | 71,436 |
| Tool calls | Supervisor 75; the Executor 69 | 33 | 32 |
| Wall time | About 30 minutes; the Executor about 23 | About 12 minutes | About 10 minutes |
| Messages to the user's conversation | 3 | 1 | 1 |
| Decisions asked of anyone | 0 | 0 | 0 |
| New tests | 27, in one file | 14, in two files | 22, in one file |
| The same eleven breakages applied to `session.js` | 11 of 11 caught | 10 of 10 with a target caught | 8 of 10 with a target caught |
| How the author checked its own work | Tests four times; exports; a scripted scenario and 480,000 random operations against the baseline; byte-identity; the git boundary; eleven breakages | Tests five times; exports; the same 53 calls to both modules under a frozen clock; byte-identity; the git boundary; 21 injected faults | A behaviour transcript before and after, 36 identical lines; byte-identity; 15 breakages |
| Public API kept without being asked | Told to | Told to | Yes, all eight names, with a note on how to remove the re-exports if a hard boundary is wanted |
| Existing tests left alone | Told to | Told to | Yes |
| Nothing committed, no dependency added | Told to | Told to | Yes |
| README | Flagged as out of date; not allowed to change it | Flagged as out of date, with a suggested text | Updated |
| Found outside the task | An order-dependent existing test, reproduced; a comment promising a version check; Node 20.11 needed, looked up | The same comment; a Node version, stated as a belief | The same comment, with an analysis of when it would matter; two pre-existing design risks, internal objects handed back by the store and guessable tokens; Node version, unverified on Node 20 |
| Not noticed by anyone | `changePassword` does not invalidate sessions | The same | The same |

## What was checked independently, after each run

Run from the main conversation, on the final files of each workspace.

- `npm test`: 35 of 35, 22 of 22 and 30 of 30.
- `git status --short`: in each, `login.js` modified and the new files listed. `README.md` modified in the third only. `git diff HEAD` on the two existing test files is empty in all three. HEAD is still 6efca1a in all three, nothing is staged, and `package.json` is unchanged in all three.
- The exports of `login.js`, compared with the baseline file loaded from git: identical in names, types and arity in all three.
- A behaviour spot check on each: login, get, legacy refresh, logout. All as expected.
- The moved session code is identical to the baseline, line for line, in all three.
- The suite in random order: the only test that fails is `getProfile returns the profile of a known user`, in the pre-existing `test/account.test.js`. It is in the baseline.
- The chain's three deliverables have the same `git hash-object` values as the Supervisor recorded.
- The new test files were read in full for the chain and for the one-sentence run, and the session tests for the contract run. No defect was found in any deliverable.

The two breakages that the one-sentence run's tests did not catch:

- "Expiry uses `<` instead of `<=`". Its tests check one millisecond before the expiry and one millisecond after it, not the instant itself. The agent said so itself: "Not pinned: whether a session is still valid at the exact expiry instant."
- "createSession issues t-prefixed tokens". Its tests check that a token is a non-empty string and unique, not its form.

## A mistake of mine in this comparison

The first version of the breakage script passed the wrong arguments to the test runner inside its loop, and reported that one breakage survived in the chain's deliverable and in the contract run's. That contradicted the Supervisor's recorded result of 11 out of 11, so the script was checked, corrected and run again. The table gives the corrected result.

## What this shows

- **All three ways met the task.** None claimed more than it had done, and each verified its own work by comparing behaviour with the baseline and by breaking the code on purpose.
- **The chain cost the most and showed no gain on this task.** The Supervisor alone used more than twice the tokens of either single agent, the Executor's share is not included, and it took about three times as long.
- **The contract's constraints were not needed for this model on this task.** The agent that was given one sentence kept the public API, left the existing tests alone, committed nothing and added nothing, as the others had been told to.
- **The one place the contract changed the result is a restriction.** It stopped the chain and the contract run from updating a README that had become wrong. The agent that was free to do so updated it.
- **The tests differ in strength.** The one-sentence run's tests let two breakages through, the other two let none through. One run each, so this may be run-to-run variation.
- **What the second party did add.** It found the order-dependent test, which neither single agent found. It looked the Node version up instead of guessing. And the user's conversation received a report when the Executor returned.

## What it does not show

- **A difference that needs more than one run to appear.**
- **A larger task, or one with a real trap in it.** This one was small, and every part of it was easy to check against a baseline that already existed.
- **A different model in the Executor's seat.** All roles ran on the same model.
- **The correction loop.** Every run passed first time.

## Cost

179,198 tokens for the chain's Supervisor, 81,555 for the single agent with the contract, 71,436 for the single agent with one sentence.

## Scripts

Under `%TEMP%\ad-e2e-20261127\check\`: `mutation-check.sh` applies the eleven breakages to a copy of a workspace and runs given test files against each; `compare-exports.mjs` compares a workspace's exports with the baseline in git.
