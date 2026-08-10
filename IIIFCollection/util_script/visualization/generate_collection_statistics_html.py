import json
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[1]
OUTPUT_HTML = SCRIPT_DIR / "collection_statistics.html"
OUTPUT_JSON = SCRIPT_DIR / "collection_statistics.json"


def normalize_label(label: Any) -> str:
    if isinstance(label, dict):
        en = label.get('en')
        if isinstance(en, str):
            return en
        if isinstance(en, list):
            return ' '.join(str(x) for x in en)
        return ' '.join(str(v) for v in label.values())
    if isinstance(label, list):
        return ' '.join(str(x) for x in label)
    return str(label) if label is not None else ''


def load_json(path: Path) -> Any:
    with path.open('r', encoding='utf-8') as fh:
        return json.load(fh)


def safe_label(label: str) -> str:
    return label.replace('"', '\\"').replace('\n', ' ')


def collect_collection_stats(root: Path) -> List[Dict[str, Any]]:
    files = sorted(root.glob('*Collection.json'))
    stats = []

    for path in files:
        try:
            data = load_json(path)
        except Exception:
            continue

        label = normalize_label(data.get('label') or path.stem)
        subcollection_count = len(data.get('collections', []) or [])
        manifests = data.get('manifests') or []
        items = data.get('items') or []
        manifest_count = len(manifests)
        item_count = len(items)
        resource_count = manifest_count if manifest_count else item_count
        total_member_count = manifest_count + item_count

        stats.append(
            {
                'file': path.name,
                'label': label,
                'subcollections': subcollection_count,
                'manifests': manifest_count,
                'items': item_count,
                'resources': resource_count,
                'members': total_member_count,
            }
        )

    stats.sort(key=lambda row: row['members'], reverse=True)
    return stats


def render_html(stats: List[Dict[str, Any]], output_path: Path) -> None:
    top_stats = stats[:30]
    labels = [safe_label(row['label'] or row['file']) for row in top_stats]
    manifests = [row['manifests'] for row in top_stats]
    items = [row['items'] for row in top_stats]
    subcollections = [row['subcollections'] for row in top_stats]

    chart_data = json.dumps(
        {
            'labels': labels,
            'manifests': manifests,
            'items': items,
            'subcollections': subcollections,
        }
    )

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IIIF Collection Statistics</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; background: #fafafa; color: #202020; }}
    h1 {{ margin-bottom: 0.25rem; }}
    .summary {{ margin-bottom: 1.5rem; }}
    .chart-box {{ max-width: 1200px; margin-bottom: 2rem; }}
    table {{ border-collapse: collapse; width: 100%; max-width: 1200px; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    th {{ background: #f0f0f0; }}
    tbody tr:nth-child(even) {{ background: #ffffff; }}
  </style>
</head>
<body>
  <h1>IIIF Collection Statistics</h1>
  <div class="summary">
    <p>Top 30 collections by total members (manifests + items).</p>
    <p>Total collections scanned: {len(stats)}</p>
  </div>

  <div class="chart-box">
    <canvas id="collectionChart" height="400"></canvas>
  </div>

  <h2>Top Collections</h2>
  <table>
    <thead>
      <tr>
        <th>#</th>
        <th>Collection file</th>
        <th>Label</th>
        <th>Subcollections</th>
        <th>Manifests</th>
        <th>Items</th>
        <th>Total members</th>
      </tr>
    </thead>
    <tbody>
"""

    for index, row in enumerate(stats[:100], start=1):
        content += (
            f"  <tr>"
            f"<td>{index}</td>"
            f"<td>{row['file']}</td>"
            f"<td>{safe_label(row['label'])}</td>"
            f"<td>{row['subcollections']}</td>"
            f"<td>{row['manifests']}</td>"
            f"<td>{row['items']}</td>"
            f"<td>{row['members']}</td>"
            f"</tr>\n"
        )

    content += """    </tbody>
  </table>

  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <script>
    const data = JSON.parse(`""" + chart_data + """`);
    const ctx = document.getElementById('collectionChart');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.labels,
        datasets: [
          {
            label: 'Manifests',
            data: data.manifests,
            backgroundColor: 'rgba(54, 162, 235, 0.7)',
          },
          {
            label: 'Items',
            data: data.items,
            backgroundColor: 'rgba(255, 159, 64, 0.7)',
          },
          {
            label: 'Subcollections',
            data: data.subcollections,
            backgroundColor: 'rgba(75, 192, 192, 0.7)',
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Top 30 IIIF Collections by Member Count' },
        },
        scales: {
          x: { stacked: true, ticks: { autoSkip: false, maxRotation: 45, minRotation: 15 } },
          y: { beginAtZero: true },
        },
      },
    });
  </script>
</body>
</html>
"""

    output_path.write_text(content, encoding='utf-8')


def save_json(stats: List[Dict[str, Any]], output_path: Path) -> None:
    output_path.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding='utf-8')


def main() -> None:
    stats = collect_collection_stats(ROOT_DIR)
    if not stats:
        raise SystemExit('No collection JSON files found')

    save_json(stats, OUTPUT_JSON)
    render_html(stats, OUTPUT_HTML)
    print('WROTE', OUTPUT_JSON)
    print('WROTE', OUTPUT_HTML)


if __name__ == '__main__':
    main()
