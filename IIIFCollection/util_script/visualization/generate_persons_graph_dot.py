import re
from pathlib import Path

script_dir = Path(__file__).resolve().parent
path = script_dir / '..' / '..' / 'Ontology' / 'PersonsRDFData.ttl'
path = path.resolve()
text = path.read_text(encoding='utf-8')
lines = text.splitlines()

entries = {}
edges = set()
current = None

symmetric_relations = {
    'isSpouseOf',
    'isBrotherOf',
    'isSisterOf',
    'isSiblingOf',
}

for raw_line in lines:
    line = raw_line.strip()
    if not line:
        current = None
        continue

    if line.startswith('mdhn:') and ' a ' in line:
        subject = line.split()[0]
        current = subject
        entries.setdefault(current, {
            'label': None,
            'wikidata': None,
            'wikidata_url': None,
            'type': None,
        })
        type_match = re.search(r'a fhkb:([A-Za-z0-9_]+)', line)
        if type_match:
            entries[current]['type'] = type_match.group(1)
        continue

    if current is None:
        continue

    if line.startswith('rdfs:label'):
        match = re.search(r'rdfs:label\s+"([^\"]+)"@en', line)
        if match:
            entries[current]['label'] = match.group(1)
        continue

    if line.startswith('mdhn:agentialWikiData'):
        match = re.search(r'mdhn:agentialWikiData\s+"([^"]*)"', line)
        if match:
            url = match.group(1).strip()
            if url:
                entries[current]['wikidata_url'] = url
                q_match = re.search(r'Q[0-9]+', url)
                if q_match:
                    entries[current]['wikidata'] = q_match.group(0)
        continue

    if line.startswith('fhkb:'):
        predicate = line.split()[0]
        relation = predicate.split(':', 1)[1]
        targets = re.findall(r'mdhn:[A-Za-z0-9_]+', line)
        for target in targets:
            entries.setdefault(target, {
                'label': None,
                'wikidata': None,
                'wikidata_url': None,
                'type': None,
            })
            if relation in symmetric_relations:
                ordered = tuple(sorted([current, target]))
                edges.add((ordered[0], ordered[1], relation, 'none'))
            else:
                edges.add((current, target, relation, 'forward'))
        continue


def node_id(uri: str) -> str:
    safe = uri.replace('mdhn:', '').replace(':', '_')
    safe = ''.join(c if c.isalnum() or c == '_' else '_' for c in safe)
    if not safe:
        safe = 'node'
    if safe[0].isdigit():
        safe = '_' + safe
    return safe


def quote(text: str) -> str:
    return text.replace('"', '\\"')

lines_out = [
    'digraph PersonsGraph {',
    '  rankdir=TB;',
    '  graph [bgcolor="#ffffff"];',
    '  node [shape=box, style=filled, fontname="Arial", fontsize=9];',
    '  edge [color="#555555", fontname="Arial", fontsize=8];',
    '  splines=true;',
    '  overlap=false;',
    '  ranksep=0.8;',
    '  nodesep=0.4;',
]

for uri, entry in entries.items():
    nid = node_id(uri)
    label = entry['label'] or uri.replace('mdhn:', '')
    if entry['wikidata']:
        label = f'{label}\\n({entry["wikidata"]})'
    tooltip_text = entry['label'] or uri.replace('mdhn:', '')
    if entry['wikidata_url']:
        tooltip_text = f'{tooltip_text}\\n{entry["wikidata_url"]}'
    else:
        tooltip_text = f'{tooltip_text}\\n{uri}'
    fill = '#d8f7d8' if entry['wikidata'] else '#f2f2f2'
    url_attr = f' URL="{entry["wikidata_url"]}"' if entry['wikidata_url'] else ''
    lines_out.append(
        f'  "{nid}" [label="{quote(label)}", tooltip="{quote(tooltip_text)}", fillcolor="{fill}", fontcolor="#111111", style="filled", shape="box"{url_attr}];'
    )

for source, target, relation, direction in sorted(edges):
    source_id = node_id(source)
    target_id = node_id(target)
    dir_attr = 'dir=none' if direction == 'none' else ''
    lines_out.append(
        f'  "{source_id}" -> "{target_id}" [label="{quote(relation)}", color="#555555", fontcolor="#333333", fontsize=8, penwidth=1.0{(", " + dir_attr) if dir_attr else ""}];'
    )

lines_out.append('}')
output = script_dir / 'persons_graph.dot'
output.write_text('\n'.join(lines_out) + '\n', encoding='utf-8')
print('WROTE', output)
print('nodes', len(entries), 'edges', len(edges))
