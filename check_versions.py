
import requests
import json

MODRINTH_API = "https://api.modrinth.com/v2"

def check_versions(slug):
    print(f"\n--- Checking {slug} ---")
    url = f"{MODRINTH_API}/project/{slug}/version"
    params = {"game_versions": json.dumps(["1.20.1"]), "loaders": json.dumps(["fabric"])}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        versions = r.json()
        for v in versions[:10]:
            print(f"Version: {v['version_number']} (ID: {v['id']})")
            print(f"  Name: {v['name']}")
            # print(f"  Dependencies: {v['dependencies']}")
    else:
        print(f"Error checking {slug}: {r.status_code}")

check_versions("deeperdarker")
check_versions("azurelib")
