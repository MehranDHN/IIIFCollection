#!/usr/bin/env python3
"""
Person-rooted neighbourhood → Markmap Markdown.

Agential counterpart of generate_iconography_concept_markmap.py.
Edit INPUT_PERSONS (or pass --person) to choose who the tree starts from.

    selected person(s)
      identity (type, labels, Wikidata Q-code)
      SKOS predicates (exactMatch, closeMatch, …)
      occupations and FHKB / family relations
      narrative episodes (mdhn:charactersInvolved)
      other ontology subjects that cite the person
      collections → resources
        metadata field that mentioned the person (Agents, Author, …)
        AsCanvas / States canvases, matching content elements, IIIF thumbs
        resources that depict an episode involving the person

Any occurrence of the person CURIE, its Wikidata Q-code, or a Biblissima
exactMatch id in any JSON field is a hit. Identity equivalents from
mdhn:saidToBeTheSameAs are included in the match set.

Example:

    python generate_persons_markmap.py
    python generate_persons_markmap.py --person mdhn:Nizami_Ganjavi
    python generate_persons_markmap.py --person mdhn:Saadi_Shirazi --person mdhn:Abul_Qasim_Firdawsi
"""

from __future__ import annotations

import argparse
import json
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any, DefaultDict, Dict, Iterable, List, Optional, Pattern, Set, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_iconography_concept_markmap import (
    bullet,
    canvas_thumbnail,
    extract_canvas_entries,
    get_label_text,
    is_states_or_ascanvas_label,
    iter_content_elements,
    md_heading,
    resource_unique_id,
    thumbnail_for,
    with_thumb,
)

# ================== CONFIGURATION ==================
ROOT_DIR = SCRIPT_DIR.parents[1]
ONTOLOGY_DIR = ROOT_DIR / "Ontology"
PERSONS_TTL = ONTOLOGY_DIR / "PersonsRDFData.ttl"
NARRATIVE_TTL = ONTOLOGY_DIR / "narrative_episodes.ttl"
RESOURCES_TTL = ONTOLOGY_DIR / "resources.ttl"
REPORTS_DIR = SCRIPT_DIR / "reports"
USER_AGENT = "IIIFCollection-persons-markmap/1.0 (https://github.com/MehranDHN/IIIFCollection)"

# Edit this list to choose the persons that should be included by default.
INPUT_PERSONS = [
    "mdhn:Nizami_Ganjavi",
]

INITIAL_EXPAND_LEVEL: int = 4
# ===================================================

PersonRec = Dict[str, Any]
EpisodeRec = Dict[str, Any]
Hit = Dict[str, Any]

SKOS_DISPLAY_ORDER = (
    "skos:exactMatch",
    "skos:closeMatch",
    "skos:relatedMatch",
    "skos:broadMatch",
    "skos:narrowMatch",
    "skos:broader",
    "skos:narrower",
    "skos:related",
)

FHKB_DISPLAY_ORDER = (
    "fhkb:hasSon",
    "fhkb:hasDaughter",
    "fhkb:hasFather",
    "fhkb:hasMother",
    "fhkb:isFatherOf",
    "fhkb:isMotherOf",
    "fhkb:isSpouseOf",
    "fhkb:isBrotherOf",
    "fhkb:isSisterOf",
    "fhkb:isSiblingOf",
    "fhkb:hasBrother",
    "fhkb:hasSister",
    "fhkb:isStudentOf",
    "fhkb:hasStudent",
    "fhkb:hasRelation",
)

SUBJECT_RE = re.compile(
    r"^(mdhn:\S+)\s+a\s+((?:fhkb|mdhn):\S+?)\s*;?\s*$"
)
PRED_START_RE = re.compile(
    r"^(fhkb:[A-Za-z0-9_]+|skos:[A-Za-z]+|rdfs:label|rdfs:comment|"
    r"owl:sameAs|rdf:type|mdhn:[A-Za-z0-9_]+|a)\b"
)
LITERAL_RE = re.compile(r'"((?:\\.|[^"\\])*)"(?:@([A-Za-z-]+))?')
IRI_RE = re.compile(
    r"<https?://[^>\s]+>|[A-Za-z][A-Za-z0-9_-]*:[\w./%-]+"
)
MDHN_TERM_RE = re.compile(r"mdhn:[\w]+")
QCODE_RE = re.compile(r"Q\d+", re.IGNORECASE)
WD_CURIE_RE = re.compile(r"(?:wd|WD):Q(\d+)", re.IGNORECASE)
WD_IRI_RE = re.compile(
    r"https?://(?:www\.)?wikidata\.org/(?:wiki|entity)/(Q\d+)",
    re.IGNORECASE,
)
BB_CURIE_RE = re.compile(r"biblissima:(Q\d+)", re.IGNORECASE)
BB_IRI_RE = re.compile(
    r"https?://data\.biblissima\.fr/(?:entity|w/Item:|w/Special:EntityData/)(Q\d+)",
    re.IGNORECASE,
)

SKIP_THUMB_KEYS = {
    "linguisticElements",
    "basse64",
    "refers",
    "elementTextBlocks",
    "elementFAText",
    "elementENText",
}

SI_MANIFEST_RE = re.compile(
    r"ids\.si\.edu/ids/manifest/(FS-[A-Za-z0-9._-]+)", re.IGNORECASE
)
SI_UID_RE = re.compile(r"^FS-[A-Za-z0-9._-]+$", re.IGNORECASE)
IMAGE_SERVICE_RE = re.compile(
    r"ImageService[23]|iiif\.io/api/image", re.IGNORECASE
)


def _service_thumb(service_id: str, width: int = 250) -> Optional[str]:
    base = service_id.strip().rstrip("/")
    if not base.startswith("http"):
        return None
    candidate = f"{base}/full/{width},/0/default.jpg"
    return thumbnail_for(candidate, width, full_region=True) or candidate


def find_image_service_ids(node: Any) -> List[str]:
    found: List[str] = []
    seen: Set[str] = set()

    def add(url: Optional[str]) -> None:
        if url and url not in seen and url.startswith("http"):
            seen.add(url)
            found.append(url)

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            type_text = str(value.get("type") or value.get("@type") or "")
            profile = str(value.get("profile") or "")
            ident = value.get("id") or value.get("@id")
            if isinstance(ident, str) and (
                IMAGE_SERVICE_RE.search(type_text)
                or IMAGE_SERVICE_RE.search(profile)
            ):
                add(ident)
            service = value.get("service")
            if service is not None:
                walk(service)
            for nested in value.values():
                if nested is service:
                    continue
                walk(nested)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(node)
    return found


