import glob
import json
import os
import re

root = r'c:/Users/Floyd/IIIFCollection/IIIFCollection'
files = glob.glob(os.path.join(root, '*Collection.json'))
labels = {}

def norm(label):
    if isinstance(label, dict):
        en = label.get('en')
        if isinstance(en, list):
            return ' '.join(str(x) for x in en)
        if isinstance(en, str):
            return en
        return ' '.join(str(v) for v in label.values())
    if isinstance(label, list):
        return ' '.join(str(x) for x in label)
    return str(label) if label is not None else ''

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        d = json.load(fh)
    for m in d.get('manifests', []) + d.get('items', []):
        for md in m.get('metadata', []):
            lab = norm(md.get('label'))
            if re.search(r'depicts|iconograph|iconography|subject', lab, re.I):
                labels[lab] = labels.get(lab, 0) + 1

for k in sorted(labels, key=lambda x: (-labels[x], x))[:100]:
    print(labels[k], k)
print('--- total labels', len(labels))
