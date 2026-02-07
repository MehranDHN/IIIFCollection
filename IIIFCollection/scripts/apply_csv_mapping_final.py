#!/usr/bin/env python3
"""
Apply CSV mapping (old_uri -> new_uri) across .json, .ttl, .md files.
Creates backups under IIIFCollection/backups/csv_replacements_<timestamp>/
Writes report to IIIFCollection/csv_replacements_report.json

Guaranteed to write report even if no files are modified.
"""
import csv
import json
import shutil
import time
from pathlib import Path

ROOT = Path(r"c:\Users\Floyd\IIIFCollection\IIIFCollection")
MAPPING_CSV = ROOT / "tgm_id_mapping.csv"
BACKUP_BASE = ROOT / "backups"
REPORT = ROOT / "csv_replacements_report.json"

EXCLUDE_DIRS = {"backups", "logs", "scripts", ".git"}
EXTS = {".json", ".ttl", ".md"}


def read_mapping():
    m = {}
    if not MAPPING_CSV.exists():
        print(f"ERROR: {MAPPING_CSV} not found")
        return m
    with MAPPING_CSV.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            old = row["old_uri"].strip()
            new = row["new_uri"].strip()
            if old and new:
                m[old] = new
    print(f"Loaded {len(m)} mappings from CSV")
    return m


def should_skip(path: Path):
    for part in path.relative_to(ROOT).parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def main():
    print("Starting CSV-based replacer...")
    mapping = read_mapping()
    
    if not mapping:
        print("No mappings loaded. Aborting.")
        return

    # sort by length descending to avoid partial overlaps
    olds_sorted = sorted(mapping.keys(), key=lambda s: -len(s))
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_root = BACKUP_BASE / f"csv_replacements_{timestamp}"
    backup_root.mkdir(parents=True, exist_ok=True)
    
    report = {"timestamp": timestamp, "files_modified": [], "total_replacements": 0}
    
    count = 0
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path):
            continue
        if path.name == MAPPING_CSV.name:
            continue
        if path.suffix.lower() not in EXTS:
            continue
        
        count += 1
        if count % 100 == 0:
            print(f"  scanned {count} files...")
        
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  skip {path}: {e}")
            continue
        
        original = text
        repl_count = 0
        
        for old in olds_sorted:
            if old in text:
                new = mapping[old]
                c = text.count(old)
                text = text.replace(old, new)
                repl_count += c
        
        if text != original:
            # create backup
            dest = backup_root / path.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
            # write updated file
            path.write_text(text, encoding="utf-8")
            rel = str(path.relative_to(ROOT))
            report["files_modified"].append({"file": rel, "replacements": repl_count})
            report["total_replacements"] += repl_count
            print(f"  updated {path.name}: {repl_count} replacements")
    
    # write report
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("\n=== CSV Replacer Complete ===")
    print(f"Files modified: {len(report['files_modified'])}")
    print(f"Total replacements: {report['total_replacements']}")
    print(f"Backups at: {backup_root}")
    print(f"Report at: {REPORT}")


if __name__ == "__main__":
    main()
