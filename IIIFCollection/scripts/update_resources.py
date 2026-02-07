#!/usr/bin/env python3
"""Direct update of ontology/resources.ttl with TGM replacements"""
import csv
import json
from pathlib import Path

# Read mappings
repo_root = Path('c:\\Users\\Floyd\\IIIFCollection\\IIIFCollection')
csv_path = repo_root / 'tgm_id_mapping.csv'
resources_path = repo_root / 'Ontology' / 'resources.ttl'

# Load mappings
mappings = {}
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        old_uri = row['old_uri'].strip()
        new_uri = row['new_uri'].strip()
        # Extract local names for prefix form
        old_local = old_uri.split('/')[-1]
        new_local = new_uri.split('/')[-1]
        mappings[old_local] = new_local

print(f"Loaded {len(mappings)} TGM ID mappings")

# Read resources.ttl
content = resources_path.read_text(encoding='utf-8')
original_lines = content.count('\n')

# Replace all old refs with new ones
for old_local, new_local in mappings.items():
    old_prefix = f'mdhn:{old_local}'
    new_prefix = f'mdhn:{new_local}'
    content = content.replace(old_prefix, new_prefix)

new_lines = content.count('\n')
print(f"Content updated: {original_lines} lines -> {new_lines} lines")

# Write back to file
resources_path.write_text(content, encoding='utf-8')
print(f"✓ Updated {resources_path}")

# Create summary
summary = {
    'action': 'TGM Prefix Form Update',
    'file': 'Ontology/resources.ttl',
    'mappings_applied': len(mappings),
    'status': 'success'
}

summary_path = repo_root / 'TGM_UPDATE_SUMMARY.json'
with open(summary_path, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"✓ Summary written to {summary_path.name}")
