import json
import requests
from copy import deepcopy

def fetch_manifest(url):
    try:
        response = requests.get(url, timeout=12)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def determine_version(manifest):
    ctx = manifest.get('@context', [])
    if isinstance(ctx, str):
        ctx = [ctx]
    for c in ctx:
        if 'presentation/3' in c:
            return 3
        if 'presentation/2' in c:
            return 2
    return 3  # default for your sources

def generate_combined_manifest(
    selected_ids,
    include_toc=False,
    output_version=None,
    base_url="https://iiif.archive.org/iiif/3/",
    local_base="https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/",  # ← change to your real base URL
):
    manifest_urls = [f"{base_url}{id_.strip()}/manifest.json" for id_ in selected_ids]
    
    sources = []
    versions = set()
    
    for url, item_id in zip(manifest_urls, selected_ids):
        manifest = fetch_manifest(url)
        if manifest is None:
            continue
        ver = determine_version(manifest)
        versions.add(ver)
        sources.append((item_id, manifest))
    
    if not sources:
        raise ValueError("No valid manifests fetched")
    if len(versions) > 1:
        raise ValueError(f"Mixed versions: {versions}")
    
    source_version = list(versions)[0]
    if output_version is None:
        output_version = source_version
    
    if output_version not in (2, 3):
        raise ValueError("Only 2 or 3 supported")
    
    print(f"Generating IIIF {output_version}.0 manifest with {len(sources)} items")
    
    # ─── New combined manifest ───────────────────────────────────────────────
    if output_version == 3:
        new_manifest = {
            "@context": "http://iiif.io/api/presentation/3/context.json",
            "id": f"{local_base}combined/manifest.json",
            "type": "Manifest",
            "label": {"none": [f"Combined selection ({len(sources)} items)"]},
            "items": [],
            "structures": [] if include_toc else None,
            "metadata": [],
            "thumbnail": sources[0][1].get("thumbnail") if sources else None
        }
    else:  # v2
        new_manifest = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": f"{local_base}combined/manifest.json",
            "@type": "sc:Manifest",
            "label": f"Combined selection ({len(sources)} items)",
            "sequences": [{
                "@id": f"{local_base}combined/sequence/default",
                "@type": "sc:Sequence",
                "canvases": []
            }],
            "structures": [] if include_toc else None,
            "metadata": [],
            "thumbnail": sources[0][1].get("thumbnail") if sources else None
        }
    
    canvas_labels = []
    
    for idx, (item_id, source) in enumerate(sources):
        # Always extract from v3 location (your sources are v3)
        source_canvases = source.get("items", [])
        
        if not source_canvases:
            print(f"Warning: {item_id} has no top-level items → skipped")
            continue
        
        # Take the first canvas
        canvas = deepcopy(source_canvases[0])
        
        # New local ID
        safe_id = item_id.replace(".", "-").replace(" ", "_")
        if output_version == 3:
            canvas["id"] = f"{local_base}combined/{safe_id}/canvas"
        else:
            canvas["@id"] = f"{local_base}combined/{safe_id}/canvas"
            # v2 requires @type on canvas
            if "@type" not in canvas:
                canvas["@type"] = "sc:Canvas"
        
        # Append correctly depending on output version
        if output_version == 3:
            new_manifest["items"].append(canvas)
        else:
            new_manifest["sequences"][0]["canvases"].append(canvas)
        
        # Label for TOC
        label = source.get("label", f"Item {idx+1}")
        if isinstance(label, dict):
            label = next(iter(label.values()))[0] if label else "Untitled"
        elif isinstance(label, (list, tuple)):
            label = label[0] if label else "Untitled"
        else:
            label = str(label)
        canvas_labels.append(label)
    
    # Validation
    if output_version == 3 and not new_manifest["items"]:
        raise ValueError("No canvases added (v3)")
    if output_version == 2 and not new_manifest["sequences"][0]["canvases"]:
        raise ValueError("No canvases added (v2)")
    
    # ─── Optional TOC / structures ──────────────────────────────────────────
    if include_toc and canvas_labels:
        if output_version == 3:
            root = {
                "id": f"{local_base}combined/range/root",
                "type": "Range",
                "label": {"en": ["Table of Contents"]},
                "items": []
            }
            for i, lbl in enumerate(canvas_labels):
                root["items"].append({
                    "id": f"{local_base}combined/range/{i}",
                    "type": "Range",
                    "label": {"none": [lbl]},
                    "items": [{"id": new_manifest["items"][i]["id"], "type": "Canvas"}]
                })
            new_manifest["structures"] = [root]
        else:
            root = {
                "@id": f"{local_base}combined/range/root",
                "@type": "sc:Range",
                "label": "Table of Contents",
                "ranges": []
            }
            for i, lbl in enumerate(canvas_labels):
                root["ranges"].append({
                    "@id": f"{local_base}combined/range/{i}",
                    "@type": "sc:Range",
                    "label": lbl,
                    "canvases": [new_manifest["sequences"][0]["canvases"][i]["@id"]]
                })
            new_manifest["structures"] = [root]
    
    # Metadata aggregation (optional)
    for item_id, src in sources:
        for md in src.get("metadata", []):
            new_manifest["metadata"].append({
                "label": f"From {item_id} – {md.get('label','Property')}",
                "value": md.get("value")
            })
    
    return new_manifest


# ─── Run example ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    selected_items = ["HV.100", "HV.30", "HV.307"]
    
    include_structures = True
    force_version = 3               # ← now should work
    
    try:
        combined = generate_combined_manifest(
            selected_items,
            include_toc=include_structures,
            output_version=force_version,
            # local_base="https://your-server.example/iiif/"
        )
        
        filename = f"C:\\Users\\Floyd\\IIIFCollection\\IIIFCollection\\util_script\\combined_manifest_v{force_version or 'auto'}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        
        print(f"\nSaved to: {filename}")
        if force_version == 3:
            print(f"Canvases: {len(combined.get('items', []))}")
        else:
            print(f"Canvases: {len(combined['sequences'][0].get('canvases', []))}")
            
    except Exception as e:
        print(f"Error: {e}")