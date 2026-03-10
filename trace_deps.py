import requests
import json
MODRINTH_API = "https://api.modrinth.com/v2"

def get_fabric_version_info(slug):
    r = requests.get(f"{MODRINTH_API}/project/{slug}/version", params={"game_versions": "[\"1.20.1\"]", "loaders": "[\"fabric\"]"})
    if r.status_code == 200:
        versions = r.json()
        if versions:
            v = versions[0]
            print(f"Slug: {slug} | Version: {v['version_number']}")
            for dep in v.get('dependencies', []):
                p_id = dep.get('project_id')
                if p_id:
                    pr = requests.get(f"{MODRINTH_API}/project/{p_id}")
                    if pr.status_code == 200:
                        print(f"  - Dep: {pr.json()['title']} | Slug: {pr.json()['slug']} ({dep.get('dependency_type')})")
        else:
            print(f"No Fabric version for {slug} on 1.20.1")

get_fabric_version_info("kubejs")
get_fabric_version_info("rhino")
get_fabric_version_info("ponderjs")
get_fabric_version_info("ponder")
