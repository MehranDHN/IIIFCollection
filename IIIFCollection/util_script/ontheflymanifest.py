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
    selected_items = [
    "HV.100", "HV.30", "HV.307", "HV.308", "HV.309", "HV.311bis", "HV.341", "HV.43", "HV.629", "HV.688",
    "HV.715", "HV.719", "HV.229", "HV.235", "HV.256", "HV.193", "HV.598", "HV.477", "HV.503", "HV.512",
    "HV.734", "HV.749", "HV.792", "HV.877", "HV.879", "HV.355", "HV.678", "HV.778", "HV.782", "HV.784",
    "HV.796", "HV.136", "HV.429", "HV.454", "HV.469", "HV.56", "HV.903", "HV.109", "HV.128", "HV.187",
    "HV.189", "HV.327", "HV.338", "HV.589", "HV.605", "HV.607", "HV.381", "HV.41", "HV.482", "HV.485",
    "HV.517", "HV.648", "HV.679", "HV.767", "HV.80", "HV.838", "HV.84", "HV.848", "HV.857", "HV.862",
    "HV.871", "HV.893", "HV.895", "HV.896", "HV.901", "HVX.18", "HV.159", "HV.198", "HV.200", "HV.303",
    "HV.314", "HV.315", "HV.45", "HV.481", "HV.506", "HV.733", "HV.757ter", "HV.890", "HV.105", "HV.244",
    "HV.251", "HV.279", "HV.581", "HV.68", "HV.687", "HV.823", "HV.832", "HVX.13", "HV.111",
    "HV.115", "HV.197", "HV.233", "HV.689", "HV.692", "HV.798", "HV.812", "HV.399", "HV.548", "HV.565",
    "HV.636", "HV.654", "HV.89", "HV.153", "HV.178B", "HV.460", "HV.743", "HVX.01", "HV.06", "HV.214",
    "HV.22", "HV.27", "HV.394", "HV.40bis", "HV.418", "HV.483", "HV.424", "HV.544", "HV.575", "HV.672",
    "HV.674", "HV.695", "HV.70", "HV.627", "HV.720", "HV.759", "HV.775", "HV.815", "HV.866", "HV.230",
    "HV.239", "HV.253", "HV.255", "HV.270", "HV.286", "HV.375", "HV.435", "HV.445", "HV.63", "HV.66",
    "HV.661", "HV.667", "HV.88", "HV.545", "HV.623", "HV.773", "HV.79", "HV.803", "HV.142", "HV.181",
    "HV.184", "HV.195", "HV.471", "HV.07", "HV.103", "HV.38", "HV.395", "HV.428", "HV.452", "HV.539",
    "HV.542", "HV.643", "HV.644", "HV.125", "HV.579", "HV.700", "HV.716", "HV.760", "HV.158", "HV.169",
    "HV.174", "HV.212", "HV.297", "HV.319", "HV.321", "HV.436", "HV.551", "HV.604", "HV.693", "HV.839B",
    "HV.894", "HV.900", "HV.278", "HV.342A", "HV.349", "HV.413", "HV.419", "HV.51", "HV.52", "HV.744",
    "HV.751", "HV.156", "HV.215", "HV.23", "HV.241", "HV.245", "HV.423", "HV.466", "HV.468", "HV.641",
    "HV.847", "HV.884", "HV.885", "HV.223", "HV.33", "HV.492", "HV.440", "HV.449", "HV.47", "HV.912",
    "HV.141", "HV.149", "HV.293", "HV.299", "HV.705", "HV.722", "HV.827", "HV.161", "HV.179", "HV.236",
    "HV.386", "HV.543", "HV.898", "HVX.08", "HV.210", "HV.361", "HV.585", "HV.614", "HV.663", "HV.665",
    "HV.697", "HV.616", "HV.651", "HV.752", "HV.851", "HV.807", "HV.130", "HV.143", "HV.145", "HV.17",
    "HV.55", "HV.592", "HV.62", "HV.728", "HV.789", "HV.847bis", "HV.853", "HVX.03", "HV.121", "HV.225",
    "HV.415", "HV.430", "HV.473", "HV.513", "HV.525",  "HV.208", "HV.295", "HV.254", "HV.269",
    "HV.345", "HV.455", "HV.549", "HV.550", "HV.610", "HV.910", "HV.118bis", "HV.124", "HV.178C", "HV.178E",
    "HV.201", "HV.204", "HV.561", "HV.370", "HV.379", "HV.478", "HV.514", "HV.638", "HV.671", "HV.714",
    "HV.721", "HV.840", "HV.846", "HV.227", "HV.25", "HV.259", "HV.262", "HV.267", "HV.294", "HV.302",
    "HV.343", "HV.344", "HV.725", "HV.74", "HV.817", "HV.102", "HV.352bis", "HV.625", "HV.649",
    "HV.732", "HV.875", "HV.902", "HV.907", "HV.113", "HV.135", "HV.171", "HV.203", "HV.206", "HV.260",
    "HV.265", "HV.268", "HV.487", "HV.427", "HV.451", "HV.61", "HV.662", "HV.706", "HV.783", "HV.794",
    "HV.795", "HV.808", "HV.818", "HV.821", "HVX.11",  "HV.305", "HV.401", "HV.414", "HV.580",
    "HV.738", "HV.797", "HVX.10", "HV.104", "HV.147", "HV.163", "HV.248", "HV.28", "HV.281", "HV.557",
    "HV.849B", "HV.870", "HV.342B", "HV.348", "HV.354", "HV.425bis", "HV.434", "HV.541", "HV.620", "HV.620bis",
    "HV.637", "HV.766", "HV.858", "HVX.07", "HV.112", "HV.117", "HV.292", "HV.316", "HV.250", "HV.264",
    "HV.573", "HV.597", "HV.615", "HV.724", "HV.830", "HVX.17", "HV.167", "HV.339",
    "HV.409", "HV.420", "HV.571", "HV.596", "HV.603", "HV.755", "HV.781", "HV.897", "HV.491", "HV.670",
    "HV.686", "HV.691", "HV.622", "HV.65", "HV.658", "HV.742", "HV.216", "HV.231", "HV.291", "HV.240",
    "HV.242", "HV.247", "HV.249", "HV.520", "HV.44", "HV.472", "HV.566", "HV.60", "HV.683", "HV.708",
    "HV.757", "HV.762", "HV.891", "HVX.02", "HV.318", "HV.325", "HV.523", "HV.64", "HV.645", "HV.657",
    "HV.677", "HV.718bis", "HV.899", "HV.05", "HV.129", "HV.536", "HV.562", "HV.599", "HV.611", "HV.366",
    "HV.373", "HV.421", "HV.447", "HV.771", "HV.788", "HV.819", "HV.837", "HV.842", "HV.867",
    "HV.331", "HV.673", "HV.710", "HV.10", "HV.12", "HV.283", "HV.16", "HV.17bis", "HV.527",
    "HV.588", "HV.602", "HV.397", "HV.446", "HV.793", "HV.806", "HV.905", "HV.337", "HV.359", "HV.360",
    "HV.642", "HV.824", "HV.839", "HV.852", "HVX.06", "HV.243", "HV.258", "HV.271", "HV.290",
    "HV.368", "HV.462", "HV.464", "HV.500", "HV.509", "HV.78", "HV.786", "HV.185", "HV.320", "HV.680",
    "HV.698", "HV.756", "HV.800", "HV.802", "HV.211", "HV.261", "HV.417", "HV.735", "HV.736", "HV.856",
    "HV.99", "HV.108", "HV.144", "HV.146", "HV.148", "HV.18", "HV.304bis", "HV.383", "HV.404", "HV.408",
    "HV.410", "HV.422", "HV.441", "HV.530", "HV.552", "HV.682", "HV.191", "HV.222", "HV.26", "HV.475",
    "HV.49", "HV.493", "HV.50", "HV.576", "HV.584", "HV.586", "HV.590", "HV.612", "HV.730", "HV.758",
    "HV.801", "HV.811", "HV.140", "HV.04", "HV.152", "HV.168", "HV.178D", "HV.180", "HV.287", "HV.300",
    "HV.257", "HV.280", "HV.328", "HV.501", "HV.433", "HV.558", "HV.567", "HV.613", "HV.668", "HV.699",
    "HV.704", "HV.617", "HV.633", "HV.754", "HV.772", "HV.805", "HV.13", "HV.175", "HV.182", "HV.367",
    "HV.37", "HV.372", "HV.385", "HV.396", "HV.405", "HV.406", "HV.438", "HV.696", "HV.73", "HV.764",
    "HV.774", "HV.831", "HV.835", "HV.878", "HV.91", "HVX.16", "HV.101", "HV.207", "HV.237", "HV.263",
    "HV.298", "HV.317", "HV.326", "HV.358", "HV.36", "HV.532", "HV.556", "HV.593", "HV.609", "HV.470",
    "HV.488", "HV.519", "HV.209", "HV.219", "HV.238", "HV.131", "HV.155", "HV.176", "HV.190", "HV.199",
    "HV.529", "HV.540", "HV.582", "HV.479", "HV.489", "HV.494", "HV.504", "HV.526", "HV.656", "HV.684",
    "HV.703", "HV.727", "HV.313", "HV.35", "HV.357", "HV.380", "HV.400", "HV.173", "HV.528", "HV.547",
    "HV.553", "HV.646", "HV.659", "HV.750", "HV.809", "HV.828", "HV.836", "HV.98", "HV.450", "HV.463",
    "HV.577", "HV.583", "HV.608", "HV.676", "HV.11", "HV.127", "HV.476", "HV.639", "HV.640", "HV.717",
    "HV.731", "HV.814", "HV.829", "HV.864", "HV.87", "HV.118", "HV.123", "HV.346", "HV.347", "HV.353",
    "HV.69", "HV.137", "HV.537", "HV.559", "HV.594", "HV.621", "HV.40", "HV.412", "HV.453", "HV.792bis",
    "HV.813", "HV.85", "HV.301", "HV.329", "HV.46", "HV.461", "HV.486", "HV.495", "HV.522", "HV.779",
    "HVX.12", "HVX.14", "HV.03", "HV.232", "HV.234", "HV.276", "HV.157", "HV.19", "HV.205", "HV.535",
    "HV.563", "HV.587", "HV.59", "HV.369", "HV.371", "HV.624", "HV.660", "HV.712", "HV.873", "HV.908",
    "HV.323", "HV.330", "HV.336", "HV.340", "HV.53", "HV.538", "HV.572", "HV.825", "HV.855", "HV.886",
    "HV.228", "HV.179bis", "HV.194", "HV.296", "HV.332", "HV.601", "HV.511", "HV.841", "HV.376", "HV.378",
    "HV.632", "HV.675", "HV.694", "HV.702", "HV.757bis", "HV.763", "HV.790", "HV.96", "HV.15", "HV.192",
    "HV.220", "HV.490", "HV.564", "HV.568", "HV.619", "HV.650", "HV.876", "HV.881", "HV.883", "HV.170",
    "HV.310", "HV.426", "HV.467", "HV.685", "HV.707", "HV.72", "HV.737", "HV.740", "HV.741", "HV.745",
    "HV.799", "HV.196", "HV.306", "HV.311", "HV.403", "HV.569", "HV.114", "HV.120", "HV.123bis", "HV.362",
    "HV.377", "HV.391", "HV.392", "HV.626", "HV.655", "HV.690", "HV.701", "HV.285", "HV.138", "HV.188",
    "HV.48", "HV.726", "HV.769", "HV.780", "HV.150", "HV.162", "HV.442", "HV.600", "HV.874",
    "HV.888", "HV.14", "HV.178", "HV.17ter", "HV.322", "HV.34", "HV.356", "HV.531", "HV.546", "HV.574",
    "HV.634", "HV.696bis", "HV.822", "HV.849", "HV.865", "HV.92", "HV.160", "HV.304", "HV.246", "HV.266",
    "HV.578", "HV.606", "HV.709", "HV.713", "HV.718", "HV.804", "HV.81", "HV.90", "HVX.05", "HV.20",
    "HV.350", "HV.39", "HV.393", "HV.407", "HV.411", "HV.664", "HV.669", "HV.630", "HV.753", "HV.846bis",
    "HV.860", "HV.887", "HV.139", "HV.165", "HV.166", "HV.595", "HV.618", "HV.652", "HV.820", "HV.826",
    "HV.843", "HV.859", "HV.02", "HV.08", "HV.106", "HV.126", "HV.21", "HV.272", "HV.277", "HV.282",
    "HV.284", "HV.31", "HV.334", "HV.335", "HV.382", "HV.437", "HV.444", "HV.474", "HV.502", "HV.516",
    "HV.76", "HV.761", "HV.904", "HV.906", "HV.333", "HV.534", "HV.560", "HV.57", "HV.58", "HV.456",
    "HV.484", "HV.510", "HV.628", "HV.681", "HV.09", "HV.221", "HV.172", "HV.183", "HV.186", "HV.202",
    "HV.402", "HV.416", "HV.431", "HV.739", "HV.747", "HV.748", "HV.768", "HV.777", "HV.834", "HV.909",
    "HVX.09", "HV.217", "HV.218", "HV.226", "HV.24", "HV.289", "HV.533", "HV.54", "HV.570", "HV.67",
    "HV.71", "HV.711", "HV.723", "HV.746", "HV.75", "HV.770", "HV.785", "HV.791", "HV.810", "HV.86",
    "HV.861", "HV.872", "HV.880", "HVX.15", "HV.119", "HV.177", "HV.312", "HV.363", "HV.374", "HV.42",
    "HV.425", "HV.518", "HV.524", "HV.97", "HV.01", "HV.107", "HV.122", "HV.213", "HV.252", "HV.288",
    "HV.29", "HV.635", "HV.83", "HV.848B", "HV.863", "HV.324", "HV.364", "HV.448", "HV.480", "HV.521",
    "HV.765", "HV.77", "HV.889", "HV.892", "HV.911", "HVX.04", "HV.224", "HV.154", "HV.164", "HV.591",
    "HV.505", "HV.507", "HV.508", "HV.515", "HV.82", "HV.833", "HV.850", "HV.882", "HV.110", "HV.116",
    "HV.32", "HV.365", "HV.653"
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