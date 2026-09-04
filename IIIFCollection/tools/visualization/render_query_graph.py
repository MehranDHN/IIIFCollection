#!/usr/bin/env python3
"""Stage 2: render Stage 1 JSON as DOT, Markmap, or statistical tables."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, DefaultDict, Dict, Iterable, List, Optional, Sequence, Set, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from viz_common import HIERARCHY_RELS, local_name  # noqa: E402

REL_EDGE_STYLE = {
    "mdhn:hasAATBroader": ("#555555", "solid", "broader"),
    "mdhn:hasIconclassBroader": ("#3b75a7", "solid", "broader"),
    "mdhn:hasTGMBroader": ("#6a3d9a", "solid", "broader"),
    "mdhn:isPartOf": ("#38761d", "solid", "isPartOf"),
    "mdhn:ispartOf": ("#38761d", "solid", "isPartOf"),
    "mdhn:charactersInvolved": ("#b45f06", "dashed", "charactersInvolved"),
    "mdhn:isInCollection": ("#124f75", "solid", "isInCollection"),
    "mdhn:partOf": ("#C1503F", "solid", "partOf"),
    "mdhn:hasResource": ("#124f75", "solid", "hasResource"),
    "mdhn:hasCanvas": ("#b45f06", "solid", "hasCanvas"),
    "mdhn:hasCroppedDetails": ("#3b75a7", "solid", "hasCroppedDetails"),
    "mdhn:hasAgential": ("#6a3d9a", "dashed", "hasAgential"),
    "skos:exactMatch": ("#b23c17", "solid", "exactMatch"),
    "skos:closeMatch": ("#3b75a7", "dashed", "closeMatch"),
    "skos:relatedMatch": ("#6a3d9a", "dashed", "relatedMatch"),
    "skos:broadMatch": ("#38761d", "dashed", "broadMatch"),
    "skos:narrowMatch": ("#38761d", "dashed", "narrowMatch"),
}

TYPE_FILL = {
    "mdhn:ResourceType": "#f2f2f2",
    "mdhn:AATSubject": "#d8f7d8",
    "mdhn:ScriptStyleType": "#e8d9f7",
    "mdhn:IconclassTerm": "#cfe2f3",
    "mdhn:NarrativeEpisode": "#fff2ac",
    "fhkb:Man": "#fce5cd",
    "fhkb:Woman": "#fce5cd",
    "fhkb:FictionalMan": "#f4cccc",
    "fhkb:FictionalWoman": "#f4cccc",
    "mdhn:DepartedCollection": "#d0e0e3",
    "mdhn:DigitalResource": "#ead1dc",
    "mdhn:ResourceCollection": "#d0e0e3",
    "mdhn:ResourceCanvas": "#fff2ac",
    "mdhn:Cropped_Details": "#cfe2f3",
}


def safe_id(value: str) -> str:
    compact = local_name(value)
    safe = re.sub(r"[^A-Za-z0-9_]", "_", compact)
    if not safe or safe[0].isdigit():
        safe = "_" + safe
    return safe


def quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def load_document(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def node_label(node: Dict[str, Any]) -> str:
    label = node.get("label") or node.get("id") or ""
    ident = local_name(node.get("id") or "")
    if ident and ident not in str(label):
        return "{}\n({})".format(label, ident)
    return str(label)


def node_fill(node: Dict[str, Any]) -> str:
    if str(node.get("attrs", {}).get("isGuideTerm", "")).lower() in {"true", "1"}:
        return "#fff2ac"
    return TYPE_FILL.get(node.get("type") or "", "#f2f2f2")


def render_dot(document: Dict[str, Any]) -> str:
    graph = document.get("graph") or {}
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    query_name = Path(document.get("meta", {}).get("query", "QueryGraph")).stem
    name = safe_id(query_name)
    lines = [
        "digraph {} {{".format(name),
        '  rankdir=TB;',
        '  graph [bgcolor="#ffffff"];',
        '  node [shape=box, style="filled,rounded", fontname="Arial", fontsize=9, penwidth=0.8];',
        '  edge [color="#555555", arrowsize=0.8];',
        "  overlap=scale;",
        "  splines=true;",
        "  ranksep=1.0;",
        "  nodesep=0.4;",
    ]
    for node in nodes:
        nid = safe_id(node["id"])
        label = quote(node_label(node))
        tooltip = quote(str(node.get("attrs", {}).get("comment") or node.get("label") or node["id"]))
        fill = node_fill(node)
        lines.append(
            '  "{nid}" [label="{label}", tooltip="{tooltip}", fillcolor="{fill}"];'.format(
                nid=nid, label=label, tooltip=tooltip, fill=fill
            )
        )
    for edge in edges:
        rel = edge.get("rel") or "related"
        color, style, elabel = REL_EDGE_STYLE.get(rel, ("#555555", "solid", local_name(rel)))
        src = safe_id(edge["source"])
        tgt = safe_id(edge["target"])
        if rel in HIERARCHY_RELS:
            parent, child = tgt, src
        else:
            parent, child = src, tgt
        lines.append(
            '  "{parent}" -> "{child}" [color="{color}", style="{style}", label="{label}"];'.format(
                parent=parent,
                child=child,
                color=color,
                style=style,
                label=quote(elabel),
            )
        )
    lines.append("}")
    return "\n".join(lines) + "\n"


THUMBNAIL_WIDTH = 200
DETAIL_TYPES = {"mdhn:Cropped_Details", "mdhn:CroppedFigure", "mdhn:CroppedPattern", "mdhn:CroppedPhoto"}
LEAF_RELS = {"mdhn:hasAgential", "mdhn:charactersInvolved", "mdhn:hasParticipantInRoleReferredTo"}
STRUCTURAL_TYPES = {
    "mdhn:ResourceCollection",
    "mdhn:DepartedCollection",
    "mdhn:DigitalResource",
    "mdhn:ResourceCanvas",
} | DETAIL_TYPES
STRUCTURAL_RELS = {"mdhn:hasResource", "mdhn:hasCanvas", "mdhn:hasCroppedDetails"}
NARRATIVE_TYPES = {"mdhn:NarrativeEpisode"}
VOCAB_TYPES = {
    "mdhn:AATTerm",
    "mdhn:AATSubject",
    "mdhn:ResourceType",
    "mdhn:ScriptStyleType",
    "mdhn:IconclassTerm",
    "mdhn:LCTGMSubject",
    "mdhn:LCSHSubject",
    "mdhn:Occupation",
}
SKIP_CONCEPT_IDS = {"mdhn:Fragment_Cropped_Image"}
SKOS_RELS = {
    "skos:exactMatch",
    "skos:closeMatch",
    "skos:relatedMatch",
    "skos:broadMatch",
    "skos:narrowMatch",
    "skos:broader",
    "skos:narrower",
}
VOCAB_RELS = {"mdhn:classifiedAs", "mdhn:hasScriptStyle", "mdhn:elementHasSubject"}
HEADING_TYPE_LABEL = {
    "mdhn:ResourceCollection": "Collection",
    "mdhn:DepartedCollection": "Departed collection",
    "mdhn:DigitalResource": "Resource",
    "mdhn:ResourceCanvas": "Canvas",
    "mdhn:NarrativeEpisode": "Episode",
}


def thumbnail_url(iiif_url: Optional[str], width: int = THUMBNAIL_WIDTH) -> Optional[str]:
    if not iiif_url or not isinstance(iiif_url, str):
        return None
    if "/full/" in iiif_url:
        return iiif_url.replace("/full/", "/{},/".format(width))
    if "/max/" in iiif_url:
        return iiif_url.replace("/max/", "/{},/".format(width))
    return iiif_url


def _node_title(node: Dict[str, Any]) -> str:
    return str(node.get("label") or local_name(node.get("id") or "")).strip()


def _markmap_heading(node: Dict[str, Any], depth: int) -> str:
    label = _node_title(node)
    type_note = HEADING_TYPE_LABEL.get(node.get("type") or "")
    if type_note and type_note.lower() not in label.lower():
        return "{} {} · {}".format("#" * min(depth, 6), label, type_note)
    return "{} {}".format("#" * min(depth, 6), label)


def _sorted_child_ids(
    child_ids: List[str],
    nodes_by_id: Dict[str, Dict[str, Any]],
) -> List[str]:
    return sorted(child_ids, key=lambda nid: (_node_title(nodes_by_id.get(nid, {"id": nid})).lower(), nid))


def _concept_bucket(node: Dict[str, Any]) -> str:
    node_id = node.get("id") or ""
    node_type = node.get("type") or ""
    if node_id in SKIP_CONCEPT_IDS:
        return "skip"
    if node_type in NARRATIVE_TYPES:
        return "narrative"
    if node_type in VOCAB_TYPES:
        return "vocab"
    local = local_name(node_id)
    if local.startswith("aat") or local.startswith("iconclass") or local.startswith("tgm") or local.startswith("sh"):
        return "vocab"
    if node_type in STRUCTURAL_TYPES:
        return "structure"
    if str(node_type).startswith("fhkb:"):
        return "persona"
    return "iconography"


def render_markmap(document: Dict[str, Any]) -> str:
    graph = document.get("graph") or {}
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    title = document.get("meta", {}).get("query", "Query")
    heading_title = Path(str(title)).stem.replace("_", " ").title()
    if not edges:
        return "# {}\n\nNo hierarchical edges in this result.\n".format(heading_title)

    nodes_by_id = {node["id"]: node for node in nodes}
    children: DefaultDict[str, List[Tuple[str, str]]] = defaultdict(list)
    incoming: Set[str] = set()
    all_ids: Set[str] = set(nodes_by_id)
    for edge in edges:
        src, tgt, rel = edge["source"], edge["target"], edge.get("rel") or "related"
        all_ids.update([src, tgt])
        invert = (not mixed) and rel in HIERARCHY_RELS
        if invert:
            parent, child = tgt, src
        else:
            parent, child = src, tgt
        children[parent].append((child, rel))
        incoming.add(child)

    roots = sorted(
        (node_id for node_id in all_ids if node_id not in incoming),
        key=lambda nid: _node_title(nodes_by_id.get(nid, {"id": nid})).lower(),
    )
    if not roots:
        roots = sorted(all_ids)

    lines = [
        "---",
        "markmap:",
        "  initialExpandLevel: 4",
        "  colorFreezeLevel: 2",
        "---",
        "",
        "# {}".format(heading_title),
        "",
    ]
    mixed = any((node.get("type") or "") in STRUCTURAL_TYPES - DETAIL_TYPES for node in nodes)
    if mixed:
        collection_types = {"mdhn:ResourceCollection", "mdhn:DepartedCollection"}
        roots = [
            node_id
            for node_id in all_ids
            if (nodes_by_id.get(node_id) or {}).get("type") in collection_types
        ]
        if not roots:
            roots = [
                node_id
                for node_id in all_ids
                if (nodes_by_id.get(node_id) or {}).get("type") == "mdhn:DigitalResource"
            ]
        roots = sorted(
            roots,
            key=lambda nid: _node_title(nodes_by_id.get(nid, {"id": nid})).lower(),
        )
    seen: Set[str] = set()

    def emit_concept_details(node_id: str, indent: str) -> None:
        nested = indent + "  "
        by_rel: DefaultDict[str, List[str]] = defaultdict(list)
        for child_id, rel in children.get(node_id, []):
            by_rel[rel].append(child_id)
        parents = by_rel.get("mdhn:isPartOf") or by_rel.get("mdhn:ispartOf") or []
        if parents:
            titles = [_node_title(nodes_by_id.get(pid, {"id": pid})) for pid in _sorted_child_ids(parents, nodes_by_id)]
            lines.append("{}- **isPartOf:** {}".format(nested, ", ".join(titles)))
        involved = []
        for rel in LEAF_RELS:
            involved.extend(by_rel.get(rel) or [])
        if involved:
            titles = [_node_title(nodes_by_id.get(pid, {"id": pid})) for pid in _sorted_child_ids(involved, nodes_by_id)]
            lines.append("{}- **Characters:** {}".format(nested, ", ".join(titles)))
        for rel in sorted(SKOS_RELS):
            matches = by_rel.get(rel) or []
            if not matches:
                continue
            titles = [_node_title(nodes_by_id.get(mid, {"id": mid})) for mid in _sorted_child_ids(matches, nodes_by_id)]
            lines.append("{}- **{}:** {}".format(nested, local_name(rel), ", ".join(titles)))

    def emit_grouped_concepts(title: str, node_ids: List[str], indent: str = "") -> None:
        ordered = [nid for nid in _sorted_child_ids(node_ids, nodes_by_id) if _concept_bucket(nodes_by_id.get(nid, {"id": nid})) != "skip"]
        if not ordered:
            return
        lines.append("{}- **{}**".format(indent, title))
        nested = indent + "  "
        for nid in ordered:
            node = nodes_by_id.get(nid, {"id": nid})
            lines.append("{}- {}".format(nested, _node_title(node)))
            emit_concept_details(nid, nested)

    def emit_detail(node_id: str, indent: str) -> None:
        node = nodes_by_id.get(node_id, {"id": node_id, "label": node_id, "attrs": {}})
        label = _node_title(node)
        lines.append("{}- {}".format(indent, label))
        nested = indent + "  "
        image = thumbnail_url((node.get("attrs") or {}).get("image"))
        if image:
            lines.append("{}- ![{}]({})".format(nested, label, image))
        by_rel: DefaultDict[str, List[str]] = defaultdict(list)
        for child_id, rel in children.get(node_id, []):
            by_rel[rel].append(child_id)
        personas = []
        for rel in LEAF_RELS:
            personas.extend(by_rel.pop(rel, []))
        if personas:
            titles = [_node_title(nodes_by_id.get(pid, {"id": pid})) for pid in _sorted_child_ids(personas, nodes_by_id)]
            lines.append("{}- **Persona:** {}".format(nested, ", ".join(titles)))
        subjects = by_rel.pop("mdhn:elementHasSubject", [])
        if subjects:
            titles = [_node_title(nodes_by_id.get(sid, {"id": sid})) for sid in _sorted_child_ids(subjects, nodes_by_id)]
            lines.append("{}- **Subject (AAT):** {}".format(nested, ", ".join(titles)))

    def walk(node_id: str, depth: int) -> None:
        node = nodes_by_id.get(node_id, {"id": node_id, "label": node_id, "type": None, "attrs": {}})
        node_type = node.get("type") or ""
        if node_type in DETAIL_TYPES:
            emit_detail(node_id, "")
            return
        if node_id in seen:
            lines.append("{} {}".format("#" * min(depth, 6), _node_title(node)))
            return
        seen.add(node_id)
        lines.append(_markmap_heading(node, depth))
        image = thumbnail_url((node.get("attrs") or {}).get("image"))
        if image:
            lines.append("- ![{}]({})".format(_node_title(node), image))

        grouped: DefaultDict[str, List[str]] = defaultdict(list)
        for child, rel in children.get(node_id, []):
            grouped[rel].append(child)

        if mixed:
            narrative_ids: List[str] = []
            iconography_ids: List[str] = []
            vocab_ids: List[str] = []
            persona_ids: List[str] = []
            for rel, child_ids in list(grouped.items()):
                if rel in STRUCTURAL_RELS:
                    continue
                if rel in VOCAB_RELS:
                    vocab_ids.extend(grouped.pop(rel, []))
                    continue
                if rel in LEAF_RELS:
                    persona_ids.extend(grouped.pop(rel, []))
                    continue
                if rel in SKOS_RELS or rel in {"mdhn:isPartOf", "mdhn:ispartOf"}:
                    grouped.pop(rel, None)
                    continue
                if rel in {"mdhn:depicts", "mdhn:elementDepicts"}:
                    grouped.pop(rel, None)
                    for cid in child_ids:
                        bucket = _concept_bucket(nodes_by_id.get(cid, {"id": cid}))
                        if bucket == "narrative":
                            narrative_ids.append(cid)
                        elif bucket == "vocab":
                            vocab_ids.append(cid)
                        elif bucket == "persona":
                            persona_ids.append(cid)
                        elif bucket == "iconography":
                            iconography_ids.append(cid)
            emit_grouped_concepts("Narrative episodes", narrative_ids)
            emit_grouped_concepts("Iconography", iconography_ids)
            emit_grouped_concepts("Controlled vocabulary", vocab_ids)
            if persona_ids:
                lines.append("- **Characters**")
                for pid in _sorted_child_ids(persona_ids, nodes_by_id):
                    lines.append("  - {}".format(_node_title(nodes_by_id.get(pid, {"id": pid}))))

        detail_ids = grouped.pop("mdhn:hasCroppedDetails", [])
        if detail_ids:
            for child in _sorted_child_ids(detail_ids, nodes_by_id):
                emit_detail(child, "")

        for rel, child_ids in grouped.items():
            ordered = _sorted_child_ids(child_ids, nodes_by_id)
            if not mixed and rel in LEAF_RELS:
                lines.append("- **Characters**")
                for child in ordered:
                    lines.append("  - {}".format(_node_title(nodes_by_id.get(child, {"id": child}))))
                continue
            if rel in STRUCTURAL_RELS or not mixed:
                for child in ordered:
                    walk(child, min(depth + 1, 6))

    for root in roots:
        walk(root, 2)
    lines.append("")
    return "\n".join(lines)


def render_stats_json(document: Dict[str, Any]) -> Dict[str, Any]:
    table = document.get("table") or {"columns": [], "rows": []}
    stats = dict(document.get("stats") or {})
    columns = table.get("columns") or []
    count_cols = [col for col in columns if "count" in col.lower()]
    numeric_total = None
    if count_cols:
        values = []
        for row in table.get("rows") or []:
            raw = row.get(count_cols[0])
            try:
                values.append(int(float(raw)))
            except (TypeError, ValueError):
                continue
        numeric_total = sum(values)
        stats["count_column"] = count_cols[0]
        stats["count_sum"] = numeric_total
        stats["groups"] = len(table.get("rows") or [])
    return {
        "meta": document.get("meta"),
        "stats": stats,
        "columns": columns,
        "rows": table.get("rows") or [],
    }


def render_stats_html(payload: Dict[str, Any]) -> str:
    title = payload.get("meta", {}).get("query", "Statistics")
    columns = payload.get("columns") or []
    rows = payload.get("rows") or []
    stats = payload.get("stats") or {}
    head = "".join("<th>{}</th>".format(html.escape(str(col))) for col in columns)
    body_rows = []
    for row in rows:
        cells = "".join(
            "<td>{}</td>".format(html.escape("" if row.get(col) is None else str(row.get(col))))
            for col in columns
        )
        body_rows.append("<tr>{}</tr>".format(cells))
    summary_bits = [
        "bindings={}".format(stats.get("bindings", len(rows))),
        "nodes={}".format(stats.get("nodes", 0)),
        "edges={}".format(stats.get("edges", 0)),
    ]
    if "count_sum" in stats:
        summary_bits.append("{}={}".format(stats.get("count_column"), stats["count_sum"]))
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{title}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 1.5rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: left; }}
    th {{ background: #f2f2f2; }}
    caption {{ text-align: left; margin-bottom: 0.6rem; font-weight: bold; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p>{summary}</p>
  <table>
    <caption>SPARQL result table</caption>
    <thead><tr>{head}</tr></thead>
    <tbody>
      {body}
    </tbody>
  </table>
</body>
</html>
""".format(
        title=html.escape(str(title)),
        summary=html.escape("; ".join(summary_bits)),
        head=head,
        body="\n      ".join(body_rows) or "<tr><td colspan='{}'>No rows</td></tr>".format(max(len(columns), 1)),
    )