def smithsonian_thumb(resource: Dict[str, Any]) -> Optional[str]:
    rid = str(resource.get("id") or resource.get("@id") or "")
    match = SI_MANIFEST_RE.search(rid)
    ident = match.group(1) if match else resource_unique_id(resource)
    if ident and SI_UID_RE.match(ident):
        return f"https://ids.si.edu/ids/iiif/{ident}/full/250,/0/default.jpg"
    return None


def looks_like_manifest_url(url: str) -> bool:
    text = url.strip().lower()
    if not text.startswith("http"):
        return False
    return "/manifest" in text or ("iiif" in text and text.endswith(".json"))


def _first_canvas(manifest: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    items = manifest.get("items")
    if isinstance(items, list) and items and isinstance(items[0], dict):
        kind = str(items[0].get("type") or items[0].get("@type") or "")
        if "Canvas" in kind or "canvas" in kind.lower() or "items" in items[0]:
            return items[0]
    sequences = manifest.get("sequences") or []
    if sequences and isinstance(sequences[0], dict):
        canvases = sequences[0].get("canvases") or []
        if canvases and isinstance(canvases[0], dict):
            return canvases[0]
    return None


def _painting_body(canvas: Dict[str, Any]) -> Any:
    images = canvas.get("images") or []
    if images and isinstance(images[0], dict):
        return images[0].get("resource") or images[0].get("body")
    for page in canvas.get("items") or []:
        if not isinstance(page, dict):
            continue
        for anno in page.get("items") or []:
            if not isinstance(anno, dict):
                continue
            motivation = str(anno.get("motivation") or "").lower()
            if motivation and "painting" not in motivation:
                continue
            body = anno.get("body")
            if isinstance(body, list) and body:
                return body[0]
            if body:
                return body
    return None


def _thumb_from_body(body: Any) -> Optional[str]:
    if isinstance(body, str):
        return thumbnail_for(body, full_region=True) or _service_thumb(body)
    if not isinstance(body, dict):
        return None
    service = body.get("service")
    services = service if isinstance(service, list) else ([service] if service else [])
    for svc in services:
        if isinstance(svc, dict):
            sid = svc.get("id") or svc.get("@id")
            if isinstance(sid, str):
                thumb = _service_thumb(sid)
                if thumb:
                    return thumb
        elif isinstance(svc, str):
            thumb = _service_thumb(svc)
            if thumb:
                return thumb
    ident = body.get("id") or body.get("@id")
    if isinstance(ident, str):
        return thumbnail_for(ident, full_region=True) or _service_thumb(ident)
    return None


def first_canvas_thumb(manifest: Dict[str, Any]) -> Optional[str]:
    """Representative still: manifest thumbnail, else first canvas painting."""
    thumb = thumbnail_for(manifest.get("thumbnail"), full_region=False)
    if thumb:
        return thumb
    canvas = _first_canvas(manifest)
    if not canvas:
        return None
    thumb = thumbnail_for(canvas.get("thumbnail"), full_region=False)
    if thumb:
        return thumb
    return _thumb_from_body(_painting_body(canvas))


class ManifestThumbCache:
    """Fetch a IIIF Presentation manifest once and cache the first-canvas thumb."""

    def __init__(self, enabled: bool = True, timeout: int = 15) -> None:
        self.enabled = enabled
        self.timeout = timeout
        self.thumbs: Dict[str, Optional[str]] = {}
        self.fetched = 0
        self.ok = 0
        self.failed = 0
        self.dead_hosts: Set[str] = set()

    def get(self, url: str) -> Optional[str]:
        url = (url or "").strip()
        if not url or not self.enabled or not looks_like_manifest_url(url):
            return None
        if url in self.thumbs:
            return self.thumbs[url]
        host = urllib.parse.urlsplit(url).netloc.lower()
        if host in self.dead_hosts:
            self.thumbs[url] = None
            return None
        self.fetched += 1
        print(f"  fetching first canvas from {url}")
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/ld+json, application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            socket.timeout,
            ValueError,
            json.JSONDecodeError,
            OSError,
        ) as exc:
            print(f"  warning: manifest fetch failed {url}: {exc}")
            self.failed += 1
            self.thumbs[url] = None
            lowered = str(exc).lower()
            if "timed out" in lowered or "handshake" in lowered or "429" in lowered:
                self.dead_hosts.add(host)
            return None
        if not isinstance(payload, dict):
            self.failed += 1
            self.thumbs[url] = None
            return None
        thumb = first_canvas_thumb(payload)
        self.thumbs[url] = thumb
        if thumb:
            self.ok += 1
        else:
            self.failed += 1
        return thumb


MANIFEST_THUMBS = ManifestThumbCache(enabled=False)


def resource_sample_thumb(
    resource: Dict[str, Any], canvases: List[Dict[str, Any]]
) -> Optional[str]:
    """Best available still for a resource heading.

    Local JSON first, then Smithsonian FS- ids, then the first canvas of
    a remote IIIF Presentation manifest linked as the resource id.
    """
    thumb = thumbnail_for(resource.get("thumbnail"), full_region=False)
    if thumb:
        return thumb
    for canvas in canvases:
        thumb = canvas_thumbnail(canvas)
        if thumb:
            return thumb
    for service_id in find_image_service_ids(resource):
        thumb = _service_thumb(service_id)
        if thumb:
            return thumb
    thumb = thumbnail_for(resource, full_region=True, skip_keys=SKIP_THUMB_KEYS)
    if thumb:
        return thumb
    thumb = smithsonian_thumb(resource)
    if thumb:
        return thumb
    rid = str(resource.get("id") or resource.get("@id") or "")
    rtype = str(resource.get("type") or resource.get("@type") or "")
    if "Manifest" in rtype or looks_like_manifest_url(rid):
        return MANIFEST_THUMBS.get(rid)
    return None


def empty_person() -> PersonRec:
    return {
        "types": set(),
        "labels": {"en": [], "fa": [], "none": []},
        "comment": "",
        "skos": defaultdict(set),
        "relations": defaultdict(set),
        "occupations": set(),
        "sameAs": set(),
        "saidToBeTheSameAs": set(),
        "wikidata": None,
        "wikidata_url": None,
        "extra": defaultdict(set),
    }


def empty_episode() -> EpisodeRec:
    return {
        "types": set(),
        "labels": {"en": [], "fa": [], "none": []},
        "parents": [],
        "characters": set(),
        "wikidata": None,
    }


def unescape_literal(text: str) -> str:
    return (
        text.replace(r"\"", '"')
        .replace(r"\n", " ")
        .replace("\n", " ")
        .strip()
    )


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


def add_label(rec: Dict[str, Any], value: str, lang: Optional[str]) -> None:
    if not value:
        return
    bucket = (lang or "none").split("-")[0].lower()
    if bucket not in rec["labels"]:
        rec["labels"][bucket] = []
    if value not in rec["labels"][bucket]:
        rec["labels"][bucket].append(value)


