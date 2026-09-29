#!/usr/bin/env python3
"""
Independent narrative-episode tree → Markdown.

Start from one term (for example mdhn:Shahnameh) and walk narrower
episodes via mdhn:isPartOf / mdhn:ispartOf in Ontology/narrative_episodes.ttl.

A second parameter chooses how much of that subtree to emit:

    all              every narrower episode
    with-resources   only episodes that have at least one associated
                     resource, plus the ancestors needed to keep the
                     path from the root (empty branches are pruned)

Resource associations come from local *Collection.json files in the
IIIFCollection folder: canvas-level ``depicts`` arrays and the
resource metadata field labeled Depicts. Each listed resource shows
its label and the collection it belongs to.

Episode headings keep the **direct** resource count (terms listed on
that episode itself) and add an **including narrower** total: unique
resources tagged with the episode or any descendant via ``isPartOf``.
A resource tagged on both a kingdom and a scene under it counts once
in the accumulated total. The same descendant is not counted twice
when it has more than one parent.

Example:

    python generate_narrative_episode_tree.py --root mdhn:Shahnameh --scope all
    python generate_narrative_episode_tree.py --root mdhn:Shahnameh --scope with-resources
    python generate_narrative_episode_tree.py --root mdhn:Kolliat_of_Saadi --scope with-resources
    python generate_narrative_episode_tree.py --root mdhn:Kolliat_of_Saadi --scope all    
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, DefaultDict, Dict, Iterable, List, Optional, Set, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
COLLECTION_DIR = SCRIPT_DIR.parents[1]
ONTOLOGY_PATH = COLLECTION_DIR / "Ontology" / "narrative_episodes.ttl"
REPORTS_DIR = SCRIPT_DIR / "reports"

DEFAULT_ROOT = "mdhn:Shahnameh"
SCOPES = ("all", "with-resources")

MDHN_TERM_RE = re.compile(r"mdhn:[A-Za-z0-9_]+")
SUBJECT_START_RE = re.compile(r"^(mdhn:[A-Za-z0-9_]+)\b")
LABEL_RE = re.compile(r'"((?:\\.|[^"\\])*)"(?:@([A-Za-z-]+))?')
WIKI_RE = re.compile(r'mdhn:icWikiDataURL\s+"([^"]*)"')
# Whitelist of Turtle predicates. Checked *before* SUBJECT_START_RE because
# CURIEs such as mdhn:aatConcept also match mdhn:Term and would otherwise
# steal the rest of the block (labels, isPartOf, wiki) from the real episode.
PRED_START_RE = re.compile(
    r"^(mdhn:is[Pp]artOf|mdhn:icWikiDataURL|rdfs:label|rdfs:comment|"
    r"mdhn:charactersInvolved|mdhn:characterInvolved|skos:[A-Za-z]+|"
    r"mdhn:aatConcept|mdhn:startVerse|mdhn:endVerse|dcterms:[A-Za-z]+|"
    r"owl:[A-Za-z]+|rdf:type|a)\b"
)

Episode = Dict[str, Any]
ResourceHit = Dict[str, str]


def normalize_term(value: str) -> str:
    text = value.strip()
    if not text:
        return text
    if text.startswith("mdhn:"):
        return text
    if re.match(r"^[A-Za-z][A-Za-z0-9_]*$", text):
        return f"mdhn:{text}"
    return text


def unescape_literal(value: str) -> str:
    return (
        value.replace(r"\"", '"')
        .replace(r"\n", " ")
        .replace(r"\t", " ")
        .replace("\\\\", "\\")
    )


def get_label_text(label: Any) -> str:
    if isinstance(label, str):
        return label.strip()
    if isinstance(label, dict):
        for key in ("en", "none", "fa"):
            if key in label and label[key]:
                val = label[key]
                return str(val[0] if isinstance(val, list) else val).strip()
        for val in label.values():
            text = get_label_text(val)
            if text:
                return text
    if isinstance(label, list) and label:
        return get_label_text(label[0])
    return str(label).strip() if label is not None else ""


def metadata_label_key(value: Any) -> str:
    return get_label_text(value).strip().lower()


def is_depicts_field_label(value: Any) -> bool:
    return metadata_label_key(value) == "depicts"


def extract_mdhn_terms(value: Any) -> List[str]:
    terms: List[str] = []
    seen: Set[str] = set()

    def add(term: str) -> None:
        if term and term not in seen:
            seen.add(term)
            terms.append(term)

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for nested in node.values():
                walk(nested)
        elif isinstance(node, list):
            for nested in node:
                walk(nested)
        elif isinstance(node, str):
            for term in MDHN_TERM_RE.findall(node):
                add(term)

    walk(value)
    return terms


def collect_depicts_key_terms(node: Any) -> List[str]:
    """mdhn: terms from any JSON key named depicts (canvas AsCanvas, etc.)."""
    terms: List[str] = []
    seen: Set[str] = set()

    def add_all(values: Iterable[str]) -> None:
        for term in values:
            if term not in seen:
                seen.add(term)
                terms.append(term)

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            for key, nested in obj.items():
                if str(key).lower() == "depicts":
                    add_all(extract_mdhn_terms(nested))
                else:
                    walk(nested)
        elif isinstance(obj, list):
            for nested in obj:
                walk(nested)

    walk(node)
    return terms


def collect_metadata_depicts_terms(resource: Dict[str, Any]) -> List[str]:
    terms: List[str] = []
    seen: Set[str] = set()
    metadata = resource.get("metadata") or []
    if not isinstance(metadata, list):
        return terms
    for meta in metadata:
        if not isinstance(meta, dict) or not is_depicts_field_label(meta.get("label")):
            continue
        for term in extract_mdhn_terms(meta.get("value")):
            if term not in seen:
                seen.add(term)
                terms.append(term)
    return terms


def resource_terms(resource: Dict[str, Any]) -> List[str]:
    terms: List[str] = []
    seen: Set[str] = set()
    for term in collect_depicts_key_terms(resource) + collect_metadata_depicts_terms(
        resource
    ):
        if term not in seen:
            seen.add(term)
            terms.append(term)
    return terms


def iter_collection_resources(collection: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    for key in ("manifests", "items", "members"):
        values = collection.get(key) or []
        if isinstance(values, list):
            for item in values:
                if isinstance(item, dict):
                    yield item


def _skip_hashes(line: str) -> str:
    in_string = False
    escaped = False
    chars: List[str] = []
    for ch in line:
        if in_string:
            chars.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            chars.append(ch)
            continue
        if ch == "#":
            break
        chars.append(ch)
    return "".join(chars)


def parse_narrative_episodes(path: Path) -> Dict[str, Episode]:
    """Parse narrative_episodes.ttl without rdflib.

    Treats mdhn:isPartOf and mdhn:ispartOf as the same parent link.
    Extra triples on an already-declared subject are merged (Turtle union).
    """
    episodes: Dict[str, Episode] = {}
    text = path.read_text(encoding="utf-8")
    in_triple_quote = False
    current: Optional[str] = None
    current_pred: Optional[str] = None
    pending_parents: List[str] = []
    order = 0

    def ensure(term: str) -> Episode:
        nonlocal order
        rec = episodes.get(term)
        if rec is None:
            rec = {
                "id": term,
                "labels": {"en": [], "fa": [], "none": []},
                "parents": [],
                "wiki": "",
                "order": order,
            }
            episodes[term] = rec
            order += 1
        return rec

    def add_label(term: str, value: str, lang: Optional[str]) -> None:
        rec = ensure(term)
        bucket = (lang or "none").split("-")[0].lower()
        if bucket not in rec["labels"]:
            rec["labels"][bucket] = []
        cleaned = unescape_literal(value).strip()
        if cleaned and cleaned not in rec["labels"][bucket]:
            rec["labels"][bucket].append(cleaned)

    def add_parents(term: str, parents: Iterable[str]) -> None:
        rec = ensure(term)
        for parent in parents:
            if parent == term:
                continue
            ensure(parent)
            if parent not in rec["parents"]:
                rec["parents"].append(parent)

    def flush_parents() -> None:
        nonlocal pending_parents, current_pred
        if current and pending_parents:
            add_parents(current, pending_parents)
        pending_parents = []
        current_pred = None

    for raw in text.splitlines():
        if in_triple_quote:
            if '"""' in raw:
                in_triple_quote = False
            continue
        if '"""' in raw and raw.count('"""') == 1:
            in_triple_quote = True
            continue

        line = _skip_hashes(raw).strip()
        if not line or line.startswith("@prefix") or line.startswith("@base"):
            continue

        pred_match = PRED_START_RE.match(line)
        subject_match = None if pred_match else SUBJECT_START_RE.match(line)
        if subject_match:
            flush_parents()
            current = subject_match.group(1)
            ensure(current)
            rest = line[subject_match.end() :].strip()
            if not rest:
                current_pred = None
                continue
            line = rest
            pred_match = PRED_START_RE.match(line)

        if current is None:
            continue

        if pred_match:
            flush_parents()
            current_pred = pred_match.group(1)
            payload = line[pred_match.end() :].strip()
        else:
            payload = line

        if current_pred in ("mdhn:isPartOf", "mdhn:ispartOf"):
            pending_parents.extend(
                term for term in MDHN_TERM_RE.findall(payload) if term != current
            )
            if payload.endswith("."):
                flush_parents()
                current = None
            continue

        if current_pred == "rdfs:label" or line.startswith("rdfs:label"):
            for value, lang in LABEL_RE.findall(payload if pred_match else line):
                add_label(current, value, lang)
        elif current_pred == "mdhn:icWikiDataURL" or line.startswith(
            "mdhn:icWikiDataURL"
        ):
            wiki_match = WIKI_RE.search(raw)
            if wiki_match:
                wiki = wiki_match.group(1).strip()
                if wiki.startswith("https://www.wikidata.org/wiki/"):
                    qid = wiki.rsplit("/", 1)[-1]
                    if qid and qid != "wiki":
                        ensure(current)["wiki"] = qid

        if line.endswith("."):
            flush_parents()
            current = None

    flush_parents()
    return episodes


