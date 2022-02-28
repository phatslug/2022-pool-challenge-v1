import requests
from pathlib import Path
import json

input_locations = json.loads(Path("input.json").read_text())

results = requests.post("http://127.0.0.1:5000/neighbours", json=input_locations).json()

if __name__ == "__main__":
    Path("output.json").write_text(json.dumps(results))
