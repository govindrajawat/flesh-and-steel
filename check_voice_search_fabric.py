
import requests
import json

def check_voice_search_fabric():
    url = "https://api.modrinth.com/v2/search"
    # Filter for Fabric 1.20.1
    facets = [
        ["versions:1.20.1"],
        ["categories:fabric"]
    ]
    params = {"query": "voice chat", "facets": json.dumps(facets)}
    r = requests.get(url, params=params).json()
    for h in r.get("hits", [])[:10]:
        print(f"Slug: {h['slug']} (Title: {h['title']})")

check_voice_search_fabric()
