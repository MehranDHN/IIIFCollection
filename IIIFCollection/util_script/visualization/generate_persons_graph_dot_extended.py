import re
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS


script_dir = Path(__file__).resolve().parent
ontology_path = script_dir / '..' / '..' / 'Ontology' / 'iiifCollectionOntology.ttl'
data_path = script_dir / '..' / '..' / 'Ontology' / 'PersonsRDFData.ttl'
out_path = script_dir / 'persons_graph_extended.dot'

ontology_path = ontology_path.resolve()
data_path = data_path.resolve()
out_path = out_path.resolve()
render_engine = 'sfdp' if shutil.which('sfdp') else 'dot'

fhkb = Namespace('http://www.example.com/genealogy.owl#')
mdhn = Namespace('http://example.com/mdhn/')


def is_uri(node):
    return isinstance(node, URIRef)


def is_literal(node):
    return isinstance(node, Literal)


def node_id(node):
    if isinstance(node, Literal):
        text = str(node.value)
    else:
        text = str(node)
    text = text.replace('http://example.com/mdhn/', 'mdhn:')
    text = text.replace('http://www.example.com/genealogy.owl#', 'fhkb:')
    text = text.replace('http://www.w3.org/2000/01/rdf-schema#', 'rdfs:')
    text = text.replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'rdf:')
    text = text.replace('http://www.w3.org/2002/07/owl#', 'owl:')
    text = re.sub(r'[^A-Za-z0-9_]+', '_', text)
    text = text.strip('_')
    if not text:
        text = 'node'
    if text[0].isdigit():
        text = '_' + text
    return text


def quote(text):
    return text.replace('"', '\\"')


def label_for(node):
    if isinstance(node, Literal):
        return str(node.value)
    if isinstance(node, BNode):
        return f'bnode:{node_id(node)}'
    uri = str(node)
    for prefix, namespace in [('mdhn:', mdhn), ('fhkb:', fhkb)]:
        if uri.startswith(str(namespace)):
            return prefix + uri[len(str(namespace)):]
    if uri.startswith('http://'):
        return uri.rsplit('/', 1)[-1]
    return uri


def preferred_label(graph, node):
    if isinstance(node, Literal):
        return str(node.value)
    if isinstance(node, BNode):
        return f'bnode:{node_id(node)}'
    labels = [str(lit.value) for lit in graph.objects(node, RDFS.label) if isinstance(lit, Literal)]
    if not labels:
        return label_for(node)
    return labels[0]


def collect_ancestors(node, parent_map):
    visited = set()
    stack = list(parent_map.get(node, set()))
    ancestors = set()
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        ancestors.add(current)
        stack.extend(parent_map.get(current, set()))
    return ancestors


def load_graph(path):
    g = Graph()
    g.parse(path, format='turtle')
    return g


ontology_graph = load_graph(ontology_path)
data_graph = load_graph(data_path)

# Combine the graphs so the script can use ontology and instance data together.
graph = ontology_graph + data_graph

# Build hierarchy maps.
class_parents = defaultdict(set)
for s, p, o in graph:
    if p == RDFS.subClassOf and is_uri(s) and is_uri(o):
        class_parents[s].add(o)

property_parents = defaultdict(set)
for s, p, o in graph:
    if p == RDFS.subPropertyOf and is_uri(s) and is_uri(o):
        property_parents[s].add(o)

inverse_map = {}
for s, p, o in graph:
    if p == OWL.inverseOf and is_uri(s) and is_uri(o):
        inverse_map[s] = o
        inverse_map[o] = s

# Domain/range information for properties.
property_domains = defaultdict(set)
property_ranges = defaultdict(set)
for s, p, o in graph:
    if p == RDFS.domain and is_uri(s) and is_uri(o):
        property_domains[s].add(o)
    if p == RDFS.range and is_uri(s) and is_uri(o):
        property_ranges[s].add(o)

# Gather all URI/BNode nodes from the data graph and relevant classes from the ontology.
all_data_nodes = set()
for s, p, o in data_graph:
    if is_uri(s) or isinstance(s, BNode):
        all_data_nodes.add(s)
    if is_uri(o) or isinstance(o, BNode):
        all_data_nodes.add(o)

# Collect explicit types and inferred types for each data node.
explicit_types = defaultdict(set)
for s, p, o in data_graph:
    if p == RDF.type and is_uri(o):
        explicit_types[s].add(o)

inferred_types = defaultdict(set)
for node in all_data_nodes:
    inferred_types[node].update(explicit_types.get(node, set()))

# Infer classes from domain/range and class hierarchy.
for s, p, o in data_graph:
    if p in property_domains:
        for domain_cls in property_domains[p]:
            inferred_types[s].add(domain_cls)
            inferred_types[s].update(collect_ancestors(domain_cls, class_parents))
    if p in property_ranges and not is_literal(o):
        for range_cls in property_ranges[p]:
            if is_uri(o) or isinstance(o, BNode):
                inferred_types[o].add(range_cls)
                inferred_types[o].update(collect_ancestors(range_cls, class_parents))

# Expand each type to its ancestors.
for node, types in list(inferred_types.items()):
    expanded = set()
    for t in types:
        expanded.add(t)
        expanded.update(collect_ancestors(t, class_parents))
    inferred_types[node] = expanded

# Also include the data nodes' own types as nodes in the graph.
class_nodes = set()
for types in inferred_types.values():
    class_nodes.update(types)

