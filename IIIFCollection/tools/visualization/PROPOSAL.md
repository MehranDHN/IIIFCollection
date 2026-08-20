# Data Visualisation Reorganisation Proposal

## Scope

This proposal reorganises the Python visualisation utilities that currently live in `IIIFCollection/util_script/visualization/`. It is based on the project model described in the repository root README: IIIF Collections and Manifests, ResourceCanvases and ContentElements, RDF/OWL ontology data, controlled vocabularies, Iconclass, narrative episodes, persons, and Knowledge Graph analysis.

The proposal does not change the IIIF data model or ontology. It changes how visualisation code, shared rendering logic, tests, and generated reports are maintained.

## Objectives

- Give every visualisation script a predictable name and responsibility.
- Separate source-data adapters, report generators, renderers, tests, and generated artefacts.
- Keep DOT, Mermaid, Markmap, HTML, JSON, SVG, and PNG outputs reproducible.
- Preserve existing commands during migration through compatibility wrappers.
- Make each report traceable to its input files and ontology relationships.
- Provide a clear path for future SPARQL and Knowledge Graph-backed reports.

## Proposed Structure

```text
IIIFCollection/
├── tools/
│   └── visualization/
│       ├── README.md                 # entry point and quick start
│       ├── PROPOSAL.md               # this migration plan
│       ├── SCRIPT_GUIDE.md           # script contracts
│       ├── pyproject.toml             # dependencies and tool configuration
│       ├── cli.py                     # optional unified command line entry point
│       ├── config/
│       │   └── styles.py              # shared visual conventions
│       ├── generators/
│       │   ├── collection.py
│       │   ├── canvas.py
│       │   ├── vocabulary.py
│       │   ├── iconography.py
│       │   ├── narrative.py
│       │   ├── persons.py
│       │   ├── reconciliation.py
│       │   └── statistics.py
│       ├── renderers/
│       │   ├── dot.py
│       │   ├── mermaid.py
│       │   ├── markmap.py
│       │   └── html.py
│       ├── tests/
│       └── reports/                   # generated files only
└── util_script/
    └── visualization/                 # compatibility layer during migration
```

`tools/visualization/` is the target home. The current `util_script/visualization/` directory remains usable until each script has a replacement and its output has been compared with the existing report.

## Unified Naming Convention

Use the following rules for new modules:

- `generate_<domain>_<view>.py` creates a source report such as DOT, Mermaid, Markmap, JSON, or HTML.
- `render_<format>.py` converts a generated representation into a presentation format such as SVG or PNG.
- `<domain>` names the data subject: `collection`, `canvas`, `aat`, `iconography`, `narrative`, `persons`, `reconciliation`, or `statistics`.
- `<view>` names the report: `hierarchy`, `graph`, `tree`, `decomposition`, `dashboard`, or `status`.
- Shared code belongs in modules named for the abstraction, not in duplicate domain-specific renderers.
- Output names use the same domain and view words as the module: for example `aat_hierarchy.dot`, `collection_tree.mmd`, and `canvas_decomposition.markmap.md`.
- Compatibility files may retain old names, but should contain only argument translation and a call to the new implementation.

## Migration Stages

### Stage 1: Inventory and contracts

Record each current script's purpose, input files, output files, command-line arguments, and external dependencies. The [Script Guide](SCRIPT_GUIDE.md) is the baseline contract.

### Stage 2: Extract shared primitives

Move repeated JSON loading, label normalisation, Turtle parsing, namespace handling, identifier escaping, and output-directory handling into shared modules. Keep the generated content unchanged while extracting these functions.

### Stage 3: Move generators by domain

Move one domain at a time into `tools/visualization/generators/`. Start with collection structure and statistics, then vocabulary hierarchies, then persons, iconography, narrative episodes, reconciliation, and canvas decomposition.

### Stage 4: Consolidate renderers

Use shared renderers for DOT, Mermaid, Markmap, and HTML. A generator should describe data and relationships; a renderer should handle format-specific escaping, layout, and file writing.

### Stage 5: Add the unified CLI

Expose commands such as:

```text
python -m tools.visualization collection tree
python -m tools.visualization vocabulary aat-hierarchy --format dot
python -m tools.visualization canvas decomposition --input PeckShahnamaCollection.json
python -m tools.visualization statistics dashboard
```

The CLI should support `--input`, `--output-dir`, `--format`, and `--check` consistently.

### Stage 6: Verify and retire wrappers

For every migrated report, compare the old and new outputs structurally and visually. Retain wrappers until the new command is documented and tested. Do not delete the old scripts as part of a bulk rename.

## Verification Requirements

Every generator should have:

- a small fixture input;
- a deterministic output check;
- tests for empty, missing, and malformed input where relevant;
- format escaping tests;
- an output manifest recording source files and generation time where useful;
- a smoke test that confirms expected nodes, edges, headings, or table fields.

Reports that depend on remote IIIF images should validate URL syntax separately from image availability. Remote providers may reject requests or rate-limit clients even when the generated IIIF URL is correct.

## Future Extensions

- Add a SPARQL adapter so reports can run against the Knowledge Graph instead of only local JSON and Turtle files.
- Add a report manifest describing inputs, ontology version, script version, and output checksums.
- Add cross-report identifiers so a node in a vocabulary graph links to the corresponding collection or canvas report.
- Add GeoJSON and map-oriented reports for `navPlace` data.
- Add accessibility checks for Mermaid, SVG, HTML, and Markmap outputs.
- Add incremental generation so unchanged source files do not rebuild every report.
