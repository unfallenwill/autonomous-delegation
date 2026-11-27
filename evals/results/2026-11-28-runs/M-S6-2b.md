1. To `main`:
   - PROGRESS_REPORT (T-101, rev 1): state WAITING_DECISION; `e7` returned and the deliverables are in place; I verified C1 (`npm test` in `/work/app`) and C2 (exported names and signatures of `login.ts`) myself; C3 is unknown, because the staging smoke suite needs a VPN this environment lacks, and `e7`'s "logic unchanged, unit tests cover it" is a claim, not the check the contract names.
   - DECISION_REQUEST (R-1): C3 cannot be confirmed here, and providing VPN access or substituting a weaker check is outside my authority; options: (a) provide VPN access or the output of a staging smoke run, (b) amend C3 by TASK_AMENDMENT, or (c) stop with T-101 BLOCKED, resumable, or FAILED; I recommend (a), and nothing can continue meanwhile.

2. To `e7`: none.

3. WAITING_DECISION (R-1 pending; handed back as BLOCKED only if I cannot safely wait).

4. C3 is mandatory and only the staging suite confirms it, so it stays unknown rather than pass, and T-101 cannot be COMPLETED. Nothing `e7` could do within its authority closes C3, so a correction round would add nothing; the missing VPN and any change to C3 are for Main.