def first_label(rec: Optional[Dict[str, Any]], lang: str = "en") -> Optional[str]:
    if not rec:
        return None
    values = (rec.get("labels") or {}).get(lang) or []
    return values[0] if values else None


def display_labels(rec: Optional[Dict[str, Any]]) -> str:
    if not rec:
        return ""
    en = first_label(rec, "en")
    fa = first_label(rec, "fa")
    if en and fa and fa != en:
        return f"{en} / {fa}"
    return en or fa or first_label(rec, "none") or ""


def extract_qcode(raw: Any) -> Optional[str]:
    if raw is None:
        return None
    match = QCODE_RE.search(str(raw).strip())
    return match.group(0).upper() if match else None


def canonical_wd(raw: Any) -> Optional[str]:
    if raw is None:
        return None
    text = str(raw).strip()
    if text.startswith("<") and text.endswith(">"):
        text = text[1:-1].strip()
    match = WD_CURIE_RE.search(text)
    if match:
        return f"wd:Q{match.group(1)}"
    iri = WD_IRI_RE.search(text)
    if iri:
        return f"wd:{iri.group(1).upper()}"
    return None


def parse_objects(fragment: str) -> List[Tuple[str, str, Optional[str]]]:
    results: List[Tuple[str, str, Optional[str]]] = []
    for match in LITERAL_RE.finditer(fragment):
        results.append(("literal", unescape_literal(match.group(1)), match.group(2)))
    for match in IRI_RE.finditer(fragment):
        token = match.group(0)
        if token.startswith("skos:") or token in {"a", "rdf:type"}:
            continue
        if token.startswith("<") and token.endswith(">"):
            token = token[1:-1]
        results.append(("iri", token, None))
    return results


def apply_person_predicate(
    rec: PersonRec, predicate: str, objects: List[Tuple[str, str, Optional[str]]]
) -> None:
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
        for kind, value, _lang in objects:
            if kind == "iri":
                rec["skos"][predicate].add(value)
        return
    if predicate.startswith("fhkb:"):
        for kind, value, _lang in objects:
            if kind == "iri":
                rec["relations"][predicate].add(value)
        return
    if predicate == "mdhn:hasOccupation":
        for kind, value, _lang in objects:
            if kind == "iri":
                rec["occupations"].add(value)
        return
    if predicate == "owl:sameAs":
        for kind, value, _lang in objects:
            if kind == "iri":
                rec["sameAs"].add(value)
        return
    if predicate == "mdhn:saidToBeTheSameAs":
        for kind, value, _lang in objects:
            wd = canonical_wd(value)
            rec["saidToBeTheSameAs"].add(wd or value)
        return
    if predicate == "mdhn:agentialWikiData":
        for kind, value, _lang in objects:
            qcode = extract_qcode(value)
            if qcode:
                rec["wikidata"] = qcode
                rec["wikidata_url"] = value if "wikidata.org" in value else (
                    f"https://www.wikidata.org/wiki/{qcode}"
                )
        return
    for kind, value, _lang in objects:
        rec["extra"][predicate].add(value if kind else value)


def apply_line_predicates(rec: PersonRec, line: str) -> None:
    text = line.rstrip(".;, ").strip()
    if not text:
        return
    parts = [p.strip() for p in re.split(r"\s*;\s*", text) if p.strip()]
    for part in parts:
        match = PRED_START_RE.match(part)
        if not match:
            continue
        predicate = match.group(1)
        fragment = part[match.end() :].strip()
        apply_person_predicate(rec, predicate, parse_objects(fragment))


def parse_persons(path: Path) -> Dict[str, PersonRec]:
    store: Dict[str, PersonRec] = {}
    current: Optional[str] = None
    if not path.exists():
        raise SystemExit(f"Persons file not found: {path}")

    def ensure(term: str) -> PersonRec:
        rec = store.get(term)
        if rec is None:
            rec = empty_person()
            store[term] = rec
        return rec

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = strip_turtle_comment(raw)
        if not line or line.startswith("@prefix") or line.startswith("@base"):
            continue
        subj = SUBJECT_RE.match(line)
        if subj:
            current = subj.group(1)
            rec = ensure(current)
            rec["types"].add(subj.group(2).rstrip(";"))
            rest = line[subj.end() :].strip()
            if rest:
                apply_line_predicates(rec, rest)
            if line.endswith("."):
                current = None
            continue
        if current is None:
            continue
        apply_line_predicates(store[current], line)
        if line.endswith("."):
            current = None
    return store


def parse_episodes(path: Path) -> Dict[str, EpisodeRec]:
    store: Dict[str, EpisodeRec] = {}
    current: Optional[str] = None
    current_pred: Optional[str] = None
    if not path.exists():
        return store

    def ensure(term: str) -> EpisodeRec:
        rec = store.get(term)
        if rec is None:
            rec = empty_episode()
            store[term] = rec
        return rec

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = strip_turtle_comment(raw)
        if not line or line.startswith("@prefix") or line.startswith("@base"):
            continue
        subj = SUBJECT_RE.match(line)
        pred_match = None if subj else PRED_START_RE.match(line)
        if subj:
            current = subj.group(1)
            rec = ensure(current)
            rec["types"].add(subj.group(2).rstrip(";"))
            rest = line[subj.end() :].strip()
            if rest:
                line = rest
                pred_match = PRED_START_RE.match(line)
            else:
                current_pred = None
                continue
        if current is None:
            continue
        if pred_match:
            current_pred = pred_match.group(1)
            payload = line[pred_match.end() :].strip()
        else:
            payload = line
        rec = ensure(current)
        if current_pred in {"a", "rdf:type"}:
            rec["types"].update(
                value for kind, value, _lang in parse_objects(payload) if kind == "iri"
            )
        elif current_pred == "rdfs:label":
            for value, lang in LITERAL_RE.findall(payload):
                add_label(rec, unescape_literal(value), lang)
        elif current_pred in {"mdhn:isPartOf", "mdhn:ispartOf"}:
            for term in MDHN_TERM_RE.findall(payload):
                if term != current and term not in rec["parents"]:
                    rec["parents"].append(term)
                    ensure(term)
        elif current_pred in {"mdhn:charactersInvolved", "mdhn:characterInvolved"}:
            rec["characters"].update(MDHN_TERM_RE.findall(payload))
        elif current_pred in {"mdhn:icWikiDataURL", "mdhn:agentialWikiData"}:
            qcode = extract_qcode(payload)
            if qcode:
                rec["wikidata"] = qcode
        if line.endswith("."):
            current = None
            current_pred = None
    return store


