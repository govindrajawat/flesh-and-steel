import requests, json

mods_to_check = [
    "yungs-better-dungeons", "yungs-better-mineshafts", "yungs-better-strongholds",
    "yungs-better-ocean-monuments", "yungs-better-nether-fortresses", "yungs-better-desert-temples",
    "yungs-better-jungle-temples", "yungs-better-witch-huts",
    "structory", "structory-towers",
    "tectonic", "geophilic", "regions-unexplored",
    "biomes-o-plenty", "traverse", "regions-unexplored",
    "chests-reimagined", "lootr", "dungeons-libraries",
    "dungeons-surface", "dungeons-enhancement",
    "villages-and-pillages", "castle-dungeons",
    "dungeon-crawl", "dungeonz",
    "corgilib", "upgrade-aquatic", "environmental",
    "betterx-wild-backport",
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
            print(f"OK  {slug} -> {v['version_number']}")
        else:
            print(f"NO  {slug}")
    except Exception as e:
        print(f"ERR {slug}: {e}")
