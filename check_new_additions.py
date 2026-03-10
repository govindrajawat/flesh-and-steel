import requests, json

# Check new mods we want to add
mods_to_check = [
    # Villagers
    "easy-villagers",
    "villager-names",
    "custom-villager-trades",
    "more-villagers",
    "villager-names-serilum",
    
    # Extra performance
    "entityculling",
    "memoryleakfix",
    "immediatelyfast",
    "krypton",
    "noisium",
    "chunky",
    "servercore",
    
    # Multiplayer fun
    "ftb-chunks",
    "ftb-teams",
    "origins",
    "pehkui",
    "do-a-barrel-roll",
    "chat-heads",
    "styled-chat",
    
    # More villages / world
    "towns-and-towers",
    "dungeons-arise",
    "yungsextras",
    "yungs-extras",
    
    # QoL / survival
    "universal-graves",
    "fractal-cosmetics",
    "numismatics",
    "leaky",
    "vein-mining",
    "xp-tome",
]

for slug in mods_to_check:
    try:
        r = requests.get(
            f"https://api.modrinth.com/v2/project/{slug}/version",
            params={"game_versions": json.dumps(["1.20.1"]), "loaders": json.dumps(["fabric"])},
            timeout=8
        )
        if r.status_code == 200 and r.json():
            v = r.json()[0]
            print(f"OK  {slug:45s} -> {v['version_number']}")
        else:
            print(f"NO  {slug}")
    except Exception as e:
        print(f"ERR {slug}: {e}")