def scan_ttl_incoming(
    ontology_dir: Path, identity: Set[str], skip_names: Set[str]
) -> List[Tuple[str, str, str, str]]:
    """Other Turtle subjects that mention a selected person term."""
    mentions: List[Tuple[str, str, str, str]] = []
    seen: Set[Tuple[str, str, str, str]] = set()
    for path in sorted(ontology_dir.glob("*.ttl")):
        if path.name in skip_names:
            continue
        current = None
        current_pred = None
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = strip_turtle_comment(raw)
            if not line or line.startswith("@prefix") or line.startswith("@base"):
                continue
            subj = SUBJECT_RE.match(line)
            pred_match = None if subj else PRED_START_RE.match(line)
            if not subj:
                loose = re.match(r"^(mdhn:\S+)\s+", line)
                if loose and not pred_match:
                    current = loose.group(1)
                    rest = line[loose.end() :].strip()
                    pred_match = PRED_START_RE.match(rest) if rest else None
                    if pred_match:
                        line = rest
            else:
                current = subj.group(1)
                rest = line[subj.end() :].strip()
                if rest:
                    line = rest
                    pred_match = PRED_START_RE.match(line)
            if pred_match:
                current_pred = pred_match.group(1)
                payload = line[pred_match.end() :].strip()
            else:
                payload = line
            if current is None or current in identity:
                continue
            for term in MDHN_TERM_RE.findall(payload):
                if term in identity:
                    row = (path.name, current, current_pred or "", term)
                    if row not in seen:
                        seen.add(row)
                        mentions.append(row)
            if line.endswith("."):
                current = None
                current_pred = None
    return mentions


def person_heading(term: str, rec: Optional[PersonRec]) -> str:
    labels = display_labels(rec)
    qcode = (rec or {}).get("wikidata") or ""
    bits = [term]
    if qcode:
        bits.append(qcode)
    ident = ", ".join(bits)
    if labels:
        return f"{labels} (`{ident}`)"
    return f"`{ident}`"


def episode_heading(term: str, rec: Optional[EpisodeRec]) -> str:
    labels = display_labels(rec)
    qcode = (rec or {}).get("wikidata") or ""
    if labels and qcode:
        return f"{labels} (`{term}`, {qcode})"
    if labels:
        return f"{labels} (`{term}`)"
    return f"`{term}`"


def identity_tokens(term: str, rec: Optional[PersonRec]) -> Set[str]:
    tokens: Set[str] = {term}
    if not rec:
        return tokens
    if rec.get("wikidata"):
        q = rec["wikidata"]
        tokens.add(f"wd:{q}")
        tokens.add(f"WD:{q}")
        tokens.add(f"https://www.wikidata.org/wiki/{q}")
        tokens.add(f"https://www.wikidata.org/entity/{q}")
    tokens.update(rec.get("sameAs") or [])
    tokens.update(rec.get("saidToBeTheSameAs") or [])
    for values in rec["skos"].values():
        for obj in values:
            tokens.add(obj)
            bb = BB_CURIE_RE.search(obj)
            if bb:
                q = bb.group(1).upper()
                tokens.add(f"biblissima:{q}")
                tokens.add(f"https://data.biblissima.fr/entity/{q}")
    return {t for t in tokens if t}


def compile_token_patterns(tokens: Set[str]) -> List[Tuple[str, Pattern]]:
    patterns: List[Tuple[str, re.Pattern[str]]] = []
    seen: Set[str] = set()
    for token in sorted(tokens, key=len, reverse=True):
        key = token.lower()
        if key in seen:
            continue
        seen.add(key)
        patterns.append(
            (token, re.compile(re.escape(token) + r"(?![A-Za-z0-9_])", re.IGNORECASE))
        )
    return patterns


def find_tokens_in_text(
    text: str, patterns: List[Tuple[str, Pattern]]
) -> List[str]:
    found: List[str] = []
    seen: Set[str] = set()
    for token, pattern in patterns:
        if pattern.search(text) and token not in seen:
            seen.add(token)
            found.append(token)
    return found


def find_token_hits(
    node: Any,
    patterns: List[Tuple[str, Pattern]],
    path: str = "",
) -> List[Tuple[str, str]]:
    """Return (json_path, matched_token) for every occurrence."""
    hits: List[Tuple[str, str]] = []
    if isinstance(node, dict):
        for key, nested in node.items():
            child = f"{path} > {key}" if path else str(key)
            hits.extend(find_token_hits(nested, patterns, child))
    elif isinstance(node, list):
        for item in node:
            hits.extend(find_token_hits(item, patterns, path))
    elif isinstance(node, str):
        for token in find_tokens_in_text(node, patterns):
            hits.append((path or "(string)", token))
    return hits


def metadata_field_name(meta: Dict[str, Any]) -> str:
    return get_label_text(meta.get("label") or "metadata").strip() or "metadata"


def md_escape(text: str) -> str:
    return text.replace("\n", " ").replace("\r", " ").strip()


def normalize_person(value: str) -> str:
    text = value.strip()
    if not text:
        return text
    if text.startswith("mdhn:"):
        return text
    if re.match(r"^[\w]+$", text):
        return f"mdhn:{text}"
    return text


def reverse_family(
    persons: Dict[str, PersonRec],
) -> Dict[str, Dict[str, Set[str]]]:
    incoming: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))
    for source, rec in persons.items():
        for pred, targets in rec["relations"].items():
            for target in targets:
                incoming[target][pred].add(source)
    return incoming


def _base_hit(
    *,
    path: Path,
    collection_label: str,
    collection_thumb: Optional[str],
    resource: Dict[str, Any],
    match_source: str,
    resource_thumb: Optional[str] = None,
) -> Hit:
    resource_id = str(
        resource.get("id") or resource.get("@id") or f"{path.name}:resource"
    )
    resource_label = get_label_text(resource.get("label") or resource_id)
    return {
        "collection": path.name,
        "collection_label": collection_label,
        "collection_thumb": collection_thumb,
        "resource_id": resource_id,
        "resource_label": resource_label,
        "resource_thumb": resource_thumb,
        "unique_id": resource_unique_id(resource),
        "match_source": match_source,
        "fields": [],
        "matched_tokens": [],
        "mid": "",
        "cid": "",
        "canvas": None,
        "canvas_label": "",
        "folio": "",
        "canvas_thumb": None,
        "matching_elements": [],
        "related_episode": "",
    }


SKIP_TTL_SCAN = {
    "PersonsRDFData.ttl",
    "LCTGM_RDF.ttl",
    "LCTGM_RDF.migrated.ttl",
    "aat_hierarchy.ttl",
    "iconclass_hierarchy.ttl",
    "lcsh_rdf_subset.ttl",
    "tgn_subset_updated.ttl",
    "ctl_vocabs.ttl",
}


