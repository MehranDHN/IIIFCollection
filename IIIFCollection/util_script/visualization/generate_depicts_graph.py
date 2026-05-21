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


def node_id(name):
    safe = re.sub(r'[^A-Za-z0-9_]', '_', name)
    if not safe or safe[0].isdigit():
        safe = '_' + safe
    return safe


def quote(label):
    return label.replace('"', '\\"')

lines = [
    'digraph IconographyAssociations {',
    '  rankdir=LR;',
    '  node [shape=box, style=filled, fillcolor="#f2f2f2"];',
]
for cid, coll in collections.items():
    label = coll['label']
    lines.append(f'  "COL_{node_id(cid)}" [label="Collection: {quote(label)}", shape=folder, fillcolor="#d5e8d4"]')

for idx, r in enumerate(resources):
    label = r['label']
    if isinstance(label, dict):
        label_text = normalize_label(label)
    else:
        label_text = str(label)
    label_text = label_text.replace('\n', ' ')
    if len(label_text) > 80:
        label_text = label_text[:80] + '...'
    rid = f'RES_{idx}'
    lines.append(f'  "{rid}" [label="Resource: {quote(label_text)}", shape=note, fillcolor="#dae8fc"]')
    coll_id = r['collection_id']
    if coll_id in collections:
        lines.append(f'  "COL_{node_id(coll_id)}" -> "{rid}" [label="contains", color="#6c8ebf"]')
    for tag in r['tags']:
        tid = f'TAG_{node_id(tag)}'
        lines.append(f'  "{rid}" -> "{tid}" [label="depicts", color="#b85450"]')

for tag in sorted(tags):
    lines.append(f'  "TAG_{node_id(tag)}" [label="Iconography: {quote(tag)}", shape=ellipse, fillcolor="#f8cecc"]')

lines.append('}')

output_path = os.path.join(root, 'iconography_association_graph.dot')
with open(output_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(lines))
print('WROTE', output_path, 'collections', len(collections), 'resources', len(resources), 'tags', len(tags))
