import csv
import json
import re
from pathlib import Path
from datetime import datetime
import shutil

def load_mappings(csv_path):
    """Load all TGM ID mappings from CSV."""
    mappings = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                mappings.append({
                    'old_uri': row['old_uri'].strip(),
                    'new_uri': row['new_uri'].strip()
                })
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None
    return mappings

def extract_local_name(uri):
    """Extract the local name from a URI."""
    parts = uri.split('/')
    return parts[-1] if parts else uri

def create_replacements(mappings):
    """Create replacement patterns for TTL and JSON files."""
    replacements = []
    for mapping in mappings:
        old_uri = mapping['old_uri']
        new_uri = mapping['new_uri']
        
        old_local = extract_local_name(old_uri)
        new_local = extract_local_name(new_uri)
        
        # For TTL files, we need both full URI and prefix forms
        # For JSON, we mainly use prefix forms
        replacements.append({
            'old_uri': old_uri,
            'new_uri': new_uri,
            'old_local': old_local,
            'new_local': new_local,
            'old_prefix': f"mdhn:{old_local}",
            'new_prefix': f"mdhn:{new_local}"
        })
    return replacements

def should_process_file(file_path):
    """Check if file should be processed."""
    path_str = str(file_path).lower()
    skip_dirs = ['backups', 'logs', 'scripts', '.git']
    for skip_dir in skip_dirs:
        if f"\\{skip_dir}\\" in path_str or f"/{skip_dir}/" in path_str:
            return False
    return True

def process_files(workspace_root, replacements, backup_dir):
    """Process all files and perform replacements."""
    files_updated = []
    total_replacements = 0
    
    workspace_path = Path(workspace_root)
    ontology_dir = workspace_path / 'IIIFCollection' / 'Ontology'
    collection_dir = workspace_path / 'IIIFCollection'
    
    # Process both directories
    for target_dir in [ontology_dir, collection_dir]:
        if not target_dir.exists():
            continue
            
        for file_path in target_dir.rglob('*'):
            if not file_path.is_file():
                continue
            
            if not should_process_file(file_path):
                continue
            
            # Only process TTL and JSON files
            suffix = file_path.suffix.lower()
            if suffix not in ['.ttl', '.json']:
                continue
            
            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                continue
            
            original_content = content
            replacements_in_file = 0
            
            if suffix == '.ttl':
                # For TTL files, replace both full URIs and prefix forms
                for repl in replacements:
                    # Replace full URIs (e.g., mdhn000900 but not as part of larger strings)
                    pattern = r'\b' + re.escape(repl['old_local']) + r'\b'
                    new_content, count1 = re.subn(pattern, repl['new_local'], content)
                    replacements_in_file += count1
                    
                    # Replace prefix forms (e.g., mdhn:tgm000900)
                    pattern = re.escape(repl['old_prefix'])
                    new_content, count2 = re.subn(pattern, repl['new_prefix'], new_content)
                    replacements_in_file += count2
                    
                    content = new_content
            else:  # JSON files
                # For JSON files, mainly replace prefix forms
                for repl in replacements:
                    pattern = re.escape(repl['old_prefix'])
                    new_content, count = re.subn(pattern, repl['new_prefix'], content)
                    replacements_in_file += count
                    content = new_content
            
            # If changes were made, update the file and copy original to backup
            if content != original_content:
                # Copy original to backup
                rel_path = file_path.relative_to(workspace_path)
                backup_file = backup_dir / rel_path
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                backup_file.write_text(original_content, encoding='utf-8')
                
                # Write updated content
                file_path.write_text(content, encoding='utf-8')
                
                files_updated.append(str(rel_path))
                total_replacements += replacements_in_file
    
    return files_updated, total_replacements

def main():
    workspace_root = r'c:\Users\Floyd\IIIFCollection'
    csv_path = Path(workspace_root) / 'IIIFCollection' / 'tgm_id_mapping.csv'
    
    # Load mappings
    mappings = load_mappings(csv_path)
    if not mappings:
        return {
            "status": "error",
            "message": "Failed to load CSV mappings"
        }
    
    # Create replacements
    replacements = create_replacements(mappings)
    
    # Create timestamped backup directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path(workspace_root) / 'backups' / f'tgm_repo_update_{timestamp}'
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Process files
    files_updated, total_replacements = process_files(workspace_root, replacements, backup_dir)
    
    # Create summary report
    report = {
        "timestamp": datetime.now().isoformat(),
        "files_updated": files_updated,
        "total_replacements": total_replacements,
        "backup_directory": str(backup_dir.relative_to(workspace_root)),
        "status": "complete"
    }
    
    # Write report
    report_path = Path(workspace_root) / 'tgm_migration_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    # Return final result
    return {
        "files_updated": files_updated,
        "total_files": len(files_updated),
        "mappings_loaded": len(mappings),
        "backup_location": str(backup_dir.relative_to(workspace_root)),
        "status": "success",
        "message": f"Processed {len(files_updated)} files with {total_replacements} total replacements"
    }

if __name__ == '__main__':
    import sys
    try:
        result = main()
        output = json.dumps(result, indent=2)
        print(output)
        with open('tgm_migration_result.json', 'w') as f:
            f.write(output)
    except Exception as e:
        import traceback
        error_result = {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }
        output = json.dumps(error_result, indent=2)
        print(output)
        with open('tgm_migration_result.json', 'w') as f:
            f.write(output)
        sys.exit(1)
