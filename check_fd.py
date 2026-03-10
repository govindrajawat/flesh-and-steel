import requests
import json
for t in ["farmers-delight-fabric"]:
    url = f"https://api.modrinth.com/v2/project/{t}/version"
    params = {"game_versions": json.dumps(["1.20.1"])}
    r = requests.get(url, params=params)
    versions = r.json()
    fabric = [v for v in versions if any(l in ["fabric", "quilt"] for l in v.get("loaders", []))]
    if fabric: print(f"{t}: OK -> {fabric[0]['version_number']}")
