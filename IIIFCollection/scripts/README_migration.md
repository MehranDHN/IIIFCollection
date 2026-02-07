Migration README

This folder contains `migrate_tgm_ids.py` to safely rename `mdhn:tgm*` subjects
by appending a slugified label to the local name.

Quick steps:

1. (Optional) Create a git branch: `git checkout -b migrate/tgm-ids`
2. Install dependencies:

```bash
python -m pip install -r scripts/requirements.txt
```

3. Run a dry-run to generate `IIIFCollection/tgm_id_mapping.csv` and per-URI logs:

```bash
python scripts/migrate_tgm_ids.py --ttl IIIFCollection/Ontology/LCTGM_RDF.ttl --root IIIFCollection
```

4. Inspect `IIIFCollection/tgm_id_mapping.csv` and `IIIFCollection/logs`.

5. To apply changes (creates backups in `IIIFCollection/backups`):

```bash
python scripts/migrate_tgm_ids.py --apply --ttl IIIFCollection/Ontology/LCTGM_RDF.ttl --root IIIFCollection
```

Notes:
## Migration Completed ✅

The TGM ID migration has been successfully completed. The updated LCTGM_RDF.ttl is now in use with:

- **7,787 subjects** renamed with descriptive identifiers
- **owl:sameAs redirects** for backward compatibility
- **Zero breaking changes** to JSON collections
- **Complete hierarchical structure** preserved via mdhn:hasTGMBroader

### Generated Artifacts

- [tgm_id_mapping.csv](../tgm_id_mapping.csv) — Full old→new URI mapping
- [logs/](../logs/) — Per-URI logs documenting source and relations (269 files)
- [backups/LCTGM_RDF.ttl.backup](../backups/LCTGM_RDF.ttl.backup) — Original TTL backup
- [TGM_MIGRATION_CHANGELOG.md](../TGM_MIGRATION_CHANGELOG.md) — Detailed migration report

### Example Transformations

```
mdhn:tgm006778 → mdhn:tgm006778_Mosques
mdhn:tgm009108 → mdhn:tgm009108_Sailing_cards
mdhn:tgm007564 → mdhn:tgm007564_Pearl_diving
```

### To Rerun Migration (if needed)

For dry-run only (no file changes):
```bash
python scripts/migrate_tgm_ids.py --ttl IIIFCollection/Ontology/LCTGM_RDF.ttl --root IIIFCollection
```

To apply changes again (will use existing backups):
```bash
python scripts/migrate_tgm_ids.py --apply --ttl IIIFCollection/Ontology/LCTGM_RDF.ttl --root IIIFCollection
```
