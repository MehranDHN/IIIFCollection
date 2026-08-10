from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generate_narrative_episode_hierarchy import parse_labels_and_parents, build_dot


def test_parse_labels_and_parents_reads_wiki_and_parent_links():
    ontology_path = Path(__file__).resolve().parents[2] / 'Ontology' / 'narrative_episodes.ttl'
    entries, edges = parse_labels_and_parents(ontology_path)

    assert 'mdhn:Shahnameh' in entries
    assert entries['mdhn:Shahnameh']['wiki'] == 'Q8279'
    assert ('mdhn:Kingdom_of_Keyumars', 'mdhn:Shahnameh') in edges

    rendered = build_dot(entries, edges)
    assert 'Q8279' in rendered
    assert 'mdhn:Shahnameh' not in rendered or 'Shahnameh' in rendered
