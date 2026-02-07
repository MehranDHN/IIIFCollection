#!/usr/bin/env python3
"""
Final migration: Replace mdhn:tgmNNNN (prefixed non-underscored) with new underscored form
across all .ttl, .json, .md files using mapping CSV.

Outputs report to: IIIFCollection/final_migration_report_<timestamp>.json
Backups to: IIIFCollection/backups/final_migration_<timestamp>/
"""
import csv
import json
import re
import shutil
import time
from pathlib import Path

ROOT = Path(r"c:\Users\Floyd\IIIFCollection\IIIFCollection")
MAPPING_CSV = ROOT / "tgm_id_mapping.csv"
BACKUP_BASE = ROOT / "backups"
EXCLUDE_DIRS = {"backups", "logs", "scripts", ".git"}
EXTS = {".ttl", ".json", ".md"}

def load_mapping():
    """Load mapping and extract mdhn:localname mappings."""
    mapping = {}
    with MAPPING_CSV.open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            old = row['old_uri'].strip()
            new = row['new_uri'].strip()
            # Extract local names
            old_local = old.rsplit('/', 1)[-1]
            new_local = new.rsplit('/', 1)[-1]
            # Map mdhn:tgmNNNN -> mdhn:tgmNNNN_Slug
            mapping[f"mdhn:{old_local}"] = f"mdhn:{new_local}"
    return mapping

def should_skip(path):
    for part in path.relative_to(ROOT).parts:
        if part in EXCLUDE_DIRS:
            return True
    return False

def main():
    mapping = load_mapping()
    ts = time.strftime('%Y%m%d_%H%M%S')
    backup_root = BACKUP_BASE / f"final_migration_{ts}"
    backup_root.mkdir(parents=True, exist_ok=True)
    
    report = {
        'timestamp': ts,
        'mapping_count': len(mapping),
        'files_modified': [],
        'total_replacements': 0
    }
    
    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        if should_skip(path):
            continue
        if path.suffix.lower() not in EXTS:
            continue
        
        try:
            text = path.read_text(encoding='utf-8')
        except:
            continue
        
        orig = text
        repl_cnt = 0
        
        # Apply replacements
        for old_prefixed, new_prefixed in mapping.items():
            if old_prefixed in text:
                c = text.count(old_prefixed)
                text = text.replace(old_prefixed, new_prefixed)
                repl_cnt += c
        
        # If modified, back up and write
        if text != orig:
            dest = backup_root / path.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
            path.write_text(text, encoding='utf-8')
            report['files_modified'].append({
                'file': str(path.relative_to(ROOT)),
                'replacements': repl_cnt
            })
            report['total_replacements'] += repl_cnt
    
    # Write report
    report_path = ROOT / f"final_migration_report_{ts}.json"
    report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    
    # Also write a log
    log_text = f"""Final Migration Report
Timestamp: {ts}
Total Mappings: {report['mapping_count']}
Files Modified: {len(report['files_modified'])}
Total Replacements: {report['total_replacements']}
Backups: {backup_root}
Report: {report_path}

Files Modified:
"""
    for entry in report['files_modified']:
        log_text += f"  {entry['file']}: {entry['replacements']} replacements\n"
    
    log_path = ROOT / f"final_migration_log_{ts}.txt"
    log_path.write_text(log_text, encoding='utf-8')

if __name__ == '__main__':
    main()
