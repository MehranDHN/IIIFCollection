# IIIFDexir Data Visualisation Tools

**Authoritative guide to the Python scripts that generate Graphviz DOT, Mermaid, Markmap and HTML statistical reports from the IIIFDexir knowledge graph and collection data.**

This folder (and the surrounding `tools/visualization/` package) turns the RDF/OWL ontology, controlled-vocabulary subsets and IIIF collection JSON files into clear, reusable diagrams and reports. The scripts are deliberately diagram-as-code: every visual artefact is regenerated from source data so that documentation stays synchronised with the underlying model.

For the migration plan and the current script contracts, see [PROPOSAL.md](PROPOSAL.md) and [SCRIPT_GUIDE.md](SCRIPT_GUIDE.md). This README remains the package-level overview; the script guide is the operational reference for inputs and outputs.

> **Status (August 2026)**  
> The original scripts lived in a flat `util_script/visualization/` directory with mixed naming. They are being refactored into a coherent package with consistent naming, shared configuration and a single CLI entry point. This README documents both the **current** scripts and the **target** organisation.

---

## Design Goals

1. **Traceability** — Every diagram is generated from Turtle or JSON source; no hand-drawn artefacts.
2. **Consistency** — Shared colour semantics, tooltip rules and layout conventions across all reports.
3. **Extensibility** — Adding a new report type should require only a new generator module + a few lines in the CLI.
4. **Scholarly usefulness** — Tooltips expose `rdfs:comment`, Wikidata QIDs, Iconclass notations and other rich metadata.
5. **Multiple output formats** — DOT (Graphviz), Mermaid, Markmap, SVG, PNG, HTML, JSON.

---

## Target Package Layout

```text
tools/visualization/
├── README.md                    ← this file
├── __init__.py
├── cli.py                       # future unified entry point
├── config/
│   └── styles.yaml              # colours, ranks, node shapes, tooltip templates
├── generators/
│   ├── __init__.py
│   ├── base.py                  # common RDF loading, namespace handling, colour helpers
│   ├── generate_aat_hierarchy.py
│   ├── persons.py
│   ├── iconography.py
│   ├── narrative.py
│   ├── generate_collection_tree.py
│   ├── generate_canvas_decomposition_markmap.py
│   └── generate_collection_statistics.py
├── renderers/
│   ├── render_graphviz.py       # .dot → SVG / PNG
│   ├── mermaid.py
│   └── markmap.py
└── reports/                     # default output directory (generated artefacts)
```

---

## Naming Convention (Target)

| Old name (current)                        | New name (target)                     | Notes |
|-------------------------------------------|---------------------------------------|-------|
| `generate_aat_hierarchy_dot.py`           | `tools/visualization/generate_aat_hierarchy.py` | compatibility wrapper retained |
| `generate_aat_hierarchy_mermaid.py`       | (merged into above)                   | |
| `render_aat_hierarchy_graph.py`           | `tools/visualization/render_graphviz.py` | compatibility wrapper retained |
| `generate_persons_graph_dot.py`           | `generators/persons.py`               | |
| `generate_persons_graph_dot_extended.py`  | (flag `--extended`)                   | |
| `render_persons_graph.py`                 | (shared renderer)                     | |
| `generate_iconography_concept_graph.py`   | `generators/iconography.py`           | |
| `generate_iconography_concept_markmap.py` | `generators/iconography.py` (Markmap view) | |
| `generate_narrative_episode_hierarchy.py` | `generators/narrative.py`             | |
| `generate_narrative_episodes_graph.py`    | (same module, different mode)         | |
| `generate_collection_tree_mermaid.py`     | `tools/visualization/generate_collection_tree.py` | compatibility wrapper retained |
| `generate_canvas_markmap.py`              | `tools/visualization/generate_canvas_decomposition_markmap.py` | compatibility wrapper retained |
| `generate_collection_statistics_html.py`  | `tools/visualization/generate_collection_statistics.py` | compatibility wrapper retained |
| `generate_depicts_graph.py` / `_mermaid`  | `generators/iconography.py` (mode)    | |
| `aat_subset_extract.py`                   | utility inside `aat_hierarchy`        | |
| `scan_iconography_labels.py`              | utility inside `iconography`          | |

All generators accept a common set of flags (`--output-dir`, `--format`, `--config`, etc.).

---

## Script Catalogue (Purpose / Input / Output)

### 1. AAT Hierarchy

**Purpose**  
Visualise the project’s subset of the Art & Architecture Thesaurus, highlighting guide terms and locally extended concepts.

