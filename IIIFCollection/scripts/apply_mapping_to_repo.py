#!/usr/bin/env python3
"""
Apply mapping CSV replacements across repository files (.json, .ttl, .md).
Creates backups under IIIFCollection/backups/modified_files/<timestamp>/...
Writes a change log at IIIFCollection/mapping_apply_report.json

Usage:
  python apply_mapping_to_repo.py

Note: run from anywhere; paths are repository-inner absolute by default.
"""
import csv
import json
import shutil
import time
from pathlib import Path

ROOT = Path(r"c:\Users\Floyd\IIIFCollection\IIIFCollection")
MAPPING_CSV = ROOT / "tgm_id_mapping.csv"
BACKUP_BASE = ROOT / "backups" / "modified_files"
REPORT = ROOT / "mapping_apply_report.json"

EXCLUDE_DIRS = {"backups", "logs", "scripts", ".git"}
EXTS = {".json", ".ttl", ".md"}


def read_mapping(csv_path: Path):
    m = {}
    with csv_path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            old = row["old_uri"].strip()
            new = row["new_uri"].strip()
            if old and new:
                m[old] = new
                # also add prefixed form if the old URI contains the mdhn local name
                # e.g. http://example.com/mdhn/tgm000375 -> mdhn:tgm000375
                parts = old.replace("\\", "/").rsplit('/', 1)
                if len(parts) == 2:
                    local = parts[1]
                    pref = f"mdhn:{local}"
                    # new prefixed form
                    new_local = new.rsplit('/', 1)[-1]
                    new_pref = f"mdhn:{new_local}"
                    m[pref] = new_pref
                    # also add bare local (tgmNNNN) -> new pref form
                    m[local] = new_pref
    return m


def should_skip(path: Path):
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def main():
    print("Starting mapping apply script")
    if not MAPPING_CSV.exists():
        print("Mapping CSV not found:", MAPPING_CSV)
        return
    mapping = read_mapping(MAPPING_CSV)
    print(f"Loaded {len(mapping)} mapping entries (including expanded forms)")
    # sort by length desc to avoid partial overlaps
    olds_sorted = sorted(mapping.keys(), key=lambda s: -len(s))

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_root = BACKUP_BASE / timestamp
    backup_root.mkdir(parents=True, exist_ok=True)

    report = {"timestamp": timestamp, "files_modified": [], "total_replacements": 0}

    for path in ROOT.rglob("*"):
        if path.is_dir():
            continue
        if should_skip(path.relative_to(ROOT)):
            continue
        if path.name == MAPPING_CSV.name:
            continue
        if path.suffix.lower() not in EXTS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        original = text
        count = 0
        for old in olds_sorted:
            if old in text:
                new = mapping[old]
                c = text.count(old)
                if c:
                    text = text.replace(old, new)
                    count += c
        if text != original:
            # backup file preserving relative structure
            dest = backup_root / path.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
            # write updated file
            path.write_text(text, encoding="utf-8")
            report_entry = {"file": str(path.relative_to(ROOT)), "replacements": count}
            report["files_modified"].append(report_entry)
            report["total_replacements"] += count
    # write report
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Done. Files modified:", len(report["files_modified"]))
    print("Total replacements:", report["total_replacements"]) 
    print("Backups at:", str(backup_root))
    print("Report at:", str(REPORT))

if __name__ == '__main__':
    main()
