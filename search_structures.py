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

print("--- Create Structures ---")
search_fabric("create structures")
search_fabric("abandoned factory")

print("\n--- Meat/Horror Structures ---")
search_fabric("graveyard")
search_fabric("horror structures")
search_fabric("gore")
search_fabric("flesh")
search_fabric("cemetery")
search_fabric("ruins")
