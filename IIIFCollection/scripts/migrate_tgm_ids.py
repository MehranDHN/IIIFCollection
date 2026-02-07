#!/usr/bin/env python3
"""
Migration script to rename mdhn:tgmNNNNNN subjects to include slugified labels,
produce per-URI log files and a CSV mapping, and (optionally) apply changes to
TTL and JSON files. Default is dry-run.

Usage:
  python migrate_tgm_ids.py --ttl path/to/LCTGM_RDF.ttl --root IIIFCollection --dry-run
  python migrate_tgm_ids.py --apply --ttl ... --root ...

Produces:
  - IIIFCollection/tgm_id_mapping.csv
  - IIIFCollection/logs/<old_localname>.log
  - LCTGM_RDF.migrated.ttl (when --apply)

Requires: rdflib
"""
import argparse
import csv
import json
import logging
import os
import re
import shutil
import sys
import time
from functools import wraps
from pathlib import Path

try:
    from rdflib import Graph, URIRef, Namespace
    from rdflib.namespace import RDFS, OWL
except Exception:
    Graph = None

LOG_DIR = Path("IIIFCollection/logs")
MAPPING_CSV = Path("IIIFCollection/tgm_id_mapping.csv")
BACKUP_DIR = Path("IIIFCollection/backups")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# retry decorator
def retry(times=3, delay=1, backoff=2, exceptions=(Exception,)):
    def deco(f):
        @wraps(f)
        def wrapper(*a, **kw):
            _delay = delay
            for attempt in range(1, times + 1):
                try:
                    return f(*a, **kw)
                except exceptions as e:
                    logging.warning("Attempt %s failed for %s: %s", attempt, f.__name__, e)
                    if attempt == times:
                        logging.error("All retries failed for %s", f.__name__)
                        raise
                    time.sleep(_delay)
                    _delay *= backoff
        return wrapper
    return deco


def slugify(text: str) -> str:
    text = text.strip()
    text = text.replace("/", "_")
    text = text.replace("-", "_")
    text = re.sub(r"[\s]+", "_", text)
    text = re.sub(r"[^A-Za-z0-9_]", "", text)
    return text.strip("_")


@retry(times=3, delay=1)
def read_file_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


@retry(times=3, delay=1)
def write_file_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def find_tgm_subjects_with_rdflib(g: Graph):
    tgm_subjects = {}
    for s in set(g.subjects()):
        if not isinstance(s, URIRef):
            continue
        local = s.split("#")[-1].split("/")[-1]
        if re.match(r"^tgm\d+", local):
            # get label
            label = None
            for p in (RDFS.label,):
                for o in g.objects(s, p):
                    label = str(o)
                    break
                if label:
                    break
            tgm_subjects[str(s)] = {"local": local, "label": label}
    return tgm_subjects


def build_mapping(tgm_subjects: dict):
    # Build a mapping that groups all existing URIs that share the same
    # tgm base (e.g., tgm000375, tgm000375_Anti-Catholicism) and maps them
    # to a single final URI using underscored slugs.
    mapping = {}
    used = set()
    # Group subjects by base id (tgm\d+)
    groups = {}
    for old_uri, info in tgm_subjects.items():
        local = info["local"]
        m = re.match(r"(tgm\d+)", local)
        if not m:
            continue
        base_id = m.group(1)
        groups.setdefault(base_id, []).append((old_uri, info))

    for base_id, entries in groups.items():
        # Prefer a label if any entry has one
        label = None
        for _, info in entries:
            if info.get("label"):
                label = info.get("label")
                break
        if not label:
            label = "unknown"
        slug = slugify(label) or "unknown"
        final_local = f"{base_id}_{slug}"
        suffix = 1
        while final_local in used:
            final_local = f"{base_id}_{slug}_{suffix}"
            suffix += 1
        used.add(final_local)
        # Build final URI using the namespace from the first entry
        first_old = entries[0][0]
        base_ns = first_old.rsplit(base_id, 1)[0]
        final_uri = base_ns + final_local
        # Map every existing URI for this base to the final URI
        for old_uri, _ in entries:
            mapping[old_uri] = final_uri

    return mapping


def detect_hasTGMBroader_relations_text(ttl_text: str, old_local: str):
    # crude search for lines containing hasTGMBroader and the subject
    pattern = re.compile(rf"(<?[^ >]+>?\s+[^\n]*hasTGMBroader[^\n]*{old_local}[^\n]*)", re.IGNORECASE)
    return pattern.findall(ttl_text)


def scan_json_references(root: Path, old_uri: str):
    occurrences = []
    for p in root.rglob("*.json"):
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if old_uri in text:
            # count and record
            count = text.count(old_uri)
            occurrences.append({"file": str(p), "count": count})
    return occurrences


def make_backup(paths: list[Path]):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    for p in paths:
        if p.exists():
            dest = BACKUP_DIR / p.name
            if p.is_file():
                shutil.copy2(p, dest)
            else:
                shutil.copytree(p, BACKUP_DIR / p.name, dirs_exist_ok=True)