| | |
|---|---|
| **Current scripts** | `tools/visualization/generate_aat_hierarchy.py`, `tools/visualization/render_graphviz.py` |
| **Compatibility commands** | `util_script/visualization/generate_aat_hierarchy_dot.py`, `util_script/visualization/render_aat_hierarchy_graph.py` |
| **Primary input** | `data/ontology/aat_hierarchy.ttl` (or `Ontology/aat_hierarchy.ttl`) |
| **Key properties used** | `mdhn:hasAATBroader`, `mdhn:isGuideTerm`, `mdhn:isInExtendedScope`, `rdfs:label`, `rdfs:comment` |
| **Outputs** | `aat_hierarchy.dot`, `aat_hierarchy_tree.mmd`, SVG, PNG |
| **Colour semantics** | Guide term → yellow `#fff2ac`<br>Extended scope → light blue `#cfe2f3`<br>Both → pink `#f4cccc` |
| **Usage** | ```bash<br>python tools/visualization/generate_aat_hierarchy.py<br>python tools/visualization/render_graphviz.py --format svg<br>``` |

---

### 2. Persons / FHKB Graph

**Purpose**  
Render kinship and social networks from the Family History Knowledge Base modelling of historical agents.

| | |
|---|---|
| **Current scripts** | `generate_persons_graph_dot.py`, `generate_persons_graph_dot_extended.py`, `render_persons_graph.py` |
| **Target module** | `generators/persons.py` |
| **Primary input** | `data/ontology/PersonsRDFData.ttl` |
| **Key properties used** | `fhkb:hasSon`, `fhkb:hasDaughter`, `fhkb:isFatherOf`, `fhkb:isMotherOf`, `fhkb:isSpouseOf`, `fhkb:isSiblingOf`, … + Wikidata QIDs |
| **Outputs** | `persons_graph.dot`, `persons_graph_extended.dot`, SVG, PNG |
| **Node labels** | English `rdfs:label` + Wikidata Q-code when available |
| **Usage (current)** | ```bash<br>python generate_persons_graph_dot.py<br>python render_persons_graph.py --format svg<br>``` |

---

### 3. Iconography Concept Graph

**Purpose**  
Build a neighbourhood graph around one or more iconographic concepts, showing exact/related matches, resources that depict them, and further concepts discovered in those resources (including narrative episodes).

| | |
|---|---|
| **Current script** | `generate_iconography_concept_graph.py` |
| **Target module** | `generators/iconography.py` |
| **Primary inputs** | All `*Collection.json` files + `data/ontology/iconography_RDF.ttl` |
| **Key properties used** | `skos:exactMatch`, `skos:relatedMatch`, `mdhn:depicts`, `mdhn:elementDepicts`, narrative-episode links |
| **Outputs** | `iconography_concept_graph.dot` (and test variants) |
| **Usage (current)** | Edit the `INPUT_CONCEPTS` array, then:<br>```bash<br>python generate_iconography_concept_graph.py<br>``` |

**Markmap view of the same neighbourhood**

| | |
|---|---|
| **Current script** | `generate_iconography_concept_markmap.py` |
| **Root** | The concept(s) listed in `INPUT_CONCEPTS` (same array as the DOT script). A single concept such as `mdhn:Divs` becomes the Markmap root; several concepts become sibling branches. |
| **Primary inputs** | All `*Collection.json` files + `Ontology/iconography_RDF.ttl`, `narrative_episodes.ttl`, `iconclass_hierarchy.ttl`, `aat_hierarchy.ttl`, `LCTGM_RDF.ttl` |
| **Key properties used** | `skos:exactMatch`, `skos:closeMatch`, `skos:relatedMatch`, `skos:broadMatch`, `mdhn:isPartOf`, `mdhn:charactersInvolved`, `mdhn:hasAATBroader`, `mdhn:hasIconclassBroader`, `mdhn:hasTGMBroader`, canvas `depicts` / `elementLOUD` |
| **Thumbnails** | IIIF Image API size segment rewritten to `/{THUMBNAIL_WIDTH},/` (default `250`) for collection, resource, canvas, and cropped-element images |
| **Outputs** | `iconography_concept_associations.markmap.md` |
| **Usage (current)** | Edit the `INPUT_CONCEPTS` array, then:<br>```bash<br>python generate_iconography_concept_markmap.py<br>``` |

---

### 4. Narrative Episode Hierarchy & Concept Graph

**Purpose**  
Visualise the hierarchical structure of narrative episodes and the conceptual relationships among them.

