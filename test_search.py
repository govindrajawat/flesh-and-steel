import requests
import json

MINECRAFT_VERSION = "1.20.1"
MODRINTH_API = "https://api.modrinth.com/v2"

MODS_TO_TEST = [
    "Bigger Reactors",
    "Ars Nouveau",
    "Alex's Mobs",
    "Better Combat",
    "Simply Swords",
    "Create: Bio-Factory",
    "Sons Of Sins",
    "BooneForgeAPI",
    "Chest Cavity",
    "Butchery"
]

results = []
for mod in MODS_TO_TEST:
    search_url = f"{MODRINTH_API}/search"
    params = {
        "query": mod,
        "facets": json.dumps([[f"versions:{MINECRAFT_VERSION}"], ["project_type:mod"]])
    }
    r = requests.get(search_url, params=params)
    results.append(f"\n--- Search results for '{mod}' ---")
    if r.status_code == 200:
        hits = r.json().get("hits", [])
        if not hits:
            results.append("No hits found.")
        for i, hit in enumerate(hits[:10]):
            results.append(f"{i+1}. Title: {hit['title']} | Slug: {hit['slug']} | ID: {hit['project_id']}")
    else:
        results.append(f"Failed to search '{mod}': {r.status_code}")

with open("search_results.txt", "w", encoding="ascii", errors="replace") as f:
    f.write("\n".join(results))
