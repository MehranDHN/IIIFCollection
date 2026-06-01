# IIIFDexir Project  

The IIIFDexir project is a dynamic catalog based on IIIF. It emphasizes several technical features: 

## Background and Motivation

This project was initiated to explore the requirements for building a modern national archive aligned with the needs of the digital transformation era and the rise of artificial intelligence. It began by studying the most successful international experiences, particularly those of prominent aggregators that combine **RDF**, **IIIF**, and **CIDOC CRM** within RDF/OWL ontologies. These systems have demonstrated how to create dynamic ecosystems capable of identifying resources, adopting appropriate publication and harvesting standards, designing iterative data pipelines, reconciling information through controlled vocabularies and knowledge bases, implementing robust monitoring tools based on real indicators, and publishing multi-layered catalogs.

![Reconstructing Dispersed Digital Heritage](/IIIFCollection/images/introduction.jpg)

Recognizing that such an ambitious undertaking would ideally require crowdsourcing and a broad community of contributors, I encountered significant practical challenges in coordinating volunteer efforts. Therefore, I decided to develop the project on a limited and controlled scale as a **Proof of Concept**. This approach enabled the core structures to take shape while revealing the main technical challenges early on.

One of the most important and decisive design choices was the adoption of **IIIF Collections** as the primary mechanism for organizing resources into dynamic, machine consumable, hierarchical lists. This structure naturally supports tree-like modeling of classified resources. The underlying information model was designed in full compliance with an RDF/OWL ontology. Initially, the ontology was intentionally minimal—containing only the core concepts of `Digital Collection` and `Digital Resource` along with their relationship to allow the project to start at a manageable/limited scale. Thanks to the remarkable flexibility of the ontology, it has since been iteratively expanded according to evolving needs.

In its original form, a single IIIF Collection functioned as the root of a nested hierarchy, with nested Collections and IIIF Manifests placed inside them. This design provided a highly flexible information model that serves both as a machine consumable resource list and as a pointer to digital assets hosted across GLAM institutions without the need to manulay download them. Because IIIF inherently supports a wide variety of digital object types including books, manuscripts, artworks, calligraphy, photographs, historical documents, maps, and even audio/video materials the system is versatile and well-suited for long-term growth.

## Key Features  

- Machine Readability: The catalog is designed to be machine-readable and consumable.
- Linked Data. IIIFDexir is fully compatible with Linked Data Paradigm and LOUD/FAIR concepts. 
- IIIF Compatibility: IIIFDexir is fully compatible with IIIF standards.  
- Hierarchical Arrangement: Resources in the catalog are all IIIF Manifests accessible online and are arranged hierarchically as nested Multipart IIIF Collection.  
- Flexible Data Structures: The data structures of the resources in the collection are JSON-LD compatible and highly flexible that can be enriched with external data sources, including XML, JSON, and RDF files.  
- Controlled Vocabularies: IIIFDexir is associated with standard controlled vocabularies and knowledge baeses like AAT, TGN, LCSH, TGM and Wikidata. In some circumestances I extend The AAT and TGM with new terms and concepts to demonstrate how easy is extending the contolled vocabularies.
- FHKB (Family History Knowledge Base). A Full version of FHKB is embeded into the project for the Agential data.  
- On The Fly Manifests. There are many use cases that we want to use a customize curated manifests from selected cavases that physically belong to other manifests. There is a python code to achive this goal which provided with some samples. These manifests are hosted locally.
- Human Usability: While the primary focus is on machine consumption, the catalog is also usable by humans via standard IIIF viewers like Mirador and OpenSeaDragon.  
- Public Accessibility: The catalog remains publicly accessible. 

![IIIFDexir](/IIIFCollection/images/IIIFDexir.JPG)

## Accessing the Collection

### Root Collection

Although the primary goal of this system is to deliver high-quality structured data for machines and enabling advanced querying, reasoning, and integration within a Knowledge Graph, it also provides rich, user-friendly access and experiences for humans. Through standard IIIF viewers such as `Mirador`, `Theseus`, or any other compatible `IIIF Viewer`, users can easily browse and explore the collections.

Some of the most important of this human interaction includes:

- Navigating hierarchical structure of the `Collections` and their nested `sub-collections`
- Exploring `IIIF Manifests` and their associated media(images/audio/video/3d Models)
- Viewing and examining high-resolution images of manuscripts, photograph albums, maps. periodical contents, artworks, and other digital assets.
- Downloading metadata and original digital assets.
- Following and even rendering of enriched data that are available via the `seeAlso`, `navPlace`, and `Annotation` fields to discover related resources across the web.

Each of these features plays a significant role in making the collection both machine-readable and human-accessible. Several practical examples are provided later in this document.
It is important to note that while the detailed metadata embedded in the `IIIF Collections` is primarily designed as a template for building the RDF/OWL Knowledge Graph (and is not directly displayed by most viewers), the viewers themselves serve as powerful interfaces for human exploration of the underlying resources. A more detailed explanation of how the Knowledge Graph is constructed from this data is provided in the sections below.

