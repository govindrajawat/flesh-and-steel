
import requests
import json

def check_voice_search():
    url = "https://api.modrinth.com/v2/search"
    params = {"query": "Simple Voice Chat", "facets": json.dumps([["versions:1.20.1"]])}
    r = requests.get(url, params=params).json()
    for h in r.get("hits", [])[:10]:
        print(f"Slug: {h['slug']} (Title: {h['title']})")

check_voice_search()