# Gather all properties used in the data graph.
data_properties = set()
for _, p, _ in data_graph:
    if is_uri(p):
        data_properties.add(p)

# Build the list of graph edges.
# Each edge entry: (source, target, label, kind, attrs)
edges = []

# Add type edges for all inferred types.
for node, types in sorted(inferred_types.items(), key=lambda item: str(item[0])):
    for class_node in sorted(types, key=lambda n: str(n)):
        if is_uri(node) or isinstance(node, BNode):
            edges.append((node, class_node, 'type', 'type', {'color': '#1f78b4', 'penwidth': '1.2'}))

# Add explicit relationship edges and their inferred equivalents.
for s, p, o in sorted(data_graph, key=lambda triple: (str(triple[0]), str(triple[1]), str(triple[2]))):
    if p == RDF.type:
        continue
    if is_literal(o):
        # Skip literal-value nodes for readability; the graph focuses on entity-to-entity relations.
        continue
    if not (is_uri(s) or isinstance(s, BNode)) or not (is_uri(o) or isinstance(o, BNode)):
        continue

    # Direct edge.
    edge_label = label_for(p)
    edges.append((s, o, edge_label, 'relation', {'color': '#b23c17', 'penwidth': '1.0'}))

    # Inferred inverse edges.
    if p in inverse_map:
        inverse_p = inverse_map[p]
        edges.append((o, s, label_for(inverse_p), 'inferred', {'color': '#7b1fa2', 'penwidth': '0.9', 'style': 'dashed'}))

    # Inferred super-property edges.
    for parent in property_parents.get(p, set()):
        edges.append((s, o, label_for(parent), 'inferred', {'color': '#6a3d9a', 'penwidth': '0.8', 'style': 'dotted'}))

    # Add domain/range type edges when relevant.
    for domain_cls in property_domains.get(p, set()):
        edges.append((s, domain_cls, 'domain', 'type', {'color': '#1f78b4', 'penwidth': '1.0'}))
    for range_cls in property_ranges.get(p, set()):
        edges.append((o, range_cls, 'range', 'type', {'color': '#1f78b4', 'penwidth': '1.0'}))

# Ensure nodes from the ontology that are used as class targets are included.
for node in list(class_nodes):
    if is_uri(node):
        all_data_nodes.add(node)

# Write DOT file.
lines = []
lines.append('digraph PersonsGraphExtended {')
lines.append('  rankdir=TB;')
lines.append('  graph [bgcolor="#ffffff", splines=true, overlap=false, outputorder=edgesfirst, layout=sfdp, pad=0.25, sep="+25", nodesep=0.7, ranksep=1.0, labelloc=t, label="Persons Graph Extended"];')
lines.append('  node [fontname="Arial", fontsize=10];')
lines.append('  edge [fontname="Arial", fontsize=8];')

# Emit nodes.
node_ids = {}
for node in sorted(all_data_nodes | class_nodes, key=lambda item: str(item)):
    node_id_value = node_id(node)
    node_ids[node] = node_id_value

# Render the main entity and ontology-class nodes only.
for node in sorted(all_data_nodes | class_nodes, key=lambda item: str(item)):
    nid = node_id(node)
    label_text = preferred_label(data_graph, node) if node in all_data_nodes else label_for(node)
    if node in inferred_types and inferred_types[node]:
        label_text = f'{label_text}'
    if node in explicit_types and explicit_types[node]:
        # Keep simple.
        pass
    if node in class_nodes:
        fillcolor = '#fff2cc'
        shape = 'box'
    else:
        has_wiki = any(isinstance(lit, Literal) and 'wikidata.org/wiki/' in str(lit.value) for lit in data_graph.objects(node, mdhn.agentialWikiData))
        fillcolor = '#d9ead3' if has_wiki else '#e7f3ff'
        shape = 'ellipse'
    lines.append(f'  "{nid}" [label="{quote(label_text)}", shape={shape}, style="filled", fillcolor="{fillcolor}"];')

# Render edges.
for source, target, label, kind, attrs in sorted(edges, key=lambda entry: (str(entry[0]), str(entry[1]), entry[2], entry[3])):
    src_id = node_id(source) if not isinstance(source, str) else source
    tgt_id = node_id(target) if not isinstance(target, str) else target
    color = attrs.get('color', '#555555')
    penwidth = attrs.get('penwidth', '1.0')
    style = attrs.get('style', 'solid')
    if kind == 'type':
        lines.append(f'  "{src_id}" -> "{tgt_id}" [label="{quote(label)}", color="{color}", penwidth={penwidth}, style="{style}", arrowhead=normal];')
    elif kind == 'literal':
        lines.append(f'  "{src_id}" -> "{tgt_id}" [label="{quote(label)}", color="{color}", penwidth={penwidth}, style="{style}", arrowhead=vee];')
    else:
        lines.append(f'  "{src_id}" -> "{tgt_id}" [label="{quote(label)}", color="{color}", penwidth={penwidth}, style="{style}", arrowhead=vee];')

lines.append('}')
out_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('WROTE', out_path)
print('nodes', len(all_data_nodes | class_nodes), 'edges', len(edges))

if shutil.which(render_engine):
    for fmt in ('png', 'svg'):
        image_path = out_path.with_suffix(f'.{fmt}')
        subprocess.run([render_engine, '-T', fmt, str(out_path), '-o', str(image_path)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print('WROTE', image_path)
else:
    print('Graphviz renderer not found; skipped image export')
