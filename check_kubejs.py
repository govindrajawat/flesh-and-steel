import requests
import json
MODRINTH_API = "https://api.modrinth.com/v2"

queries = ["kubejs", "rhino", "ponderjs"]
for q in queries:
    r = requests.get(f"{MODRINTH_API}/search", params={"query": q, "facets": "[[\"versions:1.20.1\"], [\"project_type:mod\"]] "})
    if r.status_code == 200:
        hits = r.json().get("hits", [])
        if hits:
            print(f"Query: {q} | Best match: {hits[0]['title']} | Slug: {hits[0]['slug']}")
            # Check dependencies of the best match
            project_id = hits[0]['project_id']
            v_url = f"{MODRINTH_API}/project/{project_id}/version"
            vr = requests.get(v_url, params={"game_versions": "[\"1.20.1\"]"})
            if vr.status_code == 200:
                versions = vr.json()
                if versions:
                    best_v = versions[0]
                    print(f"  Version: {best_v['version_number']}")
                    print(f"  Deps: {[d.get('project_id', d.get('version_id')) for d in best_v.get('dependencies', [])]}")
        else:
            print(f"Query: {q} | No hits")
