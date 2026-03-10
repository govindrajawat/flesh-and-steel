import requests
import json

def check_files(slug):
    url = f"https://api.modrinth.com/v2/project/{slug}/version"
    params = {"game_versions": json.dumps(["1.20.1"])}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        versions = r.json()
        if versions:
            v = versions[0]
            print(f"--- {slug} ---")
            for f in v['files']:
                print(f"File: {f['filename']} (Primary: {f['primary']})")

check_files("biomancerrerise")
check_files("ftb-quests-fabric")
check_files("ftb-library-fabric")
check_files("ftb-teams-fabric")
check_files("item-filters")
check_files("integrated-stronghold")
check_files("integrated-villages")
check_files("integrated-dungeons-and-structures")
check_files("visuality")
check_files("presence-footsteps")
check_files("sound-physics-remastered")
check_files("ambientsounds")
check_files("victus")
check_files("explorify")
check_files("choiceovers-better-villages")
