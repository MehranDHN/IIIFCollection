#!/usr/bin/env python3
"""
IIIF Manuscript Canvas Decomposition → Markmap Markdown Generator (enhanced)

Copy of generate_canvas_markmap.py with three additions:
  1. Canvas-level depicts as a heading tree (after Canvas Types / Contains)
     so markmap keeps isPartOf / SKOS nesting. Each tag lists its Wikidata
     Q-code (from mdhn:icWikiDataURL, Q-code only) and every SKOS relation.
  2. Whole-canvas thumbnail on the ResourceCanvas heading itself (not a sibling
     list item): IIIF region /x,y,w,h/ is rewritten to /full/ and the size
     segment is rewritten to /THUMBNAIL_WIDTH,/.
  3. Iconography tags (elementLOUD) list every SKOS relation of that tag, if any.

The original generate_canvas_markmap.py is left unchanged.
"""

import os
import re
from collections import defaultdict
from typing import Any, DefaultDict, Dict, List, Optional, Set, Tuple
from urllib.parse import urlsplit, urlunsplit

# ================== CONFIGURATION ==================
INPUT_DIR: str = r"C:\Users\Mehran\IIIFCollection-1\IIIFCollection"
OUTPUT_DIR: str = r"C:\Users\Mehran\IIIFCollection-1\IIIFCollection\tools\visualization"
ONTOLOGY_DIR: str = os.path.join(INPUT_DIR, "Ontology")

INPUT_JSON_FILES: List[str] = [
    "PeckShahnamaCollection.json",
    "ShahnamaMsorfol4251Collection.json",
    "ShahnamaMsorfol359Collection.json",
    "JukiShahnamaCollection.json",
    "ShahnameShahTahmasbCollection.json",
    "IbrahimSultanShahnamaCollection.json",
    "ShahnamaSmithLesouef224Collection.json",
    "SmallIlkhanidShahnameCollection.json",
    "HaftOwrangIbrahimSultanCollection.json",
    "DepartedFolioCollection.json",
    "TarikhnamaByBalamiCollection.json",
    "MiscReportAndLetterCollection.json",
    "QisasalAnbiyaCollection.json",
    "Qisas_al_Anbiya_PersianMS46Collection.json",
    "Qisas_al_Anbiya_PersianMS1Collection.json"
    # Add more filenames here
]

ONTOLOGY_FILES: List[str] = [
    "iconography_RDF.ttl",
    "PersonsRDFData.ttl",
    "narrative_episodes.ttl",
    "iconclass_hierarchy.ttl",
    "ctl_vocabs.ttl",
]

# Integer width used for the IIIF size segment: /{THUMBNAIL_WIDTH},/
THUMBNAIL_WIDTH: int = 200
# Default number of Markmap levels expanded in the generated document.
INITIAL_EXPAND_LEVEL: int = 8
OUTPUT_FILE: str = os.path.join(OUTPUT_DIR, "iiif_decomposition_markmap_enhanced.md")
# ===================================================

SkosIndex = Dict[str, Dict[str, Set[str]]]

CONTENT_KEYS: List[str] = [
    "croppedFigures",
    "croppedPatterns",
    "linguisticElements",
    "ContentElement",
    "elements",
]

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
SUBJECT_RE = re.compile(r"^(mdhn:[A-Za-z0-9_]+)\b")
SUBJECT_DECL_RE = re.compile(r"^(mdhn:[A-Za-z0-9_]+)\s+a\b")
SKOS_PRED_RE = re.compile(r"^(skos:[A-Za-z]+)\s+(.+)$")
HIERARCHY_SKOS = {"skos:broader", "skos:broadMatch"}
SKOS_OBJECT_RE = re.compile(
    r"<[^>]+>|[A-Za-z][A-Za-z0-9_-]*:[A-Za-z0-9_.:/%()'-]+"
)
MDHN_TERM_RE = re.compile(r"mdhn:[A-Za-z0-9_]+")
WIKIDATA_LINE_RE = re.compile(r'mdhn:icWikiDataURL\s+"([^"]*)"')
QCODE_RE = re.compile(r"Q\d+", re.IGNORECASE)


def get_label_text(label: Any) -> str:
    if isinstance(label, str):
        return label
    if isinstance(label, dict):
        for key in ('en', 'none', 'fa'):
            if key in label and label[key]:
                val = label[key]
                return val[0] if isinstance(val, list) else str(val)
    return str(label) if label is not None else "Unnamed"