def display_label(rec: Optional[Episode], term: str) -> str:
    if not rec:
        return term
    labels = rec.get("labels") or {}
    en = (labels.get("en") or [None])[0]
    fa = (labels.get("fa") or [None])[0]
    if en and fa:
        return f"{en} / {fa}"
    return en or fa or (labels.get("none") or [None])[0] or term


def build_children(episodes: Dict[str, Episode]) -> DefaultDict[str, List[str]]:
    children: DefaultDict[str, List[str]] = defaultdict(list)
    seen_pairs: Set[Tuple[str, str]] = set()
    for child, rec in episodes.items():
        for parent in rec["parents"]:
            pair = (parent, child)
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            children[parent].append(child)
    for parent in children:
        children[parent].sort(key=lambda term: episodes.get(term, {}).get("order", 0))
    return children


def descendants(root: str, children: Dict[str, List[str]]) -> Set[str]:
    found: Set[str] = set()
    stack = [root]
    while stack:
        node = stack.pop()
        if node in found:
            continue
        found.add(node)
        stack.extend(children.get(node, []))
    return found


def hit_identity(hit: ResourceHit) -> Tuple[str, str]:
    return (hit.get("resource_id") or hit["resource_label"], hit["collection_file"])


def direct_hit_keys(
    term: str, resource_index: Dict[str, List[ResourceHit]]
) -> Set[Tuple[str, str]]:
    return {hit_identity(hit) for hit in resource_index.get(term) or []}


