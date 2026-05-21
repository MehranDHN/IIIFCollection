import json
import os
import glob
from pathlib import Path

root_path = Path('IIIF2Collection.json')
workspace = root_path.parent
cache = {}


def load_json(path):
    path = Path(path)
    if path in cache:
        return cache[path]
    if not path.exists():
        return None
    with path.open('r', encoding='utf-8') as fh:
        data = json.load(fh)
    cache[path] = data
    return data


def get_collection_path(ref):
    if not isinstance(ref, str):
        return None
    ref = ref.strip()
    if not ref:
        return None
    basename = os.path.basename(ref)
    candidate = workspace / basename
    return candidate if candidate.exists() else None


def normalize_label(label):
    if isinstance(label, dict):
        return label.get('en') if isinstance(label.get('en'), str) else repr(label)
    return str(label or '')


def count_contents(data):
    subcs = len(data.get('collections', []))
    manifests = len(data.get('manifests', []) or [])
    items = len(data.get('items', []) or [])
    # Some IIIF2 collections use items instead of manifests
    if manifests == 0 and items > 0:
        manifests = items
    return subcs, manifests


root = load_json(root_path)
if root is None:
    raise SystemExit('Root collection file not found')

nodes = []
edges = []
seen = set()


def node_id(name):
    safe = ''.join(c if c.isalnum() else '_' for c in name)
    if not safe or safe[0].isdigit():
        safe = '_' + safe
    return safe


def walk_collection(path, parent_id=None):
    data = load_json(path)
    if data is None:
        return
    label = normalize_label(data.get('label') or path.stem)
    subc_count, manifest_count = count_contents(data)
    node_name = f'{label} ({subc_count} collections, {manifest_count} manifests)'
    nid = node_id(path.stem)
    nodes.append((nid, node_name))
    if parent_id:
        edges.append((parent_id, nid))
    if nid in seen:
        return
    seen.add(nid)
    for coll in data.get('collections', []):
        subpath = get_collection_path(coll.get('@id') or coll.get('id') or coll.get('label'))
        if subpath:
            walk_collection(subpath, nid)

walk_collection(root_path)

mermaid_lines = ['flowchart TB', '  classDef root fill:#ffe599,stroke:#333,stroke-width:2px;', '  classDef collection fill:#d9ead3,stroke:#6aa84f,stroke-width:1px;', '  classDef leaf fill:#cfe2f3,stroke:#45818e,stroke-width:1px;']
for nid, label in nodes:
    style = 'root' if nid == node_id(root_path.stem) else 'collection'
    mermaid_lines.append(f'  {nid}["{label}"]')
    mermaid_lines.append(f'  class {nid} {style};')
for parent, child in edges:
    mermaid_lines.append(f'  {parent} --> {child}')

output_path = workspace / 'collection_structure_tree.mmd'
with output_path.open('w', encoding='utf-8') as fh:
    fh.write('\n'.join(mermaid_lines) + '\n')
print('WROTE', output_path)
print('Nodes', len(nodes), 'Edges', len(edges))
