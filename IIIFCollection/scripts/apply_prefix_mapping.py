#!/usr/bin/env python3
"""
Apply prefix-style mapping (mdhn:tgmNNNN -> mdhn:tgmNNNN_Slug) across .ttl, .json, .md files.
Writes report to ROOT/prefix_mapping_report.json and backups under backups/modified_files/<ts>/
"""
from pathlib import Path
import csv, json, shutil, time

ROOT = Path(r"c:\Users\Floyd\IIIFCollection\IIIFCollection")
MAPPING_CSV = ROOT / "tgm_id_mapping.csv"
BACKUP_BASE = ROOT / "backups" / "modified_files_prefix"
REPORT = ROOT / "prefix_mapping_report.json"
EXCLUDE = {"backups","logs","scripts",".git"}
EXTS = {".ttl", ".json", ".md"}


def load_prefix_map(csvp):
    m = {}
    with csvp.open(encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            old = row['old_uri'].strip()
            new = row['new_uri'].strip()
            # derive local id
            local = old.rsplit('/',1)[-1]
            new_local = new.rsplit('/',1)[-1]
            m[f"mdhn:{local}"] = f"mdhn:{new_local}"
            m[local] = f"mdhn:{new_local}"
    return m


def should_skip(p: Path):
    for part in p.relative_to(ROOT).parts:
        if part in EXCLUDE:
            return True
    return False


def main():
    if not MAPPING_CSV.exists():
        print('mapping csv missing')
        return
    mapping = load_prefix_map(MAPPING_CSV)
    olds = sorted(mapping.keys(), key=lambda s: -len(s))
    ts = time.strftime('%Y%m%d_%H%M%S')
    back = BACKUP_BASE/ts
    back.mkdir(parents=True, exist_ok=True)
    report = {'timestamp':ts, 'files_modified':[], 'total':0}
    for p in ROOT.rglob('*'):
        if p.is_dir():
            continue
        if should_skip(p):
            continue
        if p.suffix.lower() not in EXTS:
            continue
        try:
            text = p.read_text(encoding='utf-8')
        except Exception:
            continue
        orig = text
        cnt = 0
        for o in olds:
            if o in text:
                c = text.count(o)
                text = text.replace(o, mapping[o])
                cnt += c
        if text != orig:
            dest = back / p.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
            p.write_text(text, encoding='utf-8')
            report['files_modified'].append({'file':str(p.relative_to(ROOT)),'replacements':cnt})
            report['total'] += cnt
    REPORT.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('done', report['total'], 'replacements in', len(report['files_modified']), 'files')

if __name__=='__main__':
    main()