- **Mirador (Biblissima)**: [Open in Mirador](https://iiif.biblissima.fr/mirador3/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/IIIF2Collection.json)
- **Theseus Viewer**: [Open in Theseus](https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/IIIF2Collection.json)

#### Example Sub-Collections
- [Edward Browne Collection](https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/EdwardBrowneCollection.json)

#### Current Structure of the Collections and nested sub-Collections
- [Collection Structure](https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/EdwardBrowneCollection.json)


## Content Organization

### Departed vs Resource Collections

**Here's a significantly improved, clearer, and more professional version** of your text:

---

### Departed vs. Resource Collections

IIIFDexir empower a modern, multiple-layered approach to classification that differs substantially from traditional legacy systems. While legacy catalogs often rely on rigid physical categorization, IIIFDexir emphasizes semantic unity across all resources.

#### Common Foundation of Digital Resources
At the highest level, all digital objects in IIIFDexir share a common root structure defined by two core ontology classes: **`ResourceCollection`** and **`DigitalResource`**. Every digital resource includes:

- **Standard IIIF 2.0 or 3.0 Manifest** A unique identifier and standard IIIF Manifest.
- **Agential information** (creators, artists, photographers, patrons, previous owners, etc., modeled through the `Person` class which may also represent institutions or agencies)
- **Temporal information** (dates, periods, eras)
- **Spatial information** (geographic locations, places)

This shared foundation ensures consistency while allowing rich, multi-dimensional classification.

#### Resource Collections: Human-Friendly Organization
**Resource Collections** are designed primarily for human navigation and intuitive browsing. They function similarly to hierarchical folders on a computer, allowing users to explore resources through familiar thematic or typological groupings.

For example:
- A top-level **Qurans** collection may contain sub-collections such as **Kufic Qurans**
- Multilevel Nested Collections, A typical example: **Manuscripts** → **Persian Manuscripts** → **Khamseh** 

These collections reflect how humans naturally think about cultural heritage and provide an excellent entry point for exploration via IIIF viewers such as **Mirador** or **Theseus**.

**Important Note**: Not every Quran, manuscript, or painting in the system is placed within these thematic collections. Resource Collections serve as helpful curated pathways rather than exhaustive containers.

#### Machine-First Access: Taxonomy, Queries, and Accessibility
While Resource Collections support human browsing, the system’s primary strength lies in **machine-readable structured data**. Detailed classification is achieved through taxonomy tags, controlled vocabularies (especially AAT), and semantic relationships. This enables precise, powerful querying far beyond what hierarchical folders can achieve.

Users are encouraged to explore resources through query languages such as **SPARQL** (recommended), Cypher, or GraphQL. These queries can combine multiple criteria to answer complex “WH” questions (Who, What, When, Where, Which).

**Example**: A query using the AAT identifier for Kufic script (`300194434`) can retrieve all resources related to Qurans or Hadith written in Kufic including items not listed in specified “Kufic Qurans” Resource Collection.

More advanced queries can combine numerous conditions. For instance:
> Find all paintings, calligraphic works, and detached folios (excluding complete manuscripts) by Jami, featuring Nastaliq or Thuluth script, motifs such as cypress trees, horses, or camp scenes, related to *Leili and Majnun* or *Joseph and Zuleikha*, and dated between the 9th and 11th centuries AH.

Such complex queries demonstrate the system’s analytical power and deliver highly accurate results.

#### Departed Collections: Reuniting Scattered Heritage
In addition to Resource Collections, IIIFDexir introduces the concept of **Departed Collections**. These are logical groupings created to reunite fragments of historically significant but physically dispersed works.

Unlike Resource Collections, Departed Collections do not follow IIIF nesting rules strictly. They serve as virtual reunifications of items scattered across dozens of institutions worldwide.

**Examples**:
- **Shahnameh of Shah Tahmasp** (pages and illustrations now dispersed across more than 30 museums, libraries, and galleries)
- **Haft Orang** (Ibrahim Sultan edition) – pages separated (Probably by mistake) even within the Smithsonian Archive.
- **Ernst Herzfeld** Documents and photographs related to Ernst Herzfeld, 
- **Dr. Qasem Ghani** Documents related to Dr. Qasem Ghani,
- **Great Mongol Shahnameh**  The Great Mongol Shahnameh also known as the Demotte Shahnameh or Great Ilkhanid Shahnama

#### On-the-Fly Manifests: Virtual Binding
To make these reunifications practically usable, IIIFDexir uses a custom **Python tool** to generate **on-the-fly IIIF Manifests**. This powerful feature dynamically creates a new, independent manifest containing selected canvases from multiple sources effectively creating a “virtual binding” that never existed physically.

This allows researchers to view scattered masterpieces as a cohesive digital object in any standard IIIF viewer.

#### Additional Classification Layers
- **Content Type** (based on AAT): Provides another logical dimension (e.g., endowment deeds, correspondence, telegrams, royal orders, etc.)
- **Agential Relationships**: Enables queries such as “all photographs and periodical resources such as newspapers related in any way to Naser al-Din Shah”

By combining these layers, users can construct sophisticated queries that blend What, Who, When, and Where criteria with exceptional precision.

#### Recommendation
To fully benefit from IIIFDexir, familiarity with core IIIF concepts is highly recommended:
- IIIF Collection
- IIIF Manifest
- IIIF Canvas
- IIIF Image API
- IIIF Annotation
- IIIF Content State API

A dedicated appendix explaining these concepts in the context of IIIFDexir is available in the repository. For comprehensive understanding, refer to the official [IIIF Documentation](https://iiif.io/).



### Controlled Vocabularies & Extensions

Controlled vocabularies and authoritative knowledge bases play a central role in `IIIFDexir`, ensuring consistency, interoperability, and semantic richness across the entire collection.

#### Core Vocabularies Used
The project directly incorporates several established vocabularies, including:
- **AAT** (Getty Art & Architecture Thesaurus)
- **TGN** (Getty Thesaurus of Geographic Names)
- **LCTGM** (Library of Congress Thesaurus for Graphic Materials)
- **LCSH** (Library of Congress Subject Headings)

Additional vocabularies such as **Iconclass** and **IA** (Iconography Authority) serve as major sources of inspiration. Where existing vocabularies were insufficient, custom terminologies and extensions have been developed to meet the specific needs of the Persian cultural heritage domain.

#### Person Entities & Family History Knowledge Base (FHKB)
A dedicated hierarchical list of persons has been created using the **Family History Knowledge Base (FHKB)**. This includes historical figures, artists, creators, and mythological or fictional characters (such as the White Demon, Simorgh, and Satan), all cross-referenced with **Wikidata**.

The ontology adopts concepts such as `Inheritance` from software engineering and family history modeling, distinguishing between:
- `Person` (general class)
- Gender differentiation (`Male` / `Female`)
- `Man` / `Woman`
- `FictionalMan` / `FictionalWoman`

In addition to Wikidata alignments and reconciliation, relative and causal relationships (father, mother, spouse, sibling, etc.) have been modeled where data is available. Entries without complete relational data remain as independent records and are fully usable within the system. These relationships can be incrementally enriched over time.

#### Art & Architecture Thesaurus (AAT)
The **Getty Art & Architecture Thesaurus (AAT)** is one of the most important resources in IIIFDexir due to its depth and hierarchical structure. Because of its vast scope, only a carefully selected and relevant subset is actively used. This subset continues to grow and evolve alongside the collection.

A dynamic data visualization of the current AAT subset is maintained to help examine relationships and support ongoing expansion.

- **AAT Subset** (Art & Architecture Thesaurus) — critical for this project:
  ![AAT Subset](/IIIFCollection/images/mermaid-diagram-2026-05-21-123435.svg)

#### Iconography & Narrative Episodes
For iconographic description, the project draws directly from **Iconclass** and **IA**, creating custom entries tailored to Persian visual culture. These entries are carefully aligned with **Wikidata** and **AAT** to avoid ambiguity.

A particularly important extension is the concept of **Narrative Episodes** which is inherited from the `Iconography` base class. These are hierarchical and often interconnected, especially when documenting works related to Ferdowsi’s *Shahnameh*. For example:
- The “Kingdom of Kiyumars” represents a broader historical period within the “Pishdadian Dynasty” and appears in specific artworks such as *The Court of Kiyumars* by Sultan Muhammad.
- Episodes like “The Killing of Mardas by Zahhak” or “Iblis Kissing Zahhak’s Shoulders” are sub-events within larger narratives, such as the “Story of Zahhak,” which itself belongs to the era of Jamshid’s reign.

This layered narrative model allows precise linking between visual resources and literary/historical context. Further details on alignment with scholarly editions (such as the critical text by the late Professor Jalal Khaleghi Mutlaq) will be provided in dedicated sections.

#### Geographic Names & Built Heritage (TGN)
The **Getty Thesaurus of Geographic Names (TGN)** serves as the primary reference for countries, cities, and villages. The same thesaurus has been extended to include buildings and architectural complexes (treated as a subclass). Examples include:
- Grand Mosque of Isfahan
- Golestan Palace
- Chehel Sotun

Hierarchical relationships are fully supported. For instance, while **Naqsh-e Jahan Square** is a child of Isfahan is simultaneously serving as a parent concept for the `Shah Mosque`, `Sheikh Lotfollah Mosque`, and the `Qeysariyeh Bazaar entrance`.

#### Machine-First Design Principle
All vocabularies and extensions prioritize **machine readability** and semantic precision. The structures are intentionally designed to support RDF/OWL reasoning, SPARQL querying, and Knowledge Graph construction. While this results in more complex data models than those needed for human browsing, it ensures long-term interoperability, scalability, and analytical capability.

---






## Accessing the catalog  
You can access the catalog using any standard IIIF Viewer including Mirador 3.0 and yet better free instances of it hosted in the
<a href="https://iiif.biblissima.fr/mirador3/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/IIIF2Collection.json" target="_blank">Mirador in Biblissima</a>.

![Screenshot](https://pbs.twimg.com/media/GmPDuFSbwAAR8O0?format=jpg&name=small "IIIFDexir")

## Important Notes
**Here's the improved, polished, and well-structured version** for your **Important Notes** section:

---

### Important Notes

The `IIIFDexir` dataset is **continuously evolving** in both quality and quantity while maintaining strict semantic consistency. It encompasses a wide variety of digital resources, including books, manuscripts, photographs, periodical newspapers and magazines, documents, maps, correspondence, paintings, calligraphic works, and more.

All changes and expansions in IIIFDexir are carefully governed by its **RDF/OWL Ontology**, which serves as the single source of truth for entities and their relationships. Modifications generally fall into two categories:

- Introduction of new entities (`owl:Class`)
- Definition or refinement of relationships between existing entities (`owl:ObjectProperty`)

#### Key Ontology Evolutions
- **ResourceCanvas** was added later to allow finer-grained description of individual pages, folios, and components within larger works. A single `ResourceCanvas` can contain multiple **ContentElements** (e.g., an illustration, a block of poetry, a marginal note, or a seal), each enriched with its own content-type, agential, and subject tags via controlled vocabularies and Iconography source.
- **ResourceCollection** continues to act as the container for `DigitalResources`, while **ResourceCanvas** links to its parent `DigitalResource` (e.g., a specific manuscript or album) and enables detailed analysis of its internal structure.

This layered model is especially valuable for Persian cultural materials, where a single manuscript page may combine text, image, and annotation elements.

#### Expansion of Controlled Vocabularies & other related References
Significant updates involve expanding controlled vocabularies and external references, particularly:
- **Wikidata** for literary works, narrative episodes, persons, and mythological entities
- **AAT** (Getty Art & Architecture Thesaurus) for materials, techniques, and object types
- **FHKB** (Family History Knowledge Base) for relative and causal relationships

For example, documenting a `ResourceCanvas` depicting “The Binding of Zahhak in Damavand” requires well-defined entries for the broader literary work (*Story of Zahhak*), its sub-episodes, and related characters. All such entries are aligned with Wikidata Q-codes to ensure disambiguation and interoperability. Similarly, when adding new AAT concepts (e.g., “Stuccowork”), the full hierarchical context (Broader/Narrower terms) is incorporated.

#### Adding New Content
New resources are added as an instance of **DigitalResources** (requiring a valid IIIF Manifest). When a suitable manifest does not exist, resources are uploaded to the **Internet Archive**, which automatically generates a compliant IIIF Manifest. This approach ensures all items meet IIIF standards while respecting copyright considerations.

New **Resource Collections** are created when needed for better thematic organization (e.g., a collection for 400 slides by Dennis Bali in digital Keyon which originally are not IIIF Compliant).

#### Departed Collections & On-the-Fly Manifests
As explained earlier, **Departed Collections** and dynamically generated “on-the-fly” manifests enable the virtual reunification of dispersed heritage items (such as pages from the *Shahnameh of Shah Tahmasp*).

#### Transparency & Change Tracking
IIIFDexir grows almost daily. Thanks to GitHub’s version control, every change including what was modified, when, and by whom is permanently recorded and traceable from the project’s inception.

**Core Principle**: While IIIFDexir prioritizes machine-readable structured data and semantic precision, significant effort has been made to ensure it remains accessible and useful for human researchers through standard IIIF viewers.

---


## Preparing KG 
Creating a Knowledge Graph from the IIIFDexir is straightforward. IIIF Collections and Manifests are in JSON-LD format, but we used the Turtle format to implement a simple ontology for Data visualizatio representation. The primary entities are ResourceCollection (IIIF Collection) and DigitalResource (IIIF Manifest), both represented by owl:Class.

## Ontology

**IIIF Collection Ontology**

The **IIIF Collection Ontology** serves as the semantic foundation and conceptual blueprint for the entire IIIFCollection project. Defined in RDF/OWL (Turtle format), it provides a structured, interoperable vocabulary to model digital cultural heritage resources, their metadata, and complex interrelationships within the IIIF (International Image Interoperability Framework) ecosystem.

![A Semantic Gateway to Persian Heritage](/IIIFCollection/images/Semantic_Gateway_to_Persian_Heritage.jpg)

### Purpose and Role in the Project

This ontology acts as the **central knowledge model** for the repository. It enables:

- Consistent semantic annotation of IIIF manifests and collections
- Rich, machine-readable descriptions of cultural artifacts (manuscripts, photographs, maps, calligraphy, etc.)
- Advanced querying, discovery, and linking across heterogeneous resources
- Integration with external authority sources (Getty AAT, TGN, LCSH, Wikidata, etc.)
- Support for both human-readable navigation and automated reasoning

By formalizing the project's domain concepts, the ontology ensures data consistency, facilitates future extensions, and positions the collection as part of the broader linked open data (LOD) graph in cultural heritage.

### Core Structure

The ontology is organized around several key conceptual pillars under the namespace `mdhn:` (`http://example.com/mdhn/`):

#### 1. Primary Resource Classes
- **`mdhn:ResourceCollection`** — Represents hierarchical collections of IIIF resources, supporting nested manifests and sub-collections.
- **`mdhn:DigitalResource`** — The central class representing individual IIIF manifests (books, photographs, videos, documents, etc.).
- **`mdhn:DepartedCollection`** — Special class for logically reuniting dispersed or "departed" folios into virtual collections.

#### 2. Iconography and Content Description
- **`mdhn:Iconography`** — Root class for all visual and thematic content depicted in resources.
  - Subclasses include: `BattleSignAndEquipment`, `ArchitecturalConceptOrElement`, `ClothingAndDress`, `Animals`, `MusicalInstrument`, `NaturalElement`, `MythicalConceptsOrCreatures`, `ObjectsAndTools`, etc.
- **`mdhn:NarrativeEpisode`** — For modeling specific scenes, stories, or historical events depicted.

Key properties:
- `mdhn:depicts` / `mdhn:iconographyUsedIn` — Bidirectional link between resources and iconographic subjects.

#### 3. Agents and Participation
- **`mdhn:AgentialInfo`** — Core class for people and agents (subclass of FHKB Person).
- **`mdhn:ParticipantRole`** — Defines roles.
- Generic property: `mdhn:hasParticipantInRole` (with many specialized sub-properties such as `hasParticipantInRolePhotographer`, `hasParticipantInRoleCalligrapher`, `hasParticipantInRoleIlluminator`, etc.).

This creates rich agent-resource networks with inverse properties (e.g., `photographerOf`, `authorOf`, `painterOf`).

#### 4. Subject and Classification System
- **`mdhn:AATTerm`** (root) → subclasses:
  - `mdhn:ResourceType` (first-level classification)
  - `mdhn:DocumentGenre` (second-level)
  - `mdhn:AATSubject`, `mdhn:ScriptStyleType`
- **`mdhn:SubjectSource`** hierarchy: `LCTGMSubject`, `LCSHSubject`, `GLAMSource`
- Geographic: `mdhn:GettyTGN` and `mdhn:FeaturedSSitesOrBuilding`

#### 5. Supporting Classes
- `mdhn:CanvasType`
- `mdhn:TemporalInfo`
- `mdhn:Creator`, `mdhn:Publisher`, `mdhn:GLAMSource`

### Design Principles

The ontology follows Linked Data best practices:
- Heavy reuse of existing vocabularies (OWL, RDFS, Getty AAT/TGN, LCSH, Schema.org, FOAF, etc.)
- Bidirectional inverse properties for easy traversal
- Multilingual labels (English + Persian)
- Hierarchical classification with clear domain/range restrictions
- Support for both broad (generic `hasParticipantInRole`) and specific roles

This structure allows the project to move beyond simple metadata catalogs toward a true **knowledge graph** of visual and textual cultural heritage, where resources, iconography, people, places, and narratives are deeply interconnected.

### Graphical representation of this Ontology:

![alt text](/IIIFCollection/images/ontology.JPG)


## IIIFDexir Workflow and RDF Ontology

This repository, [IIIFCollection](https://github.com/MehranDHN/IIIFCollection), provides a dynamic, machine-readable catalog based on the International Image Interoperability Framework ([IIIF](http://iiif.org)) standards, focusing on cultural, artistic, architectural, photographic, and literary resources related to Persia (Iran). This README outlines the workflow for utilizing the RDF ontology and IIIF Multipart Collections, highlights the distinction between **Departed Collections** and **Resource Collections**, and provides sample SPARQL queries to interact with the Knowledge Graph.

Class Hierarchy in Ontotext GraphDB:
![alt text](/IIIFCollection/images/classhierarchy.JPG)

## Overview of IIIF Multipart Collections

IIIF Multipart Collections are structured to organize digital resources hierarchically, adhering to IIIF standards. These collections are represented as JSON-LD and are fully compatible with IIIF viewers like Mirador and OpenSeaDragon. The collections are designed to be both machine-readable and human-usable, supporting flexible data enrichment from external sources (e.g., XML, JSON, RDF Turtle) and alignment with controlled vocabularies such as Getty's AAT, TGN, Library of Congress's TGM, Schema.org, and Wikidata.

### Key Features of IIIF Multipart Collections
- **Hierarchical Structure**: Collections can contain nested sub-collections and IIIF Manifests, enabling a tree-like organization of resources.
- **Machine Readability**: JSON-LD format ensures compatibility with semantic web technologies.
- **Public Accessibility**: Resources are accessible online via standard IIIF viewers.
- **Dynamic Enrichment**: External data sources can be integrated to enhance metadata, often referenced via the `seeAlso` field in manifests.

## Refering to Contents
All the entries in this projectd designed as an IIIF Collection. Collection and Manifest are first level objects in IIIF Ecosystem and Canvasses are special type of object that typically can be integrated inside of a manifest. Refereing to Collection and manifest can be achived by `iiif-content` Query string in standard IIIF Viewers.
Thanks to IIIF Content State API we can use this method to access a canvas inside the manifest with a little differences.

### Accessing the root collection using Theseus: 
```
https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/IIIF2Collection.json
  
```
[Root Collection using Theseus](https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/IIIF2Collection.json)

### Accessing the Edward Brown Collection:
```
https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/EdwardBrowneCollection.json
  
```
[Edward Brown Collection using Theseus](https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/EdwardBrowneCollection.json)

### Accessing specified region of an image using Content State API:


```json
{
    "id": "https://manifest.storiiies-editor.cogapp.com/v3/3e7uh/Sadi-and-the-Youth-of-Kashgar/canvases/1#xywh=3357,1820,1745,1042",
    "type": "Canvas",
    "partOf": [
        {
            "id": "https://manifest.storiiies-editor.cogapp.com/v3/3e7uh/Sadi-and-the-Youth-of-Kashgar",
            "type": "Manifest"
        }
    ]
}  
```

### base64url encoded of previoud data:
```
eyJpZCI6Imh0dHBzOi8vbWFuaWZlc3Quc3RvcmlpaWVzLWVkaXRvci5jb2dhcHAuY29tL3YzLzNlN3VoL1NhZGktYW5kLXRoZS1Zb3V0aC1vZi1LYXNoZ2FyL2NhbnZhc2VzLzEjeHl3aD0zMzU3LDE4MjAsMTc0NSwxMDQyIiwidHlwZSI6IkNhbnZhcyIsInBhcnRPZiI6W3siaWQiOiJodHRwczovL21hbmlmZXN0LnN0b3JpaWllcy1lZGl0b3IuY29nYXBwLmNvbS92My8zZTd1aC9TYWRpLWFuZC10aGUtWW91dGgtb2YtS2FzaGdhciIsInR5cGUiOiJNYW5pZmVzdCJ9XX0=
```

[Specified region inside a canvas using Theseus](https://theseusviewer.org/?iiif-content=eyJpZCI6Imh0dHBzOi8vbWFuaWZlc3Quc3RvcmlpaWVzLWVkaXRvci5jb2dhcHAuY29tL3YzLzNlN3VoL1NhZGktYW5kLXRoZS1Zb3V0aC1vZi1LYXNoZ2FyL2NhbnZhc2VzLzEjeHl3aD0zMzU3LDE4MjAsMTc0NSwxMDQyIiwidHlwZSI6IkNhbnZhcyIsInBhcnRPZiI6W3siaWQiOiJodHRwczovL21hbmlmZXN0LnN0b3JpaWllcy1lZGl0b3IuY29nYXBwLmNvbS92My8zZTd1aC9TYWRpLWFuZC10aGUtWW91dGgtb2YtS2FzaGdhciIsInR5cGUiOiJNYW5pZmVzdCJ9XX0=)

### Online base64url encoder: 
- [Online Encoder](https://simplycalc.com/base64url-encode.php)

- Screenshot of a demo representing using  Content State API to access a specified region in a canvas inside an annotated manifest:
![Query 4](/IIIFCollection/images/content_state.JPG)

Extending this sample to another level could prove truly transformative. Imagine each illustrated manuscript having its own dedicated, standalone data structure for every magnificent folio including the cover, opening pages, flyleaf, rosette, colophon, and beyond.
Additionally, each individual folio could be assigned its own specific, persistent URL, allowing it to be referenced, shared, and viewed independently without needing to navigate the entire manuscript. With the help of the `IIIF Content State API`, this vision becomes not only possible but highly practical. It opens up rich opportunities to enrich, annotate, and present each folio independently whether for scholarly analysis, educational use, high-resolution exhibition, or creative reinterpretation while maintaining the integrity and context of the complete manuscript.

[Folio 4v from Supplément persan 489](https://theseusviewer.org/?iiif-content=ewogICAgImlkIjogImh0dHBzOi8vZ2FsbGljYS5ibmYuZnIvaWlpZi9hcms6LzEyMTQ4L2J0djFiODQyMjk5NXQvY2FudmFzL2YxNiIsCiAgICAidHlwZSI6ICJDYW52YXMiLAogICAgInBhcnRPZiI6IFsKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6ICJodHRwczovL2dhbGxpY2EuYm5mLmZyL2lpaWYvYXJrOi8xMjE0OC9idHYxYjg0MjI5OTV0L21hbmlmZXN0Lmpzb24iLAogICAgICAgICAgICAidHlwZSI6ICJNYW5pZmVzdCIKICAgICAgICB9CiAgICBdCn0g)



[See the Query 13](https://github.com/MehranDHN/IIIFCollection#query-13-all-folios-that-belongs-to-manuscripts)

### RDF Ontology: Departed Collections vs. Resource Collections

The RDF ontology, implemented in Turtle format, models two primary entities: **ResourceCollection** and **DigitalResource**, alongside other classes like `Creator`, `Publisher`, `ResourceType`, and `CanvasType`. Below, we differentiate between **Departed Collections** and **Resource Collections**:

### Departed Collections
- **Purpose**: Designed to integrate digital resources scattered across various institutions, such as museums or archives worldwide.
- **Characteristics**: 
  - Aggregates resources that are not necessarily related by subject but are unified by their cultural or historical significance to Persia.
  - Facilitates interoperability by linking disparate digital assets into a cohesive collection.
  - Often references external sources via the `seeAlso` field for additional metadata.
- **Use Case**: A Departed Collection might include manuscripts from a museum in London, photographs from an archive in Tehran, and books from a library in New York, unified under a shared cultural theme.

### Resource Collections
- **Purpose**: Organized by specific subjects (e.g., Persian architecture, calligraphy, or literature) with a hierarchical structure based on IIIF Collection capabilities.
- **Characteristics**:
  - Follows a tree-like organization where collections can contain sub-collections and manifests.
  - Aligned with controlled vocabularies (e.g., AAT, TGM, Wikidata) to categorize resources by type or theme.
  - Emphasizes structured, subject-based access to resources for both human and machine consumption.
- **Use Case**: A Resource Collection might focus on "Persian Miniature Paintings," with sub-collections for different artists or periods, each containing relevant IIIF Manifests.

### Ontology Representation
The ontology defines relationships such as `hasResource`, `hasCreator`, `hasPublisher`, and `hasResourceType` to link entities. For example:
- `mdhn:ResourceCollection` represents both Departed and Resource Collections, with `mdhn:partOf` indicating hierarchical relationships.
- `mdhn:DigitalResource` represents individual IIIF Manifests, linked to collections via `mdhn:belongsTo`.

### Transforming RDF Ontology to First-Order Logic

RDF ontologies can be translated into First-Order Logic (FOL) to enable formal reasoning, theorem proving, or integration with logical systems. In FOL, classes are represented as unary predicates (e.g., `ResourceCollection(x)`), while properties are binary predicates (e.g., `hasResource(x, y)`). Domain and range constraints are axiomatized using universal quantifiers to enforce type restrictions. Inverse properties are captured with equivalence axioms.

Below, we transform the key elements of the RDF ontology into FOL axioms, with a strong emphasis on the domain and range of each object and datatype property. Note that namespaces (e.g., `mdhn:`) are omitted for brevity in the predicates, but they align with the Turtle definitions.

### Classes as Unary Predicates
- `ResourceCollection(x)`: True if x is a resource collection.
- `DigitalResource(x)`: True if x is a digital resource (IIIF Manifest).
- `Creator(x)`: True if x is a creator entity.
- `Publisher(x)`: True if x is a publisher entity.
- `ResourceType(x)`: True if x is a resource type (aligned with vocabularies like AAT).
- `CanvasType(x)`: True if x is a canvas type within a manifest.

### Object Properties with Domain and Range
Each object property is represented as a binary predicate, with axioms for domain (subject type) and range (object type). Inverse relationships are also axiomatized.

- **hasResource(x, y)**  
  - Domain: ResourceCollection (∀x ∀y (hasResource(x, y) → ResourceCollection(x)))  
  - Range: DigitalResource (∀x ∀y (hasResource(x, y) → DigitalResource(y)))  
  - Inverse: belongsTo(y, x) (∀x ∀y (hasResource(x, y) ↔ belongsTo(y, x)))

- **hasCreator(x, y)**  
  - Domain: DigitalResource (∀x ∀y (hasCreator(x, y) → DigitalResource(x)))  
  - Range: Creator (∀x ∀y (hasCreator(x, y) → Creator(y)))  
  - Inverse: createResources(y, x) (∀x ∀y (hasCreator(x, y) ↔ createResources(y, x)))

- **hasCanvasType(x, y)**  
  - Domain: DigitalResource (∀x ∀y (hasCanvasType(x, y) → DigitalResource(x)))  
  - Range: CanvasType (∀x ∀y (hasCanvasType(x, y) → CanvasType(y)))  
  - No inverse defined.

- **ofType(x, y)**  
  - Domain: DigitalResource (∀x ∀y (ofType(x, y) → DigitalResource(x)))  
  - Range: ResourceType (∀x ∀y (hasResourceType(x, y) → ResourceType(y)))  
  - Inverse: hasTypeInstance(y, x) (∀x ∀y (hasTypeInstance(x, y) ↔ resourceTypeInstance(y, x)))

- **hasPublisher(x, y)**  
  - Domain: DigitalResource (∀x ∀y (hasPublisher(x, y) → DigitalResource(x)))  
  - Range: Publisher (∀x ∀y (hasPublisher(x, y) → Publisher(y)))  
  - Inverse: publishedResource(y, x) (∀x ∀y (hasPublisher(x, y) ↔ publishedResource(y, x)))

- **belongsTo(x, y)**  
  - Domain: DigitalResource (∀x ∀y (belongsTo(x, y) → DigitalResource(x)))  
  - Range: ResourceCollection (∀x ∀y (belongsTo(x, y) → ResourceCollection(y)))  
  - Inverse of hasResource.

- **publishedResource(x, y)**  
  - Domain: Publisher (∀x ∀y (publishedResource(x, y) → Publisher(x)))  
  - Range: DigitalResource (∀x ∀y (publishedResource(x, y) → DigitalResource(y)))  
  - Inverse of hasPublisher.

- **createResources(x, y)**  
  - Domain: Creator (∀x ∀y (createResources(x, y) → Creator(x)))  
  - Range: DigitalResource (∀x ∀y (createResources(x, y) → DigitalResource(y)))  
  - Inverse of hasCreator.

- **resourceTypeInstance(x, y)**  
  - Domain: ResourceType (∀x ∀y (resourceTypeInstance(x, y) → ResourceType(x)))  
  - Range: DigitalResource (∀x ∀y (resourceTypeInstance(x, y) → DigitalResource(y)))  
  - Inverse of hasResourceType.

- **subCollectionOf(x, y)**  
  - Domain: ResourceCollection (∀x ∀y (subCollectionOf(x, y) → ResourceCollection(x)))  
  - Range: ResourceCollection (∀x ∀y (subCollectionOf(x, y) → ResourceCollection(y)))  
  - Inverse: parentCollectionOf(y, x) (∀x ∀y (parentCollectionOf(x, y) ↔ subCollectionOf(y, x)))

- **partOf(x, y)**  
  - Domain: DigitalResource (∀x ∀y (partOf(x, y) → DigitalResource(x)))  
  - Range: DepartedCollection (∀x ∀y (partOf(x, y) → DepartedCollection(y)))  
  - Inverse: contains(y, x) (∀x ∀y (contains(x, y) ↔ partOf(y, x)))  

### Datatype Properties with Domain and Range
Datatype properties link entities to literal values (e.g., strings or URIs).

- **hasUrl(x, y)**  
  - Domain: ResourceCollection or DigitalResource (∀x ∀y (hasUrl(x, y) → (ResourceCollection(x) ∨ DigitalResource(x))))  
  - Range: xsd:anyURI (∀x ∀y (hasUrl(x, y) → URI(y)))  
  - (Where URI(y) represents y being a URI value.)

- **caption(x, y)**  
  - Domain: ResourceCollection or DigitalResource (∀x ∀y (caption(x, y) → (ResourceCollection(x) ∨ DigitalResource(x))))  
  - Range: xsd:string (∀x ∀y (caption(x, y) → String(y)))  
  - (Where String(y) represents y being a string literal.)

These FOL axioms provide a formal foundation for reasoning about the ontology, such as checking consistency or inferring relationships. Tools like theorem provers (e.g., Vampire or E Prover) can utilize these axioms for advanced queries beyond SPARQL.

### Workflow for Using RDF Ontology and IIIF Collections

1. **Accessing the Collection**:
   - Use a standard IIIF viewer (e.g., Mirador 3.0, OSD, Thesus, ... ) to explore the collection.
   - Retrieve JSON-LD manifests or collections via their URLs.

2. **Enriching Data**:
   - Parse external sources referenced in the `seeAlso` field to enrich metadata.
   - Align resources with controlled vocabularies (e.g., AAT, TGM) for semantic consistency.

3. **Building a Knowledge Graph**:
   - Convert JSON-LD manifests into RDF Turtle format using the provided ontology.
   - Use tools like Apache Jena or RDFLib to load and query the Knowledge Graph.

4. **Querying the Knowledge Graph**:
   - Execute SPARQL queries to extract insights, such as resource types, creators, or hierarchical relationships.

5. **Analyzing and Visualizing**:
   - Generate statistics or visualizations based on query results, leveraging the machine-readable structure.
   - Use IIIF viewers for human-readable exploration.


### Sample SPARQL Queries

Below are sample SPARQL queries to demonstrate how to interact with the Knowledge Graph built from the IIIFDexir ontology.

#### Query 1: List All Digital Collections with the number of resources
This query retrieves all `mdhn:ResourceCollection` instances and counts number of `mdhn:DigitalResource` instances in each of them.

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

select  ?collection (Count(?s) as ?resourceCount){
    ?s a mdhn:DigitalResource;
    (mdhn:isInCollection)* ?collection.
    ?collection a mdhn:ResourceCollection.


}
Group by ?collection
Order by Desc(?resourceCount)
```

####  Query 2: Find Creators of Digital Resources
This query lists creators and their labels associated with `DigitalResource` instances.

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
SELECT ?resource ?creator ?label
WHERE {
  ?resource a mdhn:DigitalResource ;
            mdhn:hasCreator ?creator .
    ?creator rdfs:label ?label.
}
```

####  Query 3: Identify Hierarchical Structure of Resource Collections
This query retrieves parent-child relationships between `ResourceCollection` instances.

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
SELECT ?parent ?child ?childLabel
WHERE {
  ?child a mdhn:ResourceCollection ;
    mdhn:subCollectionOf ?parent ;
    mdhn:caption ?childLabel .
}
```

####  Query 4: Resources by Type Using Controlled Vocabularies
This query finds `DigitalResource` instances associated with a specific resource type from Getty's AAT.

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX aat: <https://vocab.getty.edu/aat/>
SELECT ?resource ?label
WHERE {
  ?resource a mdhn:DigitalResource ;
            mdhn:ofType mdhn:aat300027200 ;  # AAT term for "Photograph Album"
            rdfs:label ?label .
}
```
There is a difference between logical Collections and actual resource type. To get a full list of all members of `mdhn:PhotographAlbum` which is an instance of  `mdhn:ResourceCollection` the following Query can be use:

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

select ?s  ?reslabel{
    ?s a mdhn:DigitalResource;
       rdfs:label ?reslabel;
      mdhn:isInCollection mdhn:PhotographAlbum.

}
```

To limit the labels to specific Language:

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX aat: <https://vocab.getty.edu/aat/>
SELECT ?resource ?label
WHERE {
  ?resource a mdhn:DigitalResource ;
            mdhn:ofType mdhn:aat300027200 ;  # AAT term for "Photograph Album"
            rdfs:label ?label .
    FILTER(LANG(?label)="en")
    #BIND(LANG(?label) as ?languages)
    #FILTER(?languages IN ("fr", "en", "fa"))
}
```
Screenshot of running SPARQL query and its coresponding result:
![Query 4](/IIIFCollection/images/langfilter.JPG)

####  Query 5: Accessing the specified folio type (Drawings) 
This query finds all matches that have the `mdhn:folioHasDrawing` flag, which is a flag to identify the drawing resources.
In future improvements, we should associate this feature with the particular Controlled Vocabulary designed to identify folio types.

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX aat: <https://vocab.getty.edu/aat/>
SELECT *
WHERE {
  ?resource a mdhn:DigitalResource ; 
            mdhn:folioHasDrawing ?drawing;
            mdhn:partOf ?part;
            rdfs:label ?label .
}
```
![Query 5](/IIIFCollection/images/FolioType.JPG)
It is obvious that we can use filters to limit the results only for specified physical or logical collection:

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX aat: <https://vocab.getty.edu/aat/>
SELECT *
WHERE {
  ?resource a mdhn:DigitalResource ; 
            mdhn:folioHasDrawing ?drawing;
            mdhn:partOf ?part;
            rdfs:label ?label .
  Filter(?part=mdhn:vcol1000111)
}
```
####  Query 6: Accessing the resources that somehow related to specified geo spatial TGN location
This query finds all resources that related to specified TGN location based on  `mdhn:hasTGNPlace` predicate. We also `mdhn:ofType` predicate as another dimension to find the resource types.
This query can be easily extended to group the results by resource types to count the resources associated to each type. 
The `mdhn:tgn1001228` is the part of the Isfahan URI which we reconciliate with the Getty's TGN .
See [TGN](http://vocab.getty.edu/tgn/1001228)

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>
select ?s  ?place ?restype ?typelbl {
    ?s a mdhn:DigitalResource;
      mdhn:ofType ?restype;
      mdhn:hasTGNPlace ?place.
    ?restype rdfs:label ?typelbl.
    Filter(?place=mdhn:tgn1001228)
    Filter(Lang(?typelbl)="en")
}
```

####  Query 7: Using agential info of the resources
This query finds all resources that marked with Agential information which is instances of  `fhkb:Person`. Those resources associate with `mdhn:hasAgential` predicate to the Agential info which is Adapted from FHKB.

See [Family History Knowledge Base (FHKB)](https://oboacademy.github.io/obook/tutorial/fhkb/)

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

select ?person ?lblPerson{
    ?s a mdhn:DigitalResource;
       mdhn:hasAgential ?person.
    ?person rdfs:label ?lblPerson.
    Filter(Lang(?lblPerson)="fa")
}
```
![Query 7](/IIIFCollection/images/fhkbResult.JPG)

Accessing all resources that relate to specified person:
```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

select ?person ?lblPerson{
    ?s a mdhn:DigitalResource;
       mdhn:hasAgential ?person.
    ?person rdfs:label ?lblPerson.
    Filter(?person=mdhn:Naser_al_Din_Shah_Qajar)
    Filter(Lang(?lblPerson)="fa")
}
```
####  Query 8: Accessing the resources that have Kufic script style excepts those in specified collection
This query finds all resources that has specified  `mdhn:aat300194434` script style which is Kufic script in AAT Thesaurus. We limit the results to all but those that are in specified Collection `mdhn:AsarolBaghieOrMs161`.


```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>
# ليست آثاری که به خط کوفی مرتبط هستند به استثنای مجموعه آثار الباقيه
select * {
    ?s a mdhn:DigitalResource;
       mdhn:hasScriptStyle mdhn:aat300194434;
       mdhn:isInCollection ?collection.
    Filter(?collection!=mdhn:AsarolBaghieOrMs161)
  
}
```
####  Query 9: Determinig which resources have the Subject headers that reconciliated against AAT and LCSH (Not The LCTGM)
This query finds all resources that have specified subject header types. Those that are `mdhn:AATTerm` and `mdhn:LCSHSubject` because all resources reconciliate against three primary sources inclusing `LCTGM`, `LCSH` and `AAT`.
```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT *
WHERE {
    ?s a mdhn:DigitalResource ;
       mdhn:hasSubject ?subject ;
       mdhn:isInCollection ?collection .
    ?subject a ?type .
    FILTER(?type IN (mdhn:AATTerm, mdhn:LCSHSubject))
}
```
####  Query 10: Determinig the participants in resources with their roles 
This query finds all participants who involve somehow in resources. Roles such as `mdhn:hasParticipantInRolePhotographer` and `mdhn:hasParticipantInRoleIllustrator` are Object Properties which are `rdfs:subPropertyOf` the `mdhn:hasParticipantInRole` that enables us to integrate all participants of Digital Resources in an effective way.
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

SELECT *
WHERE {
    ?s a mdhn:DigitalResource ;
       mdhn:hasParticipantInRole ?Agential ;
       mdhn:isInCollection ?collection .
}
```
Obviously we can get all participants with one or more specified role:
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

SELECT *
WHERE {
    ?s a mdhn:DigitalResource ;
       mdhn:hasParticipantInRolePhotographer ?Agential ;
       mdhn:isInCollection ?collection .
}
```
Then execuating a query to get a result of aggregated agential info:
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

SELECT Distinct ?agential (Count(?s) as ?cs)
WHERE {
    ?s a mdhn:DigitalResource ;
       mdhn:hasParticipantInRole ?agential ;
       mdhn:isInCollection ?collection .
   
}
GROUP BY ?agential
```

####  Query 11: Filter the resources in specified physical collections based on particular Iconography Tag
This query finds all digital resources that has a particular Tag in specified Collection. This can be achieved with a combinations of  `mdhn:isInCollection` and `mdhn:depicts` and then using a `Filter` to narrow the result.
```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

select * {
    ?s a mdhn:DigitalResource;
       mdhn:isInCollection mdhn:DepartedDrawing;
       mdhn:depicts ?icgtag.
    ?icgtag rdfs:label ?lbltag.
    Filter(Lang(?lbltag)="en")
    Filter(?icgtag=mdhn:Boat)
}
```

####  Query 12: Filter the resources in specified physical collections based on particular Agential info and his involvement role and narrowing the result to those have valid Iconography Tag
This query finds all digital resources that has a particular Tag in specified Collection. This can be achieved with a combinations of  `mdhn:isInCollection` ,`mdhn:depicts` and `mdhn:hasParticipantInRolePoet` and then using a `Filter` to narrow the result.
```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

select *{
    ?s a mdhn:DigitalResource;
       mdhn:isInCollection mdhn:DepartedDrawing;
       mdhn:depicts ?iconography;
       mdhn:hasParticipantInRolePoet ?poet.
    ?s rdfs:label ?lblresource.
    Filter(Lang(?lblresource)="en")
    Filter(?poet=mdhn:Abul_Qasim_Firdawsi)
}
```

####  Query 13: All folios that belongs to manuscripts
This query finds all digital canvases that belongs to manuscripts. This can be achieved with a `mdhn:canvasOf` which assocates canvases to manuscripts. The data contain standalone URL based on IIIF Content State API.

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


SELECT *
WHERE {
    ?s a mdhn:ResourceCanvas;
       rdfs:label ?canvasLabel;
       mdhn:canvasIndex ?idx;
       mdhn:folioNo ?foliono;
       mdhn:folioStandaloneURL ?url;
       mdhn:canvasOf ?res.
    ?res rdfs:label ?resLabel;   
}
ORDER BY ?idx
```
## On-the-Fly IIIF Manifest Generator
A flexible Python script that dynamically combines selected IIIF manifests into a single, local-compatible manifest (Presentation API 2.0 or 3.0).
Supports:

- Multiple sources with different base URLs and API versions
- Selecting specific canvases (by zero-based index) from each manifest
- Custom canvas labels using a user-defined template
- Optional table of contents (structures/ranges)
- Custom metadata (completely independent of source manifests)
- Mixed v2 and v3 source manifests (with annotation normalization)
- Detailed logging & validation to debug problems

This tool is particularly useful for creating curated selections from heterogeneous IIIF collections (e.g. mixing archive.org HV.* items with Chester Beatty Library Persian manuscripts or any other IIIF endpoints).


## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MehranDHN/IIIFCollection.git
   ```

2. **Explore the Collection**:
   - Open the collection in a IIIF viewer like Mirador.
   - Inspect JSON-LD files for manifests and collections.

3. **Work with the Ontology**:
   Creating a full GraphDB from the data that have provided required using a Local or Cloud GraphDB System. Ontotext Graph and Stardog Cloud Service are excellent choices.
   - Load the Turtle ontology (`iiifCollectionOntology.ttl`) into a triplestore (e.g., Apache Jena).
   - Load the Turtle (`aat_hierarchy.ttl`) which is a subset of the Standard AAT for the scope of this project.
   - Load the Turtle (`iconography_RDF.ttl`) which is a limited-scope for iconography based on WikiData.   
   - Load the Turtle (`ctl_vocabs.ttl`) which is a subset of Controlled Vocabularies.   
   - Load the Turtle (`LCTGM_RDF.ttl`), (`tgn_subset_updated.ttl`) and (`PersonsRDFData.ttl`).
   - Load the (`resources.ttl`) which is actual RDF data of the collection.      
   - Use SPARQL queries to analyze the Knowledge Graph.

4. **Contribute**:
   - Enrich the collection by adding new manifests or external metadata.
   - Help to better organizing the categorizations.
   - Submit pull requests for ontology updates or new SPARQL queries.

## Notes
- The catalog is dynamic and may undergo daily updates to its structure and contents.
- Ensure proper parsing of `seeAlso` fields to incorporate external metadata.
- The ontology is designed to be extensible, allowing integration with additional vocabularies or data sources.

## About
This project is a dynamic IIIF collection featuring a hierarchical catalog related to the culture, art, architecture, photographs, and books of Persia (Iran). It aims to provide a machine-readable, semantically rich resource for researchers, developers, and enthusiasts.


---
*Updated on Nov 7, 2025, by **MehranDHN**, powered by: Grok 3 (xAI).*
