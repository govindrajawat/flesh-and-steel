import requests
import json

MODRINTH_API = "https://api.modrinth.com/v2"

def has_fabric(slug):
    r = requests.get(f"{MODRINTH_API}/project/{slug}/version", params={"game_versions": "['1.20.1']"})
    if r.status_code == 200:
        versions = r.json()
        return any("fabric" in [l.lower() for l in v.get("loaders", [])] for v in versions)
    return False

mods = ["sons-of-sins", "butchery", "neep-meat", "legendary-survival-overhaul"]
for m in mods:
    print(f"{m}: {has_fabric(m)}")
