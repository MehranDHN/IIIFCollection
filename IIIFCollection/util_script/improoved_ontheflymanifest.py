import json
import requests
from copy import deepcopy

def fetch_manifest(url):
    try:
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def get_version(manifest):
    ctx = manifest.get('@context', [])
    if isinstance(ctx, str):
        ctx = [ctx]
    for c in ctx:
        if 'presentation/3' in c:
            return 3
        if 'presentation/2' in c:
            return 2
    return 3  # default

def get_label(obj):
    """Return human-readable label as string"""
    label = obj.get('label') or obj.get('@label', 'Untitled')
    if isinstance(label, dict):
        for lang in ('en', 'none', 'fr'):
            if lang in label and label[lang]:
                return label[lang][0] if isinstance(label[lang], list) else label[lang]
        return next(iter(label.values()))[0] if label else 'Untitled'
    if isinstance(label, list):
        return label[0] if label else 'Untitled'
    return str(label)

def get_canvases(manifest):
    """Return list of all canvases regardless of v2/v3"""
    if get_version(manifest) == 3:
        return manifest.get('items', [])
    else:
        seqs = manifest.get('sequences', [])
        return seqs[0].get('canvases', []) if seqs else []

def normalize_canvas(canvas, target_version):
    """Convert canvas between v2 <-> v3 (ID/type + annotation style)"""
    c = deepcopy(canvas)
    if target_version == 3:
        if '@id' in c: c['id'] = c.pop('@id')
        if '@type' in c: c['type'] = c.pop('@type')
        # v2 → v3 annotation conversion
        if 'images' in c and isinstance(c['images'], list):
            annos = c.pop('images')
            ap = {
                'id': (c.get('id') or c.get('@id') or 'annopage') + '/1',
                'type': 'AnnotationPage',
                'items': []
            }
            for a in annos:
                anno = deepcopy(a)
                if '@id' in anno: anno['id'] = anno.pop('@id')
                if '@type' in anno: anno['type'] = anno.pop('@type')
                if 'on' in anno: anno['target'] = anno.pop('on')
                ap['items'].append(anno)
            c['items'] = [ap]
    else:  # target v2
        if 'id' in c: c['@id'] = c.pop('id')
        if 'type' in c: c['@type'] = c.pop('type')
        # v3 → v2 annotation conversion
        if 'items' in c and isinstance(c['items'], list) and c['items'] and c['items'][0].get('type') == 'AnnotationPage':
            ap = c['items'][0]
            images = []
            for item in ap.get('items', []):
                anno = deepcopy(item)
                if 'id' in anno: anno['@id'] = anno.pop('id')
                if 'type' in anno: anno['@type'] = anno.pop('type')
                if 'target' in anno: anno['on'] = anno.pop('target')
                images.append(anno)
            c['images'] = images
            c.pop('items', None)
    return c

def add_custom_metadata(new_manifest, custom_md, output_version):
    if not custom_md:
        return
    for key, val in custom_md.items():
        if output_version == 3:
            label_d = key if isinstance(key, dict) else {"en": [str(key)]}
            value_d = val if isinstance(val, dict) else {"en": [str(val)]}
            new_manifest["metadata"].append({"label": label_d, "value": value_d})
        else:  # v2 simple
            new_manifest["metadata"].append({
                "label": str(key),
                "value": str(val)
            })

