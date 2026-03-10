import requests
import json

def get_mods(query, limit=10):
    url = "https://api.modrinth.com/v2/search"
    params = {
        "query": query,
        "facets": json.dumps([["versions:1.20.1"], ["categories:fabric"]]),
        "limit": limit
    }
    r = requests.get(url, params=params)
    return r.json().get('hits', [])

def print_mods(title, queries):
    print(f"\n--- {title} ---")
    seen = set()
    for q in queries:
        for h in get_mods(q):
            if h['slug'] not in seen:
                print(f"  {h['slug']} | {h['title']}")
                seen.add(h['slug'])

print_mods("Flesh & Infection Blocks", ["flesh blocks", "neepmeat", "biomancy", "infected", "parasites", "scp", "gore blocks", "body horror", "mutated"])
print_mods("Meat Cooking & Butchery", ["butchery", "meat", "cannibalism", "slaughter"])
