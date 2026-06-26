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


## Spatial Navigation with navPlace Extension

III FDexir leverages the official **[navPlace Extension](https://iiif.io/api/extension/navplace/)** of the IIIF Presentation API 3.0 to enrich manifests with professional **geospatial metadata**.

This powerful feature allows any IIIF Manifest (or individual Canvas) to be linked to real-world geographic locations using:
- Simple coordinates (Point)
- Bounding boxes
- Complex geometries via **GeoJSON** (Polygon, LineString, MultiPolygon, etc.)

### Use Cases in Persian Cultural Heritage
- Pinpointing the exact location of mosques, palaces, archaeological sites, or historical buildings depicted in artworks or photographs
- Geotagging manuscripts, albums, or travelogues with their places of origin or depicted locations
- Enabling map-based discovery and spatial queries across the entire collection

### Demonstration
A simple working demonstration of the **navPlace** extension in IIIFDexir has been implemented and is available here:

→ **[navPlace Demonstration](https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/CRMPersianArchitecture/refs/heads/main/Jamemanifest.json)** 

![navPlace Demo](/IIIFCollection/images/navplacedemo.jpg)

This initial prototype shows how spatial features can be added to manifests. Future expansions will include more sophisticated GeoJSON representations, integration with external map viewers (such as Leaflet), and broader application across ResourceCollections.

### Technical Note
The `navPlace` property is fully compatible with the IIIFDexir ontology and Knowledge Graph. It opens new possibilities for spatial analysis, visualization, and discovery of Persian cultural heritage resources.

---



#### Machine-First Design Principle
All vocabularies and extensions prioritize **machine readability** and semantic precision. The structures are intentionally designed to support RDF/OWL reasoning, SPARQL querying, and Knowledge Graph construction. While this results in more complex data models than those needed for human browsing, it ensures long-term interoperability, scalability, and analytical capability.

---

## Accessing the catalog  
You can access the catalog using any standard IIIF Viewer including Mirador 3.0 and yet better free instances of it hosted in the
<a href="https://iiif.biblissima.fr/mirador3/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/IIIF2Collection.json" target="_blank">Mirador in Biblissima</a>.

![Screenshot](https://pbs.twimg.com/media/GmPDuFSbwAAR8O0?format=jpg&name=small "IIIFDexir")

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


## Using Data and preparing to create Knowledge Graph 


### Accessing IIIFDexir Data

There are four primary ways to access and interact with IIIFDexir data, ranging from advanced semantic querying to simple browsing:

1. **Query Languages** (Recommended for researchers and analysts)
2. **Exploring the Knowledge Graph**
3. **Standard IIIF Viewers** (Best for general users)
4. **Direct Programming Access**

#### 1. Query Languages
This is the most powerful method for retrieving precise information. It requires loading the dataset into a **Triple Store**  a specialized database designed for RDF data.

![SPARQL](/IIIFCollection/images/IIIFDexir_SPARQL.jpg "GraphDB SPARQL")

**Recommended Tools:**
- **Ontotext GraphDB Desktop** (Free local version): Ideal for individual researchers. You can run a local Triple Store on your computer, import IIIFDexir data, and execute queries via **SPARQL**.
- **Stardog** (Cloud-based): Offers both free (limited) and paid plans. Supports **SPARQL** and **GraphQL**.

After importing the data, you can run complex queries to answer sophisticated questions about persons, dates, places, narratives, materials, and more.

> **Note**: Stardog’s free tier automatically deletes inactive repositories. It is best suited for testing. For long-term use, a paid plan or a local solution like GraphDB Desktop is recommended.

#### 2. Exploring the Knowledge Graph
This method also requires a Triple Store (see above). Instead of writing formal SPARQL queries, you can visually explore the interconnected data by following relationships between entities (persons, works, places, events, etc.). Many Triple Store platforms provide graph visualization tools that make navigation intuitive and insightful.

![Knowledge Graph](/IIIFCollection/images/IIIFDexir_KG.jpg "GraphDB KG")

#### 3. Using Standard IIIF Viewers
This is the most user-friendly method and requires no technical expertise. It is ideal for those who prefer visual browsing.

Using viewers such as **Mirador** or **Theseus**, you can:
- Browse hierarchical **Resource Collections** (think of them as themed folders)
- Navigate sub-collections
- Open **IIIF Manifests** (digital representations of books, manuscripts, albums, or single items)
- View high-resolution images, zoom into details, and read metadata

![Mirador](/IIIFCollection/images/IIIFDexir_Mirador.jpg "Mirador")

**Recommended Viewers:**
- [Mirador](https://iiif.biblissima.fr/mirador3/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/IIIF2Collection.json)
- [Theseus](https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/IIIF2Collection.json)



A single manifest can represent anything from a lone photograph to a 1,400-page illustrated *Shahnameh*. Mastering these viewers takes a little practice but offers an excellent experience.

#### 4. Programming Access
Developers can work directly with the raw data files. All collections and manifests are available as:
- **JSON** files (IIIF standard)
- **Turtle** files (RDF/OWL ontology)

Using languages such as **Python**, **JavaScript/Node.js**, or any RDF-compatible library, programmers can parse, analyze, transform, or integrate the data into custom applications, scripts, or research tools.

---

This version is clearer, more professional, better organized, and easier to read while preserving all your original meaning. It uses consistent formatting, bullet points, and bold text for better scannability.

Would you like me to adjust the tone, add more details, or integrate this section into the full README?


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
- **`mdhn:ResourceCanvas`** — Special class for dealing with the details of the folios of a manuscript specially when we have a composite folio with multiple element types.
- **`mdhn:ContentElement`** — Smallest possible unit of content in a folio such as Paintings, Text, Notes and cropped Figures. Each instance of a ContentElement class should be associated with a ResourceCanvas which means it logically belongs to that ResourceCamnvas.

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

![Ontology Model](/IIIFCollection/images/ontology_model.jpg)


## Folio and Content Decomposition using IIIF Canvas

A core innovation in **IIIFDexir** is the granular decomposition of manuscript folios leveraging the **IIIF Canvas** concept (IIIF Presentation API). Each folio is modeled as a Canvas, which serves as a spatial container for its visual and textual content. This is further broken down into multiple **content elements**—discrete, semantically rich units that enable precise annotation, querying, and interoperability.

### Key Aspects of the Feature
- **Folio-Level Canvas**: Represents the entire page/image as a high-resolution, zoomable unit. There is a coresponding relation between each DigitalResource and it's ResourceCanvases. 
- **Content Elements**: Sub-divisions within the Canvas(ResourceCanvas), each with a specific **elementType** such as:
  - `CroppedFigure` (Identified by `mdhn:CroppedFigure` for illustrations, miniatures, or iconographic details).
  - `LinguisticObject` (Identified by `mdhn:Calligraphy_Inscription` for text blocks, verses/bayts, inscriptions, or calligraphy).
- **Enrichment**: Every content element includes:
  - **Iconography tags** (drawing from Iconclass, AAT, or custom extensions).
  - **Subject headings** (Wikidata QIDs, AAT identifiers, LCSH, etc.).
  - Links to the broader ontology (`mdhn:` namespace), agents, episodes, and provenance.

This decomposition transforms static manuscript images into a **machine-actionable knowledge graph layer**, supporting advanced use cases like stemmatology, variant analysis in the Shahnameh, iconographic studies, and AI-driven discovery.

### Why This Feature is Critical
- **Precision & Granularity**: Moves beyond whole-manuscript or whole-folio metadata to atomic-level access (e.g., individual figures or poetic lines), essential for philological work on dispersed works like the *Shahnameh of Shah Tahmasp*.
- **Interoperability**: Aligns with **CIDOC-CRM**, **FRBRoo**, and Linked Open Data principles, facilitating reconciliation with Wikidata, Getty vocabularies, and other GLAM resources.
- **Reusability**: Enables on-the-fly curated manifests, Web Annotations, Content State API deep-linking, and RDF/OWL population for the Knowledge Graph.
- **Scholarly & Public Impact**: Supports researchers in tracing motifs, characters (e.g., Rostam), narrative episodes, and artistic styles while making heritage accessible to non-specialists via IIIF viewers.

### Examples from Shahname Shah Tahmasp Collection
See the blueprint in [`ShahnameShahTahmasbCollection.json`](https://github.com/MehranDHN/IIIFCollection/blob/master/IIIFCollection/ShahnameShahTahmasbCollection.json) and linked manifests (e.g., [Folio 77v](https://iiif.archive.org/iiif/3/shahnama-shah-tahmasp-77v/manifest.json)).

**Sample Structure (simplified excerpt style)**:
```json
{
                {
                    "label": {
                        "en": "AsCanvas"
                    },
                    "value": {
                        "en": [
                            {
                                "index": 0,
                                "mid": "shahnama-shah-tahmasp-77v",
                                "cid": "0001",
                                "label": "Mihrab Hears of Rudaba Folly",
                                "folio": "77v",
                                "canvas": "https://iiif.archive.org/iiif/shahnama-shah-tahmasp-77v/canvas",
                                "basse64": "ewogICAgImlkIjogImh0dHBzOi8vaWlpZi5hcmNoaXZlLm9yZy9paWlmL3NoYWhuYW1hLXNoYWgtdGFobWFzcC0yMHYvY2FudmFzIiwKICAgICJ0eXBlIjogIkNhbnZhcyIsCiAgICAicGFydE9mIjogWwogICAgICAgIHsKICAgICAgICAgICAgImlkIjogImh0dHBzOi8vaWlpZi5hcmNoaXZlLm9yZy9paWlmLzMvc2hhaG5hbWEtc2hhaC10YWhtYXNwLTIwdi9tYW5pZmVzdC5qc29uIiwKICAgICAgICAgICAgInR5cGUiOiAiTWFuaWZlc3QiCiAgICAgICAgfQogICAgXQp9",
                                "refers": [
                                    "mdhn:Mihrab",
                                    "mdhn:Rudaba",
                                    "mdhn:Sindukht"
                                ],
                                "croppedFigures": [
                                    {
                                        "elementType": "mdhn:Fragment_Cropped_Image",
                                        "elementLabel": "Mihrab cropped figure from f77v",
                                        "elementStyle": ["aat:500011001"],
                                        "croppedImage": "https://iiif.archive.org/image/iiif/3/shahnama-shah-tahmasp-77v%2FFolio77v.jpg/843,2340,286,706/full/0/default.jpg",
                                        "elementLOUD": [
                                            "mdhn:Mihrab"
                                        ]
                                    },
                                    {
                                        "elementType": "mdhn:Fragment_Cropped_Image",
                                        "elementLabel": "Sindukht cropped figure from f77v",
                                        "elementStyle": ["aat:500011001"],
                                        "croppedImage": "https://iiif.archive.org/image/iiif/3/shahnama-shah-tahmasp-77v%2FFolio77v.jpg/1082,2416,572,499/full/0/default.jpg",
                                        "elementLOUD": [
                                            "mdhn:Sindukht"
                                        ]
                                    }
                                ],
                                "linguisticElements": [
                                    {
                                        "elementType": "mdhn:Calligraphy_Inscription",
                                        "elementLabel": "Inscription1 in Fig77v Q:2:127",
                                        "croppedImage": "https://iiif.archive.org/image/iiif/3/shahnama-shah-tahmasp-77v%2FFolio77v.jpg/711,314,1077,129/max/0/default.jpg",
                                        "elementStyle": ["aat:300265532"],
                                        "elementFAText": "وَإِذْ يَرْفَعُ إِبْرَاهِيمُ الْقَوَاعِدَ مِنَ الْبَيْتِ وَإِسْمَاعِيلُ رَبَّنَا تَقَبَّلْ مِنَّا ۖ إِنَّكَ أَنْتَ السَّمِيعُ الْعَلِيمُ",
                                        "elementENText": "And when Abraham and Ishmael were raising the foundations of the House, they prayed, Our Lord, accept [this] from us. Indeed You are the All-Hearing, the All-Knowing.",
                                        "elementLOUD": [
                                            "mdhn:Quran"
                                        ]
                                    },
                                    {
                                        "elementType": "mdhn:Calligraphy_Inscription",
                                        "elementLabel": "Inscription3 in Fig77v",
                                        "croppedImage": "https://iiif.archive.org/image/iiif/3/shahnama-shah-tahmasp-77v%2FFolio77v.jpg/732,722,1049,155/max/0/default.jpg",
                                        "elementStyle": ["aat:300265532"],
                                        "elementFAText": "این صفحه که هست رشک خوبان طراز آراسته پیکری‌ست بیننده نواز گویا در رحمت است کز عالم فیض بر ناظر این کتاب می‌گردد باز",
                                        "elementENText": "This page which is the envy of the good, the graceful form of a body, the beholder seems to be in mercy, as if the world of grace is turning to the observer of this book.",
                                        "elementLOUD": [
                                            "mdhn:Tahmasp_Safavid_I"
                                        ]
                                    },
                                    {
                                        "elementType": "mdhn:Calligraphy_Inscription",
                                        "elementLabel": "Inscription5 in Fig77v",
                                        "croppedImage": "https://iiif.archive.org/image/iiif/3/shahnama-shah-tahmasp-77v%2FFolio77v.jpg/433,1932,222,306/max/0/default.jpg",
                                        "elementStyle": ["aat:300265532"],
                                        "elementFAText": "يا مفتح الابواب",
                                        "elementENText": "O Opener of Doors",
                                        "elementLOUD": [
                                            "mdhn:Tahmasp_Safavid_I"
                                        ]
                                    },
                                    {
                                        "elementType": "mdhn:Calligraphy_Inscription",
                                        "elementLabel": "Inscription6 in Fig77v",
                                        "croppedImage": "https://iiif.archive.org/image/iiif/3/shahnama-shah-tahmasp-77v%2FFolio77v.jpg/737,707,1044,177/full/0/default.jpg",
                                        "elementStyle": ["aat:300265532"],
                                        "elementFAText": "این صفحه که شد رشک پریخانه‌ی چین مانی نکشیده صورتی بهتر از این  خطش به خط پری رخان می‌ماند کاراسته باشد به هزاران آیین",
                                        "elementENText": "This page, which has become the envy of the Chinese fairy house, has not drawn a single line better than this, its lines resemble the lines of a flowing fairy, may it be useful for thousands of rituals.",
                                        "elementLOUD": [
                                            "mdhn:Tahmasp_Safavid_I"
                                        ]
                                    }
                                ],
                                "depicts": [
                                    "mdhn:ZalAndRudaba",
                                    "mdhn:Architectural_Structure",
                                    "mdhn:Turban",
                                    "mdhn:Robe",
                                    "mdhn:WineBowl",
                                    "mdhn:Flower",
                                    "mdhn:Tree",
                                    "mdhn:Blossom",
                                    "mdhn:Plant",
                                    "mdhn:Headgear",
                                    "mdhn:Persian_Architecture",
                                    "mdhn:Balcony",
                                    "mdhn:Iwan",
                                    "mdhn:Calligraphy_Inscription",
                                    "mdhn:Sea_River_Pool",
                                    "mdhn:Duck",
                                    "mdhn:Pool",
                                    "mdhn:Fountain",
                                    "mdhn:Fence",
                                    "mdhn:Cypress",
                                    "mdhn:AgriculturalAndFarming",
                                    "mdhn:Persian_Garden",
                                    "mdhn:headscarf"
                                ],
                                "canvasType": [
                                    "aat:300189604",
                                    "aat:500181051",
                                    "aat:300079783",
                                    "aat:500011012",
                                    "aat:500011002"
                                ],
                                "folioContains": [
                                    "HasText",
                                    "HasPainting"
                                ],
                                "scriptStyle": [
                                    "aat:300265532"
                                ]
                            }
                        ]
                    }
                },
```

![Sample from 77v](/IIIFCollection/images/77v.JPG)

This format appears in each record of IIIF Collections assiciated with a standard IIIF Manifest. This is a very effective way to create a data model that can be easily rendered as our Final RDF format. 
This feature exemplifies IIIFDexir’s commitment to **semantic depth** and positions the project as a scalable model for Persian/Iranian cultural heritage digitization. It directly supports your ontology-driven pipelines and community contributions.




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

[Folio 16v from Supplément persan 489](https://theseusviewer.org/?iiif-content=ewogICAgImlkIjogImh0dHBzOi8vZ2FsbGljYS5ibmYuZnIvaWlpZi9hcms6LzEyMTQ4L2J0djFiODQyMjk5NXQvY2FudmFzL2Y0NCIsCiAgICAidHlwZSI6ICJDYW52YXMiLAogICAgInBhcnRPZiI6IFsKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6ICJodHRwczovL2dhbGxpY2EuYm5mLmZyL2lpaWYvYXJrOi8xMjE0OC9idHYxYjg0MjI5OTV0L21hbmlmZXN0Lmpzb24iLAogICAgICAgICAgICAidHlwZSI6ICJNYW5pZmVzdCIKICAgICAgICB9CiAgICBdCn0=)



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

####  Query 14: List All Resource Canvases in a Specific Manuscript (e.g., Peck Shahnameh)

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?collection ?resource ?resLabel ?canvas ?label ?folio ?canvasUrl  ?idx
WHERE {
  ?resource a mdhn:DigitalResource ;
            rdfs:label ?resLabel ;
            mdhn:isInCollection ?collection;
            mdhn:hasCanvas ?canvas .
  ?canvas a mdhn:ResourceCanvas ;
          rdfs:label ?label ;
          mdhn:canvasIndex ?idx;
          mdhn:folioNo ?folio ;  
          mdhn:canvasUrl ?canvasUrl .  
  #FILTER(CONTAINS(?resLabel, "Peck Shahnamah"))
  FILTER(?resource=mdhn:72507ee3_850b_4ad6_9098_141257cb319f)
}
ORDER BY ?idx
LIMIT 50
```

####  Query 15: Resource Canvases with Their Content Elements (Broad Overview)

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?canvas ?canvasLabel  ?elementLabel ?depicts ?imgurl
WHERE {
  ?resource a mdhn:DigitalResource ;
            mdhn:hasCanvas ?canvas .
  ?canvas a mdhn:ResourceCanvas ;
          rdfs:label ?canvasLabel .
  ?canvas mdhn:hasCroppedDetails|mdhn:hasLinguisticElement ?element .
  ?element a ?elementType ;
           mdhn:croppedImageUR ?imgurl;
           rdfs:label ?elementLabel .
  OPTIONAL { ?element mdhn:elementDepicts ?depicts . }
}
LIMIT 100
```

####  Query 16: Selective Cropped Figures related to specific character (e.g `mdhn:Zahhak`) from a Specific Manuscripts (e.g `mdhn:ShahnameShahTahmasb` and `mdhn:SmallIlkhanidShahname`)

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?collection ?resource ?canvas ?canvasLabel ?resLabel ?figureLabel ?imgurl  ?depictedIconography ?agential
WHERE {
  ?resource a mdhn:DigitalResource ;
            rdfs:label ?resLabel ;
            mdhn:isInCollection ?collection;
            mdhn:hasCanvas ?canvas .
  ?canvas a mdhn:ResourceCanvas ;
          rdfs:label ?canvasLabel .
  ?canvas mdhn:hasCroppedDetails ?figure .
  ?figure a mdhn:CroppedFigure ;
          rdfs:label ?figureLabel;
          mdhn:croppedImageURL ?imgurl;
  OPTIONAL { ?figure mdhn:elementDepicts ?depictedIconography . }
  OPTIONAL {?figure mdhn:hasAgential ?agential}
  FILTER(?collection IN (mdhn:ShahnameShahTahmasb , mdhn:SmallIlkhanidShahname))
  FILTER(CONTAINS(?resLabel, "Zahhak"))
  #FILTER(?agential=mdhn:Zahhak)
}
ORDER BY ?canvasLabel
```

####  Query 17: Canvases with Cropped Patterns (Decorative/Ornamental Elements)

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX aat: <https://vocab.getty.edu/aat/>

SELECT ?canvas ?canvasLabel ?patternLabel ?croppedImage ?patternStyle
WHERE {
  ?canvas a mdhn:ResourceCanvas ;
          rdfs:label ?canvasLabel ;
          mdhn:hasCroppedDetails ?pattern .
  ?pattern a mdhn:CroppedPattern ;
           rdfs:label ?patternLabel ;
           mdhn:croppedImageURL ?croppedImage .
  OPTIONAL { ?pattern mdhn:elementHasSubject ?patternStyle . }
  # Example filter for specific manuscript or motif
  # FILTER(?patternLabel CONTAINS "cypress")
}
LIMIT 15
```

####  Query 18: Linguistic Elements on Canvases (Text/Verse Extraction)

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?canvas ?canvasLabel ?lingElement ?textContent ?elementdepicts ?croppedimgurl
WHERE {
  ?canvas a mdhn:ResourceCanvas ;
          rdfs:label ?canvasLabel ;
          mdhn:hasLinguisticElement ?lingElement .
  ?lingElement a mdhn:LinguisticElement ;
               mdhn:croppedImageUR ?croppedimgurl;
               rdfs:label ?textContent . 
  OPTIONAL { ?lingElement mdhn:elementDepicts ?elementdepicts . }  # adapt to your exact props
}
ORDER BY ?canvasLabel
```

####  Query 19: Combined: Canvases + Figures + Patterns for a Departed Collection (e.g., Haft Ow rang)

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?canvas ?label (COUNT(?figure) AS ?numFigures) (COUNT(?pattern) AS ?numPatterns)
WHERE {
  ?resource a mdhn:DigitalResource ;
            mdhn:partOf|mdhn:isInCollection ?collection .  # or departed collection link
  ?resource mdhn:hasCanvas ?canvas .
  ?canvas a mdhn:ResourceCanvas ;
          rdfs:label ?label .
  OPTIONAL { ?canvas mdhn:hasCroppedDetails ?figure . ?figure a mdhn:CroppedFigure . }
  OPTIONAL { ?canvas mdhn:hasCroppedDetails ?pattern . ?pattern a mdhn:CroppedPattern . }
  #FILTER(?resource=mdhn:72507ee3_850b_4ad6_9098_141257cb319f)
}
GROUP BY ?canvas ?label
HAVING (COUNT(?figure) > 0 || COUNT(?pattern) > 0)
ORDER BY DESC(?numFigures)
```

####  Query 20: Resource Canvases Depicting Specific Iconography (e.g., `Flaming Nimbus` or `Solomon and Queen of Sheba` as a Narrative Episode)

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?canvas ?figure ?imgurl ?canvasdepicts ?canvasLabel ?figureLabel ?episode ?depicted
WHERE {
  ?canvas a mdhn:ResourceCanvas ;
          rdfs:label ?canvasLabel ;
          mdhn:depicts ?canvasdepicts;
          mdhn:hasCroppedDetails ?figure .
  ?figure a mdhn:CroppedFigure ;
          rdfs:label ?figureLabel ;
          mdhn:croppedImageURL ?imgurl;
          mdhn:elementDepicts ?depicted .
  ?depicted rdfs:label ?episode .  # or link to NarrativeEpisode
  FILTER(?canvasdepicts IN (mdhn:Flaming_Nimbus, mdhn:Solomon_and_Queen_of_Sheba))
}
```

####  Query 21: Comprehensive View: Manuscript → Canvases → All Content Elements (with Types)

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?manuscriptLabel ?canvasLabel ?elementClass (COUNT(?element) AS ?count)
WHERE {
  ?manuscript a mdhn:DigitalResource ;
              rdfs:label ?manuscriptLabel ;
              mdhn:hasCanvas ?canvas .
  ?canvas a mdhn:ResourceCanvas ;
          rdfs:label ?canvasLabel .
  ?canvas ?hasProp ?element .  # hasCroppedDetails or hasLinguisticElement
  ?element a ?elementClass .
  FILTER(?hasProp = mdhn:hasCroppedDetails || ?hasProp = mdhn:hasLinguisticElement)
}
GROUP BY ?manuscriptLabel ?canvasLabel ?elementClass
ORDER BY ?manuscriptLabel ?canvasLabel
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


### Citation

If you use IIIFDexir in your research, please cite this project as follows:

```bibtex
@misc{mehran2026iiifdexir,
  author       = {Mehran DHN},
  title        = {IIIFDexir: Dynamic IIIF Collection for Persian Cultural Heritage},
  year         = {2026},
  publisher    = {GitHub},
  url          = {https://github.com/MehranDHN/IIIFCollection},
  note         = {Machine-readable IIIF-based Knowledge Graph of Persian Art and Cultural Heritage}
}
```

**APA Style:**
Mehran DHN. (June 2, 2025). *IIIFDexir: Dynamic IIIF Collection for Persian Cultural Heritage*. https://github.com/MehranDHN/IIIFCollection

---

### Acknowledgments

The development of IIIFDexir would not have been possible without the support of several remarkable tools and platforms that empowered this ambitious project.

**Special thanks to:**

- **Grok** (by xAI) — for continuous assistance in structuring, refining ideas, and improving the quality of documentation and code.
- **Claude** (by Anthropic) — for deep technical insights and valuable contributions during the ontology design and knowledge modeling phases.
- **NotebookLM** (by Google) — for helping organize vast amounts of research material and generating clear summaries.
- **Ontotext** — for providing powerful semantic technology, particularly **GraphDB Desktop**, which serves as the backbone for the Knowledge Graph component of this project.

This project stands as a testament to the fruitful collaboration between human vision and advanced artificial intelligence tools in the service of cultural heritage preservation.

---

