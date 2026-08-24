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
    "iconclass_hierarchy.ttl",
    "aat_hierarchy.ttl",
    "ctl_vocabs.ttl",
    "LCTGM_RDF.ttl",
]

# Integer width used for the IIIF size segment: /{THUMBNAIL_WIDTH},/
THUMBNAIL_WIDTH: int = 250
# Default number of Markmap levels expanded in the generated document.
INITIAL_EXPAND_LEVEL: int = 3
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


def find_iiif_urls(node: Any) -> List[str]:
    found: List[str] = []
    seen: Set[str] = set()

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
            for nested in value.values():
                if nested is thumb:
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
) -> Optional[str]:
    for url in find_iiif_urls(node):
        rewritten = rewrite_iiif_size(url, width, full_region=full_region)
        if rewritten:
            return rewritten
    return None


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


def is_states_or_ascanvas_label(value: Any) -> bool:
    return "states" in get_label_text(value).strip().lower() or "ascanvas" in get_label_text(
        value
    ).strip().lower()


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
    if re.match(r"^(iconclass|wd|aat|tgm|biblissima|lcsh):", text):
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
        for match in CURIE_OR_IRI_RE.findall(value):
            if match.startswith("mdhn:"):
                continue
            if match.startswith(("iconclass:", "wd:", "aat:", "tgm:", "biblissima:")):
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


def canvas_depicts(canvas: Dict[str, Any]) -> List[str]:
    raw = canvas.get("depicts") or []
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
    return targets


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
    return expanded


def incoming_skos(
    store: Dict[str, ConceptRec], selected: Set[str]
) -> Dict[str, Dict[str, Set[str]]]:
    """Map selected term → {skos predicate: {source concepts}}."""
    incoming: Dict[str, Dict[str, Set[str]]] = {
        term: defaultdict(set) for term in selected
    }
    for source, rec in store.items():
        for pred, values in rec["skos"].items():
            for target in values:
                if target in selected and source != target:
                    incoming[target][pred].add(source)
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


