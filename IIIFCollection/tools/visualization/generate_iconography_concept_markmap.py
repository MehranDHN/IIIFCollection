#!/usr/bin/env python3
"""
Iconography concept neighbourhood → Markmap Markdown.

Concept-rooted counterpart of generate_iconography_concept_graph.py.
The original DOT generator is left unchanged.

A Graphviz neighbourhood is a graph. Markmap is a tree, so this report
picks the selected iconography concept(s) as the root and hangs every
association under them:

    selected concept
      identity (type, labels, Wikidata, comment)
      vocabulary alignments (SKOS → AAT / Iconclass / TGM broader chains)
      narrative episodes (charactersInvolved, isPartOf ancestry)
      collections → resources → canvases
        matching cropped content elements (IIIF thumbnails)
        co-occurring iconography tags and their SKOS
        narrative-episode tags on that canvas
      Depicts-only records (metadata Depicts, no AsCanvas / States)
        listed separately from AsCanvas canvases and from other metadata hits
      mdhn:saidToBeTheSameAs Wikidata / local identity equivalents (wd:Q… and WD:Q…)

Root recommendation
-------------------
Keep the root as the iconography concept in INPUT_CONCEPTS (for example
mdhn:Divs), not a collection or a canvas. Markmap has a single tree root;
a concept is the thing whose neighbourhood you want to inspect. Collections
and canvases then become evidence hanging from that concept. When the array
holds more than one concept, they become sibling H2 branches under a
synthetic document root.

Edit INPUT_CONCEPTS exactly as in generate_iconography_concept_graph.py.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, DefaultDict, Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import urlsplit, urlunsplit

# ================== CONFIGURATION ==================
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[1]
ONTOLOGY_DIR = ROOT_DIR / "Ontology"
OUTPUT_MARKMAP = SCRIPT_DIR / "iconography_concept_associations.markmap.md"

# Edit this list to choose the iconography concepts that should be included
# by default. Same contract as generate_iconography_concept_graph.py.
INPUT_CONCEPTS = [
    "mdhn:Divs"
    # "mdhn:Ascension_of_the_Prophet",
    # Add more concepts here.
]

ONTOLOGY_FILES: List[str] = [
    "iconography_RDF.ttl",
    "narrative_episodes.ttl",
    "PersonsRDFData.ttl",
    "iconclass_hierarchy.ttl",
    "aat_hierarchy.ttl",
    "ctl_vocabs.ttl",
    "LCTGM_RDF.ttl",
]

# Integer width used for the IIIF size segment: /{THUMBNAIL_WIDTH},/
THUMBNAIL_WIDTH: int = 250
# Default number of Markmap levels expanded in the generated document.
# 4 shows Collection → Resource; canvas / depicts stay collapsed until opened.
INITIAL_EXPAND_LEVEL: int = 4
# ===================================================

ConceptRec = Dict[str, Any]
SkosMap = Dict[str, Set[str]]

CONTENT_KEYS: List[str] = [
    "croppedFigures",
    "croppedPatterns",
    "linguisticElements",
    "ContentElement",
    "elements",
]
# Prefer painting crops for canvas thumbnails; skip text blocks and payload blobs.
THUMB_SOURCE_KEYS: List[str] = [
    "croppedFigures",
    "croppedPatterns",
    "ContentElement",
    "elements",
]
SKIP_THUMB_KEYS = {
    "linguisticElements",
    "basse64",
    "refers",
    "elementTextBlocks",
    "elementFAText",
    "elementENText",
}

SKOS_PREDICATES = (
    "skos:exactMatch",
    "skos:closeMatch",
    "skos:relatedMatch",
    "skos:broadMatch",
    "skos:narrowMatch",
    "skos:broader",
    "skos:narrower",
    "skos:related",
    "skos:relatedMath",  # known typo in some source records
)

SKOS_DISPLAY_ORDER = (
    "skos:exactMatch",
    "skos:closeMatch",
    "skos:relatedMatch",
    "skos:broadMatch",
    "skos:narrowMatch",
    "skos:broader",
    "skos:narrower",
    "skos:related",
    "skos:relatedMath",
)

IS_PART_OF = "mdhn:isPartOf"
CHARACTERS = "mdhn:charactersInvolved"
AAT_BROADER = "mdhn:hasAATBroader"
ICONCLASS_BROADER = "mdhn:hasIconclassBroader"
TGM_BROADER = "mdhn:hasTGMBroader"
WIKIDATA_PRED = "mdhn:icWikiDataURL"
SAID_SAME = "mdhn:saidToBeTheSameAs"
WD_CURIE_RE = re.compile(r"(?:wd|WD):Q(\d+)", re.IGNORECASE)

REGION_XYWH_RE = re.compile(
    r"^\d+(?:\.\d+)?,\d+(?:\.\d+)?,\d+(?:\.\d+)?,\d+(?:\.\d+)?$"
)
REGION_OK_RE = re.compile(r"^(?:full|square|pct:[0-9.,]+)$", re.IGNORECASE)
SIZE_OK_RE = re.compile(
    r"^(?:full|max|pct:[0-9.]+|!?[0-9.]*,[0-9.]*|\^[0-9.]+,)$",
    re.IGNORECASE,
)
ROTATION_OK_RE = re.compile(r"^[!]?\d+(?:\.\d+)?[!]?$")
QUALITY_OK_RE = re.compile(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9]+$")

SUBJECT_DECL_RE = re.compile(
    r"^((?:mdhn|iconclass|aat|tgm|wd|biblissima|lcsh):[A-Za-z0-9_./%-]+|<https?://[^>\s]+>)\s+a\b"
)
ONE_LINE_TRIPLE_RE = re.compile(
    r"^((?:mdhn|iconclass|aat|tgm|wd|biblissima|lcsh):[A-Za-z0-9_./%-]+|<https?://[^>\s]+>)\s+"
    r"(owl:sameAs|skos:[A-Za-z]+|rdfs:label|rdfs:comment|mdhn:[A-Za-z]+)\s+"
)
PRED_START_RE = re.compile(
    r"^(skos:[A-Za-z]+|rdfs:label|rdfs:comment|rdf:type|owl:sameAs|mdhn:[A-Za-z]+|a)\b"
)
LITERAL_RE = re.compile(r'"((?:\\.|[^"\\])*)"(?:@([A-Za-z-]+))?')
IRI_RE = re.compile(
    r"<https?://[^>\s]+>|[A-Za-z][A-Za-z0-9_-]*:[A-Za-z0-9_.:/%()'-]+"
)
QCODE_RE = re.compile(r"Q\d+", re.IGNORECASE)
MDHN_TERM_RE = re.compile(r"mdhn:[A-Za-z0-9_]+")
CURIE_OR_IRI_RE = re.compile(
    r"<https?://[^>\s]+>|[A-Za-z][A-Za-z0-9_-]*:[A-Za-z0-9_.:/%()'-]+"
)

ICONCLASS_IRI_RE = re.compile(
    r"^https?://(?:www\.)?iconclass\.org/(.+)$", re.IGNORECASE
)
AAT_IRI_RE = re.compile(
    r"^https?://vocab\.getty\.edu/aat/(\d+)$", re.IGNORECASE
)
TGM_IRI_RE = re.compile(
    r"^https?://id\.loc\.gov/vocabulary/graphicMaterials/(tgm\d+)$",
    re.IGNORECASE,
)
WD_IRI_RE = re.compile(
    r"^https?://(?:www\.)?wikidata\.org/(?:wiki|entity)/(Q\d+)$",
    re.IGNORECASE,
)

PREDICATE_ALIASES = {
    "mdhn:ispartOf": IS_PART_OF,
    "mdhn:isPartOf": IS_PART_OF,
    "mdhn:characterInvolved": CHARACTERS,
    "mdhn:charactersInvolved": CHARACTERS,
    "mdhn:isinExtendedScope": "mdhn:isInExtendedScope",
    "skos:relatedMath": "skos:relatedMatch",
}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def empty_concept() -> ConceptRec:
    return {
        "types": set(),
        "labels": {"en": [], "fa": [], "none": []},
        "comment": "",
        "skos": defaultdict(set),
        "isPartOf": set(),
        "charactersInvolved": set(),
        "hasAATBroader": set(),
        "hasIconclassBroader": set(),
        "hasTGMBroader": set(),
        "sameAs": set(),
        "saidToBeTheSameAs": set(),
        "wikidata": None,
        "iconclassNotation": None,
        "isGuideTerm": False,
        "isInExtendedScope": False,
        "lctgmURI": None,
        "source_files": set(),
    }


def ensure_concept(store: Dict[str, ConceptRec], term: str) -> ConceptRec:
    if term not in store:
        store[term] = empty_concept()
    return store[term]


def first_label(rec: Optional[ConceptRec], lang: str = "en") -> Optional[str]:
    if not rec:
        return None
    labels = rec.get("labels") or {}
    values = labels.get(lang) or []
    return values[0] if values else None


def display_labels(rec: Optional[ConceptRec]) -> str:
    if not rec:
        return ""
    en = first_label(rec, "en")
    fa = first_label(rec, "fa")
    if en and fa and fa != en:
        return f"{en} / {fa}"
    return en or fa or first_label(rec, "none") or ""


def concept_heading_text(term: str, store: Dict[str, ConceptRec]) -> str:
    labels = display_labels(store.get(term))
    return f"{term} — {labels}" if labels else term


def extract_qcode(raw: Any) -> Optional[str]:
    if raw is None:
        return None
    match = QCODE_RE.search(str(raw).strip())
    return match.group(0).upper() if match else None


def canonical_wd_term(raw: Any) -> Optional[str]:
    """Normalize WD:Q123 / wd:Q123 / Wikidata URL to wd:Q123."""
    if raw is None:
        return None
    text = str(raw).strip()
    if text.startswith("<") and text.endswith(">"):
        text = text[1:-1].strip()
    match = WD_CURIE_RE.search(text)
    if match:
        return f"wd:Q{match.group(1)}"
    wd = WD_IRI_RE.match(text)
    if wd:
        return f"wd:{wd.group(1).upper()}"
    return None


def find_wd_terms(text: str) -> List[str]:
    terms: List[str] = []
    seen: Set[str] = set()
    for match in WD_CURIE_RE.finditer(text):
        term = f"wd:Q{match.group(1)}"
        if term not in seen:
            seen.add(term)
            terms.append(term)
    for match in WD_IRI_RE.finditer(text):
        term = f"wd:{match.group(1).upper()}"
        if term not in seen:
            seen.add(term)
            terms.append(term)
    return terms


def normalize_iri(value: str) -> str:
    text = value.strip()
    if text.startswith("<") and text.endswith(">"):
        text = text[1:-1].strip()
    icon = ICONCLASS_IRI_RE.match(text)
    if icon:
        notation = icon.group(1).rstrip("/")
        return f"iconclass:{notation}"
    aat = AAT_IRI_RE.match(text)
    if aat:
        return f"mdhn:aat{aat.group(1)}"
    tgm = TGM_IRI_RE.match(text)
    if tgm:
        return f"mdhn:{tgm.group(1)}"
    wd = WD_IRI_RE.match(text)
    if wd:
        return f"wd:{wd.group(1).upper()}"
    return text


def alias_keys(term: str) -> List[str]:
    """Possible local identifiers for the same vocabulary term."""
    keys = [term]
    if term.startswith("iconclass:"):
        notation = term.split(":", 1)[1]
        keys.append(f"mdhn:iconclass{notation}")
        keys.append(f"mdhn:iconclass_{notation}")
    if term.startswith("mdhn:iconclass"):
        rest = term[len("mdhn:iconclass") :].lstrip("_")
        if rest:
            keys.append(f"iconclass:{rest}")
    if term.startswith("mdhn:tgm") and "_" not in term[8:]:
        keys.append(term)
    return list(dict.fromkeys(keys))


def resolve_term(term: str, store: Dict[str, ConceptRec], aliases: Dict[str, str]) -> str:
    if term in store:
        return term
    if term in aliases:
        return aliases[term]
    for key in alias_keys(term):
        if key in store:
            return key
        if key in aliases:
            return aliases[key]
    return term


def strip_turtle_comment(line: str) -> str:
    if line.startswith("#"):
        return ""
    in_string = False
    escaped = False
    out: List[str] = []
    for ch in line:
        if escaped:
            out.append(ch)
            escaped = False
            continue
        if ch == "\\":
            out.append(ch)
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
            out.append(ch)
            continue
        if ch == "#" and not in_string:
            break
        out.append(ch)
    return "".join(out).strip()


def unescape_literal(text: str) -> str:
    return (
        text.replace(r"\"", '"')
        .replace(r"\n", " ")
        .replace("\n", " ")
        .strip()
    )


def parse_objects(fragment: str) -> List[Tuple[str, str, Optional[str]]]:
    """Return (kind, value, lang) for IRIs and quoted literals in a predicate object list."""
    results: List[Tuple[str, str, Optional[str]]] = []
    for match in LITERAL_RE.finditer(fragment):
        results.append(("literal", unescape_literal(match.group(1)), match.group(2)))
    for match in IRI_RE.finditer(fragment):
        token = match.group(0)
        if token.startswith("skos:") or token in {"a", "rdf:type"}:
            continue
        results.append(("iri", normalize_iri(token), None))
    return results


def add_label(rec: ConceptRec, value: str, lang: Optional[str]) -> None:
    if not value:
        return
    bucket = (lang or "none").split("-")[0].lower()
    if bucket not in rec["labels"]:
        rec["labels"][bucket] = []
    if value not in rec["labels"][bucket]:
        rec["labels"][bucket].append(value)


def apply_predicate(
    rec: ConceptRec,
    predicate: str,
    objects: List[Tuple[str, str, Optional[str]]],
) -> None:
    predicate = PREDICATE_ALIASES.get(predicate, predicate)
    if predicate in {"a", "rdf:type"}:
        for kind, value, _lang in objects:
            if kind == "iri":
                rec["types"].add(value)
        return
    if predicate == "rdfs:label":
        for kind, value, lang in objects:
            if kind == "literal":
                add_label(rec, value, lang)
        return
    if predicate == "rdfs:comment":
        for kind, value, _lang in objects:
            if kind == "literal" and value and not rec["comment"]:
                rec["comment"] = value
        return
    if predicate.startswith("skos:"):
        canonical = PREDICATE_ALIASES.get(predicate, predicate)
        for kind, value, _lang in objects:
            if kind == "iri":
                rec["skos"][canonical].add(value)
        return
    if predicate == IS_PART_OF:
        for kind, value, _lang in objects:
            if kind == "iri":
                rec["isPartOf"].add(value)
        return
    if predicate == CHARACTERS:
        for kind, value, _lang in objects:
            if kind == "iri":
                rec["charactersInvolved"].add(value)
        return
    if predicate == AAT_BROADER:
        for kind, value, _lang in objects:
            if kind == "iri":
                rec["hasAATBroader"].add(value)
        return
    if predicate == ICONCLASS_BROADER:
        for kind, value, _lang in objects:
            if kind == "iri":
                rec["hasIconclassBroader"].add(value)
        return
    if predicate == TGM_BROADER:
        for kind, value, _lang in objects:
            if kind == "iri":
                rec["hasTGMBroader"].add(value)
        return
    if predicate == "owl:sameAs":
        for kind, value, _lang in objects:
            if kind == "iri":
                rec["sameAs"].add(value)
        return
    if predicate == SAID_SAME:
        for kind, value, _lang in objects:
            if kind != "iri" and kind != "literal":
                continue
            wd = canonical_wd_term(value)
            rec["saidToBeTheSameAs"].add(wd or value)
        return
    if predicate == WIKIDATA_PRED:
        for kind, value, _lang in objects:
            qcode = extract_qcode(value)
            if qcode:
                rec["wikidata"] = qcode
        return
    if predicate == "mdhn:iconclassNotation":
        for kind, value, _lang in objects:
            if kind == "literal" and value:
                rec["iconclassNotation"] = value
        return
    if predicate == "mdhn:isGuideTerm":
        rec["isGuideTerm"] = any(
            kind == "literal" and value.lower() == "true" for kind, value, _lang in objects
        )
        return
    if predicate == "mdhn:isInExtendedScope":
        rec["isInExtendedScope"] = any(
            kind == "literal" and value.lower() == "true" for kind, value, _lang in objects
        )
        return
    if predicate == "mdhn:lctgmURI":
        for kind, value, _lang in objects:
            rec["lctgmURI"] = value
            return


def parse_turtle_file(path: Path, store: Dict[str, ConceptRec]) -> None:
    if not path.exists():
        print(f"  warning: ontology file not found: {path}")
        return

    current: Optional[str] = None
    in_triple = False

    for raw in path.read_text(encoding="utf-8").splitlines():
        if in_triple:
            if '"""' in raw:
                in_triple = False
                after = raw.rsplit('"""', 1)[-1].strip()
                if after.endswith("."):
                    current = None
            continue

        line = strip_turtle_comment(raw)
        if not line or line.startswith("@prefix") or line.startswith("@base"):
            continue

        if '"""' in line and line.count('"""') == 1:
            in_triple = True
            declared = SUBJECT_DECL_RE.match(line)
            if declared:
                current = normalize_iri(declared.group(1))
                rec = ensure_concept(store, current)
                rec["source_files"].add(path.name)
                rest = line[declared.end() :].strip()
                if rest:
                    apply_line_predicates(rec, "a " + rest if not rest.startswith("a") else rest)
            continue

        declared = SUBJECT_DECL_RE.match(line)
        if declared:
            current = normalize_iri(declared.group(1))
            rec = ensure_concept(store, current)
            rec["source_files"].add(path.name)
            rest = line[declared.end() :].lstrip()
            apply_line_predicates(rec, "a " + rest if rest else "a")
        elif current is not None:
            apply_line_predicates(store[current], line)
        else:
            one_line = ONE_LINE_TRIPLE_RE.match(line)
            if one_line:
                current = normalize_iri(one_line.group(1))
                rec = ensure_concept(store, current)
                rec["source_files"].add(path.name)
                apply_line_predicates(rec, line[len(one_line.group(1)) :].strip())
                if line.endswith("."):
                    current = None
                continue

        if line.endswith("."):
            current = None


