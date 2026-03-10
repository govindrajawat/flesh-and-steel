import requests
import json

targets = [
    "obscure-api", "searchables", "bookshelf", "azurelib", 
    "smartbrainlib", "puzzles-lib", "accessories", "coroutil",
    "azurelib-armor"
]

def check_fabric(slug):
    url = f"https://api.modrinth.com/v2/project/{slug}/version"
    params = {"game_versions": json.dumps(["1.20.1"])}
    r = requests.get(url, params=params)
    if r.status_code != 200: return f"HTTP {r.status_code}"
    versions = r.json()
    fabric = [v for v in versions if any(l in ["fabric", "quilt"] for l in v.get("loaders", []))]
    if not fabric: return "NO FABRIC"
    return f"OK -> {fabric[0]['version_number']}"

for t in targets:
    print(f"{t}: {check_fabric(t)}")
