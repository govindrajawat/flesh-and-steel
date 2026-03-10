import requests, json
params = {"game_versions": json.dumps(["1.20.1"])}
r = requests.get("https://api.modrinth.com/v2/project/neepmeat/version", params=params)
with open("neepmeat_versions.txt", "w", encoding="utf-8") as f:
    for v in r.json():
        if "fabric" in [l.lower() for loader in v["loaders"] for l in loader] or "fabric" in v.get("loaders", []):
            f.write(f"- {v['version_number']}\n")
