# IIIFDexir Project  

The IIIFDexir project is a dynamic catalog based on IIIF. It emphasizes several technical features:  

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

## Accessing the catalog  
You can access the catalog using any standard IIIF Viewer including Mirador 3.0 and yet better free instances of it hosted in the
<a href="https://iiif.biblissima.fr/mirador3/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/IIIF2Collection.json" target="_blank">Mirador in Biblissima</a>.
![Screenshot](https://pbs.twimg.com/media/GmPDuFSbwAAR8O0?format=jpg&name=small "IIIFDexir")

## Important Notes

I aim to keep the catalog healthy despite daily changes in its structure and contents. As it expands, I make necessary modifications for enrichment. The final goal is a machine-readable catalog to present statistics and analytical information. Some resources reference external sources via the "seeAlso" field, which needs parsing. It's crucial to associate resources with controlled vocabularies like Getty's AAT and TGN, and the Library of Congress's TGM and SH.

## Preparing KG 
Creating a Knowledge Graph from the IIIFDexir is straightforward. IIIF Collections and Manifests are in JSON-LD format, but we used the Turtle format to implement a simple ontology for Data visualizatio representation. The primary entities are ResourceCollection (IIIF Collection) and DigitalResource (IIIF Manifest), both represented by owl:Class.

## Ontology
```turtle
                    
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix so: <https://schema.org/> .
@prefix stardog: <tag:stardog:api:> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix : <http://api.stardog.com/> .
@prefix aat: <https://vocab.getty.edu/aat/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix mdhn: <http://example.com/mdhn/> .
@prefix wd: <https://www.wikidata.org/wiki/> .
@prefix tgm: <http://id.loc.gov/vovabulary/graphicMaterials/> .
@prefix tgn: <http://vocab.getty.edu/tgn/> .
@prefix fhkb: <http://www.example.com/genealogy.owl#> .
@prefix lcsh: <https://id.loc.gov/authorities/subjects/> .

mdhn:ResourceCollection a owl:Class ;
    rdfs:comment "A collection of IIIF resources that contain manifests and nested collections." ;
    rdfs:label "Resource Collection" .

mdhn:DigitalResource a owl:Class ;
    rdfs:comment "A IIIF manifest representing a digital resource such as a book, photograph, or video." ;
    rdfs:label "Digital Resource" .

mdhn:Creator a owl:Class ;
    rdfs:comment "An entity responsible for creating the digital resource." ;
    rdfs:label "Creator" .

mdhn:AATTerm a owl:Class ;
    rdfs:comment "Root Class for all AAT inherited concepts" ;
    rdfs:label "AATTerm";
     rdfs:subClassOf  mdhn:SubjectSource  .

mdhn:AATSubject a owl:Class ;
    rdfs:comment "Classes choosed as AAT subset for Subjects and it is used to associate AATs as Topical headings to the photographs" ;
    rdfs:label "AATSubject" ;
    rdfs:subClassOf mdhn:AATTerm .

mdhn:ScriptStyleType a owl:Class ;
    rdfs:comment "Classes choosed as a small AAT subset and it is used to determine the script style of all kinds of calligraphy resources." ;
    rdfs:label "Script Style Type" ;
    rdfs:subClassOf mdhn:AATTerm .

mdhn:ResourceType a owl:Class ;
    rdfs:comment "Classes choosed as a AAT subset and it is used as First Level Classification of all resources." ;
    rdfs:label "Resource Type" ;
    rdfs:subClassOf mdhn:AATTerm .

mdhn:DocumentGenre a owl:Class ;
    rdfs:comment "Classes choosed as a subset and it is used as Second Level classification of document resources." ;
    rdfs:label "Document Genre" ;
    rdfs:subClassOf mdhn:AATTerm .

mdhn:DepartedCollection a owl:Class ;
    rdfs:comment "The class for integrating departed folios as logical collection into a single virtual collection" ;
    rdfs:label "Departed Collection" .

mdhn:Publisher a owl:Class ;
    rdfs:comment "An entity responsible for publishing or making the resource available." ;
    rdfs:label "Publisher" .

mdhn:ICSubjectSource a owl:Class ;
    rdfs:comment "Iconography subjects source based on WikiData" ;
    rdfs:label "ICSubjectSource" .    

mdhn:CanvasType a owl:Class ;
    rdfs:comment "The type of canvas used within a IIIF manifest to represent a resource page or image." ;
    rdfs:label "Canvas Type" .

mdhn:LCTGMSubject a owl:Class ;
    rdfs:comment "Classes to associate Theasures Of Graphical Material subjects to the photographs" ;
    rdfs:label "LCTGMSubject" ;
    rdfs:subClassOf mdhn:SubjectSource .

mdhn:LCSHSubject a owl:Class ;
    rdfs:comment "Classes to associate LC Subject Headings to the photographs" ;
    rdfs:label "LCSHSubject" ;
    rdfs:subClassOf mdhn:SubjectSource .

mdhn:GettyTGN a owl:Class ;
    rdfs:comment "Getty TGN Class for Geographic Places" ;
    rdfs:label "GettyTGN" .

mdhn:AgentialInfo a owl:Class ;
    rdfs:comment "Agential info based on FHKB and references to wikidata when possible" ;
    rdfs:label "AgentialInfo" ;
    rdfs:subClassOf fhkb:Person .



mdhn:TemporalInfo a owl:Class ;
    rdfs:comment "First try to support temporal entity type" ;
    rdfs:label "TemporalInfo" .

mdhn:hasCreator a owl:ObjectProperty ;
    rdfs:comment "Links a DigitalResource to its creator." ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "has creator" ;
    rdfs:range mdhn:Creator .
mdhn:hasScriptStyleBroader a owl:ObjectProperty ;
    rdfs:comment "Associate an Script Style concept to its broader concept" ;
    rdfs:label "hasScriptStyleBroader" ;
    rdfs:domain mdhn:ScriptStyleType ;
    rdfs:range mdhn:ScriptStyleType .

mdhn:hasAATSubjectBroader a owl:ObjectProperty ;
    rdfs:comment "Associate an AAT Subject concept to its broader concept" ;
    rdfs:label "hasAATSubjectBroader" ;
    rdfs:domain mdhn:AATTerm ;
    rdfs:range mdhn:AATTerm .    
mdhn:hasDocumentGenre a owl:ObjectProperty ;
    rdfs:comment "Links a DigitalResource to its document gennre" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "has Document Genre" ;
    rdfs:range mdhn:DocumentGenre .

mdhn:genreUsedIn a owl:ObjectProperty ;
    rdfs:comment "Associates a genre to its associated resources" ;
    rdfs:domain mdhn:DocumentGenre ;
    rdfs:label "genre Used In" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasDocumentGenre .

mdhn:hasTemporal a owl:ObjectProperty ;
    rdfs:comment "Links a DigitalResource to Date that is just a year in YYYY formt" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "hasTemporal" ;
    rdfs:range mdhn:TemporalInfo .

mdhn:yearOfResourse a owl:ObjectProperty ;
    rdfs:comment "Associates a year to all resources that relates to it." ;
    rdfs:domain mdhn:TemporalInfo ;
    rdfs:label "yearOfResourse" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasTemporal .

mdhn:hasScriptStyle a owl:ObjectProperty ;
    rdfs:comment "Links a DigitalResource to its canvas type." ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "has Script Style" ;
    rdfs:range mdhn:ScriptStyleType .

mdhn:scriptStyleInstance a owl:ObjectProperty ;
    rdfs:comment "Links a specified script style type to its instance in a DigitalResource." ;
    rdfs:domain mdhn:ScriptStyleType ;
    rdfs:label "scriptStyleInstance" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasScriptStyle .

mdhn:hasCanvasType a owl:ObjectProperty ;
    rdfs:comment "Links a DigitalResource to its canvas type." ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "has canvas type" ;
    rdfs:range mdhn:CanvasType .

    
mdhn:resourcesOfCanvasType a owl:ObjectProperty ;
    rdfs:comment "Links a canvas to its associated resources." ;
    rdfs:domain mdhn:CanvasType ;
    rdfs:label "resources Of Canvas Type" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasCanvasType .

mdhn:hasICSubject a owl:ObjectProperty ;
    rdfs:comment "Links a Graphic subjects in DigitalResources to Iconography Subjects Resource" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "has Iconography" ;
    rdfs:range mdhn:ICSubjectSource . 

mdhn:iconographyUsedIn a owl:ObjectProperty ;
    rdfs:comment "Links a canvas to its iconography resources." ;
    rdfs:domain mdhn:ICSubjectSource ;
    rdfs:label "iconography Used In" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasICSubject .       

mdhn:ofType a owl:ObjectProperty ;
    rdfs:comment "Associates a DigitalResource with its resource type." ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "Of Type" ;
    rdfs:range mdhn:ResourceType .

mdhn:hasTypeInstance a owl:ObjectProperty ;
    rdfs:comment "Associates Resource Type to instances." ;
    rdfs:domain mdhn:ResourceType ;
    rdfs:label "has Type Instance" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:ofType .

mdhn:PublishedBy a owl:ObjectProperty ;
    rdfs:comment "Links a DigitalResource to its publisher." ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "Published By" ;
    rdfs:range mdhn:Publisher .

mdhn:hasUrl a owl:DatatypeProperty ;
    rdfs:comment "The URL of a ResourceCollection or DigitalResource." ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( mdhn:ResourceCollection mdhn:DigitalResource )
    ] ;
    rdfs:label "has URL" ;
    rdfs:range xsd:anyURI .

mdhn:icWikiDataURL a owl:DatatypeProperty ;
    rdfs:comment "URL Of Iconograpgy source in WikiData" ;
    rdfs:domain mdhn:ICSubjectSource ;
    rdfs:label "icWikiDataURL" ;
    rdfs:range xsd:anyURI  .

mdhn:agentialWikiData a owl:DatatypeProperty ;
    rdfs:comment "URL Of Agential source in WikiData" ;
    rdfs:domain mdhn:AgentialInfo;
    rdfs:label "agentialWikiData" ;
    rdfs:range xsd:anyURI  .    
    

mdhn:caption a owl:DatatypeProperty ;
    rdfs:comment "A human-readable label for a resource or collection." ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( mdhn:ResourceCollection mdhn:DigitalResource )
    ] ;
    rdfs:label "caption" ;
    rdfs:range xsd:string .

mdhn:canvasCount a owl:DatatypeProperty ;
    rdfs:comment "Number of canvases in each resource manifest." ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "Canvas Count" ;
    rdfs:range xsd:integer .

mdhn:folioHasDrawing a owl:DatatypeProperty ;
    rdfs:comment "Folio has Drawing?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "folioHasDrawing" ;
    rdfs:range xsd:boolean .

mdhn:folioHasTable a owl:DatatypeProperty ;
    rdfs:comment "Folio has Table?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "folioHasTable" ;
    rdfs:range xsd:boolean .

mdhn:folioIsCover a owl:DatatypeProperty ;
    rdfs:comment "Folio is cover?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "folioIsCover" ;
    rdfs:range xsd:boolean .

mdhn:folioIsColophon a owl:DatatypeProperty ;
    rdfs:comment "Folio is colophon?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "folioIsColophon" ;
    rdfs:range xsd:boolean .

mdhn:foliohasDiagram a owl:DatatypeProperty ;
    rdfs:comment "Folio has diagram?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "foliohasDiagram" ;
    rdfs:range xsd:boolean .

mdhn:folioIsOpening a owl:DatatypeProperty ;
    rdfs:comment "Folio is opening page?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "folioIsOpening" ;
    rdfs:range xsd:boolean .

mdhn:folioIsFlyLeaf a owl:DatatypeProperty ;
    rdfs:comment "Folio is flyleaf?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "folioIsFlyLeaf" ;
    rdfs:range xsd:boolean .

mdhn:isInCollection a owl:ObjectProperty ;
    rdfs:comment "Specify the immediate collection of the resource" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "is In Collection" ;
    rdfs:range mdhn:ResourceCollection .

mdhn:hasResource a owl:ObjectProperty ;
    rdfs:comment "Links a ResourceCollection to its DigitalResource." ;
    rdfs:domain mdhn:ResourceCollection ;
    rdfs:label "has resource" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:isInCollection .

mdhn:hasPublished a owl:ObjectProperty ;
    rdfs:comment "Links a publisher to DigitalResource." ;
    rdfs:domain mdhn:Publisher ;
    rdfs:label "has Published" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:PublishedBy .

mdhn:createResources a owl:ObjectProperty ;
    rdfs:comment "Links a Creator to DigitalResource." ;
    rdfs:domain mdhn:Creator ;
    rdfs:label "creat eResources" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasCreator .

mdhn:subCollectionOf a owl:ObjectProperty ;
    rdfs:comment "Links a subCollection to its parrent Collection." ;
    rdfs:domain mdhn:ResourceCollection ;
    rdfs:label "sub Collection Of" ;
    rdfs:range mdhn:ResourceCollection .

mdhn:parentCollectionOf a owl:ObjectProperty ;
    rdfs:comment "Associates a parent Collection to its subCollections." ;
    rdfs:domain mdhn:ResourceCollection ;
    rdfs:label "parent Collection Of" ;
    rdfs:range mdhn:ResourceCollection ;
    owl:inverseOf mdhn:subCollectionOf .

mdhn:partOf a owl:ObjectProperty ;
    rdfs:comment "Links a ResourceCollection to it's parent" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "part Of" ;
    rdfs:range mdhn:DepartedCollection .

mdhn:contains a owl:ObjectProperty ;
    rdfs:comment "Links a ResourceCollection to it's childs" ;
    rdfs:domain mdhn:DepartedCollection ;
    rdfs:label "contains" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:partOf .

mdhn:hasSubject a owl:ObjectProperty ;
    rdfs:comment "Resource associate to SubjectSource(AAT,LCSH,TGM) as headings" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "hasSubject" ;
    rdfs:range mdhn:SubjectSource .

mdhn:usedSubject a owl:ObjectProperty ;
    rdfs:comment "Indicates Resources that used this specified SubjectSource(AAT,LCSH,TGM)" ;
    rdfs:domain mdhn:SubjectSource ;
    rdfs:label "usedSubject" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasSubject .

mdhn:hasTGMBroader a owl:ObjectProperty ;
    rdfs:comment "Associate a LCTGM concept to its broader concept" ;
    rdfs:label "hasTGMBroader" ;
    rdfs:domain mdhn:LCTGMSubject ;
    rdfs:range mdhn:LCTGMSubject .

mdhn:hasTGMNarrower a owl:ObjectProperty ;
    rdfs:comment "Associate a LCTGM concept to its narrower concept" ;
    rdfs:label "hasTGMNarrower" ;
    owl:inverseOf mdhn:hasTGMBroader ;
    rdfs:domain mdhn:LCTGMSubject ;
    rdfs:range mdhn:LCTGMSubject .

mdhn:hasBroaderDocGenre a owl:ObjectProperty ;
    rdfs:comment "Associate a Document Genre  to its broader genre" ;
    rdfs:label "hasBroaderDocGenre" ;
    rdfs:domain mdhn:DocumentGenre ;
    rdfs:range mdhn:DocumentGenre .

mdhn:hasNarrowerGenre a owl:ObjectProperty ;
    rdfs:comment "Associate a Document Genre to its narrower genre" ;
    rdfs:label "hasNarrowerGenre" ;
    owl:inverseOf mdhn:hasBroaderDocGenre ;
    rdfs:domain mdhn:DocumentGenre ;
    rdfs:range mdhn:DocumentGenre .

mdhn:lcTGMURI a owl:DatatypeProperty ;
    rdfs:comment "The LCTGM URI is used in LC TGM" ;
    rdfs:domain mdhn:LCTGMSubject ;
    rdfs:label "lcTGMURI" ;
    rdfs:range xsd:string .

mdhn:hasTGNPlace a owl:ObjectProperty ;
    rdfs:comment "TGN entry associate the resource to Getty TGN" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "hasTGNPlace" ;
    rdfs:range mdhn:GettyTGN .

mdhn:usedTGN a owl:ObjectProperty ;
    rdfs:comment "Indicates Resources that used this specified TGN" ;
    rdfs:domain mdhn:GettyTGN ;
    rdfs:label "usedTGN" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasTGNPlace .

mdhn:gettyTGNURI a owl:DatatypeProperty ;
    rdfs:comment "The TGN URI is used in Getty AAT" ;
    rdfs:domain mdhn:GettyTGN ;
    rdfs:label "gettyTGNURI" ;
    rdfs:range xsd:string .

mdhn:hasTGNNarrower a owl:ObjectProperty ;
    rdfs:comment "Indicates broader concept of specified TGN" ;
    rdfs:label "hasTGNNarrower" ;
    owl:inverseOf mdhn:hasTGNBroader ;
    so:domainIncludes mdhn:GettyTGN ;
    so:rangeIncludes mdhn:GettyTGN .

mdhn:hasTGNBroader a owl:ObjectProperty ;
    rdfs:comment "Associate a TGN concept to its broader concept" ;
    rdfs:label "hasTGNBroader" ;
    rdfs:domain mdhn:GettyTGN ;
    rdfs:range mdhn:GettyTGN .

mdhn:hasAATBroader a owl:ObjectProperty ;
    rdfs:comment "Associate an AAT concept to its broader concept" ;
    rdfs:label "hasAATBroader" ;
    rdfs:domain mdhn:AATTerm ;
    rdfs:range mdhn:AATTerm .

mdhn:isGuideTerm a owl:DatatypeProperty ;
    rdfs:comment "Flag to indicate if the AAT term is a guide term" ;
    rdfs:domain mdhn:AATTerm ;
    rdfs:label "isGuideTerm" ;
    rdfs:range xsd:boolean .

mdhn:hasAgential a owl:ObjectProperty ;
    rdfs:comment "Indicates that resource has Agential info associated to a person" ;
    rdfs:label "hasAgential" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:range mdhn:AgentialInfo .

mdhn:hasRoleInResource a owl:ObjectProperty ;
    rdfs:comment "Indicates a person has atleast one role in resource" ;
    rdfs:label "hasRoleInResource" ;
    owl:inverseOf mdhn:hasAgential ;
    rdfs:domain mdhn:AgentialInfo ;
    rdfs:range mdhn:DigitalResource .


mdhn:SubjectSource a owl:Class ;
    rdfs:comment "Root class of all Subject Sources" ;
    rdfs:label "SubjectSource" .


fhkb:DomainEntity a owl:Class .

fhkb:Man a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( fhkb:Person [ a owl:Restriction ;
                        owl:onProperty fhkb:hasSex ;
                        owl:someValuesFrom fhkb:Male ] ) ] .

fhkb:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( fhkb:Person [ a owl:Restriction ;
                        owl:onProperty fhkb:hasSex ;
                        owl:someValuesFrom fhkb:Female ] ) ] .

fhkb:Person a owl:Class ;
    rdfs:subClassOf 
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

fhkb:Marriage a owl:Class ;
    rdfs:subClassOf fhkb:DomainEntity .

fhkb:Male a owl:Class ;
    rdfs:subClassOf fhkb:Sex .

fhkb:Female a owl:Class ;
    rdfs:subClassOf fhkb:Sex ;
    owl:disjointWith fhkb:Male .

fhkb:Sex a owl:Class ;
    rdfs:subClassOf fhkb:DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Female fhkb:Male ) ] .

fhkb:Ancestor a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( fhkb:Person [ a owl:Restriction ;
                        owl:onProperty fhkb:isAncestorOf ;
                        owl:someValuesFrom fhkb:Person ] ) ] .

fhkb:hasFemalePartner a owl:ObjectProperty ;
    rdfs:range fhkb:Woman ;
    rdfs:domain fhkb:Marriage ;
    rdfs:subPropertyOf fhkb:hasPartner ;
    owl:inverseOf fhkb:isFemalePartnerIn .

fhkb:hasMalePartner a owl:ObjectProperty ;
    rdfs:range fhkb:Man ;
    rdfs:domain fhkb:Marriage ;
    rdfs:subPropertyOf fhkb:hasPartner ;
    owl:inverseOf fhkb:isMalePartnerIn .

fhkb:isFatherOf a owl:ObjectProperty .

fhkb:isMotherOf a owl:ObjectProperty .

fhkb:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain fhkb:Man ;
    rdfs:range fhkb:Person ;
    rdfs:subPropertyOf fhkb:isSiblingOf .

fhkb:isSisterOf a owl:ObjectProperty ;
    rdfs:domain fhkb:Woman ;
    rdfs:range fhkb:Person ;
    rdfs:subPropertyOf fhkb:isSiblingOf .

fhkb:hasHusband a owl:ObjectProperty ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasSpouse ;
    owl:propertyChainAxiom ( fhkb:isFemalePartnerIn fhkb:hasMalePartner ) .

fhkb:hasWife a owl:ObjectProperty ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasSpouse ;
    owl:propertyChainAxiom ( fhkb:isMalePartnerIn fhkb:hasFemalePartner ) .

fhkb:isHusbandOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasHusband .

fhkb:isWifeOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasWife .

fhkb:isPartnerIn a owl:ObjectProperty .

fhkb:hasPartner a owl:ObjectProperty ;
    rdfs:domain fhkb:Marriage ;
    rdfs:range fhkb:Person ;
    owl:inverseOf fhkb:isPartnerIn .

fhkb:isSpouseOf a owl:ObjectProperty .

fhkb:hasSpouse a owl:ObjectProperty ;
    owl:inverseOf fhkb:isSpouseOf .

fhkb:isFemalePartnerIn a owl:ObjectProperty .

fhkb:isMalePartnerIn a owl:ObjectProperty .

fhkb:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:subPropertyOf fhkb:isBloodrelationOf ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:isParentOf ) .

fhkb:hasChild a owl:ObjectProperty .

fhkb:isChildOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasChild .

fhkb:hasDaughter a owl:ObjectProperty ;
    rdfs:subPropertyOf fhkb:hasChild .

fhkb:hasSon a owl:ObjectProperty ;
    rdfs:subPropertyOf fhkb:hasChild .

fhkb:isDaughterOf a owl:ObjectProperty ;
    rdfs:subPropertyOf fhkb:isChildOf ;
    owl:inverseOf fhkb:hasDaughter .

fhkb:isSonOf a owl:ObjectProperty ;
    rdfs:subPropertyOf fhkb:isChildOf ;
    owl:inverseOf fhkb:hasSon .

fhkb:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isFatherOf .

fhkb:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isMotherOf .

fhkb:hasParent a owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person ;
    rdfs:subPropertyOf fhkb:hasAncestor ;
    owl:equivalentProperty fhkb:isChildOf ;
    owl:inverseOf fhkb:isParentOf .

fhkb:isParentOf a owl:ObjectProperty .

fhkb:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Sex .

fhkb:isAncestorOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasAncestor .

fhkb:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person .

fhkb:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:subPropertyOf fhkb:hasRelation .

fhkb:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:subPropertyOf fhkb:hasRelation .

fhkb:hasUncle a owl:ObjectProperty ;
    owl:inverseOf fhkb:isUncleOf .

fhkb:isUncleOf a owl:ObjectProperty ;
    rdfs:domain fhkb:Man ;
    rdfs:range fhkb:Person ;
    owl:propertyChainAxiom ( fhkb:isBrotherOf fhkb:isParentOf ) .

fhkb:hasGreatUncle a owl:ObjectProperty ;
    owl:inverseOf fhkb:isGreatUncleOf .

fhkb:isGreatUncleOf a owl:ObjectProperty ;
    rdfs:domain fhkb:Man ;
    rdfs:range fhkb:Person ;
    owl:propertyChainAxiom ( fhkb:isBrotherOf fhkb:isGrandParentOf ) .

fhkb:hasAunt a owl:ObjectProperty ;
    owl:inverseOf fhkb:isAuntOf .

fhkb:isAuntOf a owl:ObjectProperty ;
    rdfs:domain fhkb:Woman ;
    rdfs:range fhkb:Person ;
    owl:propertyChainAxiom ( fhkb:isSisterOf fhkb:isParentOf ) .

fhkb:hasGreatAunt a owl:ObjectProperty ;
    owl:inverseOf fhkb:isGreatAuntOf .

fhkb:isGreatAuntOf a owl:ObjectProperty ;
    rdfs:domain fhkb:Woman ;
    rdfs:range fhkb:Person ;
    owl:propertyChainAxiom ( fhkb:isSisterOf fhkb:isGrandParentOf ) .

fhkb:isCousinOf a owl:ObjectProperty ;
    rdfs:subPropertyOf fhkb:isBloodrelationOf .

fhkb:isFirstCousinOf a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:subPropertyOf fhkb:isCousinOf ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:isSiblingOf fhkb:isParentOf ) .

fhkb:isSecondCousinOf a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:subPropertyOf fhkb:isCousinOf ;
    owl:propertyChainAxiom ( fhkb:hasGrandParent fhkb:isSiblingOf fhkb:isGrandParentOf ) .

fhkb:isThirdCousinOf a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:subPropertyOf fhkb:isCousinOf ;
    owl:propertyChainAxiom ( fhkb:hasGreatGrandParent fhkb:isSiblingOf fhkb:isGreatGrandParentOf ) .

fhkb:isGrandfatherOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasGrandfather .

fhkb:isGrandmotherOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasGrandmother .

fhkb:isGrandParentOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasGrandParent .

fhkb:hasGrandfather a owl:ObjectProperty ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasGrandParent ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:hasFather ) .

fhkb:hasGrandmother a owl:ObjectProperty ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasGrandParent ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:hasMother ) .

fhkb:hasGrandParent a owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person ;
    rdfs:subPropertyOf fhkb:hasAncestor ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:hasParent ) .

fhkb:isGreatGrandfatherOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasGreatGrandfather .

fhkb:isGreatGrandmotherOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasGreatGrandmother .

fhkb:isGreatGrandParentOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasGreatGrandParent .

fhkb:hasGreatGrandfather a owl:ObjectProperty ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasGreatGrandParent ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:hasGrandfather ) .

fhkb:hasGreatGrandmother a owl:ObjectProperty ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasGreatGrandParent ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:hasGrandmother ) .

fhkb:hasGreatGrandParent a owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person ;
    rdfs:subPropertyOf fhkb:hasAncestor ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:hasParent fhkb:hasParent ) .    

```
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

## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MehranDHN/IIIFCollection.git
   ```

2. **Explore the Collection**:
   - Open the collection in a IIIF viewer like Mirador.
   - Inspect JSON-LD files for manifests and collections.

3. **Work with the Ontology**:
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
