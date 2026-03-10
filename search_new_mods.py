import requests
import json

def search(query, limit=5):
    url = "https://api.modrinth.com/v2/search"
    params = {
        "query": query,
        "facets": json.dumps([["versions:1.20.1"], ["categories:fabric"]])
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        for hit in r.json().get('hits', [])[:limit]:
            print(f"{hit['slug']} | {hit['title']}")

print("--- Quests ---")
search("FTB Quests")
search("Heracles")

print("\n--- Integrated ---")
search("Integrated Structures")
search("Integrated Dungeons")

print("\n--- Meat/Blood/Biomechanical ---")
search("Biomancy")
search("Flesh")
search("Blood")
search("Sons of Sins")
search("Victus")

print("\n--- Atmosphere ---")
search("Sound Physics")
search("AmbientSounds")
search("Visuality")
search("Effective")
search("Presence Footsteps")
search("MACE")
