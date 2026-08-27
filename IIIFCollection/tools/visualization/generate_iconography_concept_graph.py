import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[1]
ONTOLOGY_PATH = ROOT_DIR / 'Ontology' / 'iconography_RDF.ttl'
NARRATIVE_PATH = ROOT_DIR / 'Ontology' / 'narrative_episodes.ttl'
PERSONS_PATH = ROOT_DIR / 'Ontology' / 'PersonsRDFData.ttl'
OUTPUT_DOT = SCRIPT_DIR / 'iconography_concept_graph.dot'

# Edit this list to choose the iconography concepts that should be included by default.
INPUT_CONCEPTS = [
    'mdhn:Divs'
    #'mdhn:Ascension_of_the_Prophet',
    # Add more concepts here.
]

SKOS_EXACT = 'skos:exactMatch'
SKOS_RELATED = 'skos:relatedMatch'
SKOS_NARROW = 'skos:narrowMatch'
SKOS_CLOSE = 'skos:closeMatch'
SKOS_BROAD = 'skos:broadMatch'
SKOS_BROADER = 'skos:broader'
SKOS_NARROWER = 'skos:narrower'
WIKIDATA_PRED = 'mdhn:icWikiDataURL'
SAID_SAME = 'mdhn:saidToBeTheSameAs'
QCODE_RE = re.compile(r'Q\d+', re.IGNORECASE)
WD_CURIE_RE = re.compile(r'(?:wd|WD):Q(\d+)', re.IGNORECASE)
WIKIDATA_LINE_RE = re.compile(r'mdhn:icWikiDataURL\s+"([^"]*)"')
SAID_SAME_LINE_RE = re.compile(r'mdhn:saidToBeTheSameAs\b')
SKOS_PRED_RE = re.compile(r'(skos:[A-Za-z]+)')
SKOS_OBJECT_RE = re.compile(
    r"<[^>]+>|mdhn:[A-Za-z0-9_]+|[A-Za-z][A-Za-z0-9_-]*:[A-Za-z0-9_.:/%()'-]+"
)
SUBJECT_DECL_RE = re.compile(r'^(mdhn:[A-Za-z0-9_]+)\s+a\b')
IS_PART_OF = 'mdhn:isPartOf'

SKOS_EDGE_STYLE = {
    IS_PART_OF: ('isPartOf', 'solid', '#38761d'),
    SKOS_EXACT: ('exactMatch', 'solid', '#b23c17'),
    SKOS_RELATED: ('relatedMatch', 'dashed', '#6a3d9a'),
    SKOS_NARROW: ('narrowMatch', 'dashed', '#6a3d9a'),
    SKOS_CLOSE: ('closeMatch', 'dashed', '#3b75a7'),
    SKOS_BROAD: ('broadMatch', 'dashed', '#3b75a7'),
    SKOS_BROADER: ('broader', 'solid', '#38761d'),
    SKOS_NARROWER: ('narrower', 'solid', '#38761d'),
    'skos:relatedMath': ('relatedMatch', 'dashed', '#6a3d9a'),
    SAID_SAME: ('saidToBeTheSameAs', 'solid', '#b23c17'),
}


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
    if terms:
        return terms[0]
    wd_match = WD_CURIE_RE.search(text)
    if wd_match:
        return f'wd:Q{wd_match.group(1)}'
    return None


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
        terms.extend(f'wd:Q{m}' for m in WD_CURIE_RE.findall(value))
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
        for qnum in WD_CURIE_RE.findall(value):
            term = f'wd:Q{qnum}'
            if term in allowed_terms:
                terms.add(term)
    return terms


def extract_qcode(raw: Any) -> Optional[str]:
    """Return only the Wikidata Q-code (e.g. Q170544), never the full URL."""
    if raw is None:
        return None
    match = QCODE_RE.search(str(raw).strip())
    return match.group(0).upper() if match else None


def expand_allowed_terms(ontology: Dict[str, Dict[str, Set[str]]]) -> Set[str]:
    terms: Set[str] = set(ontology.keys())
    for relations in ontology.values():
        for pred, values in relations.items():
            if pred == WIKIDATA_PRED:
                continue
            terms.update(values)
    return terms


