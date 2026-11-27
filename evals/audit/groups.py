"""Groups the units classified as guidance (C) by the weight they carry, and sums the words.

Usage: python groups.py <classified.tsv>
"""
import sys
from collections import OrderedDict

GROUPS = OrderedDict([
    ('K1', ('Delivery over appearance', 'CP-019 CP-025 LP-032 SK-041')),
    ('K2', ('Autonomy over asking', 'SK-033 SK-040')),
    ('K0', ('The rule about an Executor that writes to Main, not yet decided by the owner', 'SK-039 RP-031')),
    ('K3', ('Trust over progress, at the edge of the authorization',
            'CP-029 CP-044 CP-045 CM-020 CM-021 CM-079 LP-025 LP-028 CM-044 CM-047 AD-013 AD-059 SK-043 SK-044 SK-023')),
    ('K4', ('Judgment over relay: what a report carries', 'RP-027 RP-028 SK-031 CP-030 CP-033 CM-070 CM-071 CM-072 CM-073 '
                                                      'CM-074 CM-075 CM-076 CM-077 CM-078 CM-050')),
    ('K5', ('Not pretending to know', 'CM-005 CM-006 CM-082 LP-031 LP-033 CP-004 SK-026 AD-012 AD-046')),
    ('K6', ('Respecting reality', 'CP-036 CP-037 CP-038 CP-039 CP-040 CP-041 CP-042 CP-043 RP-004')),
    ('K7', ('Authorization is not exemption: restraint inside the boundary', 'CP-034 CP-035 CP-009 CP-010 CP-011')),
    ('K8', ('Writing the contract', 'CM-014 CM-015 CM-016 CM-017 CM-018 CM-019 SK-016 SK-017 RP-023')),
    ('K9', ('Leftovers in the Executor instruction', 'CM-036 CM-045')),
    ('K10', ('Scope of the skill', 'SK-003')),
])


def main():
    words = {}
    for line in open(sys.argv[1], encoding='utf-8'):
        uid, category, count, _ = line.rstrip('\n').split('\t')
        if category == 'C':
            words[uid] = int(count)
    seen = set()
    total = 0
    for key, (name, ids) in GROUPS.items():
        members = ids.split()
        for uid in members:
            if uid not in words:
                raise SystemExit(f'{uid} is not a guidance unit')
            if uid in seen:
                raise SystemExit(f'{uid} listed twice')
            seen.add(uid)
        subtotal = sum(words[uid] for uid in members)
        total += subtotal
        print(f'{key:4} {len(members):2d} units {subtotal:4d} words  {name}')
    missing = sorted(set(words) - seen)
    print(f'total {total} words in {len(seen)} units; guidance units not in any group: {missing}')


if __name__ == '__main__':
    main()