def generate_combined_manifest(
    sources,                          # list[str | dict] — see examples below
    include_toc=False,
    output_version=None,
    default_base_url="https://viewer.cbl.ie/viewer/api/v1/records/",
    local_base="https://raw.githubusercontent.com/MehranDHN/IIIFCollection/",   # ← CHANGE THIS
    custom_global_metadata=None
):
    # Normalize sources
    normalized = []
    for s in sources:
        if isinstance(s, str):
            if s.startswith("http"):
                normalized.append({"url": s, "canvas_indices": [0]})
            else:
                url = f"{default_base_url}{s.strip()}/manifest/"
                normalized.append({"url": url, "canvas_indices": [0], "id": s})
        elif isinstance(s, dict):
            if "url" in s:
                entry = {**s}
            elif "id" in s:
                base = s.get("base_url", default_base_url)
                url = s["id"] if s["id"].startswith("http") else f"{base}{s['id'].strip()}/manifest"
                entry = {**s, "url": url}
            else:
                raise ValueError("Source dict must contain 'url' or 'id'")
            entry.setdefault("canvas_indices", [0])
            normalized.append(entry)

    # Fetch & process
    if output_version is None:
        # take version of first successful source
        output_version = 3

    if output_version not in (2, 3):
        raise ValueError("output_version must be 2 or 3")

    print(f"Generating IIIF {output_version}.0 manifest from {len(normalized)} source(s)")

    if output_version == 3:
        new_manifest = {
            "@context": "http://iiif.io/api/presentation/3/context.json",
            "id": f"{local_base}combined/manifest.json",
            "type": "Manifest",
            "label": {"none": [f"Combined Manifest ({len(normalized)} sources)"]},
            "items": [],
            "structures": [] if include_toc else None,
            "metadata": [],
            "thumbnail": None
        }
    else:
        new_manifest = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": f"{local_base}combined/manifest.json",
            "@type": "sc:Manifest",
            "label": f"Combined Manifest ({len(normalized)} sources)",
            "sequences": [{
                "@id": f"{local_base}combined/sequence/default",
                "@type": "sc:Sequence",
                "canvases": []
            }],
            "structures": [] if include_toc else None,
            "metadata": [],
            "thumbnail": None
        }

    canvas_labels = []
    global_canvas_idx = 0

    for spec in normalized:
        manifest = fetch_manifest(spec["url"])
        if not manifest:
            continue

        source_label = get_label(manifest)
        indices = spec["canvas_indices"]

        all_canvases = get_canvases(manifest)
        selected = []
        for i in indices:
            if 0 <= i < len(all_canvases):
                selected.append(all_canvases[i])
            else:
                print(f"Warning: canvas index {i} out of range in {spec.get('id', spec['url'])}")

        for c_idx, raw_canvas in enumerate(selected):
            canvas = normalize_canvas(raw_canvas, output_version)

            # New local ID
            safe = spec.get("id", spec["url"].split("/")[-2]).replace(".", "-").replace(" ", "_")
            new_canvas_id = f"{local_base}combined/{safe}/canvas-{c_idx}"

            if output_version == 3:
                canvas["id"] = new_canvas_id
            else:
                canvas["@id"] = new_canvas_id

            old_lbl = get_label(canvas)
            canvas["label"] = {"none": [f"{global_canvas_idx} from {spec.get('id', spec['url'].split('/')[-2])} {old_lbl.strip()}"]}  # Override label to item ID for clarity

            # Add to manifest
            if output_version == 3:
                new_manifest["items"].append(canvas)
            else:
                new_manifest["sequences"][0]["canvases"].append(canvas)

            # Label for TOC
            canvas_lbl = get_label(canvas)
            if canvas_lbl == "Untitled":
                canvas_lbl = f"{source_label} — Canvas {c_idx + 1}"
            canvas_labels.append(canvas_lbl)

            global_canvas_idx += 1

    if not (new_manifest.get("items") or (new_manifest.get("sequences") and new_manifest["sequences"][0].get("canvases"))):
        raise ValueError("No canvases were extracted")

    # Add custom metadata (only source of metadata)
    add_custom_metadata(new_manifest, custom_global_metadata, output_version)

    # Optional TOC
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

    return new_manifest


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Example 1: Simple IDs (default base + first canvas only)
    sources_simple = ["Per_104_1", "Per_104_3", "Per_104_4"]

    # Example 2: Mixed flexible input (recommended)
    sources_flex = [
        #"Per_104_1",                                           # simple ID → default base, canvas 0
        #{"url": "https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/manifests/combined_viollet_photograph_v3.json",
         #"canvas_indices": [0, 10, 50]},                    # full URL + specific canvases
        #{"id": "HV.307", "canvas_indices": [0]},            # ID with explicit index
        {"id": "Per_104_1", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0, 1]},
        {"id": "Per_104_3", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0, 1]},
        {"id": "Per_104_4", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0, 1]},
        {"id": "Per_104_5", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0]},
        {"id": "Per_104_6", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0, 1]},
        {"id": "Per_104_7", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0, 1]},
        {"id": "Per_104_8", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0, 1]},
        {"id": "Per_104_9", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0]},
        {"id": "Per_104_10", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0]},

        {"id": "Per_104_35", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0, 1]},
        {"id": "Per_104_18", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0]},
        {"id": "Per_104_60", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0, 1]}
    ]

    custom_md = {
        "Collection": "Combining Ilkhanid Shahnama Digital Selection",
        "Curator": "Mehran DHN",
        "Access Rights": "Educational & research use only",
        "Project Year": "2025–2026",
        "Contact": "mehrandhn@gmail.com"
    }

    for ver in [3, 2]:
        combined = generate_combined_manifest(
            sources=sources_flex,               # or sources_simple
            include_toc=True,
            output_version=ver,
            local_base="https://raw.githubusercontent.com/MehranDHN/IIIFCollection/",   # ← change to your server
            custom_global_metadata=custom_md
        )

        filename = f"C:\\Users\\Floyd\\IIIFCollection\\IIIFCollection\\util_script\\improovedcombined_v{ver}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Saved {filename}  ({len(combined.get('items', [])) or len(combined['sequences'][0]['canvases'])} canvases)")