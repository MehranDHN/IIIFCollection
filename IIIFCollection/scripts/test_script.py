import json
result = {"test": "success", "timestamp": __import__("datetime").datetime.now().isoformat()}
with open(r"c:\Users\Floyd\IIIFCollection\test_output.json", "w") as f:
    json.dump(result, f)
print("Done")
