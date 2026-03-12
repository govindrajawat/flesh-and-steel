
import requests
import json

MODRINTH_API = "https://api.modrinth.com/v2"

def get_versions(slug):
    url = f"{MODRINTH_API}/project/{slug}/version"
    r = requests.get(url)
    if r.status_code == 200:
        versions = r.json()
        for v in versions:
            if "1.20.1" in v["game_versions"] and "fabric" in v["loaders"]:
                 print(f"{v['version_number']} (ID: {v['id']})")
    else:
        print(f"Error checking {slug}: {r.status_code}")

get_versions("azurelib")
