import requests
import json

MODRINTH_API = "https://api.modrinth.com/v2"
MINECRAFT_VERSION = "1.20.1"

def search_mod(query):
    params = {
        "query": query,
        "facets": json.dumps([[f"versions:{MINECRAFT_VERSION}"], ["categories:fabric"]])
    }
    r = requests.get(f"{MODRINTH_API}/search", params=params)
    if r.status_code == 200:
        hits = r.json().get("hits", [])
        return [(h['title'], h['slug']) for h in hits[:3]]
    return []

print(f"Refined Storage: {search_mod('Refined Storage')}")
print(f"Bio-Factory: {search_mod('Bio-Factory')}")
print(f"Biomancy: {search_mod('Biomancy')}")
print(f"Balm: {search_mod('Balm')}")
