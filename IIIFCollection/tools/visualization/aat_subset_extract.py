import requests
from collections import deque

def fetch_aat_record(subject_id):
    url = f"http://vocab.getty.edu/aat/{subject_id}.json"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error fetching {url}: {response.status_code}")
    return response.json()

def get_pref_label(data):
    return data.get("_label") or "Unknown"

def get_aat_id(data_or_dict):
    if isinstance(data_or_dict, dict) and "id" in data_or_dict:
        uri = data_or_dict["id"]
    else:
        uri = data_or_dict.get("id", "")
    return uri.split("/")[-1]

def is_guide_term(label):
    return label.startswith("<") and label.endswith(">")

def build_aat_rdf_data(subject_id, direction="both", max_depth=None):
    terms = {}  # id: {'label': str, 'is_guide': bool, 'broaders': list[str]}

    queue = deque([(subject_id, 0)])  # (id, depth)
    visited = set()

    while queue:
        current_id, depth = queue.popleft()
        if current_id in visited:
            continue
        visited.add(current_id)
        if max_depth is not None and depth > max_depth:
            continue

        data = fetch_aat_record(current_id)
        label = get_pref_label(data)
        is_guide = is_guide_term(label)
        broaders = [get_aat_id(b) for b in data.get("broader", [])]

        terms[current_id] = {'label': label, 'is_guide': is_guide, 'broaders': broaders}

        # Enqueue broader terms if direction includes up
        if direction in ("up", "both"):
            for b_id in broaders:
                queue.append((b_id, depth + 1))

        # Enqueue narrower terms if direction includes down
        if direction in ("down", "both"):
            for n in data.get("narrower", []):
                n_id = get_aat_id(n)
                queue.append((n_id, depth + 1))

    return terms

def generate_turtle(terms):
    lines = [
        "@prefix aat: <http://vocab.getty.edu/aat/> .",
        "@prefix mdhn: <http://example.com/mdhn/> .",  # Replace with your actual namespace if different
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "@prefix so: <http://schema.org/> .",
        ""
    ]

    # Ontology definitions
    lines.append("mdhn:ResourceType a owl:Class ;")
    lines.append('    rdfs:comment "Classes to associate AAT as Topical headings to the photographs" ;')
    lines.append('    rdfs:label "ResourceType" .')
    lines.append("")

    lines.append("mdhn:hasAATBroader a owl:ObjectProperty ;")
    lines.append('    rdfs:comment "Associate an AAT concept to its broader concept" ;')
    lines.append('    rdfs:label "hasAATBroader" ;')
    lines.append('    so:domainIncludes mdhn:ResourceType ;')
    lines.append('    so:rangeIncludes mdhn:ResourceType .')
    lines.append("")

    lines.append("mdhn:isGuideTerm a owl:DatatypeProperty ;")
    lines.append('    rdfs:comment "Flag to indicate if the AAT term is a guide term" ;')
    lines.append('    rdfs:label "isGuideTerm" ;')
    lines.append('    rdfs:domain mdhn:ResourceType ;')
    lines.append('    rdfs:range xsd:boolean .')
    lines.append("")

    # Instances
    for term_id in sorted(terms):  # Sort by ID for consistent order
        info = terms[term_id]
        subject = f"mdhn:aat{term_id}"
        term_lines = [f"{subject} a mdhn:ResourceType ;"]

        # Escape double quotes in label
        escaped_label = info['label'].replace('"', '\\"')
        term_lines.append(f'    rdfs:label "{escaped_label}"@en ;')

        is_guide_str = str(info['is_guide']).lower()
        term_lines.append(f'    mdhn:isGuideTerm "{is_guide_str}"^^xsd:boolean')

        for broader_id in info['broaders']:
            term_lines.append(f'    mdhn:hasAATBroader mdhn:aat{broader_id}')

        # Add semicolons to all but the last property
        for i in range(len(term_lines) - 1):
            if not term_lines[i].endswith(';'):
                term_lines[i] += ' ;'
        term_lines[-1] += ' .'

        lines.extend(term_lines)
        lines.append("")

    return "\n".join(lines)

def save_turtle_file(turtle_code, filename="aat_hierarchy.ttl"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(turtle_code)
    print(f"Turtle RDF saved to '{filename}'")

# Example usage
if __name__ == "__main__":
    concept_id = "300200882"  # visual works (works) - replace with your desired AAT ID
    direction = "down"        # "up", "down", or "both"
    max_depth = 3             # Adjust to limit hierarchy size; None for unlimited (careful with broad terms!)
    node_count = 0
    try:
        terms = build_aat_rdf_data(concept_id, direction=direction, max_depth=max_depth)
        turtle_code = generate_turtle(terms)

        filename = f"C:\\IAPython\\AAT\\aat{concept_id}_hierarchy_large2.ttl" if len(terms) > 100 else f"C:\\IAPython\\AAT\\aat{concept_id}hierarchy.ttl"
        save_turtle_file(turtle_code, filename)

        print(f"\nGenerated RDF for {len(terms)} AAT concepts.")
        print("The Turtle file includes the ontology definitions and instances with hasAATBroader links from narrower to broader.")
        print("Guide terms are flagged with mdhn:isGuideTerm 'true'^^xsd:boolean.")
        print("Polyhierarchies are supported (multiple hasAATBroader per term if present).")
        print("Validate the TTL file with an RDF tool like Apache Jena or Protégé if needed.")

    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()