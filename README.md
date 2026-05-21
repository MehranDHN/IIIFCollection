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

## Subset of AAT concepts used in IIIFDexir
AAT has a hierarchical structure with 7 Facets as root many sub Branches related to Art and Architecture which has very critical role in IIIFDexir.
Below is a subset of AAT collection with limited scope suitable for use in IIIFDexir:

```mermaid

flowchart TB
  classDef normal fill:#f2f2f2,stroke:#888,stroke-width:1px;
  classDef guideTerm fill:#fff2ac,stroke:#b88f00,stroke-width:1px;
  classDef extendedScope fill:#cfe2f3,stroke:#3b75a7,stroke-width:1px;
  classDef both fill:#f4cccc,stroke:#a33b3b,stroke-width:1px;
  aat300027268["administrative reports\n(aat300027268)"]
  class aat300027268 normal
  aat300027294["communiques\n(aat300027294)"]
  class aat300027294 normal
  aat300027297["plans (reports)\n(aat300027297)"]
  class aat300027297 normal
  aat300027316["proceedings (reports)\n(aat300027316)"]
  class aat300027316 normal
  aat300027323["technical reports\n(aat300027323)"]
  class aat300027323 normal
  aat300027267["Reports, Journals and Documents\n(aat300027267)"]
  class aat300027267 normal
  aat300026606["Book Catalogs\n(aat300026606)"]
  class aat300026606 normal
  aat300189604["Manuscript Folio\n(aat300189604)"]
  class aat300189604 normal
  aat300115833["leaves (gathered matter)\n(aat300115833)"]
  class aat300115833 normal
  aat300195125["blank leaves\n(aat300195125)"]
  class aat300195125 normal
  aat300168471["gathered matter components\n(aat300168471)"]
  class aat300168471 normal
  aat300201262["information form components\n(aat300201262)"]
  class aat300201262 normal
  aat300241584["<components by specific context>\n(aat300241584)"]
  class aat300241584 guideTerm
  aat300215389["Nwespapers and Magazines\n(aat300215389)"]
  class aat300215389 normal
  aat300026657["periodicals\n(aat300026657)"]
  class aat300026657 normal
  aat300026642["serials (publications)\n(aat300026642)"]
  class aat300026642 normal
  aat300111999["publications (documents)\n(aat300111999)"]
  class aat300111999 normal
  aat300026031["document genres\n(aat300026031)"]
  class aat300026031 normal
  aat300220520["<documents by conditions of production>\n(aat300220520)"]
  class aat300220520 guideTerm
  aat300137954["<documents by form>\n(aat300137954)"]
  class aat300137954 guideTerm
  aat300137955["<documents by function>\n(aat300137955)"]
  class aat300137955 guideTerm
  aat3300026877["correspondence\n(aat3300026877)"]
  class aat3300026877 normal
  aat300026878["<correspondence by internal form>\n(aat300026878)"]
  class aat300026878 guideTerm
  aat300026879["letters (correspondence)\n(aat300026879)"]
  class aat300026879 normal
  aat300026882["circular letters\n(aat300026882)"]
  class aat300026882 normal
  aat300026884["encyclicals\n(aat300026884)"]
  class aat300026884 normal
  aat300026886["papal encyclicals\n(aat300026886)"]
  class aat300026886 normal
  aat300026888["form letters\n(aat300026888)"]
  class aat300026888 normal
  aat300026890["letters of advice\n(aat300026890)"]
  class aat300026890 normal
  aat300026892["letters of intent\n(aat300026892)"]
  class aat300026892 normal
  aat300026896["letters of recommendation\n(aat300026896)"]
  class aat300026896 normal
  aat300026904["love letters\n(aat300026904)"]
  class aat300026904 normal
  aat300026916["business letters\n(aat300026916)"]
  class aat300026916 normal
  aat300026918["sales letters\n(aat300026918)"]
  class aat300026918 normal
  aat300374882["letters of introduction\n(aat300374882)"]
  class aat300374882 normal
  aat300375753["resignation letters\n(aat300375753)"]
  class aat300375753 normal
  aat300390947["nieuwjaarsbrieven\n(aat300390947)"]
  class aat300390947 normal
  aat300429849["referral letters\n(aat300429849)"]
  class aat300429849 normal
  aat300435276["letters of condolence\n(aat300435276)"]
  class aat300435276 normal
  aat300026685["records (documents)\n(aat300026685)"]
  class aat300026685 normal
  aat300026461["christening books\n(aat300026461)"]
  class aat300026461 normal
  aat300027146["merchandise inventories\n(aat300027146)"]
  class aat300027146 normal
  aat300027352["ships' papers\n(aat300027352)"]
  class aat300027352 normal
  aat300027765["<records by provenance>\n(aat300027765)"]
  class aat300027765 guideTerm
  aat300027772["corporation records\n(aat300027772)"]
  class aat300027772 normal
  aat300027777["government records\n(aat300027777)"]
  class aat300027777 normal
  aat300027787["<government records by function>\n(aat300027787)"]
  class aat300027787 guideTerm
  aat300027790["<executive records by provenance>\n(aat300027790)"]
  class aat300027790 guideTerm
  aat300027791["judicial executive records\n(aat300027791)"]
  class aat300027791 normal
  aat300027793["presidential papers\n(aat300027793)"]
  class aat300027793 normal
  aat300027795["<executive records by function>\n(aat300027795)"]
  class aat300027795 guideTerm
  aat300027804["customs records\n(aat300027804)"]
  class aat300027804 normal
  aat300027806["executive orders\n(aat300027806)"]
  class aat300027806 normal
  aat300027808["immigration records\n(aat300027808)"]
  class aat300027808 normal
  aat300027819["letters of marque\n(aat300027819)"]
  class aat300027819 normal
  aat300027820["letters patent\n(aat300027820)"]
  class aat300027820 normal
  aat300027821["lettres de cachet\n(aat300027821)"]
  class aat300027821 normal
  aat300027822["military records\n(aat300027822)"]
  class aat300027822 normal
  aat300027830["naturalization records\n(aat300027830)"]
  class aat300027830 normal
  aat300027831["pardons\n(aat300027831)"]
  class aat300027831 normal
  aat300027832["patents\n(aat300027832)"]
  class aat300027832 normal
  aat300027842["regulations (executive records)\n(aat300027842)"]
  class aat300027842 normal
  aat300027850["judicial records\n(aat300027850)"]
  class aat300027850 normal
  aat300027856["<judicial records by form or function>\n(aat300027856)"]
  class aat300027856 guideTerm
  aat300027857["decisions (judicial records)\n(aat300027857)"]
  class aat300027857 normal
  aat300027859["subpoenas\n(aat300027859)"]
  class aat300027859 normal
  aat300027860["summonses\n(aat300027860)"]
  class aat300027860 normal
  aat300027864["writs\n(aat300027864)"]
  class aat300027864 normal
  aat300027865["<judicial records by provenance>\n(aat300027865)"]
  class aat300027865 guideTerm
  aat300027866["civil court records\n(aat300027866)"]
  class aat300027866 normal
  aat300027883["criminal court records\n(aat300027883)"]
  class aat300027883 normal
  aat300027885["legislative records\n(aat300027885)"]
  class aat300027885 normal
  aat300027887["<legislative records by form or function>\n(aat300027887)"]
  class aat300027887 guideTerm
  aat300027888["bills (legislative records)\n(aat300027888)"]
  class aat300027888 normal
  aat300027889["legislative acts\n(aat300027889)"]
  class aat300027889 normal
  aat300027904["<legislative records by provenance>\n(aat300027904)"]
  class aat300027904 guideTerm
  aat300027905["congressional records\n(aat300027905)"]
  class aat300027905 normal
  aat300027915["parliamentary papers\n(aat300027915)"]
  class aat300027915 normal
  aat300027924["<government records by provenance>\n(aat300027924)"]
  class aat300027924 guideTerm
  aat300027928["county government records\n(aat300027928)"]
  class aat300027928 normal
  aat300027931["municipal government records\n(aat300027931)"]
  class aat300027931 normal
  aat300027937["intergovernmental records\n(aat300027937)"]
  class aat300027937 normal
  aat300027942["state government records\n(aat300027942)"]
  class aat300027942 normal
  aat300027945["national government records\n(aat300027945)"]
  class aat300027945 normal
  aat300027948["federal government records\n(aat300027948)"]
  class aat300027948 normal
  aat300027957["hospital records\n(aat300027957)"]
  class aat300027957 normal
  aat300027959["manorial records\n(aat300027959)"]
  class aat300027959 normal
  aat300027963["museum records\n(aat300027963)"]
  class aat300027963 normal
  aat300027967["church records\n(aat300027967)"]
  class aat300027967 normal
  aat300027969["<church records by form or function>\n(aat300027969)"]
  class aat300027969 guideTerm
  aat300027970["baptismal certificates\n(aat300027970)"]
  class aat300027970 normal
  aat300027972["church bulletins\n(aat300027972)"]
  class aat300027972 normal
  aat300027976["baptismal registers\n(aat300027976)"]
  class aat300027976 normal
  aat300027978["burial registers\n(aat300027978)"]
  class aat300027978 normal
  aat300027980["funeral registers\n(aat300027980)"]
  class aat300027980 normal
  aat300027984["<church records by provenance>\n(aat300027984)"]
  class aat300027984 guideTerm
  aat300027987["churchwardens' accounts\n(aat300027987)"]
  class aat300027987 normal
  aat300027992["diocesan records\n(aat300027992)"]
  class aat300027992 normal
  aat300027994["parochial records\n(aat300027994)"]
  class aat300027994 normal
  aat300027996["parish inventories\n(aat300027996)"]
  class aat300027996 normal
  aat300028004["school records\n(aat300028004)"]
  class aat300028004 normal
  aat300028009["curricula\n(aat300028009)"]
  class aat300028009 normal
  aat300028011["diplomas\n(aat300028011)"]
  class aat300028011 normal
  aat300028012["faculty papers\n(aat300028012)"]
  class aat300028012 normal
  aat300028014["grade books\n(aat300028014)"]
  class aat300028014 normal
  aat300028015["report cards\n(aat300028015)"]
  class aat300028015 normal
  aat300028026["syllabi\n(aat300028026)"]
  class aat300028026 normal
  aat300028028["theses\n(aat300028028)"]
  class aat300028028 normal
  aat300028029["dissertations\n(aat300028029)"]
  class aat300028029 normal
  aat300028037["personal papers\n(aat300028037)"]
  class aat300028037 normal
  aat300028040["family papers\n(aat300028040)"]
  class aat300028040 normal
  aat300028042["professional papers\n(aat300028042)"]
  class aat300028042 normal
  aat300048720["exhibition records\n(aat300048720)"]
  class aat300048720 normal
  aat300048722["exhibit scripts\n(aat300048722)"]
  class aat300048722 normal
  aat300077723["masters theses\n(aat300077723)"]
  class aat300077723 normal
  aat300113285["estate records\n(aat300113285)"]
  class aat300113285 normal
  aat300136842["official documents\n(aat300136842)"]
  class aat300136842 normal
  aat300136907["Bible records\n(aat300136907)"]
  class aat300136907 normal
  aat300141693["business records\n(aat300141693)"]
  class aat300141693 normal
  aat300152022["papal briefs\n(aat300152022)"]
  class aat300152022 normal
  aat300152044["bulls (papal records)\n(aat300152044)"]
  class aat300152044 normal
  aat300164785["notarial documents\n(aat300164785)"]
  class aat300164785 normal
  aat300165644["territorial records\n(aat300165644)"]
  class aat300165644 normal
  aat300172756["executive records\n(aat300172756)"]
  class aat300172756 normal
  aat300205940["rewards of merit\n(aat300205940)"]
  class aat300205940 normal
  aat300256158["certificates of registry (ships' papers)\n(aat300256158)"]
  class aat300256158 normal
  aat300262614["crew lists\n(aat300262614)"]
  class aat300262614 normal
  aat300262615["Mediterranean passports\n(aat300262615)"]
  class aat300262615 normal
  aat300262808["enrollments (ships' papers)\n(aat300262808)"]
  class aat300262808 normal
  aat300263224["portage bills\n(aat300263224)"]
  class aat300263224 normal
  aat300263287["sea letters\n(aat300263287)"]
  class aat300263287 normal
  aat300312067["artist files\n(aat300312067)"]
  class aat300312067 normal
  aat300312068["architect's files\n(aat300312068)"]
  class aat300312068 normal
  aat300312069["retail inventories\n(aat300312069)"]
  class aat300312069 normal
  aat300312070["warehouse lists\n(aat300312070)"]
  class aat300312070 normal
  aat300312071["public records\n(aat300312071)"]
  class aat300312071 normal
  aat300312072["court rolls\n(aat300312072)"]
  class aat300312072 normal
  aat300312073["vestry records\n(aat300312073)"]
  class aat300312073 normal
  aat300312074["wall labels\n(aat300312074)"]
  class aat300312074 normal
  aat300312076["doctoral dissertations\n(aat300312076)"]
  class aat300312076 normal
  aat300312077["term papers\n(aat300312077)"]
  class aat300312077 normal
  aat300391118["communion registers\n(aat300391118)"]
  class aat300391118 normal
  aat300417749["academic dissertations\n(aat300417749)"]
  class aat300417749 normal
  aat300423215["citizenship certificates\n(aat300423215)"]
  class aat300423215 normal
  aat300424217["customs declarations\n(aat300424217)"]
  class aat300424217 normal
  aat300427526["military discharges\n(aat300427526)"]
  class aat300427526 normal
  aat300427682["judgment\n(aat300427682)"]
  class aat300427682 normal
  aat300430850["probate\n(aat300430850)"]
  class aat300430850 normal
  aat300431840["service records\n(aat300431840)"]
  class aat300431840 normal
  aat300434150["surrender documents\n(aat300434150)"]
  class aat300434150 normal
  aat300434414["tax rolls\n(aat300434414)"]
  class aat300434414 normal
  aat300438423["<temporary alphabetical list: government records>\n(aat300438423)"]
  class aat300438423 guideTerm
  aat300455838["synagogue records\n(aat300455838)"]
  class aat300455838 normal
  aat300455839["mosque records\n(aat300455839)"]
  class aat300455839 normal
  aat300027424["<records by form or function>\n(aat300027424)"]
  class aat300027424 guideTerm
  aat300027590["legal documents\n(aat300027590)"]
  class aat300027590 normal
  aat300027384["traffic tickets\n(aat300027384)"]
  class aat300027384 normal
  aat300027536["bid bonds\n(aat300027536)"]
  class aat300027536 normal
  aat300027594["affidavits\n(aat300027594)"]
  class aat300027594 normal
  aat300027597["articles of incorporation\n(aat300027597)"]
  class aat300027597 normal
  aat300027603["bonds (legal records)\n(aat300027603)"]
  class aat300027603 normal
  aat300027604["bail bonds\n(aat300027604)"]
  class aat300027604 normal
  aat300027606["labor and material bonds\n(aat300027606)"]
  class aat300027606 normal
  aat300027610["payment bonds\n(aat300027610)"]
  class aat300027610 normal
  aat300027612["performance bonds\n(aat300027612)"]
  class aat300027612 normal
  aat300027614["subcontractor bonds\n(aat300027614)"]
  class aat300027614 normal
  aat300027616["surety bonds\n(aat300027616)"]
  class aat300027616 normal
  aat300027619["certificates of incorporation\n(aat300027619)"]
  class aat300027619 normal
  aat300027621["charters\n(aat300027621)"]
  class aat300027621 normal
  aat300027628["agreements\n(aat300027628)"]
  class aat300027628 normal
  aat300027630["collective labor agreements\n(aat300027630)"]
  class aat300027630 normal
  aat300027640["partnership agreements\n(aat300027640)"]
  class aat300027640 normal
  aat300027649["contracts\n(aat300027649)"]
  class aat300027649 normal
  aat300027650["<contracts by form or function>\n(aat300027650)"]
  class aat300027650 guideTerm
  aat300027651["divided contracts\n(aat300027651)"]
  class aat300027651 normal
  aat300027653["separate contracts\n(aat300027653)"]
  class aat300027653 normal
  aat300027655["single contracts\n(aat300027655)"]
  class aat300027655 normal
  aat300027657["subcontracts\n(aat300027657)"]
  class aat300027657 normal
  aat300027661["<contracts by party>\n(aat300027661)"]
  class aat300027661 guideTerm
  aat300027662["architect-consultant contracts\n(aat300027662)"]
  class aat300027662 normal
  aat300027664["government contracts\n(aat300027664)"]
  class aat300027664 normal
  aat300027668["<contracts by manner of payment>\n(aat300027668)"]
  class aat300027668 guideTerm
  aat300027673["cost plus fee agreements\n(aat300027673)"]
  class aat300027673 normal
  aat300027675["cost reimbursement contracts\n(aat300027675)"]
  class aat300027675 normal
  aat300027677["fixed-price contracts\n(aat300027677)"]
  class aat300027677 normal
  aat300027749["submittals\n(aat300027749)"]
  class aat300027749 normal
  aat300027751["escrows\n(aat300027751)"]
  class aat300027751 normal
  aat300027752["franchises\n(aat300027752)"]
  class aat300027752 normal
  aat300027753["indentures\n(aat300027753)"]
  class aat300027753 normal
  aat300027754["indictments (legal documents)\n(aat300027754)"]
  class aat300027754 normal
  aat300027755["leases\n(aat300027755)"]
  class aat300027755 normal
  aat300027761["powers of attorney\n(aat300027761)"]
  class aat300027761 normal
  aat300027762["syngraphai\n(aat300027762)"]
  class aat300027762 normal
  aat300027763["warranties\n(aat300027763)"]
  class aat300027763 normal
  aat300027764["wills\n(aat300027764)"]
  class aat300027764 normal
  aat300027954["international agreements\n(aat300027954)"]
  class aat300027954 normal
  aat300027956["treaties\n(aat300027956)"]
  class aat300027956 normal
  aat300055567["guarantees\n(aat300055567)"]
  class aat300055567 normal
  aat300109737["turnkey contracts\n(aat300109737)"]
  class aat300109737 normal
  aat300136911["articles of apprenticeship\n(aat300136911)"]
  class aat300136911 normal
  aat300163664["legal instruments\n(aat300163664)"]
  class aat300163664 normal
  aat300182873["ketubahs\n(aat300182873)"]
  class aat300182873 normal
  aat300263268["charter parties\n(aat300263268)"]
  class aat300263268 normal
  aat300048709["accession records\n(aat300048709)"]
  class aat300048709 normal
  aat300027425["administrative records\n(aat300027425)"]
  class aat300027425 normal
  aat300027426["agendas (administrative records)\n(aat300027426)"]
  class aat300027426 normal
  aat300027427["amendments (administrative records)\n(aat300027427)"]
  class aat300027427 normal
  aat300027428["ballots\n(aat300027428)"]
  class aat300027428 normal
  aat300312107["bills of mortality\n(aat300312107)"]
  class aat300312107 normal
  aat300379260["black books (general lists)\n(aat300379260)"]
  class aat300379260 normal
  aat300027433["bylaws (administrative records)\n(aat300027433)"]
  class aat300027433 normal
  aat300027437["constitutions\n(aat300027437)"]
  class aat300027437 normal
  aat300027440["minutes (administrative records)\n(aat300027440)"]
  class aat300027440 normal
  aat300027441["personnel records\n(aat300027441)"]
  class aat300027441 normal
  aat300027443["attendance records\n(aat300027443)"]
  class aat300027443 normal
  aat300027447["job applications\n(aat300027447)"]
  class aat300027447 normal
  aat300027451["résumés (personnel records)\n(aat300027451)"]
  class aat300027451 normal
  aat300027457["resolutions (administrative records)\n(aat300027457)"]
  class aat300027457 normal
  aat300027462["work-flow documents\n(aat300027462)"]
  class aat300027462 normal
  aat300027463["progress reports\n(aat300027463)"]
  class aat300027463 normal
  aat300027467["progress schedules\n(aat300027467)"]
  class aat300027467 normal
  aat300027471["project calendars\n(aat300027471)"]
  class aat300027471 normal
  aat300044839["election returns\n(aat300044839)"]
  class aat300044839 normal
  aat300135375["minute books\n(aat300135375)"]
  class aat300135375 normal
  aat300428739["packing slips\n(aat300428739)"]
  class aat300428739 normal
  aat300431221["record books\n(aat300431221)"]
  class aat300431221 normal
  aat300433311["work orders\n(aat300433311)"]
  class aat300433311 normal
  aat300249172["documentaries\n(aat300249172)"]
  class aat300249172 normal
  aat300375156["documentary film\n(aat300375156)"]
  class aat300375156 normal
  aat300435711["<temporary alphabetical list: document genres>\n(aat300435711)"]
  class aat300435711 guideTerm
  aat300421680["achievement symbols\n(aat300421680)"]
  class aat300421680 normal
  aat300420457["attendance certificates\n(aat300420457)"]
  class aat300420457 normal
  aat300420497["autograph cards\n(aat300420497)"]
  class aat300420497 normal
  aat300421302["business permits\n(aat300421302)"]
  class aat300421302 normal
  aat300423556["document covers\n(aat300423556)"]
  class aat300423556 normal
  aat300423557["document files\n(aat300423557)"]
  class aat300423557 normal
  aat300028052["cartographic materials\n(aat300028052)"]
  class aat300028052 normal
  aat300163674["graphic document genres\n(aat300163674)"]
  class aat300163674 normal
  aat300026848["charts (graphic documents)\n(aat300026848)"]
  class aat300026848 normal
  aat300417769["illustrated works (documents)\n(aat300417769)"]
  class aat300417769 normal
  aat300312062["polyglots\n(aat300312062)"]
  class aat300312062 normal
  aat300009700["motifs\n(aat300009700)"]
  class aat300009700 normal
  aat300009699["design elements (attributes)\n(aat300009699)"]
  class aat300009699 normal
  aat300123558["Design Elements (hierarchy name)\n(aat300123558)"]
  class aat300123558 normal
  aat300191091["<visual works by material or technique>\n(aat300191091)"]
  class aat300191091 guideTerm
  aat300266679["electronic documents\n(aat300266679)"]
  class aat300266679 normal
  aat300028094["Map\n(aat300028094)"]
  class aat300028094 normal
  aat300046300["Single Photograph\n(aat300046300)"]
  class aat300046300 normal
  aat300027200["Photograph Album\n(aat300027200)"]
  class aat300027200 normal
  aat300435424["MP4 Video\n(aat300435424)"]
  class aat300435424 normal
  aat300010094["Scrolls\n(aat300010094)"]
  class aat300010094 normal
  aat300041273["Engrave Print\n(aat300041273)"]
  class aat300041273 normal
  aat300266747["Audio Book\n(aat300266747)"]
  class aat300266747 normal
  aat300265483["Illuminated Manuscript\n(aat300265483)"]
  class aat300265483 normal
  aat300028569["Manuscript\n(aat300028569)"]
  class aat300028569 normal
  aat300417741["Painted leather bindings\n(aat300417741)"]
  class aat300417741 normal
  aat300191086["Visual Works\n(aat300191086)"]
  class aat300191086 normal
  aat300079783["Conceptual Drawings\n(aat300079783)"]
  class aat300079783 normal
  aat001100001["Qajar Style Drawings\n(aat001100001)"]
  class aat001100001 normal
  aat300034104["Architectural Plans\n(aat300034104)"]
  class aat300034104 normal
  aat300128366["Color Slide\n(aat300128366)"]
  class aat300128366 normal
  aat300015045["Watercolor (paint)\n(aat300015045)"]
  class aat300015045 normal
  aat300183946["water-base paint\n(aat300183946)"]
  class aat300183946 normal
  aat300015030["<paint by composition or origin>\n(aat300015030)"]
  class aat300015030 guideTerm
  aat300015029["paint (coating)\n(aat300015029)"]
  class aat300015029 normal
  aat300266660["Calligraphy\n(aat300266660)"]
  class aat300266660 normal
  aat300220539["illumination (image-making process)\n(aat300220539)"]
  class aat300220539 normal
  aat300054227["cinematography\n(aat300054227)"]
  class aat300054227 normal
  aat300054228["military photography\n(aat300054228)"]
  class aat300054228 normal
  aat300054229["journalistic photography\n(aat300054229)"]
  class aat300054229 normal
  aat300054230["travel photography\n(aat300054230)"]
  class aat300054230 normal
  aat300134506["astronomical photography\n(aat300134506)"]
  class aat300134506 normal
  aat300134547["documentary photography\n(aat300134547)"]
  class aat300134547 normal
  aat300134570["psychic photography\n(aat300134570)"]
  class aat300134570 normal
  aat300134607["spirit photography\n(aat300134607)"]
  class aat300134607 normal
  aat300135798["fashion photography\n(aat300135798)"]
  class aat300135798 normal
  aat300138239["nature photography\n(aat300138239)"]
  class aat300138239 normal
  aat300138800["scientific photography\n(aat300138800)"]
  class aat300138800 normal
  aat300138804["industrial photography\n(aat300138804)"]
  class aat300138804 normal
  aat300140969["commercial portraiture\n(aat300140969)"]
  class aat300140969 normal
  aat300157838["war photography\n(aat300157838)"]
  class aat300157838 normal
  aat300229951["stop-motion photography\n(aat300229951)"]
  class aat300229951 normal
  aat300256464["forensic photography\n(aat300256464)"]
  class aat300256464 normal
  aat300263896["videography\n(aat300263896)"]
  class aat300263896 normal
  aat300386099["social documentary photography\n(aat300386099)"]
  class aat300386099 normal
  aat300386812["digital photography (digital camera)\n(aat300386812)"]
  class aat300386812 normal
  aat300451604["portrait photography\n(aat300451604)"]
  class aat300451604 normal
  aat300247929["typewriting\n(aat300247929)"]
  class aat300247929 normal
  aat300252927["handwriting\n(aat300252927)"]
  class aat300252927 normal
  aat300263372["crophony\n(aat300263372)"]
  class aat300263372 normal
  aat300034698["<drawings by material or technique>\n(aat300034698)"]
  class aat300034698 guideTerm
  aat300034707["doodles\n(aat300034707)"]
  class aat300034707 normal
  aat300034727["renderings (drawings)\n(aat300034727)"]
  class aat300034727 normal
  aat300034736["tracings (drawings)\n(aat300034736)"]
  class aat300034736 normal
  aat300075467["thumbnail sketches\n(aat300075467)"]
  class aat300075467 normal
  aat300076598["computer drawings\n(aat300076598)"]
  class aat300076598 normal
  aat300076600["plots (computer drawings)\n(aat300076600)"]
  class aat300076600 normal
  aat300100184["blot drawings (drawings)\n(aat300100184)"]
  class aat300100184 normal
  aat300100186["freehand drawings (drawings)\n(aat300100186)"]
  class aat300100186 normal
  aat300100190["gesture drawings (drawings)\n(aat300100190)"]
  class aat300100190 normal
  aat300100194["line drawings (drawings)\n(aat300100194)"]
  class aat300100194 normal
  aat300100197["contour drawings (drawings)\n(aat300100197)"]
  class aat300100197 normal
  aat300100201["blind contour drawings (contour drawings)\n(aat300100201)"]
  class aat300100201 normal
  aat300100203["cross-contour drawings (line drawings)\n(aat300100203)"]
  class aat300100203 normal
  aat300100207["outline drawings\n(aat300100207)"]
  class aat300100207 normal
  aat300100209["mechanical drawings (tool-aided drawings)\n(aat300100209)"]
  class aat300100209 normal
  aat300100217["three-tone drawings\n(aat300100217)"]
  class aat300100217 normal
  aat300100222["tone drawings\n(aat300100222)"]
  class aat300100222 normal
  aat300182745["cadavres exquis\n(aat300182745)"]
  class aat300182745 normal
  aat300215301["wireframe drawings\n(aat300215301)"]
  class aat300215301 normal
  aat300263383["sandpaper paintings (visual works)\n(aat300263383)"]
  class aat300263383 normal
  aat300263511["animation cels\n(aat300263511)"]
  class aat300263511 normal
  aat300263512["animated cartoons\n(aat300263512)"]
  class aat300263512 normal
  aat300263513["animation drawings\n(aat300263513)"]
  class aat300263513 normal
  aat300263514["limited edition cels\n(aat300263514)"]
  class aat300263514 normal
  aat300263515["serigraph cels\n(aat300263515)"]
  class aat300263515 normal
  aat300263516["courvoisiers (animation cels)\n(aat300263516)"]
  class aat300263516 normal
  aat300263760["strikings (drawings)\n(aat300263760)"]
  class aat300263760 normal
  aat300264868["nitrate cels\n(aat300264868)"]
  class aat300264868 normal
  aat300265072["blotted line drawings (drawings)\n(aat300265072)"]
  class aat300265072 normal
  aat300265265["cel set-ups\n(aat300265265)"]
  class aat300265265 normal
  aat300265273["production cels\n(aat300265273)"]
  class aat300265273 normal
  aat300265519["ledger drawings\n(aat300265519)"]
  class aat300265519 normal
  aat300266092["typestracts\n(aat300266092)"]
  class aat300266092 normal
  aat300266198["Bézier curves\n(aat300266198)"]
  class aat300266198 normal
  aat300266219["pen and wash drawings\n(aat300266219)"]
  class aat300266219 normal
  aat300379919["calligraphic drawings\n(aat300379919)"]
  class aat300379919 normal
  aat300380567["silverpoint drawings\n(aat300380567)"]
  class aat300380567 normal
  aat300389868["chiaroscuro drawings\n(aat300389868)"]
  class aat300389868 normal
  aat300390908["charcoal drawings\n(aat300390908)"]
  class aat300390908 normal
  aat300395514["chalk drawings\n(aat300395514)"]
  class aat300395514 normal
  aat300404008["oil transfer drawings (visual works)\n(aat300404008)"]
  class aat300404008 normal
  aat300404635["metalpoint drawings\n(aat300404635)"]
  class aat300404635 normal
  aat300404676["pen and ink drawings\n(aat300404676)"]
  class aat300404676 normal
  aat300410334["pencil drawings\n(aat300410334)"]
  class aat300410334 normal
  aat300438620["wall drawings\n(aat300438620)"]
  class aat300438620 normal
  aat300033690["oil sketches\n(aat300033690)"]
  class aat300033690 normal
  aat300033706["finger paintings (visual works)\n(aat300033706)"]
  class aat300033706 normal
  aat300033799["oil paintings (visual works)\n(aat300033799)"]
  class aat300033799 normal
  aat300078925["watercolors (paintings)\n(aat300078925)"]
  class aat300078925 normal
  aat300078928["gouaches (paintings)\n(aat300078928)"]
  class aat300078928 normal
  aat300177433["frescoes (paintings)\n(aat300177433)"]
  class aat300177433 normal
  aat300181918["acrylic paintings (visual works)\n(aat300181918)"]
  class aat300181918 normal
  aat300181922["encaustic paintings (visual works)\n(aat300181922)"]
  class aat300181922 normal
  aat300249221["theorems (paintings)\n(aat300249221)"]
  class aat300249221 normal
  aat300264815["bark paintings\n(aat300264815)"]
  class aat300264815 normal
  aat300311289["sargas (visual works)\n(aat300311289)"]
  class aat300311289 normal
  aat300387661["fluorescent paintings (visual works)\n(aat300387661)"]
  class aat300387661 normal
  aat300389785["tempera paintings\n(aat300389785)"]
  class aat300389785 normal
  aat300404216["aquarelles (paintings)\n(aat300404216)"]
  class aat300404216 normal
  aat300404637["ink wash paintings\n(aat300404637)"]
  class aat300404637 normal
  aat300404675["ink resist paintings\n(aat300404675)"]
  class aat300404675 normal
  aat300404909["casein paintings (visual works)\n(aat300404909)"]
  class aat300404909 normal
  aat300410255["Tüchleins (visual works)\n(aat300410255)"]
  class aat300410255 normal
  aat300410350["canvas paintings\n(aat300410350)"]
  class aat300410350 normal
  aat300420005["hide paintings\n(aat300420005)"]
  class aat300420005 normal
  aat300420006["hide painters\n(aat300420006)"]
  class aat300420006 normal
  aat300033973["drawings (visual works)\n(aat300033973)"]
  class aat300033973 normal
  aat300054238["conservation (discipline)\n(aat300054238)"]
  class aat300054238 normal
  aat300229399["preventive conservation\n(aat300229399)"]
  class aat300229399 normal
  aat300379371["architectural conservation\n(aat300379371)"]
  class aat300379371 normal
  aat300379523["archaeological conservation\n(aat300379523)"]
  class aat300379523 normal
  aat300379590["ethnographic conservation\n(aat300379590)"]
  class aat300379590 normal
  aat300387441["sustainable conservation\n(aat300387441)"]
  class aat300387441 normal
  aat300197200["<containers by function or context>\n(aat300197200)"]
  class aat300197200 guideTerm
  aat300038879["Bible boxes\n(aat300038879)"]
  class aat300038879 normal
  aat300194529["ballot boxes\n(aat300194529)"]
  class aat300194529 normal
  aat300197578["document containers\n(aat300197578)"]
  class aat300197578 normal
  aat300197601["envelopes\n(aat300197601)"]
  class aat300197601 normal
  aat300197602["folders (containers)\n(aat300197602)"]
  class aat300197602 normal
  aat300198929["portfolios (containers)\n(aat300198929)"]
  class aat300198929 normal
  aat300200341["slipcases\n(aat300200341)"]
  class aat300200341 normal
  aat300215531["file boxes\n(aat300215531)"]
  class aat300215531 normal
  aat300215608["scrinia\n(aat300215608)"]
  class aat300215608 normal
  aat300247936["record covers\n(aat300247936)"]
  class aat300247936 normal
  aat300252990["loose-leaf binders\n(aat300252990)"]
  class aat300252990 normal
  aat300252997["ring binders\n(aat300252997)"]
  class aat300252997 normal
  aat300253008["post binders\n(aat300253008)"]
  class aat300253008 normal
  aat300261924["jewel cases\n(aat300261924)"]
  class aat300261924 normal
  aat300261961["Union cases\n(aat300261961)"]
  class aat300261961 normal
  aat300266823["picture sleeves\n(aat300266823)"]
  class aat300266823 normal
  aat300379901["letter racks\n(aat300379901)"]
  class aat300379901 normal
  aat300391034["map cases\n(aat300391034)"]
  class aat300391034 normal
  aat300420473["audio recording albums\n(aat300420473)"]
  class aat300420473 normal
  aat300420474["audio recording cases\n(aat300420474)"]
  class aat300420474 normal
  aat300420487["audiotape albums\n(aat300420487)"]
  class aat300420487 normal
  aat300420488["audiotape cases\n(aat300420488)"]
  class aat300420488 normal
  aat300420658["ballot bags\n(aat300420658)"]
  class aat300420658 normal
  aat300420661["ballot containers\n(aat300420661)"]
  class aat300420661 normal
  aat300423287["clip binders\n(aat300423287)"]
  class aat300423287 normal
  aat300423554["document cases\n(aat300423554)"]
  class aat300423554 normal
  aat300423559["document tubes\n(aat300423559)"]
  class aat300423559 normal
  aat300427711["jury wheels\n(aat300427711)"]
  class aat300427711 normal
  aat300429814["record cases\n(aat300429814)"]
  class aat300429814 normal
  aat300429821["record sleeves\n(aat300429821)"]
  class aat300429821 normal
  aat300431220["record albums\n(aat300431220)"]
  class aat300431220 normal
  aat300432172["shipping envelopes\n(aat300432172)"]
  class aat300432172 normal
  aat300435277["expanding files\n(aat300435277)"]
  class aat300435277 normal
  aat300435315["flat file folders\n(aat300435315)"]
  class aat300435315 normal
  aat300440770["sutra boxes\n(aat300440770)"]
  class aat300440770 normal
  aat300052758["telecommunication systems components\n(aat300052758)"]
  class aat300052758 normal
  aat300242031["system components\n(aat300242031)"]
  class aat300242031 normal
  aat300266535["telegraphs\n(aat300266535)"]
  class aat300266535 normal
  aat300028052_["aat300028052,\n(aat300028052,)"]
  class aat300028052_ normal
  aat300053159["aat300053159\n(aat300053159)"]
  class aat300053159 normal
  aat300054225["aat300054225\n(aat300054225)"]
  class aat300054225 normal
  aat300054698["aat300054698\n(aat300054698)"]
  class aat300054698 normal
  aat300054698_["aat300054698,\n(aat300054698,)"]
  class aat300054698_ normal
  aat300033701["aat300033701\n(aat300033701)"]
  class aat300033701 normal
  aat300054573["aat300054573\n(aat300054573)"]
  class aat300054573 normal
  aat300027267 --> aat300027268
  aat300027294 --> aat300027294
  aat300027267 --> aat300027297
  aat300027267 --> aat300027316
  aat300027267 --> aat300027323
  aat300137955 --> aat300027267
  aat300115833 --> aat300189604
  aat300168471 --> aat300115833
  aat300115833 --> aat300195125
  aat300201262 --> aat300168471
  aat300241584 --> aat300201262
  aat300026657 --> aat300215389
  aat300026642 --> aat300026657
  aat300111999 --> aat300026642
  aat300220520 --> aat300111999
  aat300026031 --> aat300220520
  aat300026031 --> aat300137954
  aat300026031 --> aat300137955
  aat300137955 --> aat3300026877
  aat3300026877 --> aat300026878
  aat300026878 --> aat300026879
  aat300026879 --> aat300026882
  aat300026882 --> aat300026884
  aat300026884 --> aat300026886
  aat300026879 --> aat300026888
  aat300026879 --> aat300026890
  aat300026879 --> aat300026892
  aat300026879 --> aat300026896
  aat300026879 --> aat300026904
  aat300026879 --> aat300026916
  aat300026879 --> aat300026918
  aat300026879 --> aat300374882
  aat300026879 --> aat300375753
  aat300026879 --> aat300390947
  aat300026879 --> aat300429849
  aat300026879 --> aat300435276
  aat300137955 --> aat300026685
  aat300027969 --> aat300026461
  aat300141693 --> aat300027146
  aat300027765 --> aat300027352
  aat300026685 --> aat300027765
  aat300027765 --> aat300027772
  aat300027765 --> aat300027777
  aat300027777 --> aat300027787
  aat300172756 --> aat300027790
  aat300027790 --> aat300027791
  aat300027790 --> aat300027793
  aat300172756 --> aat300027795
  aat300027795 --> aat300027804
  aat300027795 --> aat300027806
  aat300027795 --> aat300027808
  aat300027795 --> aat300027819
  aat300027795 --> aat300027820
  aat300027795 --> aat300027821
  aat300027795 --> aat300027822
  aat300027795 --> aat300027830
  aat300027795 --> aat300027831
  aat300027795 --> aat300027832
  aat300027795 --> aat300027842
  aat300027787 --> aat300027850
  aat300027850 --> aat300027856
  aat300027856 --> aat300027857
  aat300027856 --> aat300027859
  aat300027856 --> aat300027860
  aat300027856 --> aat300027864
  aat300027850 --> aat300027865
  aat300027865 --> aat300027866
  aat300027865 --> aat300027883
  aat300027787 --> aat300027885
  aat300027885 --> aat300027887
  aat300027887 --> aat300027888
  aat300027887 --> aat300027889
  aat300027885 --> aat300027904
  aat300027904 --> aat300027905
  aat300027904 --> aat300027915
  aat300027777 --> aat300027924
  aat300027924 --> aat300027928
  aat300027924 --> aat300027931
  aat300027924 --> aat300027937
  aat300027924 --> aat300027942
  aat300027924 --> aat300027945
  aat300027945 --> aat300027948
  aat300027765 --> aat300027957
  aat300027765 --> aat300027959
  aat300027765 --> aat300027963
  aat300027765 --> aat300027967
  aat300027967 --> aat300027969
  aat300027969 --> aat300027970
  aat300027969 --> aat300027972
  aat300027969 --> aat300027976
  aat300027969 --> aat300027978
  aat300027969 --> aat300027980
  aat300027967 --> aat300027984
  aat300027984 --> aat300027987
  aat300027984 --> aat300027992
  aat300027984 --> aat300027994
  aat300027994 --> aat300027996
  aat300027765 --> aat300028004
  aat300028004 --> aat300028009
  aat300028004 --> aat300028011
  aat300028004 --> aat300028012
  aat300028004 --> aat300028014
  aat300028004 --> aat300028015
  aat300028004 --> aat300028026
  aat300028004 --> aat300028028
  aat300028028 --> aat300028029
  aat300027765 --> aat300028037
  aat300028037 --> aat300028040
  aat300027765 --> aat300028042
  aat300027963 --> aat300048720
  aat300048720 --> aat300048722
  aat300028028 --> aat300077723
  aat300027765 --> aat300113285
  aat300027765 --> aat300136842
  aat300028040 --> aat300136907
  aat300027765 --> aat300141693
  aat300027969 --> aat300152022
  aat300027969 --> aat300152044
  aat300136842 --> aat300164785
  aat300027924 --> aat300165644
  aat300027787 --> aat300172756
  aat300028004 --> aat300205940
  aat300027352 --> aat300256158
  aat300027352 --> aat300262614
  aat300027352 --> aat300262615
  aat300027352 --> aat300262808
  aat300027352 --> aat300263224
  aat300027352 --> aat300263287
  aat300028042 --> aat300312067
  aat300028042 --> aat300312068
  aat300027146 --> aat300312069
  aat300027146 --> aat300312070
  aat300027777 --> aat300312071
  aat300027856 --> aat300312072
  aat300027984 --> aat300312073
  aat300048722 --> aat300312074
  aat300028029 --> aat300312076
  aat300028028 --> aat300312077
  aat300027969 --> aat300391118
  aat300028029 --> aat300417749
  aat300438423 --> aat300423215
  aat300438423 --> aat300424217
  aat300438423 --> aat300427526
  aat300438423 --> aat300427682
  aat300438423 --> aat300430850
  aat300027787 --> aat300431840
  aat300438423 --> aat300434150
  aat300438423 --> aat300434414
  aat300027777 --> aat300438423
  aat300027765 --> aat300455838
  aat300027765 --> aat300455839
  aat300026685 --> aat300027424
  aat300027424 --> aat300027590
  aat300163664 --> aat300027384
  aat300027603 --> aat300027536
  aat300163664 --> aat300027594
  aat300163664 --> aat300027597
  aat300163664 --> aat300027603
  aat300027603 --> aat300027604
  aat300027603 --> aat300027606
  aat300027603 --> aat300027610
  aat300027603 --> aat300027612
  aat300027612 --> aat300027614
  aat300027603 --> aat300027616
  aat300163664 --> aat300027619
  aat300163664 --> aat300027621
  aat300163664 --> aat300027628
  aat300027628 --> aat300027630
  aat300027628 --> aat300027640
  aat300027628 --> aat300027649
  aat300027649 --> aat300027650
  aat300027650 --> aat300027651
  aat300027650 --> aat300027653
  aat300027650 --> aat300027655
  aat300027650 --> aat300027657
  aat300027649 --> aat300027661
  aat300027661 --> aat300027662
  aat300027661 --> aat300027664
  aat300027649 --> aat300027668
  aat300027668 --> aat300027673
  aat300027668 --> aat300027675
  aat300027668 --> aat300027677
  aat300163664 --> aat300027749
  aat300163664 --> aat300027751
  aat300163664 --> aat300027752
  aat300163664 --> aat300027753
  aat300163664 --> aat300027754
  aat300027650 --> aat300027755
  aat300163664 --> aat300027761
  aat300027650 --> aat300027762
  aat300055567 --> aat300027763
  aat300163664 --> aat300027764
  aat300027628 --> aat300027954
  aat300027954 --> aat300027956
  aat300027628 --> aat300055567
  aat300027650 --> aat300109737
  aat300027753 --> aat300136911
  aat300027590 --> aat300163664
  aat300027661 --> aat300182873
  aat300027621 --> aat300263268
  aat300027424 --> aat300048709
  aat300027424 --> aat300027425
  aat300027425 --> aat300027426
  aat300027425 --> aat300027427
  aat300027425 --> aat300027428
  aat300027425 --> aat300312107
  aat300027425 --> aat300379260
  aat300027425 --> aat300027433
  aat300027425 --> aat300027437
  aat300027425 --> aat300027440
  aat300027425 --> aat300027441
  aat300027441 --> aat300027443
  aat300027441 --> aat300027447
  aat300027441 --> aat300027451
  aat300027425 --> aat300027457
  aat300027425 --> aat300027462
  aat300027462 --> aat300027463
  aat300027462 --> aat300027467
  aat300027462 --> aat300027471
  aat300027425 --> aat300044839
  aat300027425 --> aat300135375
  aat300027425 --> aat300428739
  aat300027425 --> aat300431221
  aat300027425 --> aat300433311
  aat300137955 --> aat300249172
  aat300249172 --> aat300375156
  aat300026031 --> aat300435711
  aat300435711 --> aat300421680
  aat300435711 --> aat300420457
  aat300435711 --> aat300420497
  aat300435711 --> aat300421302
  aat300435711 --> aat300423556
  aat300435711 --> aat300423557
  aat300163674 --> aat300028052
  aat300137954 --> aat300163674
  aat300163674 --> aat300026848
  aat300137954 --> aat300417769
  aat300137954 --> aat300312062
  aat300009699 --> aat300009700
  aat300123558 --> aat300009699
  aat300191086 --> aat300191091
  aat300137954 --> aat300266679
  aat300028052_ --> aat300028094
  aat300191091 --> aat300046300
  aat300009700 --> aat300010094
  aat300266679 --> aat300266747
  aat300028569 --> aat300265483
  aat300220520 --> aat300028569
  aat300079783 --> aat001100001
  aat300183946 --> aat300015045
  aat300015030 --> aat300183946
  aat300015029 --> aat300015030
  aat300191091 --> aat300266660
  aat300053159 --> aat300220539
  aat300054225 --> aat300054227
  aat300054225 --> aat300054228
  aat300054225 --> aat300054229
  aat300054225 --> aat300054230
  aat300054225 --> aat300134506
  aat300054225 --> aat300134547
  aat300054225 --> aat300134570
  aat300054225 --> aat300134607
  aat300054225 --> aat300135798
  aat300054225 --> aat300138239
  aat300054225 --> aat300138800
  aat300054225 --> aat300138804
  aat300054225 --> aat300140969
  aat300054225 --> aat300157838
  aat300054227 --> aat300229951
  aat300054225 --> aat300256464
  aat300054225 --> aat300263896
  aat300134547 --> aat300386099
  aat300054225 --> aat300386812
  aat300054225 --> aat300451604
  aat300054698 --> aat300247929
  aat300054698 --> aat300252927
  aat300054698_ --> aat300263372
  aat300033973 --> aat300034698
  aat300034698 --> aat300034707
  aat300034698 --> aat300034727
  aat300034698 --> aat300034736
  aat300034698 --> aat300075467
  aat300034698 --> aat300076598
  aat300076598 --> aat300076600
  aat300034698 --> aat300100184
  aat300034698 --> aat300100186
  aat300034698 --> aat300100190
  aat300034698 --> aat300100194
  aat300100194 --> aat300100197
  aat300100197 --> aat300100201
  aat300100194 --> aat300100203
  aat300100194 --> aat300100207
  aat300034698 --> aat300100209
  aat300034698 --> aat300100217
  aat300034698 --> aat300100222
  aat300034698 --> aat300182745
  aat300076598 --> aat300215301
  aat300034698 --> aat300263383
  aat300034698 --> aat300263511
  aat300034698 --> aat300263512
  aat300034698 --> aat300263513
  aat300263511 --> aat300263514
  aat300263511 --> aat300263515
  aat300263511 --> aat300263516
  aat300034698 --> aat300263760
  aat300263511 --> aat300264868
  aat300034698 --> aat300265072
  aat300263511 --> aat300265265
  aat300263511 --> aat300265273
  aat300034698 --> aat300265519
  aat300034698 --> aat300266092
  aat300076598 --> aat300266198
  aat300034698 --> aat300266219
  aat300034698 --> aat300379919
  aat300404635 --> aat300380567
  aat300034698 --> aat300389868
  aat300034698 --> aat300390908
  aat300034698 --> aat300395514
  aat300034698 --> aat300404008
  aat300034698 --> aat300404635
  aat300034698 --> aat300404676
  aat300034698 --> aat300410334
  aat300034698 --> aat300438620
  aat300033799 --> aat300033690
  aat300033701 --> aat300033706
  aat300033701 --> aat300033799
  aat300033701 --> aat300078925
  aat300078925 --> aat300078928
  aat300033701 --> aat300177433
  aat300033701 --> aat300181918
  aat300033701 --> aat300181922
  aat300033701 --> aat300249221
  aat300033701 --> aat300264815
  aat300033701 --> aat300311289
  aat300033701 --> aat300387661
  aat300033701 --> aat300389785
  aat300078925 --> aat300404216
  aat300033701 --> aat300404637
  aat300033701 --> aat300404675
  aat300033701 --> aat300404909
  aat300033701 --> aat300410255
  aat300033701 --> aat300410350
  aat300033701 --> aat300420005
  aat300033701 --> aat300420006
  aat300191091 --> aat300033973
  aat300054573 --> aat300054238
  aat300054238 --> aat300229399
  aat300054238 --> aat300379371
  aat300054238 --> aat300379523
  aat300054238 --> aat300379590
  aat300054238 --> aat300387441
  aat300197578 --> aat300038879
  aat300420661 --> aat300194529
  aat300197200 --> aat300197578
  aat300197578 --> aat300197601
  aat300197578 --> aat300197602
  aat300197578 --> aat300198929
  aat300197578 --> aat300200341
  aat300197578 --> aat300215531
  aat300197578 --> aat300215608
  aat300429821 --> aat300247936
  aat300197578 --> aat300252990
  aat300252990 --> aat300252997
  aat300252990 --> aat300253008
  aat300197578 --> aat300261924
  aat300197578 --> aat300261961
  aat300247936 --> aat300266823
  aat300197578 --> aat300379901
  aat300197578 --> aat300391034
  aat300420474 --> aat300420473
  aat300197578 --> aat300420474
  aat300420473 --> aat300420487
  aat300420474 --> aat300420488
  aat300420661 --> aat300420658
  aat300197578 --> aat300420661
  aat300252990 --> aat300423287
  aat300197578 --> aat300423554
  aat300423554 --> aat300423559
  aat300197578 --> aat300427711
  aat300420474 --> aat300429814
  aat300197578 --> aat300429821
  aat300420473 --> aat300431220
  aat300197601 --> aat300432172
  aat300197602 --> aat300435277
  aat300197602 --> aat300435315
  aat300197578 --> aat300440770
  aat300242031 --> aat300052758
  aat300241584 --> aat300242031
  aat300052758 --> aat300266535


```

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
