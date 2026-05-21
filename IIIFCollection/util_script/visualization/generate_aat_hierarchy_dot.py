import json
import re
from pathlib import Path

path = Path('Ontology/aat_hierarchy.ttl')
text = path.read_text(encoding='utf-8')
lines = text.splitlines()

entries = {}
current = None
for line in lines:
    line = line.strip()
    if not line:
        current = None
        continue
    if line.startswith('mdhn:') and ' a mdhn:ResourceType' in line:
        subject = line.split()[0]
        current = subject
        entries[current] = {
            'label': None,
            'isGuideTerm': False,
            'broader': [],
        }
        continue
    if current is None:
        continue
    if line.startswith('rdfs:label'):
        m = re.search(r'rdfs:label\s+"([^"]+)"@en', line)
        if m:
            entries[current]['label'] = m.group(1)
        continue
    if line.startswith('mdhn:isGuideTerm'):
        if '"true"' in line:
            entries[current]['isGuideTerm'] = True
        else:
            entries[current]['isGuideTerm'] = False
        continue
    if line.startswith('mdhn:hasAATBroader'):
        parts = line.split()
        if len(parts) >= 2:
            broader = parts[1].rstrip(' .')
            if broader:
                entries[current]['broader'].append(broader)
        continue

# Add nodes for any broader nodes that aren't defined explicitly
for entry in list(entries.values()):
    for broader in entry['broader']:
        if broader not in entries:
            entries[broader] = {
                'label': broader.replace('mdhn:aat', 'aat'),
                'isGuideTerm': False,
                'broader': [],
            }


def node_id(uri):
    safe = uri.replace('mdhn:', '').replace(':', '_')
    safe = ''.join(c if c.isalnum() or c == '_' else '_' for c in safe)
    if safe and safe[0].isdigit():
        safe = '_' + safe
    return safe


def quote(text):
    return text.replace('"', '\\"')

lines = [
    'digraph AATHierarchy {',
    '  rankdir=TB;',
    '  node [shape=box, style=filled, fontname="Arial"];',
    '  edge [color="#555555"];',
]

for uri, entry in entries.items():
    nid = node_id(uri)
    label = entry['label'] or uri
    label = quote(f'{label}\\n({uri.replace("mdhn:", "")})')
    if entry['isGuideTerm']:
        fill = '#fff2ac'
        fontcolor = '#000000'
    else:
        fill = '#d9d9d9'
        fontcolor = '#111111'
    lines.append(f'  "{nid}" [label="{label}", fillcolor="{fill}", fontcolor="{fontcolor}"];')

for uri, entry in entries.items():
    child_id = node_id(uri)
    for broader in entry['broader']:
        parent_id = node_id(broader)
        lines.append(f'  "{parent_id}" -> "{child_id}";')

lines.append('}')
output = Path('aat_hierarchy_graph.dot')
output.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('WROTE', output)
print('nodes', len(entries), 'edges', sum(len(e['broader']) for e in entries.values()))
