"""Applies the manual audit's classification to units.tsv and sums the words.

Categories:
  P  philosophy: already a cognitive instruction (situation, weight, reason)
  A  compensates: a runtime fact or mechanic the model could not infer
  B  coordinates: a shared contract (roles, messages, states, triggers, steps)
  C  guides:      judgment written as a manual rule
  M  meta:        about the document itself (status, scope, references, notes)

Usage: python classify.py <units.tsv> <classified.tsv>
"""
import sys
from collections import OrderedDict

RANGES = {
    'SK': [('001', 'B'), ('002', 'M'), ('003', 'C'), ('004-011', 'P'), ('012-014', 'A'), ('015', 'B'),
           ('016-017', 'C'), ('018-019', 'B'), ('020-022', 'A'), ('023', 'C'), ('024-025', 'A'),
           ('026', 'C'), ('027-028', 'A'), ('029-030', 'B'), ('031', 'C'), ('032', 'A'), ('033', 'C'),
           ('034-037', 'P'), ('038', 'B'), ('039-041', 'C'), ('042', 'A'), ('043-044', 'C')],
    'RP': [('001-003', 'M'), ('004', 'C'), ('005', 'M'), ('006-016', 'P'), ('017-022', 'B'),
           ('023', 'C'), ('024-025', 'B'), ('026', 'A'), ('027-028', 'C'), ('029-030', 'B'),
           ('031', 'C')],
    'CP': [('001', 'A'), ('002-003', 'B'), ('004', 'C'), ('005-007', 'A'), ('008', 'B'),
           ('009-011', 'C'), ('012-014', 'A'), ('015', 'B'), ('016', 'A'), ('017-018', 'B'),
           ('019', 'C'), ('020-022', 'B'), ('023-024', 'B'), ('025', 'C'), ('026-027', 'B'),
           ('028', 'A'), ('029-030', 'C'), ('031-032', 'B'), ('033-045', 'C'), ('046-047', 'A')],
    'CM': [('001-004', 'B'), ('005-006', 'C'), ('007-013', 'B'), ('014-021', 'C'), ('022-024', 'B'),
           ('025', 'A'), ('026-029', 'B'), ('030-035', 'P'), ('036', 'C'), ('037-039', 'B'),
           ('040', 'A'), ('041-043', 'B'), ('044-045', 'C'), ('046', 'A'), ('047', 'C'),
           ('048-049', 'B'), ('050', 'C'), ('051-068', 'B'), ('069', 'A'), ('070-079', 'C'),
           ('080', 'A'), ('081', 'B'), ('082', 'C'), ('083', 'B')],
    'LP': [('001', 'B'), ('002', 'A'), ('003-024', 'B'), ('025', 'C'), ('026-027', 'A'),
           ('028', 'C'), ('029-030', 'A'), ('031-033', 'C'), ('034', 'A')],
    'AD': [('005', 'M'), ('012-013', 'C'), ('025-026', 'B'), ('032', 'B'), ('046', 'C'),
           ('054-055', 'M'), ('058', 'M'), ('059', 'C')],
}
DEFAULTS = {'SK': None, 'RP': None, 'CP': None, 'CM': None, 'LP': None, 'AD': 'A'}
NAMES = OrderedDict([
    ('P', 'philosophy, already a cognitive instruction'),
    ('A', 'compensates: a runtime fact or mechanic'),
    ('B', 'coordinates: a shared contract'),
    ('C', 'guides: judgment written as a rule'),
    ('M', 'about the document'),
])


def expand(spec):
    out = {}
    for span, cat in spec:
        if '-' in span:
            low, high = (int(part) for part in span.split('-'))
            for number in range(low, high + 1):
                out[number] = cat
        else:
            out[int(span)] = cat
    return out


def main():
    units = [line.rstrip('\n').split('\t') for line in open(sys.argv[1], encoding='utf-8')]
    tables = {abbr: expand(spec) for abbr, spec in RANGES.items()}
    classified = []
    for uid, kind, words, text in units:
        abbr, number = uid.split('-')
        category = tables[abbr].get(int(number)) or DEFAULTS[abbr]
        if category is None:
            raise SystemExit(f'no category for {uid}')
        classified.append((uid, category, int(words), text))
    with open(sys.argv[2], 'w', encoding='utf-8') as out:
        for uid, category, words, text in classified:
            out.write(f'{uid}\t{category}\t{words}\t{text}\n')

    total = sum(words for _, _, words, _ in classified)
    print(f'total units {len(classified)}, total words {total}')
    print('\nby category:')
    for cat, name in NAMES.items():
        units_here = [row for row in classified if row[1] == cat]
        words_here = sum(row[2] for row in units_here)
        print(f'  {cat}  {len(units_here):3d} units  {words_here:5d} words  {100 * words_here / total:5.1f}%  {name}')
    print('\nby file (words):        ' + '   '.join(f'{cat:>5}' for cat in NAMES))
    for abbr in RANGES:
        row = [sum(words for uid, cat, words, _ in classified if uid.startswith(abbr + '-') and cat == c) for c in NAMES]
        print(f'  {abbr}  ' + '   '.join(f'{value:5d}' for value in row) + f'   = {sum(row)}')


if __name__ == '__main__':
    main()
