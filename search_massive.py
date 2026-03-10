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

print_mods("Guns & Weapons", ["guns", "firearms", "weapons", "combat", "arsenal"])
print_mods("Horror & Flesh", ["horror", "blood", "flesh", "gore", "corpse", "meat", "scary", "mutant"])
print_mods("Engineering & Steel", ["factory", "industry", "tech", "create addon", "steampunk", "mech"])
print_mods("Hostile Mobs & Bosses", ["bosses", "hostile", "undead", "zombie", "monsters"])