def update_ttl_graph(g: Graph, mapping: dict) -> Graph:
    newg = Graph()
    for prefix, ns in g.namespaces():
        newg.bind(prefix, ns)
    for s, p, o in g:
        s_str = str(s)
        o_str = str(o) if isinstance(o, URIRef) else None
        new_s = URIRef(mapping[s_str]) if s_str in mapping else s
        new_o = URIRef(mapping[o_str]) if o_str and o_str in mapping else o
        newg.add((new_s, p, new_o))
    # add sameAs triples
    for old, new in mapping.items():
        newg.add((URIRef(old), OWL.sameAs, URIRef(new)))
    return newg


def replace_in_json_files(root: Path, mapping: dict, apply: bool):
    replaced_files = []
    for p in root.rglob("*.json"):
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        updated = text
        for old, new in mapping.items():
            if old in updated:
                updated = updated.replace(old, new)
        if updated != text:
            if apply:
                p.write_text(updated, encoding="utf-8")
                replaced_files.append(str(p))
            else:
                replaced_files.append(str(p))
    return replaced_files


def write_mapping_csv(mapping: dict):
    MAPPING_CSV.parent.mkdir(parents=True, exist_ok=True)
    with MAPPING_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["old_uri", "new_uri"])
        for old, new in mapping.items():
            writer.writerow([old, new])


def write_per_uri_logs(mapping: dict, root: Path, ttl_text: str):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    for old, new in mapping.items():
        local = old.rsplit("/", 1)[-1]
        logp = LOG_DIR / f"{local}.log"
        occurrences = scan_json_references(root, old)
        broader = []
        # try to find hasTGMBroader relations in ttl_text
        try:
            broader = detect_hasTGMBroader_relations_text(ttl_text, local)
        except Exception:
            broader = []
        with logp.open("w", encoding="utf-8") as fh:
            fh.write(f"old_uri: {old}\n")
            fh.write(f"new_uri: {new}\n")
            fh.write("\nJSON references:\n")
            for o in occurrences:
                fh.write(json.dumps(o, ensure_ascii=False) + "\n")
            fh.write("\nPotential hasTGMBroader lines in TTL:\n")
            for b in broader:
                fh.write(b + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ttl", required=True, help="Path to LCTGM_RDF.ttl")
    parser.add_argument("--root", default="IIIFCollection", help="Root dir to scan for JSON files")
    parser.add_argument("--apply", action="store_true", help="Apply changes (otherwise dry-run)")
    args = parser.parse_args()

    ttl_path = Path(args.ttl)
    root = Path(args.root)

    if not ttl_path.exists():
        logging.error("TTL file not found: %s", ttl_path)
        sys.exit(1)

    ttl_text = read_file_text(ttl_path)

    if Graph is None:
        logging.warning("rdflib not available; attempting regex-based inventory")
        # crude fallback: find lines like mdhn:tgm123456 or full URIs
        subjects = {}
        for m in re.finditer(r"(mdhn:tgm\d+|tgm\d+)", ttl_text):
            token = m.group(1)
            # try to find label nearby
            label_m = re.search(rf"{re.escape(token)}.*?rdfs:label\s+\"([^\"]+)\"", ttl_text[m.start():m.start()+200], re.S)
            label = label_m.group(1) if label_m else "unknown"
            full = token if token.startswith("http") else token
            subjects[full] = {"local": token.split(":")[-1], "label": label}
        mapping = build_mapping(subjects)
        write_mapping_csv(mapping)
        write_per_uri_logs(mapping, root, ttl_text)
        logging.info("Dry-run complete (rdflib missing). Mapping written to %s", MAPPING_CSV)
        return

    g = Graph()
    g.parse(str(ttl_path))
    tgm_subjects = find_tgm_subjects_with_rdflib(g)
    logging.info("Found %d TGM subjects", len(tgm_subjects))

    mapping = build_mapping(tgm_subjects)
    write_mapping_csv(mapping)
    write_per_uri_logs(mapping, root, ttl_text)

    if args.apply:
        # backups
        make_backup([ttl_path, root])
        logging.info("Backups created in %s", BACKUP_DIR)
        # replace TTL graph
        newg = update_ttl_graph(g, mapping)
        migrated = ttl_path.parent / (ttl_path.stem + ".migrated.ttl")
        newg.serialize(destination=str(migrated), format="turtle")
        logging.info("Migrated TTL written to %s", migrated)
        # replace in json files
        replaced = replace_in_json_files(root, mapping, apply=True)
        logging.info("Replaced references in %d JSON files", len(replaced))
    else:
        replaced = replace_in_json_files(root, mapping, apply=False)
        logging.info("Dry-run: found references in %d JSON files (no files modified)", len(replaced))

    logging.info("Mapping CSV: %s", MAPPING_CSV)
    logging.info("Per-URI logs in: %s", LOG_DIR)


if __name__ == '__main__':
    main()
