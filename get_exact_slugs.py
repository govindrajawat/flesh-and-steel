import requests
import json

def get_exact_slug(query, facet_list):
    url = "https://api.modrinth.com/v2/search"
    params = {"query": query, "facets": json.dumps(facet_list)}
    r = requests.get(url, params=params)
    for h in r.json().get('hits', [])[:3]:
        print(f"{h['slug']} | {h['title']}")

print("--- Quests ---")
get_exact_slug("FTB Quests", [["versions:1.20.1"], ["categories:fabric"]])
get_exact_slug("FTB Library", [["versions:1.20.1"], ["categories:fabric"]])
get_exact_slug("FTB Teams", [["versions:1.20.1"], ["categories:fabric"]])

print("\n--- Create ---")
get_exact_slug("Steam 'n' Rails", [["versions:1.20.1"], ["categories:fabric"]])

print("\n--- Integrated ---")
get_exact_slug("Integrated Stronghold", []) # Check all to see if there's a fabric one
get_exact_slug("Integrated Villages", [])
get_exact_slug("Integrated Dungeons", [])

print("\n--- Meat ---")
get_exact_slug("Sons of Sins", [["versions:1.20.1"], ["categories:fabric"]])
get_exact_slug("Victus", [["versions:1.20.1"], ["categories:fabric"]])
get_exact_slug("Blood", [["versions:1.20.1"], ["categories:fabric"]])