def apply_line_predicates(rec: ConceptRec, line: str) -> None:
    text = line.rstrip(".;, ").strip()
    if not text:
        return
    # A continuation may contain several predicates separated by `;`.
    parts = [p.strip() for p in re.split(r"\s*;\s*", text) if p.strip()]
    for part in parts:
        match = PRED_START_RE.match(part)
        if not match:
            continue
        predicate = match.group(1)
        fragment = part[match.end() :].strip()
        apply_predicate(rec, predicate, parse_objects(fragment))


def build_aliases(store: Dict[str, ConceptRec]) -> Dict[str, str]:
    aliases: Dict[str, str] = {}
    for term, rec in store.items():
        for other in rec["sameAs"]:
            aliases[other] = term
            aliases[term] = term
        for other in rec.get("saidToBeTheSameAs") or []:
            aliases.setdefault(other, term)
            wd = canonical_wd_term(other)
            if wd:
                aliases.setdefault(wd, term)
        if rec.get("wikidata"):
            aliases.setdefault(f"wd:{rec['wikidata']}", term)
        for key in alias_keys(term):
            aliases.setdefault(key, term)
        notation = rec.get("iconclassNotation")
        if notation:
            aliases[f"iconclass:{notation}"] = term
            aliases[f"mdhn:iconclass{notation}"] = term
    return aliases


