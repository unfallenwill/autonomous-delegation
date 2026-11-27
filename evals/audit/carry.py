"""Carries a classification over to a new split of the files, by matching unit text.

Units whose text is unchanged keep their category. New or changed units are listed for
assignment; give their categories in NEW_CATEGORIES below and run again.

Usage: python carry.py <old-classified.tsv> <new-units.tsv> <new-classified.tsv>
"""
import sys
from collections import OrderedDict

# Units whose text is new or changed since the previous split.
NEW_CATEGORIES = {
    # Supervisor's stance, the sentences added on 2026-11-28
    'Authorization settles what you may do, not what your doing it will cost: inside the boundary you are still answerable.': 'P',
    'What you have not checked, you believe and do not know, so say it as what it is.': 'P',
    'A guess passed on as a fact closes off the remedy: the user could still act on a doubt, but cannot undo a fact they trusted.': 'P',
    'Your judgment is a tool for getting the work done.': 'P',
    'When what you find contradicts it, follow what you found and say so.': 'P',
    'Holding on to a judgment that the facts have passed gains nothing.': 'P',
    # Main's stance, the sentences added on 2026-11-28
    'You did not do the work and you did not check it, so speak to what the Supervisor told you and call it that: a named doubt lets the user act, and a covered one is found out too late.': 'P',
    'Your reading of the task is a judgment too, and a judgment is a tool.': 'P',
    "When the Supervisor's reports show that it was wrong, follow the reports: tell the user, and change the contract rather than defend what you wrote.": 'P',
    # The Executor's stance, the sentences added on 2026-11-28
    'Authorization settles what you may change, not what your changing it will cost: inside your order you are still answerable.': 'P',
    'What you have not run, you do not know: report what you ran and what it showed, and call the rest a belief, because a guess handed up as a result closes off the remedy.': 'P',
    'Your plan is a tool: when the code, the tests or the facts disagree with it, follow them, change the plan, and say that you did.': 'P',
    # Two rules rewritten as a statement of the situation
    'If that send fails, live reporting from Executors to the Supervisor is unavailable.': 'A',
    'Otherwise report BLOCKED.': 'B',
}
NAMES = OrderedDict([
    ('P', 'philosophy, already a cognitive instruction'),
    ('A', 'compensates: a runtime fact or mechanic'),
    ('B', 'coordinates: a shared contract'),
    ('C', 'guides: judgment written as a rule'),
    ('M', 'about the document'),
])


def main():
    old = {}
    for line in open(sys.argv[1], encoding='utf-8'):
        uid, category, words, text = line.rstrip('\n').split('\t')
        old[text] = category
    new = [line.rstrip('\n').split('\t') for line in open(sys.argv[2], encoding='utf-8')]
    classified = []
    unassigned = []
    for uid, kind, words, text in new:
        category = old.get(text) or NEW_CATEGORIES.get(text)
        if category is None:
            unassigned.append((uid, text))
        classified.append((uid, category or '?', int(words), text))
    for uid, text in unassigned:
        print(f'UNASSIGNED {uid}: {text[:140]}')
    if unassigned:
        raise SystemExit(f'{len(unassigned)} units have no category')
    with open(sys.argv[3], 'w', encoding='utf-8') as out:
        for uid, category, words, text in classified:
            out.write(f'{uid}\t{category}\t{words}\t{text}\n')
    total = sum(words for _, _, words, _ in classified)
    print(f'total units {len(classified)}, total words {total}')
    for cat, name in NAMES.items():
        here = [row for row in classified if row[1] == cat]
        words_here = sum(row[2] for row in here)
        print(f'  {cat}  {len(here):3d} units  {words_here:5d} words  {100 * words_here / total:5.1f}%  {name}')


if __name__ == '__main__':
    main()