def subtree_hit_keys(
    children: Dict[str, List[str]],
    resource_index: Dict[str, List[ResourceHit]],
) -> Dict[str, Set[Tuple[str, str]]]:
    """Unique resource identities on each term plus all narrower episodes."""
    cached: Dict[str, Set[Tuple[str, str]]] = {}
    visiting: Set[str] = set()

    def collect(term: str) -> Set[Tuple[str, str]]:
        known = cached.get(term)
        if known is not None:
            return known
        if term in visiting:
            return direct_hit_keys(term, resource_index)
        visiting.add(term)
        acc = set(direct_hit_keys(term, resource_index))
        for child in children.get(term, []):
            acc |= collect(child)
        visiting.remove(term)
        cached[term] = acc
        return acc

    terms = set(children)
    for kids in children.values():
        terms.update(kids)
    terms.update(resource_index)
    for term in terms:
        collect(term)
    return cached


def count_suffix(direct: int, accumulated: int) -> str:
    if accumulated == 0 and direct == 0:
        return ""
    if accumulated == direct:
        noun = "resource" if direct == 1 else "resources"
        return f" — {direct} {noun}"
    return f" — {direct} direct, {accumulated} including narrower"


def index_resources(collection_dir: Path) -> Dict[str, List[ResourceHit]]:
    index: DefaultDict[str, List[ResourceHit]] = defaultdict(list)
    seen: Set[Tuple[str, str, str]] = set()
    files = sorted(collection_dir.glob("*Collection.json"))
    for path in files:
        try:
            collection = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"warning: skipped {path.name}: {exc}")
            continue
        if not isinstance(collection, dict):
            continue
        collection_label = (
            get_label_text(collection.get("label") or collection.get("title"))
            or path.stem
        )
        for resource in iter_collection_resources(collection):
            resource_id = str(
                resource.get("id") or resource.get("@id") or ""
            ).strip()
            resource_label = get_label_text(resource.get("label")) or resource_id
            if not resource_label:
                continue
            for term in resource_terms(resource):
                key = (term, resource_id or resource_label, path.name)
                if key in seen:
                    continue
                seen.add(key)
                index[term].append(
                    {
                        "resource_label": resource_label,
                        "resource_id": resource_id,
                        "collection_label": collection_label,
                        "collection_file": path.name,
                    }
                )
    for term in index:
        index[term].sort(
            key=lambda hit: (
                hit["collection_label"].lower(),
                hit["resource_label"].lower(),
            )
        )
    return index


