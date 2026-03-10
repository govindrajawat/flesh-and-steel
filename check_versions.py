import requests
import json

r = requests.get('https://api.modrinth.com/v2/project/toms-storage/version', params={'game_versions': json.dumps(['1.20.1'])})
versions = r.json()
for v in versions:
    print(f"{v['version_number']} | {v['id']}")
