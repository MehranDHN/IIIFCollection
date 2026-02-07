#!/usr/bin/env python3
"""Quick validation: find JSON files referencing TGM URIs"""
import csv
from pathlib import Path
from collections import defaultdict

mapping_csv = Path("IIIFCollection/tgm_id_mapping.csv")
root = Path("IIIFCollection")

# Read mapping
with mapping_csv.open() as f:
    reader = csv.DictReader(f)
    old_uris = {row['old_uri'] for row in reader}

print(f"Total TGM subjects in mapping: {len(old_uris)}")

# Scan JSON files
affected = defaultdict(lambda: {"count": 0, "uris": set()})
total_replacements = 0

for json_file in root.glob("*Collection.json"):
    try:
        content = json_file.read_text(encoding="utf-8")
    except:
        continue
    
    for old_uri in old_uris:
        if old_uri in content:
            count = content.count(old_uri)
            affected[json_file.name]["count"] += count
            affected[json_file.name]["uris"].add(old_uri)
            total_replacements += count

print(f"\nAffected collection JSON files: {len(affected)}")
print(f"Total URI occurrences across all files: {total_replacements}")

if affected:
    print("\nTop 10 most affected collections:")
    for fname, info in sorted(affected.items(), key=lambda x: x[1]["count"], reverse=True)[:10]:
        print(f"  {fname}: {info['count']} replacements ({len(info['uris'])} unique URIs)")
else:
    print("\nNo collection JSON files contain TGM URIs (they might use RDF/TTL instead)")
