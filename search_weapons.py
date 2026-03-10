import requests
import json

def search_fabric(query, limit=5):
    url = "https://api.modrinth.com/v2/search"
    params = {
        "query": query,
        "facets": json.dumps([["versions:1.20.1"], ["categories:fabric"]]),
        "limit": limit
    }
    r = requests.get(url, params=params)
    for h in r.json().get('hits', []):
        print(f"  {h['slug']} | {h['title']} | {h.get('description', '')[:50]}")

print("--- Guns & Weapons ---")
search_fabric("guns")
search_fabric("firearms")

print("\n--- Horror/Gritty ---")
search_fabric("corpse")
search_fabric("blood")
search_fabric("flesh")