def terms_with_hits_in_subtree(
    root: str,
    children: Dict[str, List[str]],
    resource_index: Dict[str, List[ResourceHit]],
) -> Set[str]:
    """Episodes that have a direct resource, or an ancestor of such an episode."""
    keep: Set[str] = set()
    memo: Dict[str, bool] = {}

    def subtree_has_resource(term: str, stack: Set[str]) -> bool:
        cached = memo.get(term)
        if cached is not None:
            return cached
        if term in stack:
            memo[term] = False
            return False
        if resource_index.get(term):
            memo[term] = True
            return True
        stack.add(term)
        result = any(
            subtree_has_resource(child, stack) for child in children.get(term, [])
        )
        stack.remove(term)
        memo[term] = result
        return result

    def mark(term: str, stack: Set[str]) -> None:
        if term in stack:
            return
        if not subtree_has_resource(term, set()):
            return
        keep.add(term)
        stack.add(term)
        for child in children.get(term, []):
            mark(child, stack)
        stack.remove(term)

    mark(root, set())
    return keep


def md_escape(text: str) -> str:
    return text.replace("\n", " ").replace("\r", " ").replace("|", "\\|").strip()


def episode_heading(term: str, rec: Optional[Episode]) -> str:
    label = md_escape(display_label(rec, term))
    wiki = (rec or {}).get("wiki") or ""
    if wiki:
        return f"**{label}** (`{term}`, {wiki})"
    if label != term:
        return f"**{label}** (`{term}`)"
    return f"**{term}**"


def render_tree(
    root: str,
    episodes: Dict[str, Episode],
    children: Dict[str, List[str]],
    resource_index: Dict[str, List[ResourceHit]],
    scope: str,
    keep: Optional[Set[str]] = None,
) -> str:
    lines: List[str] = []
    visible = keep
    rendered_nodes = 0
    rendered_resources = 0
    accumulated_keys = subtree_hit_keys(children, resource_index)

    def allowed(term: str) -> bool:
        return visible is None or term in visible

    def walk(term: str, depth: int, ancestry: Tuple[str, ...]) -> None:
        nonlocal rendered_nodes, rendered_resources
        if not allowed(term):
            return
        rec = episodes.get(term)
        hits = resource_index.get(term) or []
        direct = len(hits)
        accumulated = len(accumulated_keys.get(term) or set())
        indent = "  " * depth
        extra = count_suffix(direct, accumulated)
        lines.append(f"{indent}- {episode_heading(term, rec)}{extra}")
        rendered_nodes += 1
        if hits:
            res_indent = "  " * (depth + 1)
            item_indent = "  " * (depth + 2)
            lines.append(f"{res_indent}- *Resources*")
            for hit in hits:
                rendered_resources += 1
                label = md_escape(hit["resource_label"])
                coll = md_escape(hit["collection_label"])
                fname = hit["collection_file"]
                lines.append(f"{item_indent}- {label} — {coll} (`{fname}`)")
        next_ancestry = ancestry + (term,)
        for child in children.get(term, []):
            if child in next_ancestry:
                loop_indent = "  " * (depth + 1)
                lines.append(
                    f"{loop_indent}- *cycle omitted:* `{child}` already on this path"
                )
                continue
            if not allowed(child):
                continue
            walk(child, depth + 1, next_ancestry)

    walk(root, 0, ())
    header = [
        f"# Narrative episode tree: `{root}`",
        "",
        f"- scope: `{scope}`",
        f"- episodes in this tree: {rendered_nodes}",
        f"- resource listings: {rendered_resources}",
        "- counts: **direct** = resources tagged with that episode; "
        "**including narrower** = unique resources tagged with it or any descendant",
        "",
    ]
    return "\n".join(header + lines) + "\n"


