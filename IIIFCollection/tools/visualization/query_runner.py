#!/usr/bin/env python3
"""Stage 1: run a SPARQL .rq file against IIIFCollection/Ontology Turtle files.

Loads resources.ttl plus the sibling vocabularies in the same folder
(AAT, Iconclass, TGM, iconography, narrative episodes, persons, ctl_vocabs).
Writes SPARQL JSON Results plus a nodes/edges envelope for Stage 2.
"""

from __future__ import annotations

import argparse
import json
import pickle
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from rdflib import Graph, URIRef

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from viz_common import (  # noqa: E402
    SKIP_TTL_NAMES,
    bindings_to_graph,
    compact_iri,
    enrich_nodes_from_graph,
    expand_curie,
    term_to_binding,
)

ROOT_DIR = SCRIPT_DIR.parents[1]
DEFAULT_ONTOLOGY_DIR = ROOT_DIR / "Ontology"
DEFAULT_QUERY_DIR = SCRIPT_DIR / "queries"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "reports"
CACHE_NAME = ".ontology_graph.pkl"
BIND_TOKEN_RE = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)")


def ontology_ttl_files(ontology_dir: Path) -> List[Path]:
    files = []
    for path in sorted(ontology_dir.glob("*.ttl")):
        if path.name in SKIP_TTL_NAMES:
            continue
        files.append(path)
    return files


def cache_is_fresh(cache_path: Path, sources: Sequence[Path]) -> bool:
    if not cache_path.exists() or not sources:
        return False
    cache_mtime = cache_path.stat().st_mtime
    return all(path.stat().st_mtime <= cache_mtime for path in sources)