def collect_hits(
    selected: Set[str],
    expanded: Set[str],
) -> List[Hit]:
    hits: List[Hit] = []
    files = sorted(ROOT_DIR.glob("*Collection.json"))
    for path in files:
        try:
            collection = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
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
            metadata = resource.get("metadata") or []
            canvases = extract_canvas_entries(metadata) if isinstance(metadata, list) else []

            resource_terms = set(find_all_terms(resource))
            matched_canvases = 0
            for canvas in canvases:
                canvas_all = set(find_all_terms(canvas))
                depicts = set(canvas_depicts(canvas))
                loud_terms: Set[str] = set()
                matching_elements: List[Dict[str, Any]] = []
                for elem in iter_content_elements(canvas):
                    el_terms = set(element_loud(elem)) | set(find_all_terms(elem))
                    loud_terms.update(element_loud(elem))
                    if el_terms & expanded:
                        matching_elements.append(elem)
                matched = (depicts | loud_terms | canvas_all) & expanded
                if not matched:
                    continue
                reasons: List[str] = []
                direct = matched & selected
                aligned = matched - selected
                if depicts & selected:
                    reasons.append("canvas depicts")
                if loud_terms & selected:
                    reasons.append("content-element tag")
                if aligned:
                    reasons.append(
                        "SKOS-aligned: " + ", ".join(sorted(aligned)[:6])
                    )
                canvas_thumb = thumbnail_for(canvas, full_region=True)
                element_thumb = None
                for elem in matching_elements:
                    element_thumb = thumbnail_for(elem, full_region=False)
                    if element_thumb:
                        break
                hits.append(
                    {
                        "collection": path.name,
                        "collection_label": collection_label,
                        "collection_thumb": collection_thumb,
                        "resource_id": resource_id,
                        "resource_label": resource_label,
                        "resource_thumb": resource_thumb or canvas_thumb,
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
                    }
                )
                matched_canvases += 1

            if matched_canvases == 0 and resource_terms & expanded:
                hits.append(
                    {
                        "collection": path.name,
                        "collection_label": collection_label,
                        "collection_thumb": collection_thumb,
                        "resource_id": resource_id,
                        "resource_label": resource_label,
                        "resource_thumb": resource_thumb,
                        "canvas": None,
                        "canvas_label": "",
                        "folio": "",
                        "canvas_thumb": None,
                        "element_thumb": None,
                        "depicts": [],
                        "matching_elements": [],
                        "matched_terms": sorted(resource_terms & expanded),
                        "direct_terms": sorted(resource_terms & selected),
                        "aligned_terms": sorted((resource_terms & expanded) - selected),
                        "reasons": ["resource metadata"],
                    }
                )
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
    return f"![{safe_alt}]({url})"


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
    any_skos = any(rec["skos"].values())
    if not any_skos and not incoming.get(term):
        lines.append("- No SKOS alignments recorded for this concept.")
        lines.append("")
        return

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
    heading_level: int,
) -> None:
    el_label = get_label_text(elem.get("elementLabel") or elem.get("label"))
    el_type = elem.get("elementType") or "ContentElement"
    thumb = thumbnail_for(elem, full_region=False)
    heading = f"{el_type}: {el_label}"
    lines.append(md_heading(heading_level, with_thumb(heading, thumb, el_label)))
    loud = element_loud(elem)
    if loud:
        highlighted = []
        for tag in loud:
            mark = " ★" if tag in selected else ""
            highlighted.append(f"{tag}{mark}")
        lines.append(bullet(0, f"**elementLOUD:** {', '.join(highlighted)}"))
    styles = elem.get("elementStyle") or elem.get("style") or []
    if styles:
        lines.append(
            bullet(0, f"**Styles:** {', '.join(str(s) for s in styles)}")
        )
    for tag in loud:
        emit_skos_for_term(lines, tag, store, indent=1)
    lines.append("")


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

    # Patch emit_canvas_hit broader lookup by closing over aliases
    def emit_canvas(hit: Hit, level: int) -> None:
        canvas = hit["canvas"]
        folio = hit["folio"]
        label = hit["canvas_label"]
        if canvas is None:
            folio_bit = "Resource metadata"
            heading = f"{folio_bit} — {label}" if label else folio_bit
        else:
            folio_bit = f"f.{folio}" if folio else "Canvas"
            heading = f"{folio_bit} — {label}" if label else folio_bit
        lines.append(
            md_heading(
                level,
                with_thumb(heading, hit.get("canvas_thumb"), f"canvas {folio_bit}"),
            )
        )
        if hit.get("reasons"):
            lines.append(bullet(0, f"**Matched via:** {'; '.join(hit['reasons'])}"))
        if hit.get("direct_terms"):
            lines.append(
                bullet(
                    0,
                    f"**Selected concept(s) on this canvas:** {', '.join(hit['direct_terms'])}",
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
            lines.append(md_heading(min(level + 1, 6), "Matching content elements"))
            lines.append("")
            for elem in matching:
                emit_element(lines, elem, store, selected, min(level + 2, 6))
        depicts = hit.get("depicts") or []
        if depicts:
            lines.append(md_heading(min(level + 1, 6), "Canvas depicts"))
            lines.append("")
            ordered = [t for t in depicts if t in selected] + [
                t for t in depicts if t not in selected
            ]
            seen: Set[str] = set()
            for tag in ordered:
                if tag in seen:
                    continue
                seen.add(tag)
                star = " ★" if tag in selected else ""
                title = concept_heading_text(tag, store)
                lines.append(md_heading(min(level + 2, 6), f"{title}{star}"))
                emit_skos_for_term(lines, tag, store, indent=0)
                if is_narrative(tag, store):
                    lines.append(bullet(0, "**Narrative episode**"))
                    emit_broader_list(
                        lines, tag, store, aliases, "isPartOf", 0, "isPartOf"
                    )
                lines.append("")
        elif not canvas:
            lines.append(bullet(0, "Resource-level match (no AsCanvas / States entry)."))
            lines.append("")

    grouped: DefaultDict[str, DefaultDict[str, List[Hit]]] = defaultdict(
        lambda: defaultdict(list)
    )
    collection_meta: Dict[str, Tuple[str, Optional[str]]] = {}
    resource_meta: Dict[str, Tuple[str, Optional[str]]] = {}
    for hit in hits:
        grouped[hit["collection"]][hit["resource_id"]].append(hit)
        collection_meta[hit["collection"]] = (
            hit["collection_label"],
            hit.get("collection_thumb"),
        )
        resource_meta[hit["resource_id"]] = (
            hit["resource_label"],
            hit.get("resource_thumb"),
        )

    canvas_count = sum(1 for hit in hits if hit.get("canvas") is not None)
    lines.append(
        bullet(
            0,
            f"**{len(grouped)} collection(s), {sum(len(v) for v in grouped.values())} resource(s), {canvas_count} canvas(es)**",
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
            res_label, res_thumb = resource_meta[resource_id]
            lines.append(
                md_heading(
                    min(heading_level + 2, 6),
                    with_thumb(f"Resource: {res_label}", res_thumb, res_label),
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
) -> List[str]:
    selected_set = set(selected)
    incoming = incoming_skos(store, selected_set)
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
            lines, term, store, aliases, incoming, scoped, selected_set, 1
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
            scoped = [
                hit
                for hit in hits
                if term in (hit.get("matched_terms") or [])
                or term in (hit.get("direct_terms") or [])
            ]
            if not scoped:
                # Still show the concept even if no resource hits.
                scoped = []
            emit_concept_tree(
                lines, term, store, aliases, incoming, scoped, selected_set, 2
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

    expanded = expand_selected(set(resolved_selected), store, aliases)
    print(f"Selected concepts: {resolved_selected}")
    print(f"Expanded neighbourhood: {len(expanded)} terms")

    print("Scanning collection JSON files...")
    hits = collect_hits(set(resolved_selected), expanded)
    canvas_hits = sum(1 for hit in hits if hit.get("canvas") is not None)
    print(f"  {len(hits)} resource/canvas hits ({canvas_hits} canvases)")

    lines = generate_markmap(resolved_selected, store, aliases, hits)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE {args.output}")
    print(f"INPUT CONCEPTS: {INPUT_CONCEPTS}")
    print(f"THUMBNAIL_WIDTH: {THUMBNAIL_WIDTH}")


if __name__ == "__main__":
    main()