def suggest_roots(episodes: Dict[str, Episode], needle: str) -> List[str]:
    needle_l = needle.lower()
    hits = [term for term in episodes if needle_l in term.lower()]
    return hits[:12]


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Render a Markdown tree of narrative episodes starting from one "
            "term, optionally limited to episodes that have associated "
            "resources in local IIIF collection JSON."
        )
    )
    parser.add_argument(
        "--root",
        default=DEFAULT_ROOT,
        help=f"Starting episode CURIE (default: {DEFAULT_ROOT})",
    )
    parser.add_argument(
        "--scope",
        choices=SCOPES,
        default="all",
        help=(
            "all = every narrower term; with-resources = only terms that "
            "have at least one associated resource (ancestors kept)"
        ),
    )
    parser.add_argument(
        "--ttl",
        type=Path,
        default=ONTOLOGY_PATH,
        help="Path to narrative_episodes.ttl",
    )
    parser.add_argument(
        "--collections-dir",
        type=Path,
        default=COLLECTION_DIR,
        help="Directory of *Collection.json files",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Markdown output path (default: tools/visualization/reports/)",
    )
    return parser.parse_args(argv)


def output_path_for(root: str, scope: str, explicit: Optional[Path]) -> Path:
    if explicit is not None:
        return explicit
    safe = re.sub(r"[^A-Za-z0-9_]+", "_", root.replace("mdhn:", ""))
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return REPORTS_DIR / f"narrative_episode_tree_{safe}_{scope}.md"


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    root = normalize_term(args.root)
    ttl_path = args.ttl.resolve()
    collection_dir = args.collections_dir.resolve()

    if not ttl_path.is_file():
        raise SystemExit(f"Turtle file not found: {ttl_path}")
    if not collection_dir.is_dir():
        raise SystemExit(f"Collections directory not found: {collection_dir}")

    print(f"Parsing {ttl_path}")
    episodes = parse_narrative_episodes(ttl_path)
    children = build_children(episodes)
    if root not in episodes and root not in children:
        hints = suggest_roots(episodes, root.replace("mdhn:", ""))
        extra = f" Nearby terms: {', '.join(hints)}" if hints else ""
        raise SystemExit(f"Unknown root {root}.{extra}")

    print(f"Indexing resources in {collection_dir / '*Collection.json'}")
    resource_index = index_resources(collection_dir)

    subtree = descendants(root, children)
    keep: Optional[Set[str]] = None
    if args.scope == "with-resources":
        keep = terms_with_hits_in_subtree(root, children, resource_index)
        if root not in keep:
            keep.add(root)

    markdown = render_tree(
        root,
        episodes,
        children,
        resource_index,
        args.scope,
        keep=keep,
    )
    out = output_path_for(root, args.scope, args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")

    hits_in_subtree = sum(1 for term in subtree if resource_index.get(term))
    root_direct = len(resource_index.get(root) or [])
    root_accumulated = len(subtree_hit_keys(children, resource_index).get(root) or set())
    print(f"WROTE {out}")
    print(f"EPISODES {len(episodes)} SUBTREE {len(subtree)}")
    print(f"TERMS_WITH_RESOURCES {hits_in_subtree}")
    print(f"ROOT_RESOURCES {root_direct}")
    print(f"ROOT_INCLUDING_NARROWER {root_accumulated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