| | |
|---|---|
| **Current scripts** | `generate_narrative_episode_hierarchy.py`, `generate_narrative_episodes_graph.py` |
| **Target module** | `generators/narrative.py` |
| **Primary input** | `data/ontology/narrative_episodes.ttl` |
| **Outputs** | `narrative_episode_hierarchy.dot`, `narrative_episodes_concept_graph.dot` |
| **Usage** | See script docstrings / future CLI help |

---

### 5. Collection Structure Tree

**Purpose**  
Produce a Mermaid tree that reflects the nested Resource / Departed collection hierarchy.

| | |
|---|---|
| **Current script** | `tools/visualization/generate_collection_tree.py` |
| **Compatibility command** | `util_script/visualization/generate_collection_tree_mermaid.py` |
| **Primary input** | Root and sub-collection JSON files |
| **Output** | `tools/visualization/collection_tree.mmd` |
| **Usage** | ```bash<br>python tools/visualization/generate_collection_tree.py<br>``` |

---

### 6. Canvas / Content-Element Decomposition (Markmap)

**Purpose**  
Generate mind-maps that show how individual IIIF Canvases are decomposed into content elements (cropped figures, inscriptions, etc.). Especially useful for Shahnameh and other richly annotated manuscripts.

| | |
|---|---|
| **Current script** | `tools/visualization/generate_canvas_decomposition_markmap.py` |
| **Compatibility command** | `util_script/visualization/generate_canvas_markmap.py` |
| **Primary input** | Manifest / annotation data (and optionally collection JSON) |
| **Outputs** | `tools/visualization/canvas_decomposition.markmap.md` |
| **Usage** | See script for collection-specific flags |

---

### 7. Collection Statistics Dashboard

**Purpose**  
Produce an HTML (and companion JSON) report that summarises counts, coverage and growth metrics across all collections.

| | |
|---|---|
| **Current script** | `tools/visualization/generate_collection_statistics.py` |
| **Compatibility command** | `util_script/visualization/generate_collection_statistics_html.py` |
| **Primary input** | All `*Collection.json` files |
| **Outputs** | `tools/visualization/collection_statistics.html`, `tools/visualization/collection_statistics.json` |
| **Usage** | ```bash<br>python tools/visualization/generate_collection_statistics.py<br>``` |

---

### 8. Depicts Graph (related)

**Purpose**  
Focused graphs of `mdhn:depicts` / `mdhn:elementDepicts` relationships. Currently implemented as companion scripts; will be merged into the iconography generator.

| | |
|---|---|
| **Current scripts** | `generate_depicts_graph.py`, `generate_depicts_graph_mermaid.py` |
| **Target** | mode inside `generators/iconography.py` |

---

## Shared Rendering Conventions

- **Tooltips** — Whenever `rdfs:comment` (or equivalent descriptive text) is present it is injected as a Graphviz tooltip so that SVG viewers reveal rich context on hover.
- **Colour palette** — Defined once in `config/styles.yaml` and reused by every generator.
- **Multiple parents** — Hierarchy generators preserve the full multi-parent structure rather than forcing a tree.
- **Wikidata / external identifiers** — Shown in node labels when available.

---

## Migration Notes for Existing Users

1. Keep the current scripts working until the new package is complete.
2. New development should target the `generators/` + `renderers/` layout.
3. The old `util_script/visualization/` directory will be retained for a transition period and then removed (or turned into a thin compatibility layer).
4. Generated artefacts (`.dot`, `.mmd`, `.svg`, `.html`, …) should be written under `tools/visualization/reports/` (or a configurable output directory) rather than mixed with source scripts.

---

## Dependencies

- Python 3.9+
- `rdflib` (RDF loading and SPARQL)
- Graphviz (`dot` binary) for SVG/PNG rendering
- Optional: `mermaid-cli` or a Mermaid-capable Markdown renderer for `.mmd` files
- Optional: Markmap tooling for interactive mind-maps

---

## Extending the Suite

To add a new report type:

1. Create `generators/my_new_report.py` that inherits from (or follows the pattern of) `generators/base.py`.
2. Register it in `cli.py`.
3. Add a short section to this README (Purpose / Input / Output).
4. Optionally add a dedicated page under `docs/visualization/reports/`.

The shared style configuration and renderer modules already handle colour, tooltip and multi-format output concerns.

---

## Related Documentation

- Root project README → [Data Visualisation Reports](../../README.md#data-visualisation-reports)
- Future detailed report pages → `docs/visualization/reports/`
- Ontology source files → `data/ontology/` (or current `IIIFCollection/Ontology/`)

---

*This guide is the single source of truth for the purpose, inputs and outputs of every data-visualisation script in IIIFDexir.*