def load_ontology_graph(
    ontology_dir: Path,
    cache_dir: Path,
    use_cache: bool = True,
) -> Tuple[Graph, List[str]]:
    sources = ontology_ttl_files(ontology_dir)
    if not sources:
        raise FileNotFoundError("No Turtle files found in {}".format(ontology_dir))

    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / CACHE_NAME
    if use_cache and cache_is_fresh(cache_path, sources):
        with cache_path.open("rb") as handle:
            graph = pickle.load(handle)
        if isinstance(graph, Graph):
            return graph, [path.name for path in sources]

    graph = Graph()
    for path in sources:
        graph.parse(path.as_posix(), format="turtle")

    if use_cache:
        with cache_path.open("wb") as handle:
            pickle.dump(graph, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return graph, [path.name for path in sources]


def read_query(query_path: Path, query_dir: Path) -> str:
    text = query_path.read_text(encoding="utf-8")
    if re.search(r"(?im)^\s*PREFIX\s+", text):
        return text
    prefixes_path = query_dir / "prefixes.rq"
    if prefixes_path.exists():
        prefixes = prefixes_path.read_text(encoding="utf-8")
        return prefixes.rstrip() + "\n\n" + text
    return text


def apply_bindings(query: str, bindings: Dict[str, str]) -> str:
    tokens = set(BIND_TOKEN_RE.findall(query))
    if not tokens:
        return query
    missing = tokens - set(bindings)
    if missing:
        kept: List[str] = []
        for line in query.splitlines():
            line_tokens = set(BIND_TOKEN_RE.findall(line))
            if line_tokens & missing:
                continue
            kept.append(line)
        query = "\n".join(kept)
        tokens = set(BIND_TOKEN_RE.findall(query))
    for name in tokens:
        iri = expand_curie(bindings[name])
        query = re.sub(r"\$" + re.escape(name) + r"\b", "<{}>".format(iri), query)
    return query


def parse_bind_args(items: Optional[Sequence[str]]) -> Dict[str, str]:
    bindings: Dict[str, str] = {}
    for item in items or []:
        if "=" not in item:
            raise ValueError("Bindings must be name=value, got {!r}".format(item))
        name, value = item.split("=", 1)
        bindings[name.strip()] = value.strip()
    return bindings


def serialize_result(result: Any) -> Dict[str, Any]:
    vars_ = [str(name) for name in result.vars]
    rows: List[Dict[str, Any]] = []
    for record in result:
        row: Dict[str, Any] = {}
        for name, term in zip(vars_, record):
            binding = term_to_binding(term)
            if binding is not None:
                row[name] = binding
        rows.append(row)
    return {"head": {"vars": vars_}, "results": {"bindings": rows}}


def run_query(
    graph: Graph,
    query_text: str,
    init_bindings: Optional[Dict[str, URIRef]] = None,
) -> Any:
    if init_bindings:
        return graph.query(query_text, initBindings=init_bindings)
    return graph.query(query_text)


def build_document(
    query_path: Path,
    sources: Sequence[str],
    triple_count: int,
    serialized: Dict[str, Any],
    bindings: Dict[str, str],
    rdf_graph: Optional[Graph] = None,
) -> Dict[str, Any]:
    vars_ = serialized["head"]["vars"]
    rows = serialized["results"]["bindings"]
    model = bindings_to_graph(vars_, rows)
    if rdf_graph is not None:
        enrich_nodes_from_graph(rdf_graph, model["nodes"])
        by_type: Dict[str, int] = {}
        for node in model["nodes"]:
            ntype = node.get("type") or "untyped"
            by_type[ntype] = by_type.get(ntype, 0) + 1
        model["stats"]["by_type"] = by_type
    return {
        "meta": {
            "query": query_path.name,
            "query_path": query_path.as_posix(),
            "sources": list(sources),
            "triple_count": triple_count,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "bindings": bindings,
            "kind": model["kind"],
        },
        "head": serialized["head"],
        "results": serialized["results"],
        "graph": {"nodes": model["nodes"], "edges": model["edges"]},
        "table": model["table"],
        "stats": model["stats"],
    }


def write_json(document: Dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def list_queries(query_dir: Path) -> List[Path]:
    return sorted(
        path for path in query_dir.glob("*.rq") if path.name != "prefixes.rq"
    )


def resolve_query_path(query: str, query_dir: Path) -> Path:
    path = Path(query)
    if path.exists():
        return path.resolve()
    candidate = query_dir / query
    if candidate.exists():
        return candidate.resolve()
    if not query.endswith(".rq"):
        candidate = query_dir / (query + ".rq")
        if candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError("Query file not found: {}".format(query))


def parse_formats(value: str) -> List[str]:
    formats = [part.strip().lower() for part in value.split(",") if part.strip()]
    allowed = {"json", "dot", "markmap", "stats"}
    unknown = [item for item in formats if item not in allowed]
    if unknown:
        raise ValueError("Unknown format(s): {}".format(", ".join(unknown)))
    return formats or ["json"]


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run a SPARQL .rq file against Ontology/*.ttl and serialize JSON for Stage 2."
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Query name or path (e.g. aat_hierarchy or queries/aat_hierarchy.rq).",
    )
    parser.add_argument(
        "--list-queries",
        action="store_true",
        help="List .rq files in the query directory and exit.",
    )
    parser.add_argument(
        "--ontology-dir",
        type=Path,
        default=DEFAULT_ONTOLOGY_DIR,
        help="Folder of Turtle files (default: IIIFCollection/Ontology).",
    )
    parser.add_argument(
        "--query-dir",
        type=Path,
        default=DEFAULT_QUERY_DIR,
        help="Folder of .rq files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for JSON and rendered reports.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="JSON output path. Defaults to reports/<query>.json.",
    )
    parser.add_argument(
        "--format",
        default="json",
        help="Comma-separated: json,dot,markmap,stats (default: json).",
    )
    parser.add_argument(
        "--bind",
        action="append",
        default=[],
        help="Query variable binding, e.g. --bind seed=mdhn:Halo (repeatable).",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Rebuild the rdflib graph instead of using the pickle cache.",
    )
    args = parser.parse_args(argv)

    query_dir = args.query_dir.resolve()
    ontology_dir = args.ontology_dir.resolve()
    output_dir = args.output_dir.resolve()

    if args.list_queries:
        for path in list_queries(query_dir):
            print(path.name)
        return 0

    if not args.query:
        parser.error("query is required unless --list-queries is set")

    formats = parse_formats(args.format)
    bindings = parse_bind_args(args.bind)
    query_path = resolve_query_path(args.query, query_dir)
    query_text = apply_bindings(read_query(query_path, query_dir), bindings)

    graph, sources = load_ontology_graph(
        ontology_dir, output_dir, use_cache=not args.no_cache
    )
    result = run_query(graph, query_text)
    serialized = serialize_result(result)
    document = build_document(
        query_path, sources, len(graph), serialized, bindings, rdf_graph=graph
    )

    json_path = args.output.resolve() if args.output else output_dir / (
        query_path.stem + ".json"
    )
    write_json(document, json_path)
    print("WROTE", json_path)
    print(
        "kind={kind} bindings={bindings} nodes={nodes} edges={edges} triples={triples}".format(
            kind=document["meta"]["kind"],
            bindings=document["stats"]["bindings"],
            nodes=document["stats"]["nodes"],
            edges=document["stats"]["edges"],
            triples=document["meta"]["triple_count"],
        )
    )

    render_formats = [item for item in formats if item != "json"]
    if render_formats:
        from render_query_graph import render_document

        written = render_document(document, json_path, render_formats)
        for path in written:
            print("WROTE", path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("ERROR:", exc, file=sys.stderr)
        raise
