"""Shared IRI compacting and SPARQL-result to graph conversion."""

from typing import Any, Dict, Iterable, List, Optional, Tuple

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS
from rdflib.term import Identifier

MDHN = "http://example.com/mdhn/"

PREFIX_PAIRS: List[Tuple[str, str]] = [
    ("mdhn:", MDHN),
    ("skos:", "http://www.w3.org/2004/02/skos/core#"),
    ("rdfs:", "http://www.w3.org/2000/01/rdf-schema#"),
    ("rdf:", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    ("owl:", "http://www.w3.org/2002/07/owl#"),
    ("xsd:", "http://www.w3.org/2001/XMLSchema#"),
    ("fhkb:", "http://www.example.com/genealogy.owl#"),
    ("schema:", "http://schema.org/"),
    ("aat:", "http://vocab.getty.edu/aat/"),
    ("tgm:", "http://id.loc.gov/vocabulary/graphicMaterials/"),
    ("tgn:", "http://vocab.getty.edu/tgn/"),
    ("lcsh:", "https://id.loc.gov/authorities/subjects/"),
    ("iconclass:", "https://iconclass.org/"),
    ("biblissima:", "https://data.biblissima.fr/entity/"),
    ("wd:", "http://www.wikidata.org/entity/"),
    ("wdwiki:", "https://www.wikidata.org/wiki/"),
]

# Child --rel--> parent in the Turtle data. DOT draws parent -> child.
HIERARCHY_RELS = {
    "mdhn:hasAATBroader",
    "mdhn:hasIconclassBroader",
    "mdhn:hasTGMBroader",
    "mdhn:isPartOf",
    "mdhn:ispartOf",
    "mdhn:subCollectionOf",
}

# README Query 23 and similar SELECT * path queries:
# Collection -> Resource -> Canvas -> ContentElement -> persona
PATH_LINKS = [
    ("collection", "resource", "mdhn:hasResource"),
    ("resource", "s", "mdhn:hasCanvas"),
    ("resource", "canvas", "mdhn:hasCanvas"),
    ("s", "details", "mdhn:hasCroppedDetails"),
    ("canvas", "details", "mdhn:hasCroppedDetails"),
    ("details", "persona", "mdhn:hasAgential"),
]
NODE_LABEL_VARS = {
    "s": ("canvasLabel",),
    "canvas": ("canvasLabel",),
    "resource": ("resourceLabel",),
    "collection": ("collectionLabel",),
    "details": ("detailsLabel",),
    "persona": ("personaLabel",),
}
NODE_TYPE_HINTS = {
    "s": "mdhn:ResourceCanvas",
    "canvas": "mdhn:ResourceCanvas",
    "resource": "mdhn:DigitalResource",
    "collection": "mdhn:ResourceCollection",
    "details": "mdhn:Cropped_Details",
}
NODE_ATTR_VARS = {
    "resource": {"url": "resurl"},
    "details": {"image": "imgurl", "url": "imgurl"},
    "s": {"comment": "canvasLabel"},
    "canvas": {"comment": "canvasLabel"},
}

SKIP_TTL_NAMES = {
    "LCTGM_RDF.migrated.ttl",
}


def compact_iri(value: Any) -> str:
    text = str(value)
    for prefix, namespace in PREFIX_PAIRS:
        if text.startswith(namespace):
            return prefix + text[len(namespace) :]
    return text


def expand_curie(value: str) -> str:
    text = value.strip()
    if text.startswith("<") and text.endswith(">"):
        return text[1:-1]
    for prefix, namespace in PREFIX_PAIRS:
        if text.startswith(prefix):
            return namespace + text[len(prefix) :]
    return text


def term_to_binding(term: Optional[Identifier]) -> Optional[Dict[str, str]]:
    if term is None:
        return None
    if isinstance(term, URIRef):
        return {"type": "uri", "value": str(term), "curie": compact_iri(term)}
    if isinstance(term, BNode):
        return {"type": "bnode", "value": str(term)}
    if isinstance(term, Literal):
        binding: Dict[str, str] = {"type": "literal", "value": str(term)}
        if term.language:
            binding["xml:lang"] = term.language
        if term.datatype:
            binding["datatype"] = str(term.datatype)
        return binding
    return {"type": "literal", "value": str(term)}


def binding_value(binding: Optional[Dict[str, Any]]) -> Optional[str]:
    if not binding:
        return None
    if binding.get("type") == "uri":
        return binding.get("curie") or compact_iri(binding.get("value", ""))
    return binding.get("value")


def _row_get(row: Dict[str, Any], *names: str) -> Optional[str]:
    for name in names:
        value = binding_value(row.get(name))
        if value:
            return value
    return None


def _ensure_node(
    nodes: Dict[str, Dict[str, Any]],
    node_id: Optional[str],
    label: Optional[str] = None,
    node_type: Optional[str] = None,
    attrs: Optional[Dict[str, Any]] = None,
) -> None:
    if not node_id:
        return
    node = nodes.setdefault(
        node_id,
        {"id": node_id, "label": node_id, "type": None, "attrs": {}},
    )
    if label and (node["label"] == node_id or len(label) > len(str(node["label"]))):
        node["label"] = label
    if node_type and not node["type"]:
        node["type"] = node_type
    if attrs:
        node["attrs"].update({k: v for k, v in attrs.items() if v is not None})


def _add_path_graph(
    names: set,
    rows: List[Dict[str, Any]],
    nodes: Dict[str, Dict[str, Any]],
    edges: List[Dict[str, str]],
    seen_edges: set,
) -> None:
    active = [
        (src_var, tgt_var, rel)
        for src_var, tgt_var, rel in PATH_LINKS
        if src_var in names and tgt_var in names
    ]
    if not active:
        return
    for row in rows:
        for src_var, tgt_var, rel in active:
            source = _row_get(row, src_var)
            target = _row_get(row, tgt_var)
            if not source or not target:
                continue
            src_label = _row_get(row, *NODE_LABEL_VARS.get(src_var, ()))
            tgt_label = _row_get(row, *NODE_LABEL_VARS.get(tgt_var, ()))
            src_attrs = {
                key: _row_get(row, var)
                for key, var in NODE_ATTR_VARS.get(src_var, {}).items()
            }
            tgt_attrs = {
                key: _row_get(row, var)
                for key, var in NODE_ATTR_VARS.get(tgt_var, {}).items()
            }
            _ensure_node(
                nodes,
                source,
                src_label,
                NODE_TYPE_HINTS.get(src_var),
                src_attrs,
            )
            _ensure_node(
                nodes,
                target,
                tgt_label,
                NODE_TYPE_HINTS.get(tgt_var),
                tgt_attrs,
            )
            key = (source, target, rel)
            if key not in seen_edges:
                seen_edges.add(key)
                edges.append({"source": source, "target": target, "rel": rel})


def bindings_to_graph(vars_: Iterable[str], rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    names = set(vars_)
    has_edge = (("source" in names) or ("child" in names)) and (
        ("target" in names) or ("parent" in names)
    )
    nodes: Dict[str, Dict[str, Any]] = {}
    edges: List[Dict[str, str]] = []
    seen_edges = set()

    if has_edge:
        for row in rows:
            source = _row_get(row, "source", "child")
            target = _row_get(row, "target", "parent")
            rel = _row_get(row, "rel") or "related"
            source_label = _row_get(row, "sourceLabel", "childLabel")
            target_label = _row_get(row, "targetLabel", "parentLabel")
            source_type = _row_get(row, "sourceType", "childType")
            target_type = _row_get(row, "targetType", "parentType")
            attrs = {
                "isGuideTerm": _row_get(row, "isGuideTerm"),
                "comment": _row_get(row, "comment"),
            }
            target_attrs = {}
            imgurl = _row_get(row, "imgurl")
            if imgurl and rel == "mdhn:hasCroppedDetails":
                target_attrs["image"] = imgurl
            _ensure_node(nodes, source, source_label, source_type, attrs)
            _ensure_node(nodes, target, target_label, target_type, target_attrs)
            if source and target:
                key = (source, target, rel)
                if key not in seen_edges:
                    seen_edges.add(key)
                    edges.append({"source": source, "target": target, "rel": rel})
    else:
        _add_path_graph(names, rows, nodes, edges, seen_edges)

    table_rows: List[Dict[str, Optional[str]]] = []
    for row in rows:
        table_rows.append({name: binding_value(row.get(name)) for name in vars_})

    kind = "graph" if edges else "stats"
    by_type: Dict[str, int] = {}
    for node in nodes.values():
        ntype = node.get("type") or "untyped"
        by_type[ntype] = by_type.get(ntype, 0) + 1
    return {
        "kind": kind,
        "nodes": list(nodes.values()),
        "edges": edges,
        "table": {"columns": list(vars_), "rows": table_rows},
        "stats": {
            "bindings": len(rows),
            "nodes": len(nodes),
            "edges": len(edges),
            "by_type": by_type,
        },
    }


def enrich_nodes_from_graph(rdf_graph: Graph, nodes: List[Dict[str, Any]]) -> None:
    """Fill rdfs:label@en and rdf:type from the ontology graph."""
    for node in nodes:
        try:
            uri = URIRef(expand_curie(node["id"]))
        except Exception:
            continue
        if not node.get("label") or node["label"] == node["id"]:
            chosen = None
            for label in rdf_graph.objects(uri, RDFS.label):
                lang = getattr(label, "language", None)
                if lang == "en":
                    chosen = str(label)
                    break
                if chosen is None and lang in (None, ""):
                    chosen = str(label)
            if chosen:
                node["label"] = chosen
        if not node.get("type"):
            for term in rdf_graph.objects(uri, RDF.type):
                curie = compact_iri(term)
                if curie.startswith("mdhn:") or curie.startswith("fhkb:"):
                    node["type"] = curie
                    break
        comments = []
        for comment in rdf_graph.objects(uri, RDFS.comment):
            lang = getattr(comment, "language", None)
            if lang in ("en", None, ""):
                comments.append(str(comment))
                break
        if comments:
            node.setdefault("attrs", {})["comment"] = comments[0]


def local_name(curie_or_iri: str) -> str:
    text = compact_iri(curie_or_iri)
    if ":" in text and not text.startswith("http"):
        return text.split(":", 1)[1]
    if "/" in text:
        return text.rsplit("/", 1)[-1]
    if "#" in text:
        return text.rsplit("#", 1)[-1]
    return text
