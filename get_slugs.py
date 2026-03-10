import requests
import json

def get_slugs(query):
    url = f"https://api.modrinth.com/v2/search"
    params = {"query": query, "facets": json.dumps([["versions:1.20.1"], ["categories:fabric"]])}
    r = requests.get(url, params=params)
    for h in r.json().get('hits', [])[:3]:
        print(f"{h['slug']} | {h['title']}")

print("--- Slugs ---")
get_slugs("FTB Quests")
get_slugs("FTB Teams")
get_slugs("FTB Library")
get_slugs("Integrated Stronghold")
get_slugs("Integrated Villages")
get_slugs("Visuality")
get_slugs("Ambient Sounds")
get_slugs("Presence Footsteps")
get_slugs("Sound Physics Remastered")
get_slugs("Victus")
get_slugs("Sons of Sins")
get_slugs("Biomancy")
get_slugs("Explorify")
get_slugs("Choiceover")
