import requests
import json
MODRINTH_API = "https://api.modrinth.com/v2"

queries = ["trinkets", "fabric-language-kotlin", "libipn", "Fusion connected textures", "ponder"]
for q in queries:
    r = requests.get(f"{MODRINTH_API}/search", params={"query": q, "facets": "[[\"versions:1.20.1\"]]"})
    if r.status_code == 200:
        hits = r.json().get("hits", [])
        if hits:
            print(f"Query: {q} | Best match: {hits[0]['title']} | Slug: {hits[0]['slug']}")
        else:
            print(f"Query: {q} | No hits")
