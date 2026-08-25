# Data Visualisation Script Guide

This guide documents the current Python scripts in `IIIFCollection/util_script/visualization/`. They read the IIIF Collection JSON files and RDF/OWL Turtle data described by the root project README, then write diagram or report artefacts. Paths are interpreted relative to the script unless a script defines an absolute path or command-line option.

## Quick Start

Run a script from its current directory:

```bash
python IIIFCollection/tools/visualization/generate_collection_tree.py
python IIIFCollection/tools/visualization/generate_collection_statistics.py
python IIIFCollection/tools/visualization/generate_aat_hierarchy.py
```

Graphviz-dependent scripts additionally require the Graphviz `dot` executable. RDF-oriented scripts require the Python RDF tooling declared or imported by the script. Generated artefacts should eventually be written to `IIIFCollection/tools/visualization/reports/`.

## Script Contracts

### Collection reports

| Current script | Purpose | Inputs | Outputs |
|---|---|---|---|
| `generate_collection_tree.py` | Walk the root IIIF collection and nested collection references to show collection hierarchy and member counts. | `IIIF2Collection.json` and referenced collection JSON files. | `collection_tree.mmd`. |
| `generate_collection_statistics.py` | Summarise collection, manifest, item, member, and subcollection counts. | Files matching `*Collection.json` in the IIIFCollection directory. | `collection_statistics.html` and `collection_statistics.json`. |
| `generate_iconography_concept_markmap.py` | A Hierarchical graph presenting associations between Resources. Canvases, Content Elements and Iconography Concept | Specified Iconography Concept | Hierarchical Markmap Document `iconography_concept_associations.markmap.md` |

### Canvas and content-element reports

| Current script | Purpose | Inputs | Outputs |
|---|---|---|---|
| `generate_canvas_decomposition_markmap.py` | Produce a Markmap-compatible decomposition of ResourceCanvases and their ContentElements. | Collection or manifest JSON containing canvas metadata and element fields such as `croppedFigures`, `croppedPatterns`, and `linguisticElements`. | `canvas_decomposition.markmap.md`, including canvas headings, element headings, text, styles, and image links. |
| `generate_canvas_markmap_enhanced.py` | Enhanced canvas decomposition with canvas-level depicts hierarchy, Wikidata Q-codes, SKOS relations, `mdhn:isPartOf`, iconography details, and canvas thumbnails. | Selected collection JSON files plus ontology Turtle files listed in the script configuration. | `iiif_decomposition_markmap_enhanced.md`. |

Canvas reports are the main visualisation of the project’s ResourceCanvas and ContentElement model. They should preserve the distinction between a whole canvas, a cropped figure, a text element, and nested sub-elements.

### AAT and Iconclass vocabulary reports

| Current script | Purpose | Inputs | Outputs |
|---|---|---|---|
| `aat_subset_extract.py` | Extract or prepare the project’s selected AAT subset. | AAT source or project AAT Turtle data, according to the script configuration. | AAT subset data used by hierarchy reports. |
| `generate_aat_hierarchy.py` | Build a Graphviz hierarchy for the selected AAT terms, including project extension and guide-term semantics. | `Ontology/aat_hierarchy.ttl`. | `aat_hierarchy.dot`. |
| `generate_aat_hierarchy_mermaid.py` | Build a Mermaid representation of the AAT hierarchy. | AAT hierarchy Turtle data. | Mermaid hierarchy source, currently an AAT tree artefact. |
| `render_aat_hierarchy_graph.py` | Render the AAT DOT graph into a viewable image format. | AAT DOT graph and Graphviz. | SVG or PNG, selected with `--format`. |
| `generate_iconclass_hierarchy_dot.py` | Represent the selected Iconclass hierarchy and its relationships. | Iconclass RDF/Turtle data and project configuration. | Iconclass Graphviz DOT output. |

The AAT reports support the root README’s stated goal of maintaining a relevant, extendable subset rather than attempting to visualise the complete vocabulary. Iconclass reports support the documented integration of Biblical and Quranic narrative subjects and local extensions.

### Persons and FHKB reports

| Current script | Purpose | Inputs | Outputs |
|---|---|---|---|
| `generate_persons_graph_dot.py` | Build a graph of persons and FHKB relationships. | `Ontology/PersonsRDFData.ttl`. | `persons_graph.dot`. |
| `generate_persons_graph_dot_extended.py` | Produce the extended persons graph with additional relationship or label detail. | Persons RDF/Turtle data. | `persons_graph_extended.dot`. |
| `render_persons_graph.py` | Render persons DOT output for inspection or publication. | Persons DOT graph and Graphviz. | SVG or PNG, selected with `--format`. |

