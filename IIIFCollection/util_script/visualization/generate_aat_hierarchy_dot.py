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
    # include any subject that declares a mdhn: type (ResourceType, AATSubject, ScriptStyleType, etc.)
    if stripped.startswith('mdhn:') and ' a mdhn:' in stripped:
        subject = stripped.split()[0]
        current = subject
        # capture the declared mdhn type (e.g. mdhn:ResourceType, mdhn:AATSubject)
        type_match = re.search(r' a (mdhn:[A-Za-z0-9_]+)', stripped)
        declared_type = type_match.group(1) if type_match else None
        entries[current] = {
            'label': None,
            'isGuideTerm': False,
            'isInExtendedScope': False,
            'comment': None,
            'broader': [],
            'type': declared_type,
        }
        continue
    if current is None:
        continue
    if stripped.startswith('rdfs:label'):
        m = re.search(r'rdfs:label\s+"([^"]+)"@en', stripped)
        if m:
            entries[current]['label'] = m.group(1)
        continue
    if stripped.startswith('rdfs:comment'):
        m = re.search(r'rdfs:comment\s+"([^"]+)"@en', stripped)
        if m:
            entries[current]['comment'] = m.group(1)
        continue
    if stripped.startswith('mdhn:isGuideTerm'):
        entries[current]['isGuideTerm'] = '"true"' in stripped
        continue
    if stripped.startswith('mdhn:isInExtendedScope') or stripped.startswith('mdhn:isinExtendedScope'):
        entries[current]['isInExtendedScope'] = '"true"' in stripped
        continue
    if stripped.startswith('mdhn:hasAATBroader'):
        broader_items = re.findall(r'mdhn:aat[0-9]+', stripped)
        for broader in broader_items:
            entries[current]['broader'].append(broader)
        continue

# Add nodes for any broader nodes that aren't defined explicitly
for entry in list(entries.values()):
    for broader in entry['broader']:
        if broader not in entries:
            entries[broader] = {
                'label': broader.replace('mdhn:aat', 'aat'),
                'isGuideTerm': False,
                'isInExtendedScope': False,
                'comment': None,
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


def quote(text):
    return text.replace('"', '\\"')

lines = [
    'digraph AATHierarchy {',
    '  rankdir=TB;',
    '  graph [bgcolor="#ffffff"];',
    '  node [shape=box, style="filled,rounded", fontname="Arial", fontsize=8, penwidth=0.8];',
    '  edge [color="#555555", arrowsize=0.8];',
    '  overlap=scale;',
    '  splines=true;',
    '  ranksep=1.0;',
    '  nodesep=0.4;',
]

for uri, entry in entries.items():
    nid = node_id(uri)
    label = entry['label'] or uri
    label = quote(f'{label}\\n({uri.replace("mdhn:", "")})')
    tooltip = entry['comment'] or entry['label'] or uri
    tooltip = quote(tooltip)
    # Type-based coloring (default), but preserve guide/extended highlights as higher priority
    if entry['isGuideTerm'] and entry['isInExtendedScope']:
        fill = "#124f75"
        fontcolor = '#000000'
    elif entry['isGuideTerm']:
        fill = '#fff2ac'
        fontcolor = '#000000'
    elif entry['isInExtendedScope']:
        fill = '#C1503F'
        fontcolor = "#000000"
    else:
        type_color_map = {
            'mdhn:ResourceType': '#f2f2f2',
            'mdhn:AATSubject': '#d8f7d8',
            'mdhn:ScriptStyleType': '#e8d9f7',
        }
        declared_type = entry.get('type')
        fill = type_color_map.get(declared_type, '#f2f2f2')
        fontcolor = '#111111'
    lines.append(
        f'  "{nid}" [label="{label}", tooltip="{tooltip}", fillcolor="{fill}", fontcolor="{fontcolor}"];'
    )

for uri, entry in entries.items():
    child_id = node_id(uri)
    for broader in entry['broader']:
        parent_id = node_id(broader)
        lines.append(f'  "{parent_id}" -> "{child_id}";')

lines.append('}')
output = script_dir / 'aat_hierarchy_graph.dot'
output.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('WROTE', output)
print('nodes', len(entries), 'edges', sum(len(e['broader']) for e in entries.values()))

# Validation: ensure nodes referenced as broader have children (outgoing edges)
children = {uri: set() for uri in entries.keys()}
for child, entry in entries.items():
    for broader in entry['broader']:
        children.setdefault(broader, set()).add(child)

inconsistencies = []
for uri, entry in entries.items():
    referenced_as_broader = any(uri in e['broader'] for e in entries.values())
    child_count = len(children.get(uri, set()))
    if referenced_as_broader and child_count == 0:
        inconsistencies.append((uri, entry.get('label'), [e for e in entries.values() if uri in e['broader']]))

report_path = script_dir / 'aat_hierarchy_validation.txt'
with report_path.open('w', encoding='utf-8') as f:
    f.write(f'Total nodes: {len(entries)}\n')
    f.write(f'Nodes referenced as broader but with zero children: {len(inconsistencies)}\n\n')
    for uri, label, refs in inconsistencies:
        f.write(f'Node {uri} ({label}) referenced by {len(refs)} nodes but has 0 computed children:\n')
        # list up to 10 ref subjects
        count = 0
        for subj_uri, subj_entry in entries.items():
            if uri in subj_entry['broader']:
                f.write(f'  - {subj_uri} label={subj_entry.get("label")}\n')
                count += 1
                if count >= 50:
                    f.write('  ... (truncated)\n')
                    break
        f.write('\n')

    # Cycle detection in parent-child graph
    visited = set()
    cycles = []

    def dfs(node, path):
        if node in path:
            idx = path.index(node)
            cycle = path[idx:] + [node]
            cycles.append(cycle)
            return
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        for child in children.get(node, []):
            dfs(child, path)
        path.pop()

    for node in entries.keys():
        if node not in visited:
            dfs(node, [])

    f.write('Cycle detection report:\n')
    f.write(f'Cycles found: {len(cycles)}\n')
    for cycle in cycles:
        labels = [f'{node} ({entries[node].get("label")})' for node in cycle]
        f.write('  - ' + ' -> '.join(labels) + '\n')

print('WROTE', report_path)
