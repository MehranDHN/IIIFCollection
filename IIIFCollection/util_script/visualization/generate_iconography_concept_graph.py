import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[1]
ONTOLOGY_PATH = ROOT_DIR / 'Ontology' / 'iconography_RDF.ttl'
OUTPUT_DOT = SCRIPT_DIR / 'iconography_concept_graph.dot'

# Edit this list to choose the iconography concepts that should be included by default.
INPUT_CONCEPTS = [
    'mdhn:Mourning',
    # 'mdhn:Simurgh',
    # Add more concepts here.
]

SKOS_EXACT = 'skos:exactMatch'
SKOS_RELATED = 'skos:relatedMatch'
SKOS_NARROW = 'skos:narrowMatch'


def normalize_term(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, dict):
        vals = []
        for v in value.values():
            term = normalize_term(v)
            if term:
                vals.append(term)
        return vals[0] if vals else None
    if isinstance(value, list):
        for v in value:
            term = normalize_term(v)
            if term:
                return term
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.startswith('<') and text.endswith('>'):
        text = text[1:-1].strip()
    terms = re.findall(r'mdhn:[A-Za-z0-9_]+', text)
    return terms[0] if terms else None


def normalize_label(value: Any) -> str:
    if isinstance(value, dict):
        en = value.get('en')
        if isinstance(en, list):
            return ' '.join(str(x) for x in en)
        if isinstance(en, str):
            return en
        return ' '.join(str(v) for v in value.values())
    if isinstance(value, list):
        return ' '.join(str(x) for x in value)
    return str(value) if value is not None else ''


def is_states_or_ascanvas_label(value: Any) -> bool:
    label_text = normalize_label(value).strip().lower()
    return 'states' in label_text or 'ascanvas' in label_text


def find_all_terms(value: Any) -> List[str]:
    terms: List[str] = []
    if isinstance(value, dict):
        for v in value.values():
            terms.extend(find_all_terms(v))
    elif isinstance(value, list):
        for v in value:
            terms.extend(find_all_terms(v))
    elif isinstance(value, str):
        terms.extend(re.findall(r'mdhn:[A-Za-z0-9_]+', value))
    return terms


def extract_allowed_terms(value: Any, allowed_terms: Set[str]) -> Set[str]:
    terms: Set[str] = set()
    if isinstance(value, dict):
        for v in value.values():
            terms.update(extract_allowed_terms(v, allowed_terms))
    elif isinstance(value, list):
        for v in value:
            terms.update(extract_allowed_terms(v, allowed_terms))
    elif isinstance(value, str):
        for term in re.findall(r'mdhn:[A-Za-z0-9_]+', value):
            if term in allowed_terms:
                terms.add(term)
    return terms


def expand_allowed_terms(ontology: Dict[str, Dict[str, Set[str]]]) -> Set[str]:
    terms: Set[str] = set(ontology.keys())
    for relations in ontology.values():
        for values in relations.values():
            terms.update(values)
    return terms


def parse_iconography_ontology(path: Path) -> Dict[str, Dict[str, Set[str]]]:
    if not path.exists():
        raise FileNotFoundError(f'Iconography ontology not found: {path}')

    concepts: Dict[str, Dict[str, Set[str]]] = {}
    current_subject: Optional[str] = None

    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue

        subject_match = re.match(r'^(mdhn:[A-Za-z0-9_]+)\b', line)
        if subject_match and not line.startswith('skos:'):
            current_subject = subject_match.group(1)
            if current_subject not in concepts:
                concepts[current_subject] = {SKOS_EXACT: set(), SKOS_RELATED: set()}

        if current_subject is None:
            continue

        if SKOS_EXACT in line:
            values = re.findall(r'mdhn:[A-Za-z0-9_]+', line)
            concepts[current_subject][SKOS_EXACT].update(values)
        if SKOS_RELATED in line or SKOS_NARROW in line:
            values = re.findall(r'mdhn:[A-Za-z0-9_]+', line)
            concepts[current_subject][SKOS_RELATED].update(values)

        if line.endswith('.'):
            current_subject = None

    return concepts


