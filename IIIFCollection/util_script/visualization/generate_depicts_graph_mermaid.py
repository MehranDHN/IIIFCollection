import glob
import json
import os
import re

root = r'c:/Users/Floyd/IIIFCollection/IIIFCollection'
files = glob.glob(os.path.join(root, '*Collection.json'))


def normalize_label(label):
    if isinstance(label, dict):
        en = label.get('en')
        if isinstance(en, list):
            return ' '.join(str(x) for x in en)
        if isinstance(en, str):
            return en
        return ' '.join(str(v) for v in label.values())
    if isinstance(label, list):
        return ' '.join(str(x) for x in label)
    return str(label) if label is not None else ''


def extract_tags(md):
    label = normalize_label(md.get('label'))
    if not label:
        return []
    if label.strip().lower() == 'depicts' or 'iconograph' in label.lower():
        value = md.get('value')
        if isinstance(value, dict):
            vals = []
            for v in value.values():
                if isinstance(v, list):
                    vals.extend(v)
                else:
                    vals.append(v)
        elif isinstance(value, list):
            vals = value
        elif value is not None:
            vals = [value]
        else:
            vals = []
        return [str(v).strip() for v in vals if v is not None and str(v).strip()]
    return []


def safe_id(label):
    safe = re.sub(r'[^A-Za-z0-9_]', '_', label)
    if not safe or safe[0].isdigit():
        safe = '_' + safe
    return safe


collections = {}
resources = []
tags = set()

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            d = json.load(fh)
    except Exception:
        continue
    cid = os.path.basename(f)
    coll_label = d.get('label') or cid
    found = False
    for m in d.get('manifests', []) + d.get('items', []):
        tags_found = []
        for md in m.get('metadata', []):
            tags_found.extend(extract_tags(md))
        tags_found = sorted(set(tags_found))
        if tags_found:
            found = True
            resources.append({
                'collection_id': cid,
                'collection_label': coll_label,
                'id': m.get('id'),
                'label': m.get('label'),
                'tags': tags_found,
            })
            tags.update(tags_found)
    if found:
        collections[cid] = {'label': coll_label, 'file': f}

if not collections:
    raise SystemExit('No collections found with Depicts iconography-tagged resources')

lines = ['flowchart LR']
for cid, coll in collections.items():
    col_id = safe_id(f'COL_{cid}')
    lines.append(f'  {col_id}["Collection: {coll["label"]}"]')

for idx, r in enumerate(resources):
    rid = safe_id(f'RES_{idx}')
    label_text = normalize_label(r['label'])
    if len(label_text) > 60:
        label_text = label_text[:60] + '...'
    lines.append(f'  {rid}["Resource: {label_text}"]')
    col_id = safe_id(f'COL_{r["collection_id"]}')
    lines.append(f'  {col_id} --> {rid}')
    for tag in r['tags']:
        tid = safe_id(f'TAG_{tag}')
        lines.append(f'  {rid} --> {tid}(["{tag}"])')

output_path = os.path.join(root, 'iconography_association_graph.mmd')
with open(output_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(lines))
print('WROTE', output_path, 'collections', len(collections), 'resources', len(resources), 'tags', len(tags))
