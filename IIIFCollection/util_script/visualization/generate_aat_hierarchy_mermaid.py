import re
from pathlib import Path

script_dir = Path(__file__).resolve().parent
path = script_dir / '..' / '..' / 'Ontology' / 'aat_hierarchy.ttl'
path = path.resolve()
text = path.read_text(encoding='utf-8')
lines = text.splitlines()

entries = {}
current = None
for line in lines:
    stripped = line.strip()
    if not stripped:
        current = None
        continue
    if stripped.startswith('mdhn:') and ' a mdhn:ResourceType' in stripped:
        subject = stripped.split()[0]
        current = subject
        entries[current] = {
            'label': None,
            'isGuideTerm': False,
            'isInExtendedScope': False,
            'broader': [],
        }
        continue
    if current is None:
        continue
    if stripped.startswith('rdfs:label'):
        match = re.search(r'rdfs:label\s+"([^"]+)"@en', stripped)
        if match:
            entries[current]['label'] = match.group(1)
        continue
    if stripped.startswith('mdhn:isGuideTerm'):
        entries[current]['isGuideTerm'] = '"true"' in stripped
        continue
    if stripped.startswith('mdhn:isInExtendedScope'):
        entries[current]['isInExtendedScope'] = '"true"' in stripped
        continue
    if stripped.startswith('mdhn:hasAATBroader'):
        broader_items = re.findall(r'mdhn:aat[0-9]+', stripped)
        for broader in broader_items:
            entries[current]['broader'].append(broader)
        continue

# Add missing broader nodes to ensure all edges resolve
for entry in list(entries.values()):
    for broader in entry['broader']:
        if broader not in entries:
            entries[broader] = {
                'label': broader.replace('mdhn:aat', 'aat'),
                'isGuideTerm': False,
                'isInExtendedScope': False,
                'broader': [],
            }


def node_id(uri):
    safe = uri.replace('mdhn:', '').replace(':', '_')
    safe = ''.join(c if c.isalnum() or c == '_' else '_' for c in safe)
    if not safe:
        safe = 'node'
    if safe[0].isdigit():
        safe = '_' + safe
    return safe


def quote_text(value):
    return value.replace('"', '\\"')

lines = [
    'flowchart TB',
    '  classDef normal fill:#f2f2f2,stroke:#888,stroke-width:1px;',
    '  classDef guideTerm fill:#fff2ac,stroke:#b88f00,stroke-width:1px;',
    '  classDef extendedScope fill:#cfe2f3,stroke:#3b75a7,stroke-width:1px;',
    '  classDef both fill:#f4cccc,stroke:#a33b3b,stroke-width:1px;',
]

for uri, entry in entries.items():
    nid = node_id(uri)
    label = entry['label'] or uri
    label = quote_text(f'{label}\\n({uri.replace("mdhn:", "")})')
    if entry['isGuideTerm'] and entry['isInExtendedScope']:
        css = 'both'
    elif entry['isGuideTerm']:
        css = 'guideTerm'
    elif entry['isInExtendedScope']:
        css = 'extendedScope'
    else:
        css = 'normal'
    lines.append(f'  {nid}["{label}"]')
    lines.append(f'  class {nid} {css}')

for uri, entry in entries.items():
    child_id = node_id(uri)
    for broader in entry['broader']:
        parent_id = node_id(broader)
        lines.append(f'  {parent_id} --> {child_id}')

output = script_dir / 'aat2_hierarchy_tree.mmd'
output.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('WROTE', output)
print('nodes', len(entries), 'edges', sum(len(entry['broader']) for entry in entries.values()))