def render_document(
    document: Dict[str, Any],
    json_path: Path,
    formats: Iterable[str],
) -> List[Path]:
    written: List[Path] = []
    stem_path = json_path.with_suffix("")
    for fmt in formats:
        if fmt == "dot":
            path = stem_path.with_suffix(".dot")
            path.write_text(render_dot(document), encoding="utf-8")
            written.append(path)
        elif fmt == "markmap":
            path = Path(str(stem_path) + ".markmap.md")
            path.write_text(render_markmap(document), encoding="utf-8")
            written.append(path)
        elif fmt == "stats":
            payload = render_stats_json(document)
            json_stats = Path(str(stem_path) + ".stats.json")
            html_stats = Path(str(stem_path) + ".stats.html")
            json_stats.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            html_stats.write_text(render_stats_html(payload), encoding="utf-8")
            written.extend([json_stats, html_stats])
        elif fmt == "json":
            continue
        else:
            raise ValueError("Unsupported format: {}".format(fmt))
    return written


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render Stage 1 SPARQL JSON into DOT, Markmap, or statistics."
    )
    parser.add_argument("json_path", type=Path, help="JSON document written by query_runner.py")
    parser.add_argument(
        "--format",
        default="dot,stats",
        help="Comma-separated: dot,markmap,stats (default: dot,stats).",
    )
    args = parser.parse_args(argv)
    json_path = args.json_path.resolve()
    document = load_document(json_path)
    formats = [part.strip().lower() for part in args.format.split(",") if part.strip()]
    written = render_document(document, json_path, formats)
    for path in written:
        print("WROTE", path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("ERROR:", exc, file=sys.stderr)
        raise
