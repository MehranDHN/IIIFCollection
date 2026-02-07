#!/usr/bin/env python3
"""Direct TTL migration with file-based logging"""
import csv
import json
import logging
import sys
from pathlib import Path
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDFS, OWL

log_file = Path("c:\\Users\\Floyd\\IIIFCollection\\migration_execution.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

ttl_path = Path("c:\\Users\\Floyd\\IIIFCollection\\IIIFCollection\\Ontology\\LCTGM_RDF.ttl")
mapping_csv = Path("c:\\Users\\Floyd\\IIIFCollection\\IIIFCollection\\tgm_id_mapping.csv")
backup_ttl = Path("c:\\Users\\Floyd\\IIIFCollection\\IIIFCollection\\backups\\LCTGM_RDF.ttl.backup")
migrated_ttl = ttl_path.parent / (ttl_path.stem + ".migrated.ttl")

logging.info("Starting direct migration")

# Read mapping
mapping = {}
with mapping_csv.open() as f:
    reader = csv.DictReader(f)
    for row in reader:
        mapping[row["old_uri"]] = row["new_uri"]
logging.info(f"Loaded {len(mapping)} mappings from CSV")

# Parse TTL
logging.info(f"Parsing {ttl_path}")
g = Graph()
g.parse(str(ttl_path))
logging.info(f"Parsed graph with {len(g)} triples")

# Create backup
backup_ttl.parent.mkdir(parents=True, exist_ok=True)
g.serialize(destination=str(backup_ttl), format="turtle")
logging.info(f"Backup created at {backup_ttl}")

# Build new graph
logging.info("Building migrated graph with new URIs and owl:sameAs redirects")
newg = Graph()
for prefix, ns in g.namespaces():
    newg.bind(prefix, ns)

replaced_count = 0
for s, p, o in g:
    s_str = str(s)
    o_str = str(o) if isinstance(o, URIRef) else None
    
    new_s = URIRef(mapping[s_str]) if s_str in mapping else s
    new_p = p
    new_o = URIRef(mapping[o_str]) if o_str and o_str in mapping else o
    
    newg.add((new_s, new_p, new_o))
    
    if s_str in mapping or (o_str and o_str in mapping):
        replaced_count += 1

logging.info(f"Replaced {replaced_count} triples with new URIs")

# Add owl:sameAs for backward compatibility
logging.info("Adding owl:sameAs redirects for backward compatibility")
for old, new in mapping.items():
    newg.add((URIRef(old), OWL.sameAs, URIRef(new)))
logging.info(f"Added {len(mapping)} owl:sameAs triples")

# Serialize
logging.info(f"Serializing to {migrated_ttl}")
newg.serialize(destination=str(migrated_ttl), format="turtle")
logging.info(f"Migration complete. Migrated TTL written to {migrated_ttl}")

# Verify
newg2 = Graph()
newg2.parse(str(migrated_ttl))
logging.info(f"Verification: migrated graph contains {len(newg2)} triples")

logging.info("SUCCESS: Migration completed")
