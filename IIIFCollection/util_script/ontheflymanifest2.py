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
    base_url="https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/manifests/",
    local_base="https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/",  # ← change to your real base URL
):
    manifest_urls = [f"{base_url}{id_.strip()}.json" for id_ in selected_ids]
    
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
        canvas["label"] = {"none": [f"{idx+1} from {item_id}"]}  # Override label to item ID for clarity
        #canvas_lbl = canvas.get("label", f"Canvas {idx+1}")
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
    #for item_id, src in sources:
        #for md in src.get("metadata", []):
            #new_manifest["metadata"].append({
                #"label": f"From {item_id} – {md.get('label','Property')}",
                #"value": md.get("value")
            #})
    
    return new_manifest


# ─── Run example ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    selected_items =  [
"AG20K002297",
"AG20K002298",
"AG20K002299",
"AG20K002300",
"AG20K002301",
"AG20K002302",
"AG20K002303",
"AG20K002304",
"AG20K002305",
"AG20K002306",
"AG20K002307",
"AG20K002308",
"AG20K002309",
"AG20K002310",
"AG20K002311",
"AG20K002312",
"AG20K002313",
"AG20K002314",
"AG20K002315",
"AG20K002325",
"AG20K002326",
"AG20K002327",
"AG20K002328",
"AG20K002329",
"AG20K002330",
"AG20K002331",
"AG20K002332",
"AG20K002333",
"AG20K002334",
"AG20K002335",
"AG20K002336",
"AG20K002337",
"AG20K002338",
"AG20K002339",
"AG20K002340",
"AG20K002367",
"AG20K002368",
"AG20K002369",
"AG20K002370",
"AG20K002371",
"AG20K002372",
"AG20K002373",
"AG20K002374",
"AG20K002375",
"AG20K002376",
"AG20K002377",
"AG20K002378",
"AG20K002379",
"AG20K002380",
"AG20K002381",
"AG20K002382",
"AG20K004089",
"AG20K005111",
"AG20K005112",
"AG20K005113",
"AG20K005114",
"AG20K005115",
"AG20K005116",
"AG20K005117",
"AG20K005119",
"AG20K005120",
"AG20K005121",
"AG20K005122",
"AG20K005123",
"AG20K005124",
"AG20K005125",
"AG20K005127",
"AG20K005128",
"AG20K005129",
"AG20K005130",
"AG20K005132",
"AG20K005133",
"AG20K005134",
"AG20K005135",
"AG20K005136",
"AG20K005137",
"AG20K005138",
"AG20K005139",
"AG20K005140",
"AG20K005141",
"AG20K005142",
"AG20K005143",
"AG20K005144",
"AG20K005145",
"AG20K005146",
"AG20K005147",
"AG20K005148",
"AG20K005150",
"AG20K005151",
"AG20K005152",
"AG20K005153",
"AG20K005154",
"AG20K005155",
"AG20K005156",
"AG20K005157",
"AG20K005158",
"AG20K005159",
"AG20K005160",
"AG20K005161",
"AG20K005162",
"AG20K005163",
"AG20K005164",
"AG20K005165",
"AG20K005166",
"AG20K005167",
"AG20K005168",
"AG20K005169",
"AG20K005170",
"AG20K005171",
"AG20K005172",
"AG20K005174",
"AG20K005175",
"AG20K005176",
"AG20K005177",
"AG20K005178",
"AG20K005179",
"AG20K005180",
"AG20K005181",
"AG20K005182",
"AG20K005183",
"AG20K005185",
"AG20K005186",
"AG20K005187",
"AG20K005188",
"AG20K005189",
"AG20K005190",
"AG20K005191",
"AG20K005192",
"AG20K005193",
"AG20K005194",
"AG20K005197",
"AG20K005198",
"AG20K005199",
"AG20K005200",
"AG20K005201",
"AG20K005204",
"AG20K005205",
"AG20K005206",
"AG20K005207",
"AG20K005208",
"AG20K005209",
"AG20K005210",
"AG20K005211",
"AG20K005212",
"AG20K005213",
"AG20K005214",
"AG20K005215",
"AG20K005216",
"AG20K005217"
]
    
    include_structures = True
    force_version = 3               # ← now should work
    
    try:
        combined = generate_combined_manifest(
            selected_items,
            include_toc=include_structures,
            output_version=force_version,
            # local_base="https://your-server.example/iiif/"
        )
        
        filename = f"C:\\Users\\Floyd\\IIIFCollection\\IIIFCollection\\util_script\\combined_Agabriel_manifest_v{force_version or 'auto'}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        
        print(f"\nSaved to: {filename}")
        if force_version == 3:
            print(f"Canvases: {len(combined.get('items', []))}")
        else:
            print(f"Canvases: {len(combined['sequences'][0].get('canvases', []))}")
            
    except Exception as e:
        print(f"Error: {e}")