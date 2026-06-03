import json
import requests
from copy import deepcopy

def fetch_manifest(url):
    """Try both /manifest and /manifest.json (common on v2 servers)"""
    base = url.rstrip("/")
    for suffix in ["/manifest", "/manifest.json"]:
        full_url = base + suffix
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}            
            resp = requests.get(full_url, headers=headers, timeout=10)
            if resp.status_code == 200:
                print(f"✅ Fetched: {full_url}")
                return resp.json()
            else:
                print(f"⚠️  Failed to fetch {full_url} (status {resp.status_code})")
        except Exception as e:
            print(f"Fetch failed for {full_url}: {e}")
    print(f"❌ Could not fetch manifest: {base} ")
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
    return 3  # fallback

def get_label(obj):
    """Extract clean string label from any IIIF label object"""
    label = obj.get('label') or obj.get('@label', 'Untitled')
    if isinstance(label, dict):
        for lang in ('en', 'none', 'fr'):
            if lang in label and label[lang]:
                val = label[lang]
                return val[0] if isinstance(val, list) else str(val)
        return next(iter(label.values()))[0] if label else 'Untitled'
    if isinstance(label, list):
        return label[0] if label else 'Untitled'
    return str(label)

def get_canvases(manifest):
    ver = get_version(manifest)
    if ver == 3:
        return manifest.get('items', [])
    else:
        seqs = manifest.get('sequences', [])
        return seqs[0].get('canvases', []) if seqs else []

def normalize_canvas(canvas, target_version):
    """Convert canvas between v2 <-> v3 (ID, type, annotations)"""
    c = deepcopy(canvas)
    if target_version == 3:
        if '@id' in c: c['id'] = c.pop('@id')
        if '@type' in c: c['type'] = c.pop('@type')
        if 'images' in c and isinstance(c['images'], list):
            annos = c.pop('images')
            page = {
                'id': (c.get('id') or '') + '/annotation-page/1',
                'type': 'AnnotationPage',
                'items': []
            }
            for a in annos:
                anno = deepcopy(a)
                if '@id' in anno: anno['id'] = anno.pop('@id')
                if '@type' in anno: anno['type'] = anno.pop('@type')
                if 'on' in anno: anno['target'] = anno.pop('on')
                page['items'].append(anno)
            c['items'] = [page]
    else:  # target v2
        if 'id' in c: c['@id'] = c.pop('id')
        if 'type' in c: c['@type'] = c.pop('type')
        if 'items' in c and c['items'] and c['items'][0].get('type') == 'AnnotationPage':
            page = c.pop('items')[0]
            c['images'] = []
            for item in page.get('items', []):
                anno = deepcopy(item)
                if 'id' in anno: anno['@id'] = anno.pop('id')
                if 'type' in anno: anno['@type'] = anno.pop('type')
                if 'target' in anno: anno['on'] = anno.pop('target')
                c['images'].append(anno)
    return c

def add_custom_metadata(new_manifest, custom_md, output_version):
    if not custom_md:
        return
    for key, val in custom_md.items():
        if output_version == 3:
            lbl = key if isinstance(key, dict) else {"en": [str(key)]}
            value_d = val if isinstance(val, dict) else {"en": [str(val)]}
            new_manifest["metadata"].append({"label": lbl, "value": value_d})
        else:
            new_manifest["metadata"].append({
                "label": str(key),
                "value": str(val)
            })

