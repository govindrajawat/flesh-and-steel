import requests
import json

search_url = "https://api.modrinth.com/v2/search"
params = {"query": "Bells & Whistles", "facets": json.dumps([["versions:1.20.1"], ["categories:fabric"]])}
r = requests.get(search_url, params=params)
for hit in r.json().get('hits', []):
    print(f"{hit['slug']} | {hit['title']}")