def collect_iconography_tags(resource: Any, allowed_terms: Set[str]) -> Dict[str, Set[str]]:
    direct_terms: Set[str] = set()
    canvas_terms: Set[str] = set()

    if isinstance(resource, dict):
        for key, value in resource.items():
            if key == 'metadata' and isinstance(value, list):
                for meta in value:
                    if isinstance(meta, dict) and is_states_or_ascanvas_label(meta.get('label')):
                        canvas_terms.update(extract_allowed_terms(meta.get('value'), allowed_terms))
                    else:
                        direct_terms.update(extract_allowed_terms(meta, allowed_terms))
            else:
                direct_terms.update(extract_allowed_terms(value, allowed_terms))
    else:
        direct_terms.update(extract_allowed_terms(resource, allowed_terms))

    direct_terms = {t for t in direct_terms if t in allowed_terms}
    canvas_terms = {t for t in canvas_terms if t in allowed_terms}
    return {
        'direct': direct_terms,
        'canvas': canvas_terms,
        'all': direct_terms | canvas_terms,
    }


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def safe_id(value: str) -> str:
    safe = re.sub(r'[^A-Za-z0-9_]', '_', value)
    if not safe or safe[0].isdigit():
        safe = '_' + safe
    return safe


def quote(value: str) -> str:
    return value.replace('"', '\\"').replace('\n', ' ')


def node_label(value: str, prefix: Optional[str] = None) -> str:
    label = value
    if prefix:
        label = f'{prefix}: {value}'
    return quote(label)


def find_relating_resources(root: Path, concepts: Set[str], ontology_concepts: Set[str]) -> List[Dict[str, Any]]:
    files = sorted(root.glob('*Collection.json'))
    resources: List[Dict[str, Any]] = []

    for path in files:
        try:
            collection = load_json(path)
        except Exception:
            continue

        collection_label = collection.get('label') or path.stem

        for resource in collection.get('manifests', []) + collection.get('items', []):
            tags = collect_iconography_tags(resource, ontology_concepts)
            if not tags['all']:
                continue
            if not tags['all'].intersection(concepts):
                continue

            resource_id = resource.get('id') or resource.get('@id') or f'{path.name}:{len(resources)+1}'
            resource_label = resource.get('label') or resource_id
            resources.append(
                {
                    'id': resource_id,
                    'label': resource_label,
                    'collection': str(path.name),
                    'collection_label': collection_label,
                    'concepts': sorted(tags['all']),
                    'direct_concepts': sorted(tags['direct']),
                    'canvas_concepts': sorted(tags['canvas']),
                }
            )

    return resources


