import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[1]
ONTOLOGY_PATH = ROOT_DIR / 'Ontology' / 'narrative_episodes.ttl'
OUTPUT_DOT = SCRIPT_DIR / 'narrative_episode_hierarchy.dot'


def safe_id(value: str) -> str:
    safe = re.sub(r'[^A-Za-z0-9_]', '_', value)
    if not safe or safe[0].isdigit():
        safe = '_' + safe
    return safe


def quote(value: str) -> str:
    return value.replace('"', '\\"').replace('\n', ' ')


def parse_labels_and_parents(path: Path) -> Tuple[Dict[str, Dict[str, object]], List[Tuple[str, str]]]:
    entries: Dict[str, Dict[str, object]] = {}
    edges: List[Tuple[str, str]] = []
    current_subject: Optional[str] = None

    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue

        subject_match = re.match(r'^(mdhn:[A-Za-z0-9_]+)\s+a\s+(mdhn:[A-Za-z0-9_]+)', line)
        if subject_match:
            current_subject = subject_match.group(1)
            declared_type = subject_match.group(2)
            if current_subject not in entries:
                entries[current_subject] = {
                    'label': None,
                    'wiki': None,
                    'parents': [],
                }
            if declared_type != 'mdhn:NarrativeEpisode':
                entries[current_subject]['declared_type'] = declared_type
            continue

        if current_subject is None:
            continue

        if line.startswith('rdfs:label'):
            m = re.search(r'rdfs:label\s+"([^"]+)"@en', line)
            if m:
                entries[current_subject]['label'] = m.group(1)
            continue

        if line.startswith('mdhn:icWikiDataURL'):
            m = re.search(r'mdhn:icWikiDataURL\s+"([^"]*)"', line)
            if m:
                wiki = m.group(1).strip()
                if wiki and wiki.startswith('https://www.wikidata.org/wiki/'):
                    qid = wiki.rsplit('/', 1)[-1]
                    if qid and qid != 'wiki':
                        entries[current_subject]['wiki'] = qid
            continue

        if line.startswith('mdhn:isPartOf'):
            parent_match = re.search(r'mdhn:isPartOf\s+(mdhn:[A-Za-z0-9_]+)', line)
            if parent_match:
                parent = parent_match.group(1)
                entries[current_subject]['parents'].append(parent)
                if current_subject not in entries:
                    entries[current_subject] = {'label': current_subject, 'wiki': None, 'parents': []}
                if parent not in entries:
                    entries[parent] = {'label': parent, 'wiki': None, 'parents': []}
                edges.append((current_subject, parent))
            continue

        if line.endswith('.'):
            current_subject = None

    return entries, edges


def build_dot(entries: Dict[str, Dict[str, object]], edges: List[Tuple[str, str]]) -> str:
    lines = [
        'digraph NarrativeEpisodeHierarchy {',
        '  rankdir=TB;',
        '  graph [bgcolor="#ffffff"];',
        '  node [shape=box, style="filled,rounded", fontname="Arial", fontsize=9, penwidth=0.8];',
        '  edge [color="#555555", arrowsize=0.8];',
        '  overlap=scale;',
        '  splines=true;',
        '  ranksep=1.0;',
        '  nodesep=0.4;',
    ]

    for subject in sorted(entries):
        data = entries[subject]
        label = data.get('label') or subject
        wiki = data.get('wiki')
        display = label if not wiki else f'{label} [{wiki}]'
        display = quote(display)
        lines.append(f'  "{safe_id(subject)}" [label="{display}", fillcolor="#f2f2f2", fontcolor="#111111"];')

    for child, parent in edges:
        lines.append(f'  "{safe_id(parent)}" -> "{safe_id(child)}";')

    lines.append('}')
    return '\n'.join(lines) + '\n'


def main() -> None:
    entries, edges = parse_labels_and_parents(ONTOLOGY_PATH)
    dot_text = build_dot(entries, edges)
    OUTPUT_DOT.write_text(dot_text, encoding='utf-8')
    print(f'WROTE {OUTPUT_DOT}')
    print(f'NODES {len(entries)} EDGES {len(edges)}')


if __name__ == '__main__':
    main()
