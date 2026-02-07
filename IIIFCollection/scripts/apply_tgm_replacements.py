#!/usr/bin/env python3
"""
Apply TGM ID replacements across all repo files using CSV mapping.
Handles both full URIs and prefix forms.
"""

import csv
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple

def load_mappings(csv_path: Path) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Load mappings from CSV.
    Returns: (full_uri_map, prefix_map)
    """
    full_uri_map = {}  # http://example.com/mdhn/tgmNNNN -> http://example.com/mdhn/tgmNNNN_Slug
    prefix_map = {}    # mdhn:tgmNNNN -> mdhn:tgmNNNN_Slug
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            old_uri = row['old_uri'].strip()
            new_uri = row['new_uri'].strip()
            full_uri_map[old_uri] = new_uri
            
            # Extract local names for prefix form
            old_local = old_uri.split('/')[-1]  # tgmNNNN
            new_local = new_uri.split('/')[-1]  # tgmNNNN_Slug
            prefix_map[f'mdhn:{old_local}'] = f'mdhn:{new_local}'
    
    return full_uri_map, prefix_map

def apply_replacements(file_path: Path, mappings: Dict[str, str], backup_dir: Path) -> int:
    """Apply replacements to a file. Returns count of replacements made."""
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    # Apply all mappings
    for old, new in mappings.items():
        # Use word boundaries for safety
        pattern = r'\b' + re.escape(old) + r'\b'
        content = re.sub(pattern, new, content)
    
    count = 0
    if content != original_content:
        count = len(mappings)  # Rough count
        
        # Create backup
        relative = file_path.relative_to(Path('c:\\Users\\Floyd\\IIIFCollection\\IIIFCollection'))
        backup_path = backup_dir / relative
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        backup_path.write_text(original_content, encoding='utf-8')
        
        # Write updated content
        file_path.write_text(content, encoding='utf-8')
    
    return count

def main():
    repo_root = Path('c:\\Users\\Floyd\\IIIFCollection\\IIIFCollection')
    csv_path = repo_root / 'tgm_id_mapping.csv'
    
    print(f"Loading mappings from {csv_path}...")
    full_uri_map, prefix_map = load_mappings(csv_path)
    print(f"Loaded {len(prefix_map)} prefix mappings")
    
    # Create timestamped backup directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = repo_root / 'backups' / f'tgm_repo_update_{timestamp}'
    backup_dir.mkdir(parents=True, exist_ok=True)
    print(f"Backup directory: {backup_dir}")
    
    # Process files
    exclude_dirs = {'.git', '__pycache__', 'backups', 'logs', 'scripts'}
    file_counts = {}
    total_replacements = 0
    
    for pattern in ['**/*.ttl', '**/*.json', '**/*.md']:
        for file_path in repo_root.glob(pattern):
            # Skip excluded directories
            if any(excl in file_path.parts for excl in exclude_dirs):
                continue
            
            print(f"Processing {file_path.relative_to(repo_root)}...", end=' ')
            count = apply_replacements(file_path, prefix_map, backup_dir)
            if count > 0:
                file_counts[str(file_path.relative_to(repo_root))] = count
                total_replacements += 1
                print(f"✓ ({count} mappings applied)")
            else:
                print("(no changes)")
    
    # Write report
    report = {
        'timestamp': timestamp,
        'total_files_updated': len(file_counts),
        'files_updated': list(file_counts.keys()),
        'mappings_count': len(prefix_map),
        'backup_directory': str(backup_dir)
    }
    
    report_path = repo_root / f'tgm_replacement_report_{timestamp}.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✓ Complete! Report: {report_path}")
    print(f"  Files updated: {len(file_counts)}")
    print(f"  Mappings applied: {len(prefix_map)}")
    print(f"  Backups saved to: {backup_dir}")

if __name__ == '__main__':
    main()
