"""Splits the skill files into units for the manual audit.

A unit is a sentence of prose, or one row of a table. Headings, frontmatter and table
header rows are left out. Output: units.tsv with id, file, words, text.

Usage: python split.py <output.tsv> <file> [<file> ...]
  Each <file> is given as ABBR=PATH.
"""
import re
import sys

SENTENCE_END = re.compile(r'(?<=[.!?])["\')\]]*\s+(?=[A-Z"(\[`])')
LIST_MARKER = re.compile(r'^\s*(?:\d+\.|[-*])\s+')


def split_sentences(text):
    return [s.strip() for s in SENTENCE_END.split(text) if s.strip()]


def units_of(path, abbr):
    with open(path, encoding='utf-8') as handle:
        lines = handle.read().replace('\r\n', '\n').split('\n')
    result = []
    in_frontmatter = False
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line == '---':
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter or line.startswith('#'):
            continue
        if line.startswith('|'):
            if re.match(r'^\|[\s:|-]+\|$', line):
                continue
            result.append(('row', line))
            continue
        line = LIST_MARKER.sub('', line)
        for sentence in split_sentences(line):
            result.append(('sentence', sentence))
    return [(f'{abbr}-{i:03d}', kind, len(text.split()), text) for i, (kind, text) in enumerate(result, 1)]


def main():
    out_path = sys.argv[1]
    rows = []
    for spec in sys.argv[2:]:
        abbr, path = spec.split('=', 1)
        rows.extend(units_of(path, abbr))
    with open(out_path, 'w', encoding='utf-8') as out:
        for uid, kind, words, text in rows:
            out.write(f'{uid}\t{kind}\t{words}\t{text}\n')
    for uid, kind, words, text in rows:
        shown = text if len(text) <= 150 else text[:147] + '...'
        print(f'{uid}\t{words}\t{shown}')


if __name__ == '__main__':
    main()