def collect_collection_hits(
    patterns: List[Tuple[str, Pattern]],
    episode_terms: Set[str],
) -> List[Hit]:
    hits: List[Hit] = []
    episode_patterns = compile_token_patterns(episode_terms) if episode_terms else []
    files = sorted(ROOT_DIR.glob("*Collection.json"))
    for path in files:
        try:
            collection = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"  warning: skipped {path.name}: {exc}")
            continue
        if not isinstance(collection, dict):
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
        seen_resources: Set[str] = set()
        for resource in resources:
            if not isinstance(resource, dict):
                continue
            resource_key = str(
                resource.get("id") or resource.get("@id") or ""
            ).strip()
            if resource_key:
                if resource_key in seen_resources:
                    continue
                seen_resources.add(resource_key)
            metadata = resource.get("metadata") or []
            canvases = (
                extract_canvas_entries(metadata) if isinstance(metadata, list) else []
            )
            sample_thumb: Optional[str] = None
            sample_ready = False

            def ensure_sample() -> Optional[str]:
                nonlocal sample_thumb, sample_ready
                if not sample_ready:
                    sample_thumb = resource_sample_thumb(resource, canvases)
                    sample_ready = True
                return sample_thumb

            matched_canvas = False
            for canvas in canvases:
                field_hits = find_token_hits(canvas, patterns, "AsCanvas")
                if not field_hits:
                    continue
                matched_canvas = True
                hit = _base_hit(
                    path=path,
                    collection_label=collection_label,
                    collection_thumb=collection_thumb,
                    resource=resource,
                    match_source="ascanvas",
                    resource_thumb=ensure_sample(),
                )
                fields = sorted({path_text for path_text, _tok in field_hits})
                tokens = sorted({tok for _path, tok in field_hits})
                matching_elements: List[Dict[str, Any]] = []
                for elem in iter_content_elements(canvas):
                    if find_token_hits(elem, patterns):
                        matching_elements.append(elem)
                hit.update(
                    {
                        "fields": fields,
                        "matched_tokens": tokens,
                        "mid": str(canvas.get("mid") or ""),
                        "cid": str(canvas.get("cid") or ""),
                        "canvas": canvas,
                        "canvas_label": get_label_text(canvas.get("label")),
                        "folio": canvas.get("folio") or "",
                        "canvas_thumb": canvas_thumbnail(canvas),
                        "matching_elements": matching_elements,
                    }
                )
                hits.append(hit)

            field_groups: DefaultDict[str, Set[str]] = defaultdict(set)
            if isinstance(metadata, list):
                for meta in metadata:
                    if not isinstance(meta, dict):
                        continue
                    if is_states_or_ascanvas_label(meta.get("label")):
                        continue
                    label = metadata_field_name(meta)
                    for path_text, token in find_token_hits(
                        meta.get("value"), patterns, label
                    ):
                        field_groups[path_text].add(token)
            for key, nested in resource.items():
                if key == "metadata":
                    continue
                for path_text, token in find_token_hits(nested, patterns, str(key)):
                    field_groups[path_text].add(token)

            if field_groups:
                hit = _base_hit(
                    path=path,
                    collection_label=collection_label,
                    collection_thumb=collection_thumb,
                    resource=resource,
                    match_source="metadata",
                    resource_thumb=ensure_sample(),
                )
                hit["fields"] = sorted(field_groups)
                tokens: Set[str] = set()
                for values in field_groups.values():
                    tokens.update(values)
                hit["matched_tokens"] = sorted(tokens)
                hits.append(hit)
            elif not matched_canvas and episode_patterns:
                depicts_hits = find_token_hits(resource, episode_patterns)
                episode_found = sorted(
                    {tok for _path, tok in depicts_hits if tok in episode_terms}
                )
                if episode_found:
                    hit = _base_hit(
                        path=path,
                        collection_label=collection_label,
                        collection_thumb=collection_thumb,
                        resource=resource,
                        match_source="related_episode",
                        resource_thumb=ensure_sample(),
                    )
                    hit["fields"] = sorted({path_text for path_text, _tok in depicts_hits})
                    hit["matched_tokens"] = episode_found
                    hit["related_episode"] = episode_found[0]
                    hits.append(hit)
    return hits


def count_suffix(n_resources: int, n_fields: int) -> str:
    if n_resources == 0:
        return ""
    noun = "resource" if n_resources == 1 else "resources"
    return f" — {n_resources} {noun}, {n_fields} field hit(s)"


def emit_identity(
    lines: List[str], term: str, rec: Optional[PersonRec], indent: int = 0
) -> None:
    if not rec:
        lines.append(bullet(indent, "No record in PersonsRDFData.ttl."))
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
        url = rec.get("wikidata_url") or f"https://www.wikidata.org/wiki/{rec['wikidata']}"
        lines.append(bullet(indent, f"**Wikidata:** [{rec['wikidata']}]({url})"))
    if rec.get("occupations"):
        lines.append(
            bullet(
                indent,
                f"**Occupation:** {', '.join(sorted(rec['occupations']))}",
            )
        )
    if rec.get("comment"):
        comment = rec["comment"].replace("\n", " ").strip()
        if len(comment) > 420:
            comment = comment[:417] + "..."
        lines.append(bullet(indent, f"**Comment:** {comment}"))
    extra_skip = {
        "mdhn:agentialWikiData",
        "mdhn:hasOccupation",
        "mdhn:saidToBeTheSameAs",
    }
    for pred, values in sorted((rec.get("extra") or {}).items()):
        if pred in extra_skip or not values:
            continue
        lines.append(bullet(indent, f"**{pred}:** {', '.join(sorted(values))}"))


def emit_skos(lines: List[str], rec: Optional[PersonRec], indent: int = 0) -> None:
    if not rec:
        return
    any_skos = any(rec["skos"].values())
    same = sorted(rec.get("saidToBeTheSameAs") or [])
    same_as = sorted(rec.get("sameAs") or [])
    if not any_skos and not same and not same_as:
        lines.append(bullet(indent, "No SKOS alignments recorded."))
        return
    if rec.get("wikidata"):
        lines.append(bullet(indent, f"Wikidata Q-code: {rec['wikidata']}"))
    for pred in SKOS_DISPLAY_ORDER:
        objects = sorted(rec["skos"].get(pred, set()))
        if objects:
            lines.append(bullet(indent, f"**{pred}:** {', '.join(objects)}"))
    leftover = sorted(
        pred for pred in rec["skos"] if pred not in SKOS_DISPLAY_ORDER and rec["skos"][pred]
    )
    for pred in leftover:
        lines.append(
            bullet(indent, f"**{pred}:** {', '.join(sorted(rec['skos'][pred]))}")
        )
    if same:
        lines.append(
            bullet(indent, f"**mdhn:saidToBeTheSameAs:** {', '.join(same)}")
        )
    if same_as:
        lines.append(bullet(indent, f"**owl:sameAs:** {', '.join(same_as)}"))


