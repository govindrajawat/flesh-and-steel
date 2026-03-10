import requests
import json

def check_fabric(slug):
    url = f"https://api.modrinth.com/v2/project/{slug}/version"
    params = {"game_versions": json.dumps(["1.20.1"])}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return f"HTTP {r.status_code}"
    versions = r.json()
    fabric = [v for v in versions if any(l in ["fabric", "quilt"] for l in v.get("loaders", []))]
    if not fabric:
        return "NO FABRIC"
    v = fabric[0]
    return f"OK -> {v['version_number']} | {v['files'][0]['filename']}"

for s in ["flesh-to-leather", "forsaken-corpses"]:
    print(f"{s}: {check_fabric(s)}")