def normalize_term(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.startswith("<") and text.endswith(">"):
        text = text[1:-1].strip()
    found = MDHN_TERM_RE.findall(text)
    if found:
        return found[0]
    if text.startswith("mdhn:"):
        return text
    if ":" not in text and re.match(r"^[A-Za-z][A-Za-z0-9_]*$", text):
        return f"mdhn:{text}"
    return text


def get_thumbnail_url(iiif_url: str, width: int = THUMBNAIL_WIDTH) -> Optional[str]:
    """Resize a cropped IIIF image; keep the existing region (element crops)."""
    if not iiif_url or not isinstance(iiif_url, str):
        return None
    if '/full/' in iiif_url:
        return iiif_url.replace('/full/', f'/{width},/')
    if '/max/' in iiif_url:
        return iiif_url.replace('/max/', f'/{width},/')
    return iiif_url


def _iiif_path_segments(iiif_url: str) -> Optional[Tuple[urlsplit, List[str]]]:
    if not iiif_url or not isinstance(iiif_url, str):
        return None
    parsed = urlsplit(iiif_url)
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


def get_full_canvas_thumbnail_url(
    iiif_url: str, width: int = THUMBNAIL_WIDTH
) -> Optional[str]:
    """Whole-canvas thumbnail: region /x,y,w,h/ → /full/, size → /{width},/."""
    parsed_segs = _iiif_path_segments(iiif_url)
    if parsed_segs is None:
        return None
    parsed, segs = parsed_segs
    segs[-4] = "full"
    segs[-3] = f"{width},"
    return urlunsplit(
        (parsed.scheme, parsed.netloc, "/".join(segs), parsed.query, parsed.fragment)
    )


def find_first_iiif_image(node: Any) -> Optional[str]:
    if isinstance(node, dict):
        for key in ("croppedImage", "image"):
            val = node.get(key)
            if isinstance(val, str) and val:
                return val
        for key in CONTENT_KEYS + ["Element"]:
            found = find_first_iiif_image(node.get(key))
            if found:
                return found
        return None
    if isinstance(node, list):
        for item in node:
            found = find_first_iiif_image(item)
            if found:
                return found
    return None


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


def subject_from_line(line: str) -> Optional[str]:
    """Only a Turtle type declaration starts a new subject (not mdhn:isPartOf etc.)."""
    match = SUBJECT_DECL_RE.match(line)
    return match.group(1) if match else None


def parse_skos_file(path: str) -> SkosIndex:
    concepts: DefaultDict[str, DefaultDict[str, Set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    if not os.path.exists(path):
        print(f"⚠️  Ontology file not found: {path}")
        return {}

    current_subject: Optional[str] = None
    in_triple = False

    with open(path, "r", encoding="utf-8") as handle:
        for raw in handle:
            if in_triple:
                if '"""' in raw:
                    in_triple = False
                    after = raw.rsplit('"""', 1)[-1].strip()
                    if after.endswith("."):
                        current_subject = None
                continue

            line = strip_turtle_comment(raw)
            if not line or line.startswith("@prefix") or line.startswith("@base"):
                continue

            if '"""' in line and line.count('"""') == 1:
                in_triple = True
                declared = subject_from_line(line)
                if declared:
                    current_subject = declared
                continue

            declared = subject_from_line(line)
            if declared:
                current_subject = declared

            if current_subject is not None:
                pred_match = SKOS_PRED_RE.match(line)
                if pred_match:
                    predicate = pred_match.group(1)
                    for obj in SKOS_OBJECT_RE.findall(pred_match.group(2)):
                        if obj == current_subject:
                            continue
                        concepts[current_subject][predicate].add(obj)

            if line.endswith("."):
                current_subject = None

    return {term: dict(rels) for term, rels in concepts.items()}


def load_skos_index() -> Tuple[SkosIndex, Dict[str, str]]:
    merged: DefaultDict[str, DefaultDict[str, Set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    for filename in ONTOLOGY_FILES:
        parsed = parse_skos_file(os.path.join(ONTOLOGY_DIR, filename))
        for term, rels in parsed.items():
            for pred, objs in rels.items():
                merged[term][pred].update(objs)

    exact: SkosIndex = {term: dict(rels) for term, rels in merged.items()}
    casefold_keys = {term.lower(): term for term in exact}
    return exact, casefold_keys


def extract_qcode(raw: Any) -> Optional[str]:
    if raw is None:
        return None
    match = QCODE_RE.search(str(raw).strip())
    return match.group(0).upper() if match else None


def parse_wikidata_file(path: str) -> Dict[str, str]:
    codes: Dict[str, str] = {}
    if not os.path.exists(path):
        return codes

    current_subject: Optional[str] = None
    in_triple = False
    with open(path, "r", encoding="utf-8") as handle:
        for raw in handle:
            if in_triple:
                if '"""' in raw:
                    in_triple = False
                    after = raw.rsplit('"""', 1)[-1].strip()
                    if after.endswith("."):
                        current_subject = None
                continue

            line = strip_turtle_comment(raw)
            if not line or line.startswith("@prefix") or line.startswith("@base"):
                continue

            if '"""' in line and line.count('"""') == 1:
                in_triple = True
                declared = subject_from_line(line)
                if declared:
                    current_subject = declared
                continue

            declared = subject_from_line(line)
            if declared:
                current_subject = declared

            if current_subject is not None:
                wiki_match = WIKIDATA_LINE_RE.search(line)
                if wiki_match:
                    qcode = extract_qcode(wiki_match.group(1))
                    if qcode:
                        codes[current_subject] = qcode

            if line.endswith("."):
                current_subject = None
    return codes


def load_wikidata_index() -> Tuple[Dict[str, str], Dict[str, str]]:
    merged: Dict[str, str] = {}
    for filename in ONTOLOGY_FILES:
        merged.update(parse_wikidata_file(os.path.join(ONTOLOGY_DIR, filename)))
    casefold_keys = {term.lower(): term for term in merged}
    return merged, casefold_keys


def parse_hierarchy_file(path: str) -> Dict[str, Set[str]]:
    """Collect mdhn:isPartOf parents for each concept."""
    parents: DefaultDict[str, Set[str]] = defaultdict(set)
    if not os.path.exists(path):
        return {}

    current_subject: Optional[str] = None
    in_triple = False
    with open(path, "r", encoding="utf-8") as handle:
        for raw in handle:
            if in_triple:
                if '"""' in raw:
                    in_triple = False
                    after = raw.rsplit('"""', 1)[-1].strip()
                    if after.endswith("."):
                        current_subject = None
                continue

            line = strip_turtle_comment(raw)
            if not line or line.startswith("@prefix") or line.startswith("@base"):
                continue

            if '"""' in line and line.count('"""') == 1:
                in_triple = True
                declared = subject_from_line(line)
                if declared:
                    current_subject = declared
                continue

            declared = subject_from_line(line)
            if declared:
                current_subject = declared

            if current_subject is not None and line.startswith("mdhn:isPartOf"):
                for obj in MDHN_TERM_RE.findall(line):
                    if obj not in ("mdhn:isPartOf", current_subject):
                        parents[current_subject].add(obj)

            if line.endswith("."):
                current_subject = None
    return dict(parents)


def load_hierarchy_index() -> Tuple[Dict[str, Set[str]], Dict[str, str]]:
    merged: DefaultDict[str, Set[str]] = defaultdict(set)
    for filename in ONTOLOGY_FILES:
        parsed = parse_hierarchy_file(os.path.join(ONTOLOGY_DIR, filename))
        for term, vals in parsed.items():
            merged[term].update(vals)
    exact = {term: set(vals) for term, vals in merged.items()}
    casefold_keys = {term.lower(): term for term in exact}
    return exact, casefold_keys


def lookup_is_part_of(
    tag: str, hierarchy_index: Dict[str, Set[str]], casefold_keys: Dict[str, str]
) -> Set[str]:
    term = normalize_term(tag)
    if not term:
        return set()
    if term in hierarchy_index:
        return set(hierarchy_index[term])
    canonical = casefold_keys.get(term.lower())
    if canonical:
        return set(hierarchy_index.get(canonical, set()))
    return set()


def lookup_qcode(
    tag: str, wikidata_index: Dict[str, str], casefold_keys: Dict[str, str]
) -> Optional[str]:
    term = normalize_term(tag)
    if not term:
        return None
    if term in wikidata_index:
        return wikidata_index[term]
    canonical = casefold_keys.get(term.lower())
    if canonical:
        return wikidata_index.get(canonical)
    return None


def lookup_skos(
    tag: str, skos_index: SkosIndex, casefold_keys: Dict[str, str]
) -> Dict[str, Set[str]]:
    term = normalize_term(tag)
    if not term:
        return {}
    if term in skos_index:
        return skos_index[term]
    canonical = casefold_keys.get(term.lower())
    if canonical:
        return skos_index.get(canonical, {})
    return {}


def md_heading(level: int, text: str) -> str:
    """Markdown headings (h1–h6) are the structure markmap actually renders."""
    return f"{'#' * max(1, min(level, 6))} {text}"


def format_tag_details(
    tag: str,
    skos_index: SkosIndex,
    skos_casefold: Dict[str, str],
    wikidata_index: Optional[Dict[str, str]] = None,
    wikidata_casefold: Optional[Dict[str, str]] = None,
    hierarchy_index: Optional[Dict[str, Set[str]]] = None,
    hierarchy_casefold: Optional[Dict[str, str]] = None,
) -> List[str]:
    """One-level list of Q-code / isPartOf / SKOS (safe as markmap children)."""
    lines: List[str] = []
    qcode = lookup_qcode(tag, wikidata_index or {}, wikidata_casefold or {})
    if qcode:
        lines.append(f"- {qcode}")
    parents = lookup_is_part_of(tag, hierarchy_index or {}, hierarchy_casefold or {})
    if parents:
        lines.append(f"- mdhn:isPartOf: {', '.join(sorted(parents))}")
    relations = lookup_skos(tag, skos_index, skos_casefold)
    for pred in sorted(relations):
        objects = sorted(relations[pred])
        if objects:
            lines.append(f"- {pred}: {', '.join(objects)}")
    return lines


def structural_parents(
    tag: str,
    skos_index: SkosIndex,
    skos_casefold: Dict[str, str],
    hierarchy_index: Dict[str, Set[str]],
    hierarchy_casefold: Dict[str, str],
) -> List[str]:
    """Parents used to nest depicts: isPartOf, skos:broader, skos:broadMatch."""
    parents: List[str] = []
    seen: Set[str] = set()
    for parent in sorted(lookup_is_part_of(tag, hierarchy_index, hierarchy_casefold)):
        if parent not in seen:
            seen.add(parent)
            parents.append(parent)
    relations = lookup_skos(tag, skos_index, skos_casefold)
    for pred in HIERARCHY_SKOS:
        for parent in sorted(relations.get(pred, set())):
            if parent not in seen:
                seen.add(parent)
                parents.append(parent)
    return parents


def format_depicts_hierarchy(
    tags: List[Any],
    skos_index: SkosIndex,
    skos_casefold: Dict[str, str],
    wikidata_index: Dict[str, str],
    wikidata_casefold: Dict[str, str],
    hierarchy_index: Dict[str, Set[str]],
    hierarchy_casefold: Dict[str, str],
    heading_level: int = 3,
) -> List[str]:
    """Depicts tree as headings so markmap keeps every nesting level."""
    items: List[Tuple[str, str]] = []
    for raw in tags:
        if not raw:
            continue
        tag = str(raw)
        term = normalize_term(tag) or tag
        items.append((tag, term))

    present = {term for _, term in items}
    children: DefaultDict[str, List[Tuple[str, str]]] = defaultdict(list)
    roots: List[Tuple[str, str]] = []
    attached: Set[str] = set()

    for tag, term in items:
        in_list = [
            parent
            for parent in structural_parents(
                term, skos_index, skos_casefold, hierarchy_index, hierarchy_casefold
            )
            if parent in present
        ]
        if in_list and term not in in_list:
            children[in_list[0]].append((tag, term))
            attached.add(term)
        else:
            roots.append((tag, term))

    # A tag that was also chosen as a root (appears twice, or parent missing)
    # should not be emitted twice if it was attached as a child.
    roots = [(tag, term) for tag, term in roots if term not in attached]

    lines = [md_heading(heading_level, "Depicts"), ""]

    def emit(tag: str, term: str, level: int, stack: Set[str]) -> None:
        lines.append(md_heading(level, tag))
        details = format_tag_details(
            tag,
            skos_index,
            skos_casefold,
            wikidata_index,
            wikidata_casefold,
            hierarchy_index,
            hierarchy_casefold,
        )
        lines.extend(details)
        lines.append("")
        if term in stack:
            return
        next_stack = set(stack)
        next_stack.add(term)
        for child_tag, child_term in children.get(term, []):
            emit(child_tag, child_term, min(level + 1, 6), next_stack)

    for tag, term in roots:
        emit(tag, term, min(heading_level + 1, 6), set())
    return lines


def format_iconography_tags(
    loud: List[Any],
    skos_index: SkosIndex,
    casefold_keys: Dict[str, str],
    wikidata_index: Optional[Dict[str, str]] = None,
    wikidata_casefold: Optional[Dict[str, str]] = None,
    hierarchy_index: Optional[Dict[str, Set[str]]] = None,
    hierarchy_casefold: Optional[Dict[str, str]] = None,
    heading_level: int = 4,
) -> List[str]:
    lines = [md_heading(heading_level, "Iconography Tags (elementLOUD)"), ""]
    for raw_tag in loud:
        tag = str(raw_tag)
        lines.append(md_heading(min(heading_level + 1, 6), tag))
        lines.extend(
            format_tag_details(
                tag,
                skos_index,
                casefold_keys,
                wikidata_index,
                wikidata_casefold,
                hierarchy_index,
                hierarchy_casefold,
            )
        )
        lines.append("")
    return lines


def process_content_element(
    elem: Dict[str, Any],
    element_type_fallback: str = "ContentElement",
    skos_index: Optional[SkosIndex] = None,
    casefold_keys: Optional[Dict[str, str]] = None,
    wikidata_index: Optional[Dict[str, str]] = None,
    wikidata_casefold: Optional[Dict[str, str]] = None,
    hierarchy_index: Optional[Dict[str, Set[str]]] = None,
    hierarchy_casefold: Optional[Dict[str, str]] = None,
) -> List[str]:
    skos_index = skos_index or {}
    casefold_keys = casefold_keys or {}
    lines: List[str] = []
    el_label = get_label_text(elem.get('elementLabel') or elem.get('label'))
    el_type = elem.get('elementType', element_type_fallback)

    lines.append(f"### {el_type}: {el_label}")

    cropped_img = elem.get('croppedImage') or elem.get('image')
    thumb = get_thumbnail_url(cropped_img)
    if thumb:
        #lines.append(f"- **{el_label}** ![ {el_label} ]({thumb})")
        lines.append(f"#### **{el_label}** ![ {el_label} ]({thumb})")

    styles = elem.get('elementStyle', []) or elem.get('style', [])
    if styles:
        lines.append(f"- **Styles:** {', '.join(str(s) for s in styles)}")

    fa_text = elem.get('elementFAText', '') or elem.get('faText', '')
    en_text = elem.get('elementENText', '') or elem.get('enText', '')
    if fa_text:
        lines.append(f"- **Persian Text:** {fa_text}")
    if en_text:
        lines.append(f"- **English Text:** {en_text}")

    loud = elem.get('elementLOUD', []) or elem.get('loud', [])
    if loud:
        lines.append("")
        lines.extend(
            format_iconography_tags(
                loud,
                skos_index,
                casefold_keys,
                wikidata_index,
                wikidata_casefold,
                hierarchy_index,
                hierarchy_casefold,
                heading_level=4,
            )
        )

    if 'Element' in elem and isinstance(elem.get('Element'), list):
        lines.append("- **Sub-Elements:**")
        for sub_elem in elem['Element']:
            sub_lines = process_content_element(
                sub_elem,
                "Sub-Element",
                skos_index,
                casefold_keys,
                wikidata_index,
                wikidata_casefold,
                hierarchy_index,
                hierarchy_casefold,
            )
            lines.extend(["    " + line for line in sub_lines])

    lines.append("")
    return lines


def extract_canvas_entries(metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    canvas_entries: List[Dict[str, Any]] = []

    for meta in metadata:
        label_text = get_label_text(meta.get('label'))
        if not label_text:
            continue

        normalized_label = label_text.strip().lower()
        if 'states' not in normalized_label and 'ascanvas' not in normalized_label:
            continue

        value = meta.get('value', {})
        raw_entries: Any = []
        if isinstance(value, dict):
            if 'en' in value:
                raw_entries = value['en']
            else:
                for candidate in value.values():
                    if (
                        isinstance(candidate, list)
                        and candidate
                        and isinstance(candidate[0], dict)
                        and any(
                            key in candidate[0]
                            for key in ('depicts', 'folio', 'canvasType', 'croppedFigures')
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


def generate_markmap_from_json(
    json_path: str,
    skos_index: SkosIndex,
    casefold_keys: Dict[str, str],
    wikidata_index: Optional[Dict[str, str]] = None,
    wikidata_casefold: Optional[Dict[str, str]] = None,
    hierarchy_index: Optional[Dict[str, Set[str]]] = None,
    hierarchy_casefold: Optional[Dict[str, str]] = None,
) -> List[str]:
    import json

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    manuscript_label = get_label_text(data.get('label', os.path.basename(json_path)))
    lines = [f"# {manuscript_label}"]
    lines.append("")
    lines.append("**Hierarchical Canvas Decomposition (ResourceCanvas → Content Elements)**")
    lines.append("")

    manifests = data.get('manifests', []) or [data]

    for manifest in manifests:
        manifest_label = get_label_text(manifest.get('label', 'Manifest'))
        metadata = manifest.get('metadata', [])
        canvas_entries = extract_canvas_entries(metadata)

        if not canvas_entries:
            continue

        lines.append(f"## Manifest: {manifest_label}")
        lines.append("")

        for state in canvas_entries:
            folio = state.get('folio', '')
            label = get_label_text(state.get('label'))

            source_image = find_first_iiif_image(state)
            canvas_thumb = (
                get_full_canvas_thumbnail_url(source_image) if source_image else None
            )
            heading = f"## ResourceCanvas: f.{folio} — {label}"
            if canvas_thumb:
                heading = f"{heading} ![Canvas thumbnail](<{canvas_thumb}>)"
            lines.append(heading)

            if state.get('canvasType'):
                lines.append(f"- **Canvas Types:** {', '.join(state['canvasType'])}")
            if state.get('folioContains'):
                lines.append(f"- **Contains:** {', '.join(state['folioContains'])}")
            depicts = state.get('depicts') or []
            if isinstance(depicts, str):
                depicts = [depicts]
            if depicts:
                lines.append("")
                lines.extend(
                    format_depicts_hierarchy(
                        depicts,
                        skos_index,
                        casefold_keys,
                        wikidata_index or {},
                        wikidata_casefold or {},
                        hierarchy_index or {},
                        hierarchy_casefold or {},
                    )
                )

            lines.append("")

            for key in CONTENT_KEYS:
                elems = state.get(key, [])
                if not elems:
                    continue
                for elem in elems:
                    elem_lines = process_content_element(
                        elem,
                        key.rstrip('s').title(),
                        skos_index,
                        casefold_keys,
                        wikidata_index,
                        wikidata_casefold,
                        hierarchy_index,
                        hierarchy_casefold,
                    )
                    lines.extend(elem_lines)

            lines.append("---")
            lines.append("")

    return lines


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("📚 Loading SKOS relations from ontology files...")
    skos_index, casefold_keys = load_skos_index()
    wikidata_index, wikidata_casefold = load_wikidata_index()
    hierarchy_index, hierarchy_casefold = load_hierarchy_index()
    print(f"   → {len(skos_index)} concepts with at least one SKOS relation")
    print(f"   → {len(wikidata_index)} concepts with a Wikidata Q-code")
    print(f"   → {len(hierarchy_index)} concepts with mdhn:isPartOf parents")

    all_lines: List[str] = []
    all_lines.append("---")
    all_lines.append("markmap:")
    all_lines.append(f"  initialExpandLevel: {INITIAL_EXPAND_LEVEL}")
    all_lines.append("  maxWidth: 360")
    all_lines.append("---")
    all_lines.append("")
    all_lines.append("اين گزارش بوسيله ماشين تهيه شده و به منظور تست صحت اطلاعات و ساختار مدل اطلاعات ساختار يافته و رابطه های سلسله مراتبی اجزای يک صفحه از نسخه دستنويس يا نگاره طراحی شده . ")
    all_lines.append("")
    all_lines.append("---")
    all_lines.append("Testing Canvas decomposition to Multiple type of ContentElement **Machine generated report**")        
    for filename in INPUT_JSON_FILES:
        json_path = os.path.join(INPUT_DIR, filename)
        if not os.path.exists(json_path):
            print(f"⚠️  File not found: {json_path}")
            continue
        print(f"📄 Processing: {json_path}")
        file_lines = generate_markmap_from_json(
            json_path,
            skos_index,
            casefold_keys,
            wikidata_index,
            wikidata_casefold,
            hierarchy_index,
            hierarchy_casefold,
        )
        all_lines.extend(file_lines)
        all_lines.append("\n\n")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_lines))

    print(f"\n✅ Enhanced markmap document successfully generated:\n{OUTPUT_FILE}")
    print("   → Open it in VS Code with the Markmap extension or at https://markmap.js.org/")


if __name__ == "__main__":
    main()
