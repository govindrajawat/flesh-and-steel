import requests
import json
MODRINTH_API = "https://api.modrinth.com/v2"

r = requests.get(f"{MODRINTH_API}/search", params={"query": "PonderJS", "facets": "[[\"versions:1.20.1\"]] "})
if r.status_code == 200:
    for h in r.json().get("hits", []):
        print(f"Title: {h['title']} | Slug: {h['slug']} | ID: {h['project_id']}")
else:
    print(r.status_code)
