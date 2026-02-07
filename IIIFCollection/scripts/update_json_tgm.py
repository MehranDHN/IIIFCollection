#!/usr/bin/env python3
"""Replace TGM IDs in all JSON files"""

import csv
import re
import json
from pathlib import Path

csv_path = Path(r'c:\Users\Floyd\IIIFCollection\IIIFCollection\tgm_id_mapping.csv')
mapping = {}
with open(csv_path) as f:
    for row in csv.DictReader(f):
        old = row['old_uri'].split('/')[-1]
        new = row['new_uri'].split('/')[-1]
        mapping[old] = new

# Process JSON files
json_files = list(Path(r'c:\Users\Floyd\IIIFCollection\IIIFCollection').rglob('*.json'))
json_files = [f for f in json_files if 'scripts' not in str(f) and 'backups' not in str(f)]

pattern = r'\btgm(' + '|'.join(re.escape(k[3:]) for k in mapping.keys()) + r')\b'
def replacer(m):
    return f"tgm{mapping['tgm' + m.group(1)]}"

updated_count = 0
for jfile in json_files:
    try:
        content = jfile.read_text(encoding='utf-8')
        original = content
        content = re.sub(pattern, replacer, content)
        if content != original:
            jfile.write_text(content, encoding='utf-8')
            updated_count += 1
    except Exception as e:
        print(f"Error processing {jfile.name}: {e}")

print(f'✓ Updated {updated_count} JSON files')
