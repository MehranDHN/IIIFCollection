import json
import glob
import os

root = r"c:\Users\Mehran\IIIFCollection-1\IIIFCollection"
count = 0

for fp in sorted(glob.glob(os.path.join(root, '*.json'))):
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as exc:
        print(f"SKIP {os.path.basename(fp)}: {exc}")
        continue

    manifests = data.get('manifests', []) if isinstance(data, dict) else []
    if not isinstance(manifests, list):
        continue

    for manifest in manifests:
        if not isinstance(manifest, dict):
            continue

        metadata = manifest.get('metadata', [])
        if not isinstance(metadata, list):
            continue

        has_field = any(
            isinstance(item, dict)
            and isinstance(item.get('label'), dict)
            and item['label'].get('en') == 'FihristRecord'
            for item in metadata
        )
        if has_field:
            continue

        hosted_by = None
        for item in metadata:
            if not isinstance(item, dict):
                continue
            label = item.get('label', {})
            value = item.get('value', {})
            if isinstance(label, dict) and label.get('en') == 'Hosted By' and isinstance(value, dict):
                hosted_by = value.get('en')
                break

        if hosted_by in {'Manchester University Library', 'Bodleian Libraries', 'Cambridge University Library'}:
            metadata.append({
                'label': {'en': 'FihristRecord'},
                'value': {'en': ['', '']}
            })
            count += 1

    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write('\n')

print(f'Added {count} FihristRecord placeholder fields')
