
import requests
import json

def check_mod(slug):
    url = f"https://api.modrinth.com/v2/project/{slug}/version"
    r = requests.get(url)
    if r.status_code == 200:
        versions = r.json()
        fabric_1201 = [v for v in versions if "1.20.1" in v["game_versions"] and "fabric" in v["loaders"]]
        if fabric_1201:
            print(f"FOUND: {slug}")
        else:
            print(f"NOT FOUND: {slug}")
    else:
        print(f"ERROR {r.status_code}: {slug}")

check_mod("born-in-chaos")
check_mod("creeper-overhaul")
check_mod("naturalist")
check_mod("cataclysm")