def generate_combined_manifest(
    sources,
    include_toc=False,
    output_version=None,
    default_base_url="https://viewer.cbl.ie/viewer/api/v1/records/",
    local_base="https://raw.githubusercontent.com/MehranDHN/IIIFCollection/",
    custom_global_metadata=None
):
    # Normalize sources
    normalized = []
    for s in sources:
        if isinstance(s, str):
            if s.startswith("http"):
                normalized.append({"url": s, "canvas_indices": [0]})
            else:
                url = f"{default_base_url.rstrip('/')}/{s.strip()}"
                normalized.append({"url": url, "canvas_indices": [0], "id": s})
        elif isinstance(s, dict):
            if "url" in s:
                entry = {**s}
            elif "id" in s:
                base = s.get("base_url", default_base_url).rstrip("/")
                entry = {**s, "url": f"{base}/{s['id'].strip()}"}
            else:
                raise ValueError("Source dict must have 'url' or 'id'")
            entry.setdefault("canvas_indices", [0])
            normalized.append(entry)

    if output_version is None:
        output_version = 3

    if output_version not in (2, 3):
        raise ValueError("output_version must be 2 or 3")

    print(f"Building IIIF {output_version}.0 manifest from {len(normalized)} source(s)")

    # Create base manifest
    if output_version == 3:
        new_manifest = {
            "@context": "http://iiif.io/api/presentation/3/context.json",
            "id": f"{local_base.rstrip('/')}/combined/manifest",
            "type": "Manifest",
            "label": {"none": ["Combined Multi-Source Manifest"]},
            "items": [],
            "structures": [] if include_toc else None,
            "metadata": [],
        }
    else:
        new_manifest = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": f"{local_base.rstrip('/')}/combined/manifest",
            "@type": "sc:Manifest",
            "label": "Combined Multi-Source Manifest",
            "sequences": [{
                "@id": f"{local_base.rstrip('/')}/combined/sequence/1",
                "@type": "sc:Sequence",
                "canvases": []
            }],
            "structures": [] if include_toc else None,
            "metadata": [],
        }

    canvas_labels = []

    for spec in normalized:
        manifest = fetch_manifest(spec["url"])
        if not manifest:
            continue

        source_id = spec.get("id") or spec["url"].split("/")[-2] or "Unknown"
        indices = spec["canvas_indices"]
        all_canvases = get_canvases(manifest)

        if not all_canvases:
            print(f"Warning: No canvases in {source_id}")
            continue

        for idx in indices:
            if not (0 <= idx < len(all_canvases)):
                print(f"Warning: Canvas index {idx} out of range in {source_id}")
                continue

            raw_canvas = all_canvases[idx]
            canvas = normalize_canvas(raw_canvas, output_version)

            # === YOUR REQUESTED LABEL TEMPLATE ===
            old_lbl = get_label(canvas)
            if old_lbl == "Untitled":
                old_lbl = ""
            else:
                old_lbl = f" {old_lbl.strip()}"

            canvas_num = idx + 1   # 1-based for readability
            new_label_text = f"{canvas_num} from {source_id}{old_lbl}"

            new_label_dict = {"none": [new_label_text]}

            if output_version == 3:
                canvas["label"] = new_label_dict
            else:
                canvas["label"] = new_label_text   # v2 prefers string

            # New local ID
            safe_id = source_id.replace(".", "-").replace(" ", "_")
            new_id = f"{local_base.rstrip('/')}/combined/{safe_id}/canvas/{canvas_num}"

            if output_version == 3:
                canvas["id"] = new_id
            else:
                canvas["@id"] = new_id

            # Add canvas to manifest
            if output_version == 3:
                new_manifest["items"].append(canvas)
            else:
                new_manifest["sequences"][0]["canvases"].append(canvas)

            # Store same label for TOC
            canvas_labels.append(new_label_text)

    # Validation
    if output_version == 3:
        if not new_manifest["items"]:
            raise ValueError("No canvases were extracted")
    else:
        if not new_manifest["sequences"][0]["canvases"]:
            raise ValueError("No canvases were extracted")

    # Add only custom metadata (ignore source metadata)
    add_custom_metadata(new_manifest, custom_global_metadata, output_version)

    # Optional TOC / structures using the same formatted labels
    if include_toc and canvas_labels:
        if output_version == 3:
            root = {
                "id": f"{local_base.rstrip('/')}/combined/range/root",
                "type": "Range",
                "label": {"en": ["Table of Contents"]},
                "items": []
            }
            for i, lbl in enumerate(canvas_labels):
                root["items"].append({
                    "id": f"{local_base.rstrip('/')}/combined/range/{i}",
                    "type": "Range",
                    "label": {"none": [lbl]},
                    "items": [{"id": new_manifest["items"][i]["id"], "type": "Canvas"}]
                })
            new_manifest["structures"] = [root]
        else:
            root = {
                "@id": f"{local_base.rstrip('/')}/combined/range/root",
                "@type": "sc:Range",
                "label": "Table of Contents",
                "ranges": []
            }
            for i, lbl in enumerate(canvas_labels):
                root["ranges"].append({
                    "@id": f"{local_base.rstrip('/')}/combined/range/{i}",
                    "@type": "sc:Range",
                    "label": lbl,
                    "canvases": [new_manifest["sequences"][0]["canvases"][i]["@id"]]
                })
            new_manifest["structures"] = [root]

    return new_manifest


# ─── EXAMPLE USAGE ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sources_simple = ["Per_104_1", "Per_104_3", "Per_104_4"]

    sources_flex = [
        {"id": "Per_104_35", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0, 1]},
        {"id": "Per_104_18", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0]},
        {"id": "Per_104_60", "base_url": "https://viewer.cbl.ie/viewer/api/v1/records/", "canvas_indices": [0, 1]}
    ]

    custom_md = {
        "Collection": "Chester Beatty Library – Persian Manuscripts",
        "Curator": "Mehran DHN",
        "Access Rights": "For educational and research use only"
    }

    # Generate both versions
    for ver in [3, 2]:
        combined = generate_combined_manifest(
            sources=sources_simple,
            include_toc=True,
            output_version=ver,
            local_base="https://raw.githubusercontent.com/MehranDHN/IIIFCollection/",
            custom_global_metadata=custom_md
        )

        filename = f"C:\\Users\\Floyd\\IIIFCollection\\IIIFCollection\\util_script\\combined_cbl2_v{ver}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)

        count = len(combined.get("items", [])) or len(combined["sequences"][0]["canvases"])
        print(f"✅ Saved {filename} — {count} canvases")