The reports should retain labels and Wikidata identifiers where available, because the root README treats persons as agential information and Wikidata as an authority bridge.

### Iconography and narrative reports

| Current script | Purpose | Inputs | Outputs |
|---|---|---|---|
| `generate_iconography_concept_graph.py` | Build a neighbourhood graph around selected iconographic concepts, their SKOS links, and resources that reference them. | Collection JSON files and iconography RDF/Turtle data; concepts supplied through the `INPUT_CONCEPTS` array. | Iconography concept DOT graph. |
| `generate_iconography_concept_markmap.py` | Concept-rooted Markmap of the same neighbourhood: SKOS alignments (AAT, Iconclass, TGM), narrative episodes, collections, resources, canvases, matching content elements, and IIIF thumbnails. | Same `INPUT_CONCEPTS` array as the DOT graph, all `*Collection.json` files, plus `iconography_RDF.ttl`, `narrative_episodes.ttl`, `iconclass_hierarchy.ttl`, `aat_hierarchy.ttl`, and `LCTGM_RDF.ttl`. | `iconography_concept_associations.markmap.md`. |
| `generate_depicts_graph.py` | Build a graph of `mdhn:depicts` and related resource-to-concept associations. | Collection JSON and ontology data used by the script. | Depicts graph DOT output. |
| `generate_depicts_graph_mermaid.py` | Emit the depicts relationships as Mermaid source. | Collection JSON and ontology data. | Mermaid depicts graph. |
| `generate_narrative_episodes_graph.py` | Build a graph of narrative episode concepts and their links. | `Ontology/narrative_episodes.ttl` and related project data. | Narrative episode concept DOT output. |
| `generate_narrative_episode_hierarchy.py` | Build the broader-to-narrower narrative episode structure. | Narrative episode Turtle data. | `narrative_episode_hierarchy.dot`. |
| `scan_iconography_labels.py` | Inspect collection data for iconography labels and coverage issues. | Collection JSON files. | Diagnostic console output or scan artefact, as configured by the script. |

These reports make the root README’s Iconography, Narrative Episodes, Iconclass, AAT, TGM, and Wikidata relationships inspectable rather than leaving them only in RDF or JSON.

### Reconciliation reports

| Current script | Purpose | Inputs | Outputs |
|---|---|---|---|
| `generate_reconciliation_association_graph.py` | Visualise associations and reconciliation status between controlled vocabulary concepts and related authorities. | Reconciliation inputs and controlled-vocabulary RDF/JSON data configured by the script. | Reconciliation Mermaid or graph artefacts, including association and status reports where configured. |

This area should eventually expose orphan, bridge, and unresolved-authority counts in a stable machine-readable report so vocabulary maintenance can be tracked over time.

## Output Format Rules

- `.dot` is source for Graphviz and should remain deterministic.
- `.mmd` is Mermaid source intended for Markdown, Mermaid-compatible viewers, or later rendering.
- `.markmap.md` is Markdown whose heading hierarchy is the report structure.
- `.html` is a browser-oriented report and may include companion `.json` data.
- `.svg` and `.png` are rendered artefacts and should not be treated as source.
- Output filenames should use the same domain and view terms as the future module names.

## Recommended Future Names

The proposed target names are:

| Current family | Target module |
|---|---|
| collection tree and statistics | `tools/visualization/generators/collection.py`, `statistics.py` |
| canvas Markmap reports | `tools/visualization/generators/canvas.py` |
| AAT and Iconclass hierarchies | `tools/visualization/generators/vocabulary.py` |
| persons and FHKB | `tools/visualization/generators/persons.py` |
| iconography and depicts | `tools/visualization/generators/iconography.py` |
| narrative episodes | `tools/visualization/generators/narrative.py` |
| reconciliation | `tools/visualization/generators/reconciliation.py` |
| DOT, Mermaid, Markmap, HTML conversion | `tools/visualization/renderers/` |

Move implementations only after their current input and output behaviour has a fixture-based test. Keep old filenames as compatibility entry points during the transition.

## Future Extensions

- Add explicit `--input`, `--output`, and `--output-dir` options to every generator.
- Add a shared configuration for ontology paths and report destinations.
- Add SPARQL-backed generators for Knowledge Graph queries.
- Add `navPlace` map reports and GeoJSON outputs.
- Record source files, ontology versions, and checksums beside generated reports.
- Add image availability checks that distinguish a malformed IIIF URL from a remote provider or network failure.
