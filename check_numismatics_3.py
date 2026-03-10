import requests, json

slug = "numismatics"
MINECRAFT_VERSION = "1.20.1"

r = requests.get(
    f"https://api.modrinth.com/v2/project/{slug}/version",
    params={"game_versions": json.dumps([MINECRAFT_VERSION]), "loaders": json.dumps(["fabric"])},
    timeout=10
)

if r.status_code == 200:
    for v in r.json()[::-1]: # Start from the oldest
        print(f"Version: {v['version_number']}")
        for dep in v['dependencies']:
            if dep['project_id'] == 'Xbc0uyRg': # Create
                print(f"  Create Dep: {dep.get('version_id', 'Any')} ({dep.get('dependency_type', 'required')})")
        print("-" * 20)
else:
    print(f"Error: {r.status_code}")
