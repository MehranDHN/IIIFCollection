#!/usr/bin/env python3
"""
Run both replacer scripts, capture their stdout/stderr, and produce a summary report
at IIIFCollection/migration_reports_summary.json. This wrapper always writes a
report (even if replacers produced no files) and lists backup folders created.
"""
import subprocess
import json
from pathlib import Path
import time

ROOT = Path(r"c:\Users\Floyd\IIIFCollection\IIIFCollection")
REPORT = ROOT / "migration_reports_summary.json"
SCRIPTS = [ROOT / 'scripts' / 'apply_prefix_mapping.py', ROOT / 'scripts' / 'apply_mapping_to_repo.py']
BACKUP_ROOT = ROOT / 'backups'

summary = {'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'), 'runs': []}

for script in SCRIPTS:
    entry = {'script': str(script.name), 'stdout': '', 'stderr': '', 'returncode': None}
    if not script.exists():
        entry['stderr'] = 'script not found'
        entry['returncode'] = -1
        summary['runs'].append(entry)
        continue
    try:
        proc = subprocess.run(['python', str(script)], capture_output=True, text=True, timeout=600)
        entry['stdout'] = proc.stdout
        entry['stderr'] = proc.stderr
        entry['returncode'] = proc.returncode
    except Exception as e:
        entry['stderr'] = str(e)
        entry['returncode'] = -2
    summary['runs'].append(entry)

# collect backup folders created under backups
backups = []
if BACKUP_ROOT.exists():
    for p in sorted(BACKUP_ROOT.iterdir()):
        if p.is_dir():
            # count files inside
            count = sum(1 for _ in p.rglob('*') if _.is_file())
            backups.append({'path': str(p.relative_to(ROOT)), 'file_count': count})
summary['backups'] = backups

# list any report JSONs present at repo root
reports = []
for name in ('prefix_mapping_report.json','mapping_apply_report.json','prefix_mapping_report.json','ontology_ttl_report.json'):
    p = ROOT / name
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            data = None
        reports.append({'path': str(p.relative_to(ROOT)), 'size': p.stat().st_size, 'parsed': data is not None})
summary['reports'] = reports

REPORT.write_text(json.dumps(summary, indent=2), encoding='utf-8')
print('Summary written to', REPORT)
