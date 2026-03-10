import requests
import json
MODRINTH_API = "https://api.modrinth.com/v2"

def get_versions(slug):
    r = requests.get(f"{MODRINTH_API}/project/{slug}/version", params={"game_versions": "[\"1.20.1\"]"})
    if r.status_code == 200:
        print(f"--- {slug} ---")
        for v in r.json()[:5]:
            print(f"{v['version_number']} | Loaders: {v['loaders']}")
            
get_versions("kubejs")
get_versions("grim-and-bleak")