def load_ontology() -> Tuple[Dict[str, ConceptRec], Dict[str, str]]:
    store: Dict[str, ConceptRec] = {}
    for filename in ONTOLOGY_FILES:
        path = ONTOLOGY_DIR / filename
        print(f"  loading {filename} ...")
        parse_turtle_file(path, store)
    aliases = build_aliases(store)
    return store, aliases


# ---------------------------------------------------------------------------
# IIIF thumbnails
# ---------------------------------------------------------------------------

def _iiif_path_segments(iiif_url: str) -> Optional[Tuple[Any, List[str]]]:
    if not iiif_url or not isinstance(iiif_url, str):
        return None
    iiif_url = iiif_url.strip()
    if iiif_url.startswith("<") and iiif_url.endswith(">"):
        iiif_url = iiif_url[1:-1].strip()
    parsed = urlsplit(iiif_url)
    if parsed.scheme not in {"http", "https"}:
        return None
    segs = parsed.path.split("/")
    if len(segs) < 4:
        return None
    region, size, rotation, quality = segs[-4], segs[-3], segs[-2], segs[-1]
    region_ok = bool(REGION_XYWH_RE.match(region) or REGION_OK_RE.match(region))
    if not (
        region_ok
        and SIZE_OK_RE.match(size)
        and ROTATION_OK_RE.match(rotation)
        and QUALITY_OK_RE.match(quality)
    ):
        return None
    return parsed, segs


def rewrite_iiif_size(
    iiif_url: str,
    width: int = THUMBNAIL_WIDTH,
    *,
    full_region: bool = False,
) -> Optional[str]:
    """Rewrite an IIIF Image API URL to /{width},/ (and optionally region /full/)."""
    if not iiif_url or not isinstance(iiif_url, str):
        return None
    iiif_url = iiif_url.strip()
    if iiif_url.startswith("<") and iiif_url.endswith(">"):
        iiif_url = iiif_url[1:-1].strip()
    parsed_segs = _iiif_path_segments(iiif_url)
    if parsed_segs is not None:
        parsed, segs = parsed_segs
        if full_region:
            segs[-4] = "full"
        segs[-3] = f"{width},"
        return urlunsplit(
            (parsed.scheme, parsed.netloc, "/".join(segs), parsed.query, parsed.fragment)
        )
    if "/full/" in iiif_url:
        return iiif_url.replace("/full/", f"/{width},/")
    if "/max/" in iiif_url:
        return iiif_url.replace("/max/", f"/{width},/")
    return None


def find_iiif_urls(node: Any, skip_keys: Optional[Set[str]] = None) -> List[str]:
    found: List[str] = []
    seen: Set[str] = set()
    skip_keys = skip_keys or set()

    def add(url: Optional[str]) -> None:
        if url and url not in seen:
            seen.add(url)
            found.append(url)

    def walk(value: Any) -> None:
        if isinstance(value, str):
            if _iiif_path_segments(value) is not None:
                add(value)
            return
        if isinstance(value, dict):
            for key in ("croppedImage", "image", "id", "@id"):
                candidate = value.get(key)
                if isinstance(candidate, str) and _iiif_path_segments(candidate) is not None:
                    add(candidate)
            thumb = value.get("thumbnail")
            if thumb is not None:
                walk(thumb)
            for key, nested in value.items():
                if key in skip_keys or key == "thumbnail" or key in (
                    "croppedImage",
                    "image",
                ):
                    continue
                walk(nested)
            return
        if isinstance(value, list):
            for item in value:
                walk(item)

    walk(node)
    return found


def thumbnail_for(
    node: Any,
    width: int = THUMBNAIL_WIDTH,
    *,
    full_region: bool = False,
    skip_keys: Optional[Set[str]] = None,
) -> Optional[str]:
    for url in find_iiif_urls(node, skip_keys=skip_keys):
        rewritten = rewrite_iiif_size(url, width, full_region=full_region)
        if rewritten:
            return rewritten
    return None


def canvas_thumbnail(canvas: Dict[str, Any], width: int = THUMBNAIL_WIDTH) -> Optional[str]:
    """Whole-folio thumb from a painting crop, not from linguisticElements."""
    for key in THUMB_SOURCE_KEYS:
        nested = canvas.get(key)
        if not nested:
            continue
        thumb = thumbnail_for(nested, width, full_region=True, skip_keys=SKIP_THUMB_KEYS)
        if thumb:
            return thumb
    return thumbnail_for(canvas, width, full_region=True, skip_keys=SKIP_THUMB_KEYS)


# ---------------------------------------------------------------------------
# JSON collection walking
# ---------------------------------------------------------------------------

def get_label_text(label: Any) -> str:
    if isinstance(label, str):
        return label
    if isinstance(label, dict):
        for key in ("en", "none", "fa"):
            if key in label and label[key]:
                val = label[key]
                return val[0] if isinstance(val, list) else str(val)
        for val in label.values():
            if isinstance(val, list) and val:
                return str(val[0])
            if isinstance(val, str) and val:
                return val
    if isinstance(label, list) and label:
        return get_label_text(label[0])
    return str(label) if label is not None else "Unnamed"


def metadata_label_key(value: Any) -> str:
    return get_label_text(value).strip().lower()


def is_states_or_ascanvas_label(value: Any) -> bool:
    key = metadata_label_key(value)
    return "states" in key or "ascanvas" in key


def is_depicts_field_label(value: Any) -> bool:
    """True for the resource-level Depicts metadata field, not AsCanvas.depicts."""
    return metadata_label_key(value) == "depicts"


