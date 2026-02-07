#!/usr/bin/env python3
"""
Validation script to analyze which JSON files would be affected by the TGM ID migration.
Produces a validation report without modifying any files.

Usage:
  python validate_tgm_migration.py --mapping IIIFCollection/tgm_id_mapping.csv --root IIIFCollection
"""
import argparse
import csv
import json
import logging
from pathlib import Path
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

REPORT_FILE = Path("IIIFCollection/migration_validation_report.txt")


def read_mapping_csv(csv_path: Path) -> dict:
    mapping = {}
    with csv_path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            mapping[row["old_uri"]] = row["new_uri"]
    return mapping


def scan_json_files(root: Path, mapping: dict):
    """Scan all JSON files and find which ones contain old URIs."""
    affected_files = defaultdict(lambda: {"count": 0, "old_uris": set()})
    
    for json_path in root.rglob("*.json"):
        try:
            text = json_path.read_text(encoding="utf-8")
        except Exception as e:
            logging.warning("Failed to read %s: %s", json_path, e)
            continue
        
        for old_uri in mapping:
            if old_uri in text:
                count = text.count(old_uri)
                affected_files[str(json_path)]["count"] += count
                affected_files[str(json_path)]["old_uris"].add(old_uri)
    
    return affected_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping", required=True, help="Path to tgm_id_mapping.csv")
    parser.add_argument("--root", default="IIIFCollection", help="Root dir to scan for JSON files")
    args = parser.parse_args()

    mapping_path = Path(args.mapping)
    root = Path(args.root)

    if not mapping_path.exists():
        logging.error("Mapping file not found: %s", mapping_path)
        return

    mapping = read_mapping_csv(mapping_path)
    logging.info("Loaded mapping: %d old→new URI pairs", len(mapping))

    affected_files = scan_json_files(root, mapping)
    logging.info("Found %d JSON files with old TGM URIs", len(affected_files))

    total_replacements = sum(info["count"] for info in affected_files.values())
    logging.info("Total URI occurrences to replace: %d", total_replacements)

    # Write detailed report
    with REPORT_FILE.open("w", encoding="utf-8") as fh:
        fh.write("=" * 80 + "\n")
        fh.write("TGM ID Migration Validation Report\n")
        fh.write("=" * 80 + "\n\n")
        
        fh.write(f"Mapping entries: {len(mapping)}\n")
        fh.write(f"Affected JSON files: {len(affected_files)}\n")
        fh.write(f"Total URI replacements: {total_replacements}\n\n")
        
        fh.write("Affected Files (sorted by replacement count):\n")
        fh.write("-" * 80 + "\n")
        
        for filepath, info in sorted(affected_files.items(), 
                                      key=lambda x: x[1]["count"], 
                                      reverse=True):
            fh.write(f"\nFile: {filepath}\n")
            fh.write(f"  Occurrences: {info['count']}\n")
            fh.write(f"  Old URIs found: {len(info['old_uris'])}\n")
            for old_uri in sorted(info['old_uris']):
                count = Path(filepath).read_text(encoding="utf-8").count(old_uri)
                fh.write(f"    - {old_uri}: {count} times\n")

    logging.info("Validation report written to %s", REPORT_FILE)

    # Print summary to console
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Mapping entries:         {len(mapping)}")
    print(f"Affected JSON files:     {len(affected_files)}")
    print(f"Total replacements:      {total_replacements}")
    print(f"\nReport saved to: {REPORT_FILE}")
    print("\nTop 10 most affected files:")
    for filepath, info in sorted(affected_files.items(), 
                                  key=lambda x: x[1]["count"], 
                                  reverse=True)[:10]:
        fname = Path(filepath).name
        print(f"  {fname}: {info['count']} replacements")


if __name__ == '__main__':
    main()
