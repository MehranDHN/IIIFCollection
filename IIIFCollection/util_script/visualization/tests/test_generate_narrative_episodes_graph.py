import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generate_narrative_episodes_graph as graph


def test_find_relating_resources_decomposes_page_entries(tmp_path: Path) -> None:
    collection_path = tmp_path / 'TestCollection.json'
    collection = {
        'label': 'Test Collection',
        'manifests': [
            {
                'id': 'manifest/1',
                'label': 'Manifest 1',
                'metadata': [
                    {
                        'label': {'en': 'States'},
                        'value': {
                            'en': [
                                {
                                    'label': 'Page One',
                                    'folio': '1r',
                                    'canvas': 'canvas/1',
                                    'depicts': ['mdhn:Story_of_Moses'],
                                },
                                {
                                    'label': 'Page Two',
                                    'folio': '2r',
                                    'canvas': 'canvas/2',
                                    'depicts': ['mdhn:Qarun_swallowed_by_the_earth'],
                                },
                            ]
                        },
                    }
                ],
            }
        ],
    }
    collection_path.write_text(json.dumps(collection), encoding='utf-8')

    concepts = {'mdhn:Story_of_Moses', 'mdhn:Qarun_swallowed_by_the_earth'}
    ontology_concepts = concepts | {'mdhn:Other'}

    resources = graph.find_relating_resources(tmp_path, concepts, ontology_concepts)

    assert len(resources) == 2
    labels = {resource['label'] for resource in resources}
    assert labels == {'Page One', 'Page Two'}
    page_one = next(resource for resource in resources if resource['label'] == 'Page One')
    page_two = next(resource for resource in resources if resource['label'] == 'Page Two')
    assert page_one['canvas_concepts'] == ['mdhn:Story_of_Moses']
    assert page_two['canvas_concepts'] == ['mdhn:Qarun_swallowed_by_the_earth']