def iter_resource_metadata(resource: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    metadata = resource.get("metadata") or []
    if isinstance(metadata, list):
        for meta in metadata:
            if isinstance(meta, dict):
                yield meta


def metadata_field_value(resource: Dict[str, Any], *names: str) -> Any:
    wanted = {name.lower() for name in names}
    for meta in iter_resource_metadata(resource):
        if metadata_label_key(meta.get("label")) in wanted:
            return meta.get("value")
    return None


def resource_unique_id(resource: Dict[str, Any]) -> str:
    for name in ("Unique ID", "UniqueID", "Shelfmark"):
        value = metadata_field_value(resource, name)
        if value is None:
            continue
        text = get_label_text(value).strip()
        if text:
            return text
    rid = str(resource.get("id") or resource.get("@id") or "").rstrip("/")
    return rid.split("/")[-1] if rid else ""


def extract_depicts_field_terms(metadata: Any) -> List[str]:
    """Terms from metadata labeled 'Depicts' (term list, not an AsCanvas object)."""
    terms: List[str] = []
    seen: Set[str] = set()
    if not isinstance(metadata, list):
        return terms
    for meta in metadata:
        if not isinstance(meta, dict) or not is_depicts_field_label(meta.get("label")):
            continue
        for term in find_all_terms(meta.get("value")):
            if term and term not in seen:
                seen.add(term)
                terms.append(term)
    return terms


def normalize_term(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, dict):
        for nested in value.values():
            term = normalize_term(nested)
            if term:
                return term
        return None
    if isinstance(value, list):
        for nested in value:
            term = normalize_term(nested)
            if term:
                return term
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.startswith("<") and text.endswith(">"):
        text = text[1:-1].strip()
    found = MDHN_TERM_RE.findall(text)
    if found:
        return found[0]
    wd = canonical_wd_term(text)
    if wd:
        return wd
    if re.match(r"^(iconclass|wd|aat|tgm|biblissima|lcsh):", text, re.IGNORECASE):
        return normalize_iri(text)
    return None


def find_all_terms(value: Any) -> List[str]:
    terms: List[str] = []
    if isinstance(value, dict):
        for nested in value.values():
            terms.extend(find_all_terms(nested))
    elif isinstance(value, list):
        for nested in value:
            terms.extend(find_all_terms(nested))
    elif isinstance(value, str):
        terms.extend(MDHN_TERM_RE.findall(value))
        terms.extend(find_wd_terms(value))
        for match in CURIE_OR_IRI_RE.findall(value):
            if match.startswith("mdhn:"):
                continue
            if match.lower().startswith("wd:"):
                continue
            if match.startswith(("iconclass:", "aat:", "tgm:", "biblissima:")):
                terms.append(normalize_iri(match))
    return terms


def extract_canvas_entries(metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    canvas_entries: List[Dict[str, Any]] = []
    for meta in metadata:
        if not isinstance(meta, dict):
            continue
        if not is_states_or_ascanvas_label(meta.get("label")):
            continue
        value = meta.get("value", {})
        raw_entries: Any = []
        if isinstance(value, dict):
            if "en" in value:
                raw_entries = value["en"]
            else:
                for candidate in value.values():
                    if (
                        isinstance(candidate, list)
                        and candidate
                        and isinstance(candidate[0], dict)
                        and any(
                            key in candidate[0]
                            for key in (
                                "depicts",
                                "folio",
                                "canvasType",
                                "croppedFigures",
                            )
                        )
                    ):
                        raw_entries = candidate
                        break
        elif isinstance(value, list):
            raw_entries = value
        if isinstance(raw_entries, dict):
            raw_entries = [raw_entries]
        if isinstance(raw_entries, list):
            for entry in raw_entries:
                if isinstance(entry, dict):
                    canvas_entries.append(entry)
    return canvas_entries


def iter_content_elements(node: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(node, dict):
        if any(
            key in node
            for key in ("elementLOUD", "croppedImage", "elementType", "elementLabel")
        ):
            yield node
        for key in CONTENT_KEYS + ["Element"]:
            nested = node.get(key)
            if nested is not None:
                yield from iter_content_elements(nested)
    elif isinstance(node, list):
        for item in node:
            yield from iter_content_elements(item)


def extract_depicts_terms(value: Any) -> List[str]:
    """Every mdhn: / wd: term from canvas-level 'depicts' arrays (nested)."""
    terms: List[str] = []
    seen: Set[str] = set()

    def add(term: Optional[str]) -> None:
        if term and term not in seen:
            seen.add(term)
            terms.append(term)

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if "depicts" in node:
                raw = node.get("depicts") or []
                if isinstance(raw, str):
                    raw = [raw]
                if isinstance(raw, list):
                    for item in raw:
                        add(normalize_term(item))
                        if isinstance(item, str):
                            for wd in find_wd_terms(item):
                                add(wd)
            for nested in node.values():
                walk(nested)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(value)
    return terms


def canvas_depicts(canvas: Dict[str, Any]) -> List[str]:
    return extract_depicts_terms(canvas)


def element_loud(elem: Dict[str, Any]) -> List[str]:
    raw = elem.get("elementLOUD") or elem.get("loud") or []
    if isinstance(raw, str):
        raw = [raw]
    terms: List[str] = []
    seen: Set[str] = set()
    for item in raw:
        term = normalize_term(item)
        if term and term not in seen:
            seen.add(term)
            terms.append(term)
    return terms


def skos_targets(store: Dict[str, ConceptRec], term: str) -> Set[str]:
    rec = store.get(term)
    if not rec:
        return set()
    targets: Set[str] = set()
    for values in rec["skos"].values():
        targets.update(values)
    targets.update(rec["isPartOf"])
    targets.update(rec["charactersInvolved"])
    targets.update(rec["hasAATBroader"])
    targets.update(rec["hasIconclassBroader"])
    targets.update(rec["hasTGMBroader"])
    targets.update(rec.get("saidToBeTheSameAs") or set())
    return targets


def identity_equivalents(
    term: str,
    store: Dict[str, ConceptRec],
    aliases: Dict[str, str],
) -> Set[str]:
    """Local concept plus owl:sameAs / saidToBeTheSameAs / primary Wikidata Q-code."""
    found: Set[str] = set()
    resolved = resolve_term(term, store, aliases)
    found.add(resolved)
    wd = canonical_wd_term(term)
    if wd:
        found.add(wd)
    rec = store.get(resolved)
    if not rec:
        return found
    if rec.get("wikidata"):
        found.add(f"wd:{rec['wikidata']}")
    for other in rec.get("sameAs") or set():
        found.add(resolve_term(other, store, aliases))
        other_wd = canonical_wd_term(other)
        if other_wd:
            found.add(other_wd)
    for other in rec.get("saidToBeTheSameAs") or set():
        found.add(resolve_term(other, store, aliases))
        other_wd = canonical_wd_term(other)
        if other_wd:
            found.add(other_wd)
    return found


def identity_closure(
    selected: Set[str],
    store: Dict[str, ConceptRec],
    aliases: Dict[str, str],
) -> Set[str]:
    """Transitive identity set, including reverse saidToBeTheSameAs."""
    identity: Set[str] = set()
    for term in selected:
        identity.update(identity_equivalents(term, store, aliases))
    for _ in range(4):
        snapshot = set(identity)
        for source, rec in store.items():
            src_ids = identity_equivalents(source, store, aliases)
            if src_ids & identity:
                identity.add(source)
                identity.update(src_ids)
                identity.update(rec.get("saidToBeTheSameAs") or set())
        if identity == snapshot:
            break
    return identity


def expand_selected(
    selected: Set[str],
    store: Dict[str, ConceptRec],
    aliases: Dict[str, str],
) -> Set[str]:
    expanded: Set[str] = set()
    for raw in selected:
        term = resolve_term(raw, store, aliases)
        expanded.add(term)
        expanded.update(skos_targets(store, term))
        rec = store.get(term)
        if rec:
            for other in rec["sameAs"]:
                expanded.add(resolve_term(other, store, aliases))
    expanded.update(identity_closure(selected, store, aliases))
    # Same neighbourhood rule as the DOT graph: identity of SKOS neighbours
    # and reverse saidToBeTheSameAs into the match set.
    expanded.update(identity_closure(set(expanded), store, aliases))
    return expanded


def incoming_skos(
    store: Dict[str, ConceptRec],
    selected: Set[str],
    aliases: Optional[Dict[str, str]] = None,
) -> Dict[str, Dict[str, Set[str]]]:
    """Map selected term → {skos predicate: {source concepts}}."""
    aliases = aliases or {}
    incoming: Dict[str, Dict[str, Set[str]]] = {
        term: defaultdict(set) for term in selected
    }
    identity_of = {
        term: identity_equivalents(term, store, aliases) for term in selected
    }
    for source, rec in store.items():
        for pred, values in rec["skos"].items():
            for target in values:
                if target in selected and source != target:
                    incoming[target][pred].add(source)
        for target in rec.get("saidToBeTheSameAs") or set():
            if source in selected:
                continue
            target_ids = {target}
            wd = canonical_wd_term(target)
            if wd:
                target_ids.add(wd)
            for sel, ids in identity_of.items():
                if target_ids & ids:
                    incoming[sel][SAID_SAME].add(source)
    return incoming


def is_narrative(term: str, store: Dict[str, ConceptRec]) -> bool:
    rec = store.get(term)
    if not rec:
        return False
    types = rec.get("types") or set()
    return any("NarrativeEpisode" in t or t.endswith("NarrativeEpisode") for t in types)


def related_narratives(
    selected: Set[str],
    store: Dict[str, ConceptRec],
    canvas_terms: Set[str],
) -> Tuple[List[str], List[str]]:
    """Return (episodes that reference the concept, episodes co-depicted on matching canvases)."""
    direct: Set[str] = set()
    co_depicted: Set[str] = set()
    for term, rec in store.items():
        if not is_narrative(term, store):
            continue
        involves = bool(
            rec["charactersInvolved"] & selected
            or rec["isPartOf"] & selected
            or any(values & selected for values in rec["skos"].values())
            or term in selected
        )
        if involves:
            direct.add(term)
        elif term in canvas_terms:
            co_depicted.add(term)
    return sorted(direct), sorted(co_depicted)


# ---------------------------------------------------------------------------
# Resource / canvas hits
# ---------------------------------------------------------------------------

Hit = Dict[str, Any]


def _base_hit(
    *,
    path: Path,
    collection_label: str,
    collection_thumb: Optional[str],
    resource_id: str,
    resource_label: str,
    resource_thumb: Optional[str],
    unique_id: str,
    match_source: str,
) -> Hit:
    return {
        "collection": path.name,
        "collection_label": collection_label,
        "collection_thumb": collection_thumb,
        "resource_id": resource_id,
        "resource_label": resource_label,
        "resource_thumb": resource_thumb,
        "unique_id": unique_id,
        "match_source": match_source,
        "mid": "",
        "cid": "",
        "canvas": None,
        "canvas_label": "",
        "folio": "",
        "canvas_thumb": None,
        "element_thumb": None,
        "depicts": [],
        "matching_elements": [],
        "matched_terms": [],
        "direct_terms": [],
        "aligned_terms": [],
        "reasons": [],
        "identity_via_wikidata": False,
    }


def _identity_via_wikidata(
    matched: Set[str], original_selected: Set[str], identity: Set[str]
) -> bool:
    if matched & original_selected:
        return False
    wd_ids = {t for t in identity if t.startswith("wd:")}
    local_ids = identity - original_selected - wd_ids
    return bool(matched & (wd_ids | local_ids))


def collect_hits(
    selected: Set[str],
    expanded: Set[str],
    original_selected: Optional[Set[str]] = None,
) -> List[Hit]:
    original_selected = original_selected or selected
    hits: List[Hit] = []
    files = sorted(ROOT_DIR.glob("*Collection.json"))
    for path in files:
        try:
            collection = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"  warning: skipped {path.name}: {exc}")
            continue
        collection_label = get_label_text(
            collection.get("label") or collection.get("title") or path.stem
        )
        collection_thumb = thumbnail_for(collection.get("thumbnail"), full_region=False)
        resources = (
            list(collection.get("manifests") or [])
            + list(collection.get("items") or [])
            + list(collection.get("members") or [])
        )
        for resource in resources:
            if not isinstance(resource, dict):
                continue
            resource_id = (
                resource.get("id") or resource.get("@id") or f"{path.name}:{len(hits)+1}"
            )
            resource_label = get_label_text(resource.get("label") or resource_id)
            resource_thumb = thumbnail_for(resource.get("thumbnail"), full_region=False)
            unique_id = resource_unique_id(resource)
            metadata = resource.get("metadata") or []
            canvases = extract_canvas_entries(metadata) if isinstance(metadata, list) else []
            depicts_field_terms = extract_depicts_field_terms(metadata)
            depicts_field_set = set(depicts_field_terms)

            resource_terms = set(find_all_terms(resource))
            matched_canvases = 0
            for canvas in canvases:
                canvas_all = set(find_all_terms(canvas))
                depicts = set(canvas_depicts(canvas))
                loud_terms: Set[str] = set()
                matching_elements: List[Dict[str, Any]] = []
                seen_elems: List[int] = []
                for elem in iter_content_elements(canvas):
                    el_terms = set(element_loud(elem)) | set(find_all_terms(elem))
                    loud_terms.update(element_loud(elem))
                    if el_terms & expanded:
                        matching_elements.append(elem)
                        seen_elems.append(id(elem))
                # Painting crops on a matching canvas even when elementLOUD is missing
                # (Ramayana Div figures have labels but no LOUD tags).
                for key in ("croppedFigures", "croppedPatterns"):
                    for elem in canvas.get(key) or []:
                        if isinstance(elem, dict) and id(elem) not in seen_elems:
                            matching_elements.append(elem)
                            seen_elems.append(id(elem))
                matched = (depicts | loud_terms | canvas_all) & expanded
                if not matched:
                    continue
                reasons: List[str] = []
                direct = matched & selected
                aligned = matched - selected
                via_wd = _identity_via_wikidata(
                    matched, original_selected, selected
                )
                if depicts & selected:
                    reasons.append("AsCanvas depicts")
                if loud_terms & selected:
                    reasons.append("content-element tag")
                wd_hit = {t for t in matched if t.startswith("wd:")} & selected
                if wd_hit or via_wd:
                    reasons.append(
                        "saidToBeTheSameAs Wikidata: "
                        + ", ".join(sorted(wd_hit or (matched & selected))[:6])
                    )
                if aligned:
                    reasons.append(
                        "SKOS-aligned: " + ", ".join(sorted(aligned)[:6])
                    )
                canvas_thumb = canvas_thumbnail(canvas)
                element_thumb = None
                for elem in matching_elements:
                    element_thumb = thumbnail_for(
                        elem, full_region=False, skip_keys=SKIP_THUMB_KEYS
                    )
                    if element_thumb:
                        break
                hit = _base_hit(
                    path=path,
                    collection_label=collection_label,
                    collection_thumb=collection_thumb,
                    resource_id=str(resource_id),
                    resource_label=resource_label,
                    resource_thumb=resource_thumb or canvas_thumb,
                    unique_id=unique_id,
                    match_source="ascanvas",
                )
                hit.update(
                    {
                        "mid": str(canvas.get("mid") or ""),
                        "cid": str(canvas.get("cid") or ""),
                        "canvas": canvas,
                        "canvas_label": get_label_text(canvas.get("label")),
                        "folio": canvas.get("folio") or "",
                        "canvas_thumb": canvas_thumb,
                        "element_thumb": element_thumb,
                        "depicts": canvas_depicts(canvas),
                        "matching_elements": matching_elements,
                        "matched_terms": sorted(matched),
                        "direct_terms": sorted(direct),
                        "aligned_terms": sorted(aligned),
                        "reasons": reasons,
                        "identity_via_wikidata": via_wd,
                    }
                )
                hits.append(hit)
                matched_canvases += 1

            if matched_canvases:
                continue

            matched_depicts = depicts_field_set & expanded
            if matched_depicts:
                via_wd = _identity_via_wikidata(
                    matched_depicts, original_selected, selected
                )
                reasons = [
                    "Depicts metadata field (no AsCanvas / States on this record)"
                ]
                wd_hit = {t for t in matched_depicts if t.startswith("wd:")} & selected
                if wd_hit or via_wd:
                    reasons.append(
                        "saidToBeTheSameAs Wikidata: "
                        + ", ".join(sorted(wd_hit or (matched_depicts & selected))[:6])
                    )
                hit = _base_hit(
                    path=path,
                    collection_label=collection_label,
                    collection_thumb=collection_thumb,
                    resource_id=str(resource_id),
                    resource_label=resource_label,
                    resource_thumb=resource_thumb,
                    unique_id=unique_id,
                    match_source="depicts_field",
                )
                hit.update(
                    {
                        "depicts": depicts_field_terms,
                        "matched_terms": sorted(matched_depicts),
                        "direct_terms": sorted(matched_depicts & selected),
                        "aligned_terms": sorted(matched_depicts - selected),
                        "reasons": reasons,
                        "identity_via_wikidata": via_wd,
                    }
                )
                hits.append(hit)
                continue

            other_terms = resource_terms & expanded
            if other_terms:
                via_wd = _identity_via_wikidata(
                    other_terms, original_selected, selected
                )
                reasons = [
                    "other resource metadata (not AsCanvas, not Depicts field)"
                ]
                wd_hit = {t for t in other_terms if t.startswith("wd:")} & selected
                if wd_hit or via_wd:
                    reasons.append(
                        "saidToBeTheSameAs Wikidata: "
                        + ", ".join(sorted(wd_hit or (other_terms & selected))[:6])
                    )
                hit = _base_hit(
                    path=path,
                    collection_label=collection_label,
                    collection_thumb=collection_thumb,
                    resource_id=str(resource_id),
                    resource_label=resource_label,
                    resource_thumb=resource_thumb,
                    unique_id=unique_id,
                    match_source="resource_metadata",
                )
                hit.update(
                    {
                        "matched_terms": sorted(other_terms),
                        "direct_terms": sorted(other_terms & selected),
                        "aligned_terms": sorted(other_terms - selected),
                        "reasons": reasons,
                        "identity_via_wikidata": via_wd,
                    }
                )
                hits.append(hit)
    return hits


# ---------------------------------------------------------------------------
# Markmap emission
# ---------------------------------------------------------------------------

def md_heading(level: int, text: str) -> str:
    return f"{'#' * max(1, min(level, 6))} {text}"


def md_image(alt: str, url: Optional[str]) -> str:
    if not url:
        return ""
    safe_alt = alt.replace("[", "(").replace("]", ")").replace("\n", " ")
    # Angle brackets keep commas in IIIF region/size (x,y,w,h and 250,) inside the URL.
    return f"![{safe_alt}](<{url}>)"


def with_thumb(text: str, url: Optional[str], alt: str) -> str:
    image = md_image(alt, url)
    return f"{text} {image}" if image else text


def bullet(indent: int, text: str) -> str:
    return f"{'  ' * indent}- {text}"


def emit_parent_tree(
    lines: List[str],
    term: str,
    store: Dict[str, ConceptRec],
    aliases: Dict[str, str],
    field: str,
    indent: int,
    seen: Optional[Set[str]] = None,
) -> None:
    """Nest each broader/isPartOf parent as a sibling, not a flattened chain."""
    seen = seen if seen is not None else set()
    resolved = resolve_term(term, store, aliases)
    rec = store.get(resolved)
    if not rec:
        return
    for parent in sorted(rec.get(field) or set()):
        parent = resolve_term(parent, store, aliases)
        if parent in seen:
            continue
        parent_rec = store.get(parent)
        extras: List[str] = []
        if parent_rec and parent_rec.get("isGuideTerm"):
            extras.append("guide term")
        if parent_rec and parent_rec.get("isInExtendedScope"):
            extras.append("extended scope")
        suffix = f" ({', '.join(extras)})" if extras else ""
        lines.append(bullet(indent, f"{concept_heading_text(parent, store)}{suffix}"))
        emit_parent_tree(
            lines, parent, store, aliases, field, indent + 1, seen | {parent, resolved}
        )


def emit_broader_list(
    lines: List[str],
    start_term: str,
    store: Dict[str, ConceptRec],
    aliases: Dict[str, str],
    field: str,
    indent: int,
    heading: str,
) -> None:
    resolved = resolve_term(start_term, store, aliases)
    rec = store.get(resolved)
    if not rec or not rec.get(field):
        return
    lines.append(bullet(indent, f"**{heading}**"))
    emit_parent_tree(lines, resolved, store, aliases, field, indent + 1, {resolved})


def emit_identity(
    lines: List[str],
    term: str,
    store: Dict[str, ConceptRec],
    indent: int = 0,
) -> None:
    rec = store.get(term)
    if not rec:
        lines.append(bullet(indent, "No ontology record found for this concept."))
        return
    if rec["types"]:
        lines.append(bullet(indent, f"**Type:** {', '.join(sorted(rec['types']))}"))
    en = first_label(rec, "en")
    fa = first_label(rec, "fa")
    none = first_label(rec, "none")
    if en:
        lines.append(bullet(indent, f"**Label (en):** {en}"))
    if fa:
        lines.append(bullet(indent, f"**Label (fa):** {fa}"))
    if none and none not in {en, fa}:
        lines.append(bullet(indent, f"**Label:** {none}"))
    if rec.get("wikidata"):
        lines.append(bullet(indent, f"**Wikidata:** {rec['wikidata']}"))
    same_as = sorted(rec.get("saidToBeTheSameAs") or [])
    if same_as:
        lines.append(
            bullet(
                indent,
                f"**{SAID_SAME} (same Wikidata / local records):** {', '.join(same_as)}",
            )
        )
    if rec.get("iconclassNotation"):
        lines.append(
            bullet(indent, f"**Iconclass notation:** {rec['iconclassNotation']}")
        )
    if rec.get("isGuideTerm"):
        lines.append(bullet(indent, "**AAT guide term**"))
    if rec.get("isInExtendedScope"):
        lines.append(bullet(indent, "**In extended AAT scope**"))
    if rec.get("comment"):
        comment = rec["comment"].replace("\n", " ").strip()
        if len(comment) > 420:
            comment = comment[:417] + "..."
        lines.append(bullet(indent, f"**Comment:** {comment}"))
    if rec.get("lctgmURI"):
        lines.append(bullet(indent, f"**TGM URI:** {rec['lctgmURI']}"))
    sources = sorted(rec.get("source_files") or [])
    if sources:
        lines.append(bullet(indent, f"**Source:** {', '.join(sources)}"))


def emit_skos_for_term(
    lines: List[str],
    term: str,
    store: Dict[str, ConceptRec],
    indent: int = 0,
    *,
    include_qid: bool = True,
    include_is_part_of: bool = True,
) -> None:
    rec = store.get(term)
    if not rec:
        return
    if include_qid and rec.get("wikidata"):
        lines.append(bullet(indent, rec["wikidata"]))
    same_as = sorted(rec.get("saidToBeTheSameAs") or [])
    if same_as:
        lines.append(bullet(indent, f"{SAID_SAME}: {', '.join(same_as)}"))
    if include_is_part_of and rec.get("isPartOf"):
        lines.append(
            bullet(indent, f"{IS_PART_OF}: {', '.join(sorted(rec['isPartOf']))}")
        )
    for pred in SKOS_DISPLAY_ORDER:
        objects = sorted(rec["skos"].get(pred, set()))
        if objects:
            lines.append(bullet(indent, f"{pred}: {', '.join(objects)}"))


def emit_aligned_term(
    lines: List[str],
    term: str,
    store: Dict[str, ConceptRec],
    aliases: Dict[str, str],
    heading_level: int,
) -> None:
    resolved = resolve_term(term, store, aliases)
    lines.append(md_heading(heading_level, concept_heading_text(resolved, store)))
    emit_identity(lines, resolved, store, indent=0)
    emit_skos_for_term(
        lines, resolved, store, indent=0, include_qid=False, include_is_part_of=False
    )
    rec = store.get(resolved)
    if rec:
        if rec["hasAATBroader"] or resolved.startswith("mdhn:aat"):
            emit_broader_list(
                lines, resolved, store, aliases, "hasAATBroader", 0, "AAT broader"
            )
        if rec["hasIconclassBroader"] or resolved.startswith(
            ("mdhn:iconclass", "iconclass:")
        ):
            emit_broader_list(
                lines,
                resolved,
                store,
                aliases,
                "hasIconclassBroader",
                0,
                "Iconclass broader",
            )
        if rec["hasTGMBroader"] or resolved.startswith("mdhn:tgm"):
            emit_broader_list(
                lines, resolved, store, aliases, "hasTGMBroader", 0, "TGM broader"
            )
        if rec["isPartOf"] and is_narrative(resolved, store):
            emit_broader_list(
                lines,
                resolved,
                store,
                aliases,
                "isPartOf",
                0,
                "Narrative isPartOf",
            )
    lines.append("")


def emit_vocabulary_branch(
    lines: List[str],
    term: str,
    store: Dict[str, ConceptRec],
    aliases: Dict[str, str],
    incoming: Dict[str, Dict[str, Set[str]]],
    heading_level: int,
) -> None:
    rec = store.get(term) or empty_concept()
    lines.append(md_heading(heading_level, "Vocabulary alignments"))
    lines.append("")
    same_as = sorted(rec.get("saidToBeTheSameAs") or [])
    any_skos = any(rec["skos"].values())
    if not any_skos and not incoming.get(term) and not same_as:
        lines.append("- No SKOS alignments recorded for this concept.")
        lines.append("")
        return

    if same_as:
        lines.append(
            md_heading(
                min(heading_level + 1, 6),
                f"{SAID_SAME} (same Wikidata / local records)",
            )
        )
        lines.append("")
        for obj in same_as:
            emit_aligned_term(lines, obj, store, aliases, min(heading_level + 2, 6))

    for pred in SKOS_DISPLAY_ORDER:
        objects = sorted(rec["skos"].get(pred, set()))
        if not objects:
            continue
        lines.append(md_heading(min(heading_level + 1, 6), pred))
        lines.append("")
        for obj in objects:
            emit_aligned_term(lines, obj, store, aliases, min(heading_level + 2, 6))

    incoming_for = incoming.get(term) or {}
    if incoming_for:
        lines.append(md_heading(min(heading_level + 1, 6), "Incoming associations"))
        lines.append("")
        for pred in sorted(incoming_for):
            sources = sorted(incoming_for[pred])
            lines.append(md_heading(min(heading_level + 2, 6), f"← {pred}"))
            lines.append("")
            for source in sources:
                emit_aligned_term(
                    lines, source, store, aliases, min(heading_level + 3, 6)
                )


def emit_episode(
    lines: List[str],
    episode: str,
    store: Dict[str, ConceptRec],
    aliases: Dict[str, str],
    heading_level: int,
) -> None:
    resolved = resolve_term(episode, store, aliases)
    rec = store.get(resolved) or empty_concept()
    lines.append(md_heading(heading_level, concept_heading_text(resolved, store)))
    emit_identity(lines, resolved, store, indent=0)
    involved = sorted(rec.get("charactersInvolved") or [])
    if involved:
        lines.append(bullet(0, f"**{CHARACTERS}:** {', '.join(involved)}"))
    emit_broader_list(
        lines, resolved, store, aliases, "isPartOf", 0, "isPartOf ancestry"
    )
    emit_skos_for_term(
        lines, resolved, store, indent=0, include_qid=False, include_is_part_of=False
    )
    lines.append("")


def emit_narrative_branch(
    lines: List[str],
    term: str,
    store: Dict[str, ConceptRec],
    aliases: Dict[str, str],
    direct_episodes: List[str],
    co_depicted: List[str],
    heading_level: int,
) -> None:
    lines.append(md_heading(heading_level, "Narrative episodes"))
    lines.append("")
    if not direct_episodes and not co_depicted:
        lines.append("- No narrative episodes reference this concept.")
        lines.append("")
        return
    if direct_episodes:
        lines.append(md_heading(min(heading_level + 1, 6), "Directly involving this concept"))
        lines.append("")
        for episode in direct_episodes:
            emit_episode(lines, episode, store, aliases, min(heading_level + 2, 6))
    if co_depicted:
        lines.append(
            md_heading(min(heading_level + 1, 6), "Co-depicted on matching canvases")
        )
        lines.append("")
        for episode in co_depicted:
            emit_episode(lines, episode, store, aliases, min(heading_level + 2, 6))


def emit_element(
    lines: List[str],
    elem: Dict[str, Any],
    store: Dict[str, ConceptRec],
    selected: Set[str],
    indent: int,
) -> None:
    """Emit a content element as nested list items (avoids Markdown h6 ceiling)."""
    el_label = get_label_text(elem.get("elementLabel") or elem.get("label"))
    el_type = elem.get("elementType") or "ContentElement"
    thumb = thumbnail_for(elem, full_region=False, skip_keys=SKIP_THUMB_KEYS)
    heading = f"{el_type}: {el_label}"
    lines.append(bullet(indent, with_thumb(heading, thumb, el_label)))
    loud = element_loud(elem)
    if loud:
        highlighted = []
        for tag in loud:
            mark = " ★" if tag in selected else ""
            highlighted.append(f"{tag}{mark}")
        lines.append(bullet(indent + 1, f"**elementLOUD:** {', '.join(highlighted)}"))
    styles = elem.get("elementStyle") or elem.get("style") or []
    if styles:
        lines.append(
            bullet(indent + 1, f"**Styles:** {', '.join(str(s) for s in styles)}")
        )
    for tag in loud:
        emit_skos_for_term(lines, tag, store, indent=indent + 1)


def emit_resources_branch(
    lines: List[str],
    hits: List[Hit],
    store: Dict[str, ConceptRec],
    aliases: Dict[str, str],
    selected: Set[str],
    heading_level: int,
) -> None:
    lines.append(md_heading(heading_level, "Depicted in collections"))
    lines.append("")
    if not hits:
        lines.append("- No collection resources reference this concept.")
        lines.append("")
        return

    def emit_depicts_list(title: str, depicts: List[str]) -> None:
        if not depicts:
            return
        lines.append(bullet(0, f"**{title}**"))
        ordered = [t for t in depicts if t in selected] + [
            t for t in depicts if t not in selected
        ]
        seen: Set[str] = set()
        for tag in ordered:
            if tag in seen:
                continue
            seen.add(tag)
            star = " ★" if tag in selected else ""
            title_text = concept_heading_text(tag, store)
            lines.append(bullet(1, f"{title_text}{star}"))
            emit_skos_for_term(lines, tag, store, indent=2)
            if is_narrative(tag, store):
                lines.append(bullet(2, "**Narrative episode**"))
                emit_broader_list(
                    lines, tag, store, aliases, "isPartOf", 2, "isPartOf"
                )

    def record_heading(hit: Hit) -> str:
        source = hit.get("match_source") or ""
        unique_id = str(hit.get("unique_id") or "")
        mid = str(hit.get("mid") or "")
        ident = mid or unique_id
        folio = hit.get("folio") or ""
        label = hit.get("canvas_label") or ""
        via_wd = bool(hit.get("identity_via_wikidata"))
        wd_note = "saidToBeTheSameAs Wikidata" if via_wd else ""
        if source == "ascanvas":
            folio_bit = f"f.{folio}" if folio else "AsCanvas"
            parts = ["AsCanvas"]
            if ident:
                parts.append(ident)
            parts.append(folio_bit if folio else "canvas")
            heading = " — ".join(dict.fromkeys(parts))
            if label:
                heading = f"{heading} — {label}"
            if wd_note:
                heading = f"{heading} — {wd_note}"
            return heading
        if source == "depicts_field":
            heading = "Depicts field (no AsCanvas / States)"
            if wd_note:
                heading = f"{heading} — {wd_note}"
            if ident:
                heading = f"{heading} — {ident}"
            return heading
        if via_wd:
            heading = "saidToBeTheSameAs Wikidata (no AsCanvas, not Depicts field)"
        else:
            heading = "Other resource metadata (no AsCanvas, not Depicts field)"
        if ident:
            heading = f"{heading} — {ident}"
        return heading

    def emit_canvas(hit: Hit, level: int) -> None:
        source = hit.get("match_source") or ""
        canvas = hit["canvas"]
        heading = record_heading(hit)
        thumb = hit.get("canvas_thumb") if canvas is not None else None
        lines.append(
            md_heading(level, with_thumb(heading, thumb, heading))
        )
        ident = hit.get("unique_id") or hit.get("mid") or ""
        if ident:
            lines.append(bullet(0, f"**Record ID:** `{ident}`"))
        if hit.get("mid") or hit.get("cid"):
            bits = []
            if hit.get("mid"):
                bits.append(f"mid `{hit['mid']}`")
            if hit.get("cid"):
                bits.append(f"cid `{hit['cid']}`")
            lines.append(bullet(0, f"**AsCanvas identifiers:** {', '.join(bits)}"))
        if hit.get("reasons"):
            lines.append(bullet(0, f"**Matched via:** {'; '.join(hit['reasons'])}"))
        if hit.get("direct_terms"):
            if source == "depicts_field":
                where = "in Depicts field"
            elif source == "ascanvas":
                where = "on this AsCanvas"
            else:
                where = "in other resource metadata"
            lines.append(
                bullet(
                    0,
                    f"**Selected concept(s) {where}:** {', '.join(hit['direct_terms'])}",
                )
            )
        if canvas:
            types = canvas.get("canvasType") or []
            if types:
                lines.append(
                    bullet(0, f"**Canvas types:** {', '.join(str(t) for t in types)}")
                )
            contains = canvas.get("folioContains") or []
            if contains:
                lines.append(
                    bullet(0, f"**Contains:** {', '.join(str(t) for t in contains)}")
                )
        matching = hit.get("matching_elements") or []
        if matching:
            lines.append(bullet(0, "**Matching content elements**"))
            for elem in matching:
                emit_element(lines, elem, store, selected, indent=1)
        depicts = hit.get("depicts") or []
        if source == "depicts_field":
            emit_depicts_list("Depicts field", depicts)
        elif canvas:
            emit_depicts_list("AsCanvas depicts", depicts)
        elif source == "resource_metadata":
            if hit.get("identity_via_wikidata"):
                lines.append(
                    bullet(
                        0,
                        "Matched via mdhn:saidToBeTheSameAs (same Wikidata record); "
                        "this record has no AsCanvas / States and the selected concept "
                        "is not in a Depicts field.",
                    )
                )
                emit_depicts_list(
                    "saidToBeTheSameAs Wikidata terms",
                    hit.get("direct_terms") or hit.get("matched_terms") or [],
                )
            else:
                lines.append(
                    bullet(
                        0,
                        "Matched in Agents or other metadata; this record has no AsCanvas / States "
                        "and the selected concept is not in a Depicts field.",
                    )
                )
        lines.append("")

    grouped: DefaultDict[str, DefaultDict[str, List[Hit]]] = defaultdict(
        lambda: defaultdict(list)
    )
    collection_meta: Dict[str, Tuple[str, Optional[str]]] = {}
    resource_meta: Dict[str, Tuple[str, Optional[str], str]] = {}
    for hit in hits:
        grouped[hit["collection"]][hit["resource_id"]].append(hit)
        collection_meta[hit["collection"]] = (
            hit["collection_label"],
            hit.get("collection_thumb"),
        )
        prev = resource_meta.get(hit["resource_id"])
        thumb = hit.get("resource_thumb")
        unique_id = str(hit.get("unique_id") or "")
        if prev is None:
            resource_meta[hit["resource_id"]] = (
                hit["resource_label"],
                thumb,
                unique_id,
            )
        elif not prev[1] and thumb:
            resource_meta[hit["resource_id"]] = (prev[0], thumb, prev[2] or unique_id)
        elif not prev[2] and unique_id:
            resource_meta[hit["resource_id"]] = (prev[0], prev[1], unique_id)

    ascanvas_count = sum(1 for hit in hits if hit.get("match_source") == "ascanvas")
    depicts_field_count = sum(
        1 for hit in hits if hit.get("match_source") == "depicts_field"
    )
    other_meta_count = sum(
        1 for hit in hits if hit.get("match_source") == "resource_metadata"
    )
    wd_same_count = sum(1 for hit in hits if hit.get("identity_via_wikidata"))
    lines.append(
        bullet(
            0,
            f"**{len(grouped)} collection(s), "
            f"{sum(len(v) for v in grouped.values())} resource(s), "
            f"{ascanvas_count} AsCanvas, "
            f"{depicts_field_count} Depicts-only (no AsCanvas), "
            f"{other_meta_count} other metadata (no AsCanvas, not Depicts field), "
            f"{wd_same_count} saidToBeTheSameAs Wikidata**",
        )
    )
    lines.append("")

    for collection in sorted(grouped, key=lambda name: collection_meta[name][0].lower()):
        coll_label, coll_thumb = collection_meta[collection]
        lines.append(
            md_heading(
                min(heading_level + 1, 6),
                with_thumb(f"Collection: {coll_label}", coll_thumb, coll_label),
            )
        )
        lines.append(bullet(0, f"`{collection}`"))
        lines.append("")
        for resource_id, resource_hits in grouped[collection].items():
            res_label, res_thumb, unique_id = resource_meta[resource_id]
            if unique_id and unique_id not in res_label:
                res_heading = f"Resource: {unique_id} — {res_label}"
            else:
                res_heading = f"Resource: {res_label}"
            lines.append(
                md_heading(
                    min(heading_level + 2, 6),
                    with_thumb(res_heading, res_thumb, res_label),
                )
            )
            lines.append("")
            for hit in resource_hits:
                emit_canvas(hit, min(heading_level + 3, 6))


def representative_thumb(hits: List[Hit]) -> Optional[str]:
    for hit in hits:
        if hit.get("element_thumb"):
            return hit["element_thumb"]
    for hit in hits:
        if hit.get("canvas_thumb"):
            return hit["canvas_thumb"]
    for hit in hits:
        if hit.get("resource_thumb"):
            return hit["resource_thumb"]
    return None


def hits_for_concept(term: str, selected: Set[str], all_hits: List[Hit]) -> List[Hit]:
    """Hits whose matched terms include this concept."""
    if len(selected) == 1 and term in selected:
        return all_hits
    scoped = [
        hit
        for hit in all_hits
        if term in (hit.get("matched_terms") or [])
        or term in (hit.get("direct_terms") or [])
    ]
    return scoped


def emit_concept_tree(
    lines: List[str],
    term: str,
    store: Dict[str, ConceptRec],
    aliases: Dict[str, str],
    incoming: Dict[str, Dict[str, Set[str]]],
    hits: List[Hit],
    selected: Set[str],
    heading_level: int,
) -> None:
    thumb = representative_thumb(hits)
    title = concept_heading_text(term, store)
    lines.append(md_heading(heading_level, with_thumb(title, thumb, term)))
    lines.append("")
    emit_identity(lines, term, store, indent=0)
    lines.append("")
    emit_vocabulary_branch(lines, term, store, aliases, incoming, heading_level + 1)
    canvas_terms: Set[str] = set()
    for hit in hits:
        canvas_terms.update(hit.get("depicts") or [])
        canvas_terms.update(hit.get("matched_terms") or [])
    direct_episodes, co_depicted = related_narratives({term}, store, canvas_terms)
    emit_narrative_branch(
        lines,
        term,
        store,
        aliases,
        direct_episodes,
        co_depicted,
        heading_level + 1,
    )
    emit_resources_branch(lines, hits, store, aliases, selected, heading_level + 1)


def generate_markmap(
    selected: List[str],
    store: Dict[str, ConceptRec],
    aliases: Dict[str, str],
    hits: List[Hit],
    identity_terms: Optional[Set[str]] = None,
) -> List[str]:
    selected_set = set(selected)
    identity_terms = identity_terms or selected_set
    incoming = incoming_skos(store, selected_set, aliases)
    lines: List[str] = [
        "---",
        "markmap:",
        f"  initialExpandLevel: {INITIAL_EXPAND_LEVEL}",
        "  maxWidth: 420",
        "  colorFreezeLevel: 2",
        "---",
        "",
    ]
    if len(selected) == 1:
        term = selected[0]
        scoped = hits_for_concept(term, selected_set, hits)
        emit_concept_tree(
            lines, term, store, aliases, incoming, scoped, identity_terms, 1
        )
    else:
        lines.append("# Iconography concept associations")
        lines.append("")
        lines.append(
            bullet(
                0,
                f"**Selected concepts:** {', '.join(selected)}",
            )
        )
        lines.append(
            "- Root of this Markmap is the selected iconography concept array "
            "(same `INPUT_CONCEPTS` contract as the DOT neighbourhood graph)."
        )
        lines.append("")
        for term in selected:
            ids = identity_equivalents(term, store, aliases)
            scoped = [
                hit
                for hit in hits
                if ids & set(hit.get("matched_terms") or [])
                or ids & set(hit.get("direct_terms") or [])
            ]
            emit_concept_tree(
                lines, term, store, aliases, incoming, scoped, ids, 2
            )
    return lines


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def normalize_input_concepts(raw_values: Iterable[str]) -> List[str]:
    selected: List[str] = []
    seen: Set[str] = set()
    for raw in raw_values:
        term = normalize_term(raw) or str(raw).strip()
        if not term or term in seen:
            continue
        seen.add(term)
        selected.append(term)
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a Markmap of hierarchical associations around the "
            "iconography concepts listed in INPUT_CONCEPTS."
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_MARKMAP,
        help="Output Markmap Markdown file path.",
    )
    args = parser.parse_args()

    selected = normalize_input_concepts(INPUT_CONCEPTS)
    if not selected:
        raise SystemExit("At least one concept must be defined in INPUT_CONCEPTS.")

    print("Loading ontology files...")
    store, aliases = load_ontology()
    print(f"  {len(store)} concepts loaded")

    resolved_selected: List[str] = []
    for term in selected:
        resolved = resolve_term(term, store, aliases)
        resolved_selected.append(resolved)
        if resolved not in store:
            print(f"  warning: {term} was not found in the ontology files")

    identity = identity_closure(set(resolved_selected), store, aliases)
    expanded = expand_selected(set(resolved_selected), store, aliases)
    expanded.update(identity)
    print(f"Selected concepts: {resolved_selected}")
    print(f"Identity equivalents (saidToBeTheSameAs / Wikidata): {sorted(identity)}")
    print(f"Expanded neighbourhood: {len(expanded)} terms")

    print("Scanning collection JSON files...")
    hits = collect_hits(
        identity, expanded, original_selected=set(resolved_selected)
    )
    canvas_hits = sum(1 for hit in hits if hit.get("canvas") is not None)
    print(f"  {len(hits)} resource/canvas hits ({canvas_hits} canvases)")

    lines = generate_markmap(
        resolved_selected, store, aliases, hits, identity_terms=identity
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE {args.output}")
    print(f"INPUT CONCEPTS: {INPUT_CONCEPTS}")
    print(f"THUMBNAIL_WIDTH: {THUMBNAIL_WIDTH}")


if __name__ == "__main__":
    main()