def build_graph(
    selected_concepts: Set[str],
    ontology: Dict[str, Dict[str, Set[str]]],
    resources: List[Dict[str, Any]],
) -> List[str]:
    dot_lines: List[str] = [
        'digraph IconographyConceptGraph {',
        '  rankdir=LR;',
        '  node [fontname="Arial", fontsize=10, shape=box];',
        '  edge [fontname="Arial", fontsize=8];',
    ]

    all_concepts: Set[str] = set(selected_concepts)
    for concept in selected_concepts:
        all_concepts.update(ontology.get(concept, {}).get(SKOS_EXACT, set()))
        all_concepts.update(ontology.get(concept, {}).get(SKOS_RELATED, set()))

    for resource in resources:
        all_concepts.update(resource['concepts'])

    concept_style = {}
    for concept in sorted(all_concepts):
        if concept in selected_concepts:
            concept_style[concept] = ('box', '#f4cccc', '#a33b3b')
        elif any(concept in ontology.get(c, {}).get(SKOS_EXACT, set()) for c in selected_concepts):
            concept_style[concept] = ('diamond', '#fff2ac', '#b88f00')
        elif any(concept in ontology.get(c, {}).get(SKOS_RELATED, set()) for c in selected_concepts):
            concept_style[concept] = ('ellipse', '#cfe2f3', '#3b75a7')
        else:
            concept_style[concept] = ('oval', '#d9ead3', '#3b6a37')

    for concept in sorted(all_concepts):
        nid = safe_id(concept)
        shape, fillcolor, color = concept_style[concept]
        label = node_label(concept)
        dot_lines.append(
            f'  "{nid}" [label="{label}", shape={shape}, style=filled, fillcolor="{fillcolor}", color="{color}"]'
        )

    for concept in sorted(selected_concepts):
        nid = safe_id(concept)
        for exact in sorted(ontology.get(concept, {}).get(SKOS_EXACT, set())):
            dot_lines.append(
                f'  "{nid}" -> "{safe_id(exact)}" [label="exactMatch", color="#b23c17"]'
            )
        for related in sorted(ontology.get(concept, {}).get(SKOS_RELATED, set())):
            dot_lines.append(
                f'  "{nid}" -> "{safe_id(related)}" [label="relatedMatch", style=dashed, color="#6a3d9a"]'
            )

    for resource in resources:
        rid = safe_id(resource['id'])
        resource_label = quote(f"{resource['label']}\n({resource['collection_label']})")
        dot_lines.append(
            f'  "{rid}" [label="{resource_label}", shape=note, fillcolor="#dae8fc", color="#6c8ebf"]'
        )
        coll_id = safe_id(f"COL_{resource['collection']}")
        coll_label = quote(resource['collection_label'])
        dot_lines.append(
            f'  "{coll_id}" [label="Collection: {coll_label}", shape=folder, fillcolor="#d5e8d4", color="#6aa84f"]'
        )
        dot_lines.append(
            f'  "{coll_id}" -> "{rid}" [label="contains", color="#6c8ebf"]'
        )
        for concept in resource['concepts']:
            if concept in resource['direct_concepts'] and concept in resource['canvas_concepts']:
                label = 'depicts / page'
                style = 'bold'
                color = '#b85450'
            elif concept in resource['direct_concepts']:
                label = 'depicts'
                style = 'solid'
                color = '#b85450'
            else:
                label = 'page/canvas'
                style = 'dashed'
                color = '#2f74b5'

            dot_lines.append(
                f'  "{rid}" -> "{safe_id(concept)}" [label="{label}", style={style}, color="{color}"]'
            )

    dot_lines.append('}')
    return dot_lines


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate a DOT graph for Iconography concepts and matching resources.'
    )
    parser.add_argument(
        '--dot',
        type=Path,
        default=OUTPUT_DOT,
        help='Output DOT file path.',
    )
    args = parser.parse_args()

    selected_concepts = set()
    for raw in INPUT_CONCEPTS:
        term = normalize_term(raw)
        if term:
            selected_concepts.add(term)
        else:
            selected_concepts.add(raw.strip())

    if not selected_concepts:
        raise SystemExit('At least one concept must be defined in INPUT_CONCEPTS.')

    ontology = parse_iconography_ontology(ONTOLOGY_PATH)
    allowed_terms = expand_allowed_terms(ontology)

    expanded_concepts = set(selected_concepts)
    for concept in list(selected_concepts):
        expanded_concepts.update(ontology.get(concept, {}).get(SKOS_EXACT, set()))
        expanded_concepts.update(ontology.get(concept, {}).get(SKOS_RELATED, set()))

    resources = find_relating_resources(ROOT_DIR, expanded_concepts, allowed_terms)

    if not resources:
        print('No resources found referencing the selected concepts. The graph will still include the selected nodes.')

    dot_lines = build_graph(selected_concepts, ontology, resources)
    args.dot.parent.mkdir(parents=True, exist_ok=True)
    args.dot.write_text('\n'.join(dot_lines) + '\n', encoding='utf-8')
    print(f'WROTE {args.dot}')
    print(f'INPUT CONCEPTS: {sorted(INPUT_CONCEPTS)}')
    print(f'SELECTED CONCEPTS: {sorted(selected_concepts)}')
    print(f'EXPANDED CONCEPTS: {sorted(expanded_concepts)}')
    print(f'RESOURCE NODES: {len(resources)}')


if __name__ == '__main__':
    main()