def related_person_line(
    term: str, persons: Dict[str, PersonRec]
) -> str:
    return person_heading(term, persons.get(term))


def emit_relations(
    lines: List[str],
    term: str,
    rec: Optional[PersonRec],
    persons: Dict[str, PersonRec],
    incoming: Dict[str, Dict[str, Set[str]]],
    indent: int = 0,
) -> None:
    outgoing = rec["relations"] if rec else {}
    incoming_for = incoming.get(term) or {}
    if not outgoing and not incoming_for:
        lines.append(bullet(indent, "No FHKB / family relations recorded."))
        return
    ordered = [p for p in FHKB_DISPLAY_ORDER if outgoing.get(p)]
    ordered.extend(sorted(p for p in outgoing if p not in FHKB_DISPLAY_ORDER and outgoing[p]))
    for pred in ordered:
        lines.append(bullet(indent, f"**{pred}**"))
        for other in sorted(outgoing[pred]):
            lines.append(bullet(indent + 1, related_person_line(other, persons)))
    if incoming_for:
        lines.append(bullet(indent, "**Incoming relations**"))
        for pred in sorted(incoming_for):
            lines.append(bullet(indent + 1, f"← {pred}"))
            for other in sorted(incoming_for[pred]):
                lines.append(bullet(indent + 2, related_person_line(other, persons)))


def person_label_needles(term: str, rec: Optional[PersonRec]) -> List[str]:
    needles: List[str] = []
    seen: Set[str] = set()
    values: List[str] = []
    if rec:
        for lang in ("en", "fa", "none"):
            values.extend(rec.get("labels", {}).get(lang) or [])
    local = term.split(":", 1)[-1].replace("_", " ")
    values.append(local)
    for value in values:
        text = value.strip()
        if len(text) >= 5 and text.lower() not in seen:
            seen.add(text.lower())
            needles.append(text)
        for part in re.split(r"[\s,./_-]+", text):
            if len(part) >= 5 and part.lower() not in seen:
                seen.add(part.lower())
                needles.append(part)
    return needles


def episode_mentions_person(
    episode: EpisodeRec, needles: List[Tuple[str, Pattern]]
) -> bool:
    labels = episode.get("labels") or {}
    parts: List[str] = []
    for lang in ("en", "fa", "none"):
        parts.extend(labels.get(lang) or [])
    haystack = " ".join(parts)
    if not haystack:
        return False
    return any(pattern.search(haystack) for _text, pattern in needles)


def related_episodes(
    term: str, rec: Optional[PersonRec], episodes: Dict[str, EpisodeRec]
) -> Tuple[List[str], List[str]]:
    involved = [
        ep
        for ep, erec in episodes.items()
        if term in (erec.get("characters") or set())
    ]
    needle_patterns = [
        (text, re.compile(r"\b" + re.escape(text) + r"\b", re.IGNORECASE))
        for text in person_label_needles(term, rec)
    ]
    mentioned = [
        ep
        for ep, erec in episodes.items()
        if ep not in involved and episode_mentions_person(erec, needle_patterns)
    ]
    involved.sort(key=lambda ep: display_labels(episodes[ep]) or ep)
    mentioned.sort(key=lambda ep: display_labels(episodes[ep]) or ep)
    return involved, mentioned


def emit_episode_item(
    lines: List[str], ep: str, rec: EpisodeRec, indent: int
) -> None:
    lines.append(bullet(indent, episode_heading(ep, rec)))
    chars = sorted(rec.get("characters") or [])
    if chars:
        lines.append(
            bullet(indent + 1, f"**charactersInvolved:** {', '.join(chars)}")
        )
    if rec.get("parents"):
        chain = " ← ".join(rec["parents"])
        lines.append(bullet(indent + 1, f"**isPartOf:** {chain}"))


def emit_episodes(
    lines: List[str],
    term: str,
    rec: Optional[PersonRec],
    episodes: Dict[str, EpisodeRec],
    indent: int = 0,
) -> List[str]:
    involved, mentioned = related_episodes(term, rec, episodes)
    if not involved and not mentioned:
        lines.append(
            bullet(
                indent,
                "No narrative episodes list this person in charactersInvolved or in episode labels.",
            )
        )
        return []
    if involved:
        lines.append(bullet(indent, "**charactersInvolved**"))
        for ep in involved:
            emit_episode_item(lines, ep, episodes[ep], indent + 1)
    if mentioned:
        lines.append(bullet(indent, "**Named in episode labels**"))
        for ep in mentioned:
            emit_episode_item(lines, ep, episodes[ep], indent + 1)
    return involved + mentioned


def parse_resource_index(path: Path) -> Dict[str, Dict[str, str]]:
    """Map mdhn:DigitalResource subjects to label + mdhn:hasUrl."""
    store: Dict[str, Dict[str, str]] = {}
    current: Optional[str] = None
    if not path.exists():
        return store

    def ensure(term: str) -> Dict[str, str]:
        rec = store.get(term)
        if rec is None:
            rec = {"url": "", "label": ""}
            store[term] = rec
        return rec

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = strip_turtle_comment(raw)
        if not line or line.startswith("@prefix") or line.startswith("@base"):
            continue
        subj = SUBJECT_RE.match(line)
        if subj:
            current = subj.group(1)
            ensure(current)
            rest = line[subj.end() :].strip()
            if rest:
                line = rest
            else:
                continue
        if current is None:
            continue
        if line.startswith("mdhn:hasUrl") or " mdhn:hasUrl " in f" {line}":
            match = LITERAL_RE.search(line)
            if match:
                ensure(current)["url"] = unescape_literal(match.group(1))
        if line.startswith("rdfs:label") and not store[current]["label"]:
            match = LITERAL_RE.search(line)
            if match:
                store[current]["label"] = unescape_literal(match.group(1))
        if line.endswith("."):
            current = None
    return {term: rec for term, rec in store.items() if rec.get("url")}


def subject_lookup_keys(subject: str) -> List[str]:
    local = subject.split(":", 1)[-1]
    keys = [local, local.replace("_", "-"), local.replace("-", "_")]
    seen: Set[str] = set()
    ordered: List[str] = []
    for key in keys:
        if key and key not in seen:
            seen.add(key)
            ordered.append(key)
    return ordered


