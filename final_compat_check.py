import requests
import json

confirmed = [
    "heracles",                      # Quest mod for Fabric
    "integrated-stronghold",
    "when-dungeons-arise",
    "explorify",
    "dungeons-and-taverns",
    "repurposed-structures-fabric",
    "create-steam-n-rails",
    "sanguine-blood-particles",
    "rot-n-putrid",
    "victus",
    "visuality",
    "presence-footsteps",
    "sound-physics-remastered",
    "ambientsounds",
    "effective",
]

def check_fabric(slug):
    url = f"https://api.modrinth.com/v2/project/{slug}/version"
    params = {"game_versions": json.dumps(["1.20.1"])}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        print(f"[MISS] {slug}: HTTP {r.status_code}")
        return
    versions = r.json()
    if not versions:
        print(f"[MISS] {slug}: NO VERSIONS")
        return
    fabric_versions = [v for v in versions if any(l in ["fabric", "quilt"] for l in v.get("loaders", []))]
    if not fabric_versions:
        print(f"[MISS] {slug}: NO FABRIC")
        return
    v = fabric_versions[0]
    print(f"[OK]   {slug} -> {v['version_number']} | {v['files'][0]['filename']}")

for s in confirmed:
    check_fabric(s)
