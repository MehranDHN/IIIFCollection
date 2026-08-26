#!/usr/bin/env python3
"""
IIIF Manuscript Canvas Decomposition → Markmap Markdown Generator
Clean version with - list items for better hierarchy
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# ================== CONFIGURATION ==================
SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_DIR = SCRIPT_DIR.parents[1]
OUTPUT_DIR = SCRIPT_DIR

INPUT_JSON_FILES: List[str] = [
    "PeckShahnamaCollection.json",
    "ShahnamaMsorfol4251Collection.json",
    "ShahnamaMsorfol359Collection.json",
    "JukiShahnamaCollection.json",
    "ShahnameShahTahmasbCollection.json",
    "IbrahimSultanShahnamaCollection.json",
    "ShahnamaSmithLesouef224Collection.json",
    "SmallIlkhanidShahnameCollection.json",
    "DepartedFolioCollection.json",
    "QisasalAnbiyaCollection.json",
    "Qisas_al_Anbiya_PersianMS46Collection.json",
    "Qisas_al_Anbiya_PersianMS1Collection.json",
    "RamayanaV1Collection.json",
    "RamayanaV2Collection.json"
    # Add more filenames here
]

THUMBNAIL_WIDTH: int = 200
OUTPUT_FILE = OUTPUT_DIR / "canvas_decomposition.markmap.md"
# ===================================================

def get_label_text(label: Any) -> str:
    if isinstance(label, str):
        return label
    if isinstance(label, dict):
        for key in ('en', 'none', 'fa'):
            if key in label and label[key]:
                val = label[key]
                return val[0] if isinstance(val, list) else str(val)
    return str(label) if label is not None else "Unnamed"


def get_thumbnail_url(iiif_url: str, width: int = THUMBNAIL_WIDTH) -> Optional[str]:
    if not iiif_url or not isinstance(iiif_url, str):
        return None
    if '/full/' in iiif_url:
        return iiif_url.replace('/full/', f'/{width},/')
    if '/max/' in iiif_url:
        return iiif_url.replace('/max/', f'/{width},/')    
    return iiif_url


def process_content_element(elem: Dict[str, Any], element_type_fallback: str = "ContentElement") -> List[str]:
    lines: List[str] = []
    el_label = get_label_text(elem.get('elementLabel') or elem.get('label'))
    el_type = elem.get('elementType', element_type_fallback)
    
    lines.append(f"### {el_type}: {el_label}")
    
    cropped_img = elem.get('croppedImage') or elem.get('image')
    thumb = get_thumbnail_url(cropped_img)
    if thumb:
        lines.append(f"- ![ {el_label} ]({thumb})")
    
    loud = elem.get('elementLOUD', []) or elem.get('loud', [])
    if loud:
        lines.append(f"- **Iconography Tags (elementLOUD):** {', '.join(str(t) for t in loud)}")
    
    styles = elem.get('elementStyle', []) or elem.get('style', [])
    if styles:
        lines.append(f"- **Styles:** {', '.join(str(s) for s in styles)}")
    
    fa_text = elem.get('elementFAText', '') or elem.get('faText', '')
    en_text = elem.get('elementENText', '') or elem.get('enText', '')
    if fa_text:
        lines.append(f"- **Persian Text:** {fa_text}")
    if en_text:
        lines.append(f"- **English Text:** {en_text}")
    
    if 'Element' in elem and isinstance(elem.get('Element'), list):
        lines.append("- **Sub-Elements:**")
        for sub_elem in elem['Element']:
            sub_lines = process_content_element(sub_elem, "Sub-Element")
            lines.extend(["    " + line for line in sub_lines])
    
    lines.append("")
    return lines


def extract_canvas_entries(metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    canvas_entries: List[Dict[str, Any]] = []

    for meta in metadata:
        label_text = get_label_text(meta.get('label'))
        if not label_text:
            continue

        normalized_label = label_text.strip().lower()
        if 'states' not in normalized_label and 'ascanvas' not in normalized_label:
            continue

        value = meta.get('value', {})
        if isinstance(value, dict) and 'en' in value:
            raw_entries = value['en']
        elif isinstance(value, list):
            raw_entries = value
        else:
            raw_entries = []

        if isinstance(raw_entries, list):
            for entry in raw_entries:
                if isinstance(entry, dict):
                    canvas_entries.append(entry)

    return canvas_entries


def generate_markmap_from_json(json_path: str) -> List[str]:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    manuscript_label = get_label_text(data.get('label', Path(json_path).name))
    lines = [f"# {manuscript_label}"]
    lines.append("")
    lines.append("**Hierarchical Canvas Decomposition (ResourceCanvas → Content Elements)**")
    lines.append("")
    
    manifests = data.get('manifests', []) or [data]
    
    for manifest in manifests:
        manifest_label = get_label_text(manifest.get('label', 'Manifest'))
        metadata = manifest.get('metadata', [])
        canvas_entries = extract_canvas_entries(metadata)
        
        if not canvas_entries:
            continue
        
        lines.append(f"## Manifest: {manifest_label}")
        lines.append("")
        
        for state in canvas_entries:
            folio = state.get('folio', '')
            label = get_label_text(state.get('label'))
            
            lines.append(f"## ResourceCanvas: f.{folio} — {label}")
            
            if state.get('canvasType'):
                lines.append(f"- **Canvas Types:** {', '.join(state['canvasType'])}")
            if state.get('folioContains'):
                lines.append(f"- **Contains:** {', '.join(state['folioContains'])}")
            
            lines.append("")
            
            content_keys = ['croppedFigures', 'croppedPatterns', 'linguisticElements', 
                           'ContentElement', 'elements']
            for key in content_keys:
                elems = state.get(key, [])
                if not elems:
                    continue
                for elem in elems:
                    elem_lines = process_content_element(elem, key.rstrip('s').title())
                    lines.extend(elem_lines)
            
            lines.append("---")
            lines.append("")
    
    return lines


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_lines: List[str] = []
    all_lines.append("اين گزارش بوسيله ماشين تهيه شده و به منظور تست صحت اطلاعات و ساختار مدل اطلاعات ساختار يافته و رابطه های سلسله مراتبی اجزای يک صفحه از نسخه دستنويس يا نگاره طراحی شده . ")
    all_lines.append("---")
    for filename in INPUT_JSON_FILES:
        json_path = INPUT_DIR / filename
        if not json_path.exists():
            print(f"⚠️  File not found: {json_path}")
            continue
        print(f"📄 Processing: {json_path}")
        file_lines = generate_markmap_from_json(json_path)
        all_lines.extend(file_lines)
        all_lines.append("\n\n")
    
    with OUTPUT_FILE.open('w', encoding='utf-8') as f:
        f.write('\n'.join(all_lines))
    
    print(f"\n✅ Markmap document successfully generated:\n{OUTPUT_FILE}")
    print("   → Open it in VS Code with the Markmap extension or at https://markmap.js.org/")


if __name__ == "__main__":
    main()