def parse_iconography_ontology(
    path: Path,
) -> Tuple[Dict[str, Dict[str, Set[str]]], Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f'Iconography ontology not found: {path}')

    concepts: Dict[str, Dict[str, Set[str]]] = {}
    wikidata: Dict[str, str] = {}
    current_subject: Optional[str] = None
    in_triple = False

    for raw_line in path.read_text(encoding='utf-8').splitlines():
        if in_triple:
            if '"""' in raw_line:
                in_triple = False
                after = raw_line.rsplit('"""', 1)[-1].strip()
                if after.endswith('.'):
                    current_subject = None
            continue

        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue

        if '"""' in line and line.count('"""') == 1:
            in_triple = True
            subject_match = SUBJECT_DECL_RE.match(line)
            if subject_match:
                current_subject = subject_match.group(1)
                if current_subject not in concepts:
                    concepts[current_subject] = {}
            continue

        subject_match = SUBJECT_DECL_RE.match(line)
        if subject_match:
            current_subject = subject_match.group(1)
            if current_subject not in concepts:
                concepts[current_subject] = {}

        if current_subject is None:
            continue

        if 'skos:' in line:
            pred_match = SKOS_PRED_RE.search(line)
            if pred_match:
                predicate = pred_match.group(1)
                values = [
                    term
                    for term in SKOS_OBJECT_RE.findall(line)
                    if not term.startswith('skos:') and term != current_subject
                ]
                if values:
                    concepts[current_subject].setdefault(predicate, set()).update(values)

        if line.startswith(IS_PART_OF):
            values = [
                term
                for term in SKOS_OBJECT_RE.findall(line)
                if term not in (IS_PART_OF, current_subject)
                and not term.startswith('skos:')
            ]
            if values:
                concepts[current_subject].setdefault(IS_PART_OF, set()).update(values)

        if SAID_SAME_LINE_RE.search(line):
            values = set()
            for term in SKOS_OBJECT_RE.findall(line):
                if term in {SAID_SAME, current_subject} or term.startswith('skos:'):
                    continue
                wd_match = WD_CURIE_RE.search(term)
                values.add(f'wd:Q{wd_match.group(1)}' if wd_match else term)
            if values:
                concepts[current_subject].setdefault(SAID_SAME, set()).update(values)

        wiki_match = WIKIDATA_LINE_RE.search(line)
        if wiki_match:
            qcode = extract_qcode(wiki_match.group(1))
            if qcode:
                wikidata[current_subject] = qcode

        if line.endswith('.'):
            current_subject = None

    return concepts, wikidata


def extract_depicts_terms(value: Any) -> Set[str]:
    """Every mdhn: term from a canvas-level 'depicts' array (AsCanvas / States)."""
    terms: Set[str] = set()
    if isinstance(value, dict):
        if 'depicts' in value:
            for item in value.get('depicts') or []:
                term = normalize_term(item)
                if term:
                    terms.add(term)
        for nested in value.values():
            terms.update(extract_depicts_terms(nested))
    elif isinstance(value, list):
        for item in value:
            terms.update(extract_depicts_terms(item))
    return terms


def collect_iconography_tags(resource: Any, allowed_terms: Set[str]) -> Dict[str, Set[str]]:
    direct_terms: Set[str] = set()
    canvas_terms: Set[str] = set()

    if isinstance(resource, dict):
        for key, value in resource.items():
            if key == 'metadata' and isinstance(value, list):
                for meta in value:
                    if isinstance(meta, dict) and is_states_or_ascanvas_label(meta.get('label')):
                        canvas_terms.update(extract_allowed_terms(meta.get('value'), allowed_terms))
                        # Depicts tags must appear even when they live only in
                        # narrative_episodes.ttl (isPartOf hierarchy), not iconography_RDF.
                        canvas_terms.update(extract_depicts_terms(meta.get('value')))
                    else:
                        direct_terms.update(extract_allowed_terms(meta, allowed_terms))
            else:
                direct_terms.update(extract_allowed_terms(value, allowed_terms))
    else:
        direct_terms.update(extract_allowed_terms(resource, allowed_terms))

    direct_terms = {t for t in direct_terms if t in allowed_terms}
    canvas_terms = {
        t
        for t in canvas_terms
        if t in allowed_terms or t.startswith('mdhn:') or t.startswith('wd:')
    }
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


def concept_label(
    concept: str,
    wikidata: Dict[str, str],
    relations: Optional[Dict[str, Set[str]]] = None,
) -> str:
    """Concept id, then Q-code and every SKOS relation, each on its own line."""
    parts = [quote(concept)]
    qcode = wikidata.get(concept)
    if qcode:
        parts.append(quote(qcode))
    for pred in sorted(relations or {}):
        objects = sorted(relations[pred])
        if objects:
            parts.append(quote(f'{pred}: {", ".join(objects)}'))
    return '\\n'.join(parts)


def skos_targets(ontology: Dict[str, Dict[str, Set[str]]], concept: str) -> Set[str]:
    targets: Set[str] = set()
    for values in ontology.get(concept, {}).values():
        targets.update(values)
    return targets


