#!/usr/bin/env python3
"""Batch replace all TGM IDs in resources.ttl with efficient regex"""

import csv
import re
from pathlib import Path

csv_path = Path(r'c:\Users\Floyd\IIIFCollection\IIIFCollection\tgm_id_mapping.csv')
mapping = {}
with open(csv_path) as f:
    for row in csv.DictReader(f):
        old = row['old_uri'].split('/')[-1]
        new = row['new_uri'].split('/')[-1]
        mapping[old] = new

res_path = Path(r'c:\Users\Floyd\IIIFCollection\IIIFCollection\Ontology\resources.ttl')
content = res_path.read_text(encoding='utf-8')

# Build one regex pattern for all replacements
pattern = r'\bmdhn:(' + '|'.join(re.escape(k) for k in mapping.keys()) + r')\b'
def replacer(m):
    return f"mdhn:{mapping[m.group(1)]}"

content = re.sub(pattern, replacer, content)
res_path.write_text(content, encoding='utf-8')
print(f'✓ Done: {len(mapping)} TGM IDs replaced')
