import requests
import json
MODRINTH_API = "https://api.modrinth.com/v2"
MINECRAFT_VERSION = "1.20.1"

def check(slug):
    url = f"{MODRINTH_API}/project/{slug}/version"
    params = {"game_versions": json.dumps([MINECRAFT_VERSION])}
    r = requests.get(url, params=params)
    print(f"{slug}: {r.status_code}")
    if r.status_code == 200:
        print(f"Versions found: {len(r.json())}")

check("created-pretty-pipes")
check("fresh-animations")
check("grim-and-bleak")