def find_relating_resources(root: Path, concepts: Set[str], ontology_concepts: Set[str]) -> List[Dict[str, Any]]:
    files = sorted(root.glob('*Collection.json'))
    resources: List[Dict[str, Any]] = []

    for path in files:
        try:
            collection = load_json(path)
        except Exception:
            continue

        collection_label = collection.get('label') or path.stem

        for resource in (
            list(collection.get('manifests') or [])
            + list(collection.get('items') or [])
            + list(collection.get('members') or [])
        ):
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
    wikidata: Optional[Dict[str, str]] = None,
) -> List[str]:
    wikidata = wikidata or {}
    dot_lines: List[str] = [
        'digraph IconographyConceptGraph {',
        '  rankdir=LR;',
        '  node [fontname="Arial", fontsize=10, shape=box];',
        '  edge [fontname="Arial", fontsize=8];',
    ]

    all_concepts: Set[str] = set(selected_concepts)
    for resource in resources:
        all_concepts.update(resource['concepts'])

    # Include one hop of SKOS neighbours so depicted tags keep their hierarchy.
    for concept in list(all_concepts):
        all_concepts.update(skos_targets(ontology, concept))

    selected_exact = set()
    selected_related = set()
    for concept in selected_concepts:
        selected_exact.update(ontology.get(concept, {}).get(SKOS_EXACT, set()))
        selected_exact.update(ontology.get(concept, {}).get(SAID_SAME, set()))
        for pred, values in ontology.get(concept, {}).items():
            if pred not in {SKOS_EXACT, SAID_SAME}:
                selected_related.update(values)

    concept_style = {}
    for concept in sorted(all_concepts):
        if concept in selected_concepts:
            concept_style[concept] = ('box', '#f4cccc', '#a33b3b')
        elif concept in selected_exact:
            concept_style[concept] = ('diamond', '#fff2ac', '#b88f00')
        elif concept in selected_related:
            concept_style[concept] = ('ellipse', '#cfe2f3', '#3b75a7')
        else:
            concept_style[concept] = ('oval', '#d9ead3', '#3b6a37')

    for concept in sorted(all_concepts):
        nid = safe_id(concept)
        shape, fillcolor, color = concept_style[concept]
        label = concept_label(concept, wikidata, ontology.get(concept, {}))
        dot_lines.append(
            f'  "{nid}" [label="{label}", shape={shape}, style=filled, fillcolor="{fillcolor}", color="{color}"]'
        )

    drawn_edges: Set[Tuple[str, str, str]] = set()
    for concept in sorted(all_concepts):
        nid = safe_id(concept)
        for pred, values in sorted(ontology.get(concept, {}).items()):
            edge_label, style, color = SKOS_EDGE_STYLE.get(
                pred, (pred.replace('skos:', ''), 'dashed', '#666666')
            )
            for target in sorted(values):
                key = (nid, safe_id(target), edge_label)
                if key in drawn_edges:
                    continue
                drawn_edges.add(key)
                dot_lines.append(
                    f'  "{nid}" -> "{safe_id(target)}" '
                    f'[label="{edge_label}", style={style}, color="{color}"]'
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

    ontology, wikidata = parse_iconography_ontology(ONTOLOGY_PATH)
    for extra_path in (NARRATIVE_PATH, PERSONS_PATH):
        if not extra_path.exists():
            continue
        extra_ontology, extra_wiki = parse_iconography_ontology(extra_path)
        for term, rels in extra_ontology.items():
            if term not in ontology:
                ontology[term] = {}
            for pred, values in rels.items():
                ontology[term].setdefault(pred, set()).update(values)
        for term, qcode in extra_wiki.items():
            wikidata.setdefault(term, qcode)
    allowed_terms = expand_allowed_terms(ontology)
    for qcode in wikidata.values():
        if qcode:
            allowed_terms.add(f'wd:{qcode}')

    expanded_concepts = set(selected_concepts)
    for concept in list(selected_concepts):
        expanded_concepts.update(skos_targets(ontology, concept))
        qcode = wikidata.get(concept)
        if qcode:
            expanded_concepts.add(f'wd:{qcode}')
    # Reverse saidToBeTheSameAs: other concepts that identify as the same Wikidata record.
    for source, rels in ontology.items():
        same = rels.get(SAID_SAME, set())
        if same & expanded_concepts or source in expanded_concepts:
            expanded_concepts.add(source)
            expanded_concepts.update(same)

    resources = find_relating_resources(ROOT_DIR, expanded_concepts, allowed_terms)

    if not resources:
        print('No resources found referencing the selected concepts. The graph will still include the selected nodes.')

    dot_lines = build_graph(selected_concepts, ontology, resources, wikidata)
    args.dot.parent.mkdir(parents=True, exist_ok=True)
    args.dot.write_text('\n'.join(dot_lines) + '\n', encoding='utf-8')
    print(f'WROTE {args.dot}')
    print(f'INPUT CONCEPTS: {sorted(INPUT_CONCEPTS)}')
    print(f'SELECTED CONCEPTS: {sorted(selected_concepts)}')
    print(f'EXPANDED CONCEPTS: {sorted(expanded_concepts)}')
    print(f'RESOURCE NODES: {len(resources)}')


if __name__ == '__main__':
    main()
