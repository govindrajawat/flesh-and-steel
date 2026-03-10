import requests, json

mods = ["kubejs", "ponderjs", "morejs", "rhino"]
MINECRAFT_VERSION = "1.20.1"

for m in mods:
    r = requests.get(
        f"https://api.modrinth.com/v2/project/{m}",
        timeout=10
    )
    if r.status_code == 200:
        p = r.json()
        print(f"Slug: {p['slug']}, ID: {p['id']}")
    else:
        print(f"Failed to find {m}")