def hit_thumb_index(hits: List[Hit]) -> Dict[str, str]:
    index: Dict[str, str] = {}
    for hit in hits:
        thumb = hit.get("canvas_thumb") or hit.get("resource_thumb")
        if not thumb:
            continue
        unique_id = str(hit.get("unique_id") or "")
        if unique_id:
            index[unique_id] = thumb
            index[unique_id.replace("-", "_")] = thumb
            index[unique_id.replace("_", "-")] = thumb
        rid = str(hit.get("resource_id") or "").rstrip("/")
        if rid:
            index[rid.split("/")[-1]] = thumb
    return index


def thumb_for_ontology_subject(
    subject: str,
    resource_index: Dict[str, Dict[str, str]],
    thumbs: Dict[str, str],
) -> Optional[str]:
    for key in subject_lookup_keys(subject):
        if key in thumbs:
            return thumbs[key]
        if SI_UID_RE.match(key):
            return f"https://ids.si.edu/ids/iiif/{key}/full/250,/0/default.jpg"
    rec = resource_index.get(subject) or {}
    url = rec.get("url") or ""
    if url:
        local = smithsonian_thumb({"id": url, "metadata": []})
        if local:
            return local
        if looks_like_manifest_url(url):
            return MANIFEST_THUMBS.get(url)
    return None


def emit_ontology_mentions(
    lines: List[str],
    mentions: List[Tuple[str, str, str, str]],
    episodes: Dict[str, EpisodeRec],
    persons: Dict[str, PersonRec],
    resource_index: Dict[str, Dict[str, str]],
    hits: List[Hit],
    indent: int = 0,
) -> None:
    if not mentions:
        lines.append(bullet(indent, "No other ontology files cite this person."))
        return
    thumbs = hit_thumb_index(hits)
    grouped: DefaultDict[str, List[Tuple[str, str, str]]] = defaultdict(list)
    for filename, subject, pred, token in mentions:
        grouped[filename].append((subject, pred, token))
    for filename in sorted(grouped):
        lines.append(bullet(indent, f"`{filename}`"))
        for subject, pred, token in grouped[filename]:
            rec = resource_index.get(subject) or {}
            label = (
                rec.get("label")
                or display_labels(episodes.get(subject) or persons.get(subject))
            )
            title = f"{label} (`{subject}`)" if label else f"`{subject}`"
            pred_bit = f" {pred}" if pred else ""
            text = f"{title} —{pred_bit} `{token}`"
            thumb = thumb_for_ontology_subject(subject, resource_index, thumbs)
            lines.append(bullet(indent + 1, with_thumb(text, thumb, label or subject)))


def emit_element(lines: List[str], elem: Dict[str, Any], indent: int) -> None:
    el_label = get_label_text(elem.get("elementLabel") or elem.get("label"))
    el_type = elem.get("elementType") or "ContentElement"
    thumb = thumbnail_for(elem, full_region=False, skip_keys=SKIP_THUMB_KEYS)
    heading = f"{el_type}: {el_label}"
    lines.append(bullet(indent, with_thumb(heading, thumb, el_label)))
    loud = elem.get("elementLOUD") or elem.get("loud") or []
    if loud:
        if isinstance(loud, str):
            loud = [loud]
        lines.append(
            bullet(indent + 1, f"**elementLOUD:** {', '.join(str(t) for t in loud)}")
        )


def emit_resources(
    lines: List[str],
    hits: List[Hit],
    heading_level: int,
) -> None:
    if not hits:
        lines.append("- No collection JSON fields mention this person.")
        lines.append("")
        return

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
        thumb = hit.get("resource_thumb") or hit.get("canvas_thumb")
        unique_id = str(hit.get("unique_id") or "")
        if prev is None:
            resource_meta[hit["resource_id"]] = (
                hit["resource_label"],
                thumb,
                unique_id,
            )
        elif not prev[1] and thumb:
            resource_meta[hit["resource_id"]] = (prev[0], thumb, prev[2] or unique_id)

    n_collections = len(grouped)
    n_resources = sum(len(v) for v in grouped.values())
    n_canvas = sum(1 for hit in hits if hit.get("match_source") == "ascanvas")
    n_meta = sum(1 for hit in hits if hit.get("match_source") == "metadata")
    n_ep = sum(1 for hit in hits if hit.get("match_source") == "related_episode")
    lines.append(
        bullet(
            0,
            f"**{n_collections} collection(s), {n_resources} resource(s), "
            f"{n_canvas} AsCanvas, {n_meta} metadata field, "
            f"{n_ep} related-episode**",
        )
    )
    lines.append("")

    def source_heading(hit: Hit) -> str:
        source = hit.get("match_source") or ""
        unique_id = str(hit.get("unique_id") or "")
        if source == "ascanvas":
            folio = hit.get("folio") or ""
            label = hit.get("canvas_label") or ""
            parts = ["AsCanvas"]
            if hit.get("mid"):
                parts.append(str(hit["mid"]))
            parts.append(f"f.{folio}" if folio else "canvas")
            heading = " — ".join(dict.fromkeys(parts))
            if label:
                heading = f"{heading} — {label}"
            return heading
        if source == "related_episode":
            heading = "Related narrative episode (person not named on the record)"
            if unique_id:
                heading = f"{heading} — {unique_id}"
            return heading
        heading = "Metadata / other fields"
        if unique_id:
            heading = f"{heading} — {unique_id}"
        return heading

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
                heading = source_heading(hit)
                thumb = hit.get("canvas_thumb") or hit.get("resource_thumb")
                lines.append(
                    md_heading(
                        min(heading_level + 3, 6),
                        with_thumb(heading, thumb, heading),
                    )
                )
                if hit.get("matched_tokens"):
                    lines.append(
                        bullet(
                            0,
                            f"**Matched tokens:** {', '.join(hit['matched_tokens'])}",
                        )
                    )
                if hit.get("fields"):
                    lines.append(bullet(0, "**Fields**"))
                    for field in hit["fields"]:
                        lines.append(bullet(1, md_escape(field)))
                if hit.get("related_episode"):
                    lines.append(
                        bullet(
                            0,
                            f"**Episode:** `{hit['related_episode']}`",
                        )
                    )
                matching = hit.get("matching_elements") or []
                if matching:
                    lines.append(bullet(0, "**Matching content elements**"))
                    for elem in matching:
                        emit_element(lines, elem, indent=1)
                lines.append("")


def unique_resource_count(hits: List[Hit]) -> Tuple[int, int]:
    resources = {(h["collection"], h["resource_id"]) for h in hits}
    fields = sum(len(h.get("fields") or []) for h in hits)
    return len(resources), fields


