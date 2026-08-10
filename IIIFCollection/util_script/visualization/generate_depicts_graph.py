import json
import os
import re
from pathlib import Path

root = Path(__file__).resolve().parents[2]
ontology_path = root / 'Ontology' / 'iiifCollectionOntology.ttl'
ontology_files = [
    ontology_path,
    root / 'Ontology' / 'iconography_RDF.ttl',
    root / 'Ontology' / 'narrative_episodes.ttl',
]
files = sorted(root.glob('*Collection.json'))


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


def normalize_term(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.startswith('<') and text.endswith('>'):
        text = text[1:-1]
    if text.startswith('mdhn:'):
        return text
    if ':' in text:
        prefix, local = text.split(':', 1)
        if prefix.lower() == 'mdhn':
            return f'mdhn:{local}'
    return f'mdhn:{text}'


def flatten_values(value):
    if isinstance(value, dict):
        vals = []
        for v in value.values():
            vals.extend(flatten_values(v))
        return vals
    if isinstance(value, list):
        vals = []
        for v in value:
            vals.extend(flatten_values(v))
        return vals
    if value is None:
        return []
    return [value]


def extract_tags(node):
    tags = []
    if isinstance(node, dict):
        label = normalize_label(node.get('label'))
        if label.strip().lower() == 'depicts' or 'iconograph' in label.lower():
            values = flatten_values(node.get('value'))
            for value in values:
                term = normalize_term(value)
                if term:
                    tags.append(term)
        if 'depicts' in node:
            values = flatten_values(node.get('depicts'))
            for value in values:
                term = normalize_term(value)
                if term:
                    tags.append(term)
        for value in node.values():
            tags.extend(extract_tags(value))
    elif isinstance(node, list):
        for item in node:
            tags.extend(extract_tags(item))
    return tags


def parse_class_hierarchy(ontology_path):
    if not ontology_path.exists():
        return set(), {}
    classes = set()
    parents = {}
    current_class = None
    for raw_line in ontology_path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('@prefix'):
            continue
        match = re.match(r'(mdhn:[A-Za-z0-9_]+)\s+a\s+owl:Class\s*[.;]', line)
        if match:
            current_class = match.group(1)
            classes.add(current_class)
            continue
        match = re.search(r'rdfs:subClassOf\s+(mdhn:[A-Za-z0-9_]+)', line)
        if match and current_class:
            parents.setdefault(current_class, set()).add(match.group(1))
    return classes, parents


def descendants_of(class_name, parents):
    found = set()
    stack = [class_name]
    while stack:
        current = stack.pop()
        for child, parent_set in parents.items():
            if current in parent_set and child not in found:
                found.add(child)
                stack.append(child)
    return found


def parse_instance_types(paths):
    instance_types = {}
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        for entity, entity_type in re.findall(r'(mdhn:[A-Za-z0-9_]+)\s+a\s+(mdhn:[A-Za-z0-9_]+)\s*;', text):
            instance_types.setdefault(entity, set()).add(entity_type)
    return instance_types


def is_relevant_term(term, relevant_classes, instance_types):
    if not term:
        return False
    if term in relevant_classes:
        return True
    for entity_type in instance_types.get(term, set()):
        if entity_type in relevant_classes:
            return True
    return False


def classify_tag(term, instance_types):
    if not term:
        return 'Iconography', 'Iconography', '#f8cecc'
    if 'mdhn:NarrativeEpisode' in instance_types.get(term, set()):
        return 'NarrativeEpisode', 'Narrative Episode', '#d5e8d4'
    return 'Iconography', 'Iconography', '#f8cecc'


classes, parents = parse_class_hierarchy(ontology_path)
relevant_classes = {'mdhn:Iconography'} | descendants_of('mdhn:Iconography', parents)
instance_types = parse_instance_types(ontology_files)

collections = {}
resources = []
tags = set()

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            d = json.load(fh)
    except Exception:
        continue
    cid = f.name
    coll_label = d.get('label') or cid
    found = False
    for m in d.get('manifests', []) + d.get('items', []):
        tags_found = []
        for md in m.get('metadata', []):
            tags_found.extend(extract_tags(md))
        tags_found.extend(extract_tags(m))
        relevant_tags = []
        for tag in sorted(set(tags_found)):
            norm_tag = normalize_term(tag)
            if is_relevant_term(norm_tag, relevant_classes, instance_types):
                relevant_tags.append(norm_tag)
        if relevant_tags:
            found = True
            resources.append({
                'collection_id': cid,
                'collection_label': coll_label,
                'id': m.get('id'),
                'label': m.get('label'),
                'tags': relevant_tags,
            })
            tags.update(relevant_tags)
    if found:
        collections[cid] = {'label': coll_label, 'file': f}

if not collections:
    raise SystemExit('No collections found with Iconography or NarrativeEpisode tagged resources')


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
    _, label_prefix, fillcolor = classify_tag(tag, instance_types)
    lines.append(f'  "TAG_{node_id(tag)}" [label="{label_prefix}: {quote(tag)}", shape=ellipse, fillcolor="{fillcolor}"]')

lines.append('}')

output_path = root / 'iconography_association_graph.dot'
with open(output_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(lines))
print('WROTE', output_path, 'collections', len(collections), 'resources', len(resources), 'tags', len(tags))
