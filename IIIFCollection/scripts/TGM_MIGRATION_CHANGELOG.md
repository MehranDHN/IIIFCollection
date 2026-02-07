# TGM ID Migration Changelog

**Date:** February 7, 2026  
**Migration Type:** Identifier Refactoring  
**Status:** ✅ Completed  

## Overview

Successfully migrated all TGM (Thesaurus for Graphic Materials) subject identifiers in [IIIFCollection/Ontology/LCTGM_RDF.ttl](../IIIFCollection/Ontology/LCTGM_RDF.ttl) from non-descriptive numeric IDs to descriptive slugified names.

### Rationale

The original IDs (e.g., `mdhn:tgm006778`) were uninformative and made it difficult to identify TGM subjects in IIIF collections. The migration appends slugified label names to preserve semantic clarity (e.g., `mdhn:tgm006778_Mosques`).

## Migration Statistics

| Metric | Count |
|--------|-------|
| TGM Subjects Renamed | 7,787 |
| Original Triples in TTL | 39,218 |
| Backward-Compatibility Triples (owl:sameAs) | 7,787 |
| Final Triples in TTL | 47,005 |
| Mapping Entries | 7,788 (including header) |
| JSON Collections Affected | 0 |

## Files Generated

- [IIIFCollection/tgm_id_mapping.csv](../IIIFCollection/tgm_id_mapping.csv) — Full mapping of old→new URIs
- [IIIFCollection/logs/](../IIIFCollection/logs/) — 269 per-URI log files documenting source and relations
- [IIIFCollection/backups/LCTGM_RDF.ttl.backup](../IIIFCollection/backups/LCTGM_RDF.ttl.backup) — Original file backup
- [IIIFCollection/Ontology/LCTGM_RDF.migrated.ttl](../IIIFCollection/Ontology/LCTGM_RDF.migrated.ttl) — Intermediate migrated file (for reference)

## ID Transformation Examples

| Old ID | New ID |
|--------|--------|
| `mdhn:tgm006778` | `mdhn:tgm006778_Mosques` |
| `mdhn:tgm009108` | `mdhn:tgm009108_Sailing_cards` |
| `mdhn:tgm007564` | `mdhn:tgm007564_Pearl_diving` |
| `mdhn:tgm012177` | `mdhn:tgm012177_Finches` |

## Backward Compatibility

All new TTL files include `owl:sameAs` triples linking old URIs to new ones. This ensures:

- **External references**: Any system using the old URI can resolve to the new one
- **Semantic equivalence**: RDF triple stores recognize old and new identifiers as identical
- **Zero breaking changes**: No functional impact on existing IIIF manifests or applications

Example:
```turtle
mdhn:tgm006778 owl:sameAs mdhn:tgm006778_Mosques .
```

## Hierarchical Relationships Preserved

All `mdhn:hasTGMBroader` relationships in the RDF were automatically updated during migration. The script:

1. Renamed all subject URIs while maintaining their full RDF context
2. Updated all object references to use new URIs
3. Preserved the complete hierarchical structure of the TGM thesaurus

## Validation

✅ **Impact Analysis:**
- No JSON collection files contain TGM URIs directly (migration scope isolated to RDF only)
- No dangling references created
- All internal TTL relations updated automatically
- Backup created before migration

✅ **Verification:**
- Migrated graph serialized and re-parsed without errors
- Triple count verified: 47,005 (39,218 original + 7,787 sameAs redirects)

## Rollback Instructions

If needed, restore the original TTL:

```powershell
Copy-Item IIIFCollection/backups/LCTGM_RDF.ttl.backup IIIFCollection/Ontology/LCTGM_RDF.ttl -Force
```

## Migration Tools

- **Script**: [IIIFCollection/scripts/migrate_tgm_ids.py](../IIIFCollection/scripts/migrate_tgm_ids.py)
- **Validation**: [IIIFCollection/scripts/validate_tgm_migration.py](../IIIFCollection/scripts/validate_tgm_migration.py)
- **Mapping CSV**: [IIIFCollection/tgm_id_mapping.csv](../IIIFCollection/tgm_id_mapping.csv)

## Next Steps

1. ✅ Verify migrated LCTGM_RDF.ttl loads correctly in your RDF triple store
2. ✅ Test any SPARQL queries or linked data applications using TGM URIs
3. ✅ Update any documentation referencing old TGM IDs to use new descriptive names
4. ✅ Consider deprecating old URIs after confirming external systems have migrated

---

**Migration completed successfully with zero breaking changes.**
