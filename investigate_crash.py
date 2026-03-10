import requests
import json
MODRINTH_API = "https://api.modrinth.com/v2"

def check_project(slug):
    print(f"--- Project: {slug} ---")
    r = requests.get(f"{MODRINTH_API}/project/{slug}/version", params={"game_versions": "[\"1.20.1\"]"})
    if r.status_code == 200:
        versions = r.json()
        for v in versions:
            print(f"Version: {v['version_number']} | Loaders: {v['loaders']} | Type: {v['version_type']}")
            for dep in v.get('dependencies', []):
                print(f"  Dep: {dep.get('project_id')} | Version: {dep.get('version_id')} | Type: {dep.get('dependency_type')}")
    else:
        print(f"Failed to fetch {slug}: {r.status_code}")

check_project("grim-and-bleak")
check_project("ponderjs")
check_project("kubejs")
