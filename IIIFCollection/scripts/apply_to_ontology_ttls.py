#!/usr/bin/env python3
from pathlib import Path
import csv, json, shutil, time, re

ROOT = Path(r"c:\Users\Floyd\IIIFCollection\IIIFCollection\Ontology")
MAPPING = Path(r"c:\Users\Floyd\IIIFCollection\IIIFCollection\tgm_id_mapping.csv")
BACKUP = Path(r"c:\Users\Floyd\IIIFCollection\IIIFCollection\backups\ontology_ttls_")
REPORT = Path(r"c:\Users\Floyd\IIIFCollection\IIIFCollection\ontology_ttl_report.json")

# load mapping into dict of local->new_local
map_local = {}
with MAPPING.open(encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        old = row['old_uri'].strip()
        new = row['new_uri'].strip()
        local = old.rsplit('/',1)[-1]
        new_local = new.rsplit('/',1)[-1]
        map_local[local] = new_local

# regex to find mdhn:tgmNNNN
pattern = re.compile(r"mdhn:tgm(\d{3,6})")

ts = time.strftime('%Y%m%d_%H%M%S')
backup_dir = BACKUP.with_name(BACKUP.name + ts)
backup_dir.mkdir(parents=True, exist_ok=True)
report = {'timestamp':ts, 'files':[], 'total':0}

for ttl in ROOT.glob('*.ttl'):
    if ttl.name.lower() in ('lctgm_rdf.ttl','lctgm_rdf.migrated.ttl'):
        continue
    text = ttl.read_text(encoding='utf-8')
    modified = False
    repl_count = 0
    def repl(m):
        nonlocal modified, repl_count
        local = 'tgm' + m.group(1)
        if local in map_local:
            new_local = map_local[local]
            modified = True
            repl_count += 1
            return f'mdhn:{new_local}'
        return m.group(0)
    newtext = pattern.sub(repl, text)
    if modified:
        dest = backup_dir / ttl.name
        shutil.copy2(ttl, dest)
        ttl.write_text(newtext, encoding='utf-8')
        report['files'].append({'file':str(ttl.name),'replacements':repl_count})
        report['total'] += repl_count

REPORT.write_text(json.dumps(report, indent=2), encoding='utf-8')
print('Done', report['total'], 'replacements in', len(report['files']), 'files')
