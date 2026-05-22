# AAT Hierarchy Visualization

This folder contains scripts and outputs for generating visualizations from the `Ontology/aat_hierarchy.ttl` dataset.

## DOT graph generation

- `generate_aat_hierarchy_dot.py` reads `Ontology/aat_hierarchy.ttl`.
- It generates `aat_hierarchy_graph.dot` in this folder.
- The script highlights nodes using these colors:
  - `mdhn:isGuideTerm true`: yellow (`#fff2ac`)
  - `mdhn:isInExtendedScope true`: light blue (`#cfe2f3`)
  - both true: pink (`#f4cccc`)

## Usage

From `util_script/visualization`:

```bash
python generate_aat_hierarchy_dot.py
```

To render an interactive SVG with tooltips for node comments:

```bash
python render_aat_hierarchy_graph.py --format svg
```

To render a PNG:

```bash
python render_aat_hierarchy_graph.py --format png
```

If you already have Graphviz installed, the renderer will use `dot` automatically.

## Persons RDF Visualization

- `generate_persons_graph_dot.py` reads `Ontology/PersonsRDFData.ttl`.
- It generates `persons_graph.dot` in this folder.
- Node labels include the English `rdfs:label` and Wikidata Q-code when available.
- Edges are created for `fhkb:` relationships such as `hasSon`, `hasDaughter`, `isFatherOf`, `isMotherOf`, `isSpouseOf`, `isSiblingOf`, and other FHKB predicates.

## Usage for Persons RDF

From `util_script/visualization`:

```bash
python generate_persons_graph_dot.py
```

Then render SVG:

```bash
python render_persons_graph.py --format svg
```

Or render PNG:

```bash
python render_persons_graph.py --format png
```

## Notes

- Hierarchy edges are derived from `mdhn:hasAATBroader`.
- Each node can have multiple parents and the script keeps the full hierarchy.
- Node tooltips now include `rdfs:comment` when available, making details accessible in SVG viewers.