def emit_person_tree(
    lines: List[str],
    term: str,
    persons: Dict[str, PersonRec],
    episodes: Dict[str, EpisodeRec],
    incoming_family: Dict[str, Dict[str, Set[str]]],
    ontology_mentions: List[Tuple[str, str, str, str]],
    hits: List[Hit],
    resource_index: Dict[str, Dict[str, str]],
    heading_level: int,
) -> None:
    rec = persons.get(term)
    n_res, n_fields = unique_resource_count(hits)
    thumb = None
    for hit in hits:
        thumb = hit.get("canvas_thumb") or hit.get("resource_thumb")
        if thumb:
            break
    title = person_heading(term, rec) + count_suffix(n_res, n_fields)
    lines.append(md_heading(heading_level, with_thumb(title, thumb, term)))
    lines.append("")

    lines.append(md_heading(heading_level + 1, "Identity"))
    lines.append("")
    emit_identity(lines, term, rec)
    lines.append("")

    lines.append(md_heading(heading_level + 1, "SKOS and authority identifiers"))
    lines.append("")
    emit_skos(lines, rec)
    lines.append("")

    lines.append(md_heading(heading_level + 1, "Relations"))
    lines.append("")
    emit_relations(lines, term, rec, persons, incoming_family)
    lines.append("")

    lines.append(md_heading(heading_level + 1, "Narrative episodes"))
    lines.append("")
    emit_episodes(lines, term, rec, episodes)
    lines.append("")

    lines.append(md_heading(heading_level + 1, "Ontology citations"))
    lines.append("")
    emit_ontology_mentions(
        lines, ontology_mentions, episodes, persons, resource_index, hits
    )
    lines.append("")

    lines.append(md_heading(heading_level + 1, "Resources"))
    lines.append("")
    emit_resources(lines, hits, heading_level + 1)


def generate_markmap(
    selected: List[str],
    persons: Dict[str, PersonRec],
    episodes: Dict[str, EpisodeRec],
    incoming_family: Dict[str, Dict[str, Set[str]]],
    mentions_by_person: Dict[str, List[Tuple[str, str, str, str]]],
    hits_by_person: Dict[str, List[Hit]],
    resource_index: Dict[str, Dict[str, str]],
) -> List[str]:
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
        emit_person_tree(
            lines,
            term,
            persons,
            episodes,
            incoming_family,
            mentions_by_person.get(term) or [],
            hits_by_person.get(term) or [],
            resource_index,
            1,
        )
        return lines

    lines.append("# Agential associations")
    lines.append("")
    lines.append(bullet(0, f"**Selected persons:** {', '.join(selected)}"))
    lines.append(
        "- Root of this Markmap is the selected person array (`INPUT_PERSONS` / `--person`)."
    )
    lines.append("")
    for term in selected:
        emit_person_tree(
            lines,
            term,
            persons,
            episodes,
            incoming_family,
            mentions_by_person.get(term) or [],
            hits_by_person.get(term) or [],
            resource_index,
            2,
        )
    return lines


def slug_for(selected: List[str]) -> str:
    parts = [term.split(":", 1)[-1] for term in selected]
    slug = "_".join(parts)
    slug = re.sub(r"[^\w]+", "_", slug).strip("_")
    return slug[:80] or "persons"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a Markmap of hierarchical associations around the "
            "persons listed in INPUT_PERSONS."
        )
    )
    parser.add_argument(
        "--person",
        action="append",
        dest="persons",
        default=None,
        help="Person CURIE (repeatable). Defaults to INPUT_PERSONS.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output Markmap Markdown file path.",
    )
    parser.add_argument(
        "--no-manifest-fetch",
        action="store_true",
        help="Do not HTTP-fetch remote IIIF manifests for first-canvas thumbnails.",
    )
    parser.add_argument(
        "--manifest-timeout",
        type=int,
        default=8,
        help="Timeout in seconds for each manifest fetch.",
    )
    args = parser.parse_args()
    global MANIFEST_THUMBS
    MANIFEST_THUMBS = ManifestThumbCache(
        enabled=not args.no_manifest_fetch,
        timeout=max(1, args.manifest_timeout),
    )

    raw_selected = args.persons if args.persons else list(INPUT_PERSONS)
    selected: List[str] = []
    seen: Set[str] = set()
    for raw in raw_selected:
        term = normalize_person(raw)
        if term and term not in seen:
            seen.add(term)
            selected.append(term)
    if not selected:
        raise SystemExit("At least one person must be defined in INPUT_PERSONS.")

    print("Loading PersonsRDFData.ttl ...")
    persons = parse_persons(PERSONS_TTL)
    print(f"  {len(persons)} person records")
    print("Loading narrative_episodes.ttl ...")
    episodes = parse_episodes(NARRATIVE_TTL)
    print(f"  {len(episodes)} episode records")
    print("Loading resource URLs from resources.ttl ...")
    resource_index = parse_resource_index(RESOURCES_TTL)
    print(f"  {len(resource_index)} resources with mdhn:hasUrl")
    incoming_family = reverse_family(persons)

    resolved: List[str] = []
    for term in selected:
        if term not in persons:
            print(f"  warning: {term} was not found in PersonsRDFData.ttl")
        resolved.append(term)

    hits_by_person: Dict[str, List[Hit]] = {}
    mentions_by_person: Dict[str, List[Tuple[str, str, str, str]]] = {}
    print("Scanning ontology TTL and collection JSON ...")
    for term in resolved:
        rec = persons.get(term)
        tokens = identity_tokens(term, rec)
        patterns = compile_token_patterns(tokens)
        involved_list, mentioned_list = related_episodes(term, rec, episodes)
        involved_episodes = set(involved_list) | set(mentioned_list)
        mentions = scan_ttl_incoming(
            ONTOLOGY_DIR,
            {term} | (rec["saidToBeTheSameAs"] if rec else set()),
            skip_names=SKIP_TTL_SCAN,
        )
        mentions_by_person[term] = mentions
        hits = collect_collection_hits(patterns, involved_episodes)
        hits_by_person[term] = hits
        n_res, n_fields = unique_resource_count(hits)
        print(
            f"  {term}: {len(tokens)} identity tokens, "
            f"{n_res} resources, {n_fields} field paths, "
            f"{len(involved_episodes)} episodes, {len(mentions)} ontology citations"
        )

    lines = generate_markmap(
        resolved,
        persons,
        episodes,
        incoming_family,
        mentions_by_person,
        hits_by_person,
        resource_index,
    )
    output = args.output
    if output is None:
        output = REPORTS_DIR / f"persons_markmap_{slug_for(resolved)}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE {output}")
    print(
        f"manifest fetches: {MANIFEST_THUMBS.fetched} "
        f"(ok {MANIFEST_THUMBS.ok}, failed {MANIFEST_THUMBS.failed})"
    )


if __name__ == "__main__":
    main()
