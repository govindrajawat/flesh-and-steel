import requests
import json

def search_fabric(query):
    url = "https://api.modrinth.com/v2/search"
    params = {
        "query": query,
        "facets": json.dumps([["versions:1.20.1"], ["categories:fabric"]]),
        "limit": 4
    }
    r = requests.get(url, params=params)
    for h in r.json().get('hits', []):
        print(f"  {h['slug']} | {h['title']}")

print("--- Quest mods ---")
search_fabric("quest book")
search_fabric("Heracles quest")
search_fabric("FTB Quests")

print("\n--- Repurposed Structures ---")
search_fabric("repurposed structures")

print("\n--- Blood/Gore/Flesh thematic ---")
search_fabric("blood particles")
search_fabric("gore mod")
search_fabric("flesh horror")
search_fabric("vampire")

print("\n--- Create Steam ---")
search_fabric("create steam")
