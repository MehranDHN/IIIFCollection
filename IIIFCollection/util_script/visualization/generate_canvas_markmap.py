#!/usr/bin/env python3
"""
IIIF Manuscript Canvas Decomposition → Markmap Markdown Generator
Clean version with - list items for better hierarchy
"""

import json
import os
from typing import List, Dict, Any, Optional

# ================== CONFIGURATION ==================
INPUT_DIR: str = r"C:\Users\Mehran\IIIFCollection-1\IIIFCollection"
OUTPUT_DIR: str = r"C:\Users\Mehran\IIIFCollection-1\IIIFCollection\util_script\visualization"

INPUT_JSON_FILES: List[str] = [
    "PeckShahnamaCollection.json",
    "ShahnamaMsorfol4251Collection.json",
    "ShahnamaMsorfol359Collection.json",
    "JukiShahnamaCollection.json",
    "IbrahimSultanShahnamaCollection.json",
    "ShahnamaSmithLesouef224Collection.json",
    "QisasalAnbiyaCollection.json"
    # Add more filenames here
]

THUMBNAIL_WIDTH: int = 130
OUTPUT_FILE: str = os.path.join(OUTPUT_DIR, "iiif_decomposition_markmap.md")
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


def generate_markmap_from_json(json_path: str) -> List[str]:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    manuscript_label = get_label_text(data.get('label', os.path.basename(json_path)))
    lines = [f"# {manuscript_label}"]
    lines.append("")
    lines.append("**Hierarchical Canvas Decomposition (ResourceCanvas → Content Elements)**")
    lines.append("")
    
    manifests = data.get('manifests', []) or [data]
    
    for manifest in manifests:
        manifest_label = get_label_text(manifest.get('label', 'Manifest'))
        lines.append(f"## Manifest: {manifest_label}")
        lines.append("")
        
        metadata = manifest.get('metadata', [])
        states = []
        for meta in metadata:
            if 'States' in get_label_text(meta.get('label')):
                value = meta.get('value', {})
                if isinstance(value, dict) and 'en' in value:
                    states = value['en']
                elif isinstance(value, list):
                    states = value
                break
        
        if not states:
            lines.append("*No States found.*")
            continue
        
        for state in states:
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
    
    for filename in INPUT_JSON_FILES:
        json_path = os.path.join(INPUT_DIR, filename)
        if not os.path.exists(json_path):
            print(f"⚠️  File not found: {json_path}")
            continue
        print(f"📄 Processing: {json_path}")
        file_lines = generate_markmap_from_json(json_path)
        all_lines.extend(file_lines)
        all_lines.append("\n\n")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_lines))
    
    print(f"\n✅ Markmap document successfully generated:\n{OUTPUT_FILE}")
    print("   → Open it in VS Code with the Markmap extension or at https://markmap.js.org/")


if __name__ == "__main__":
    main()