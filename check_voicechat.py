
import requests
import json

def check_voicechat():
    url = "https://api.modrinth.com/v2/project/voicechat/version"
    params = {"game_versions": json.dumps(["1.20.1"]), "loaders": json.dumps(["fabric"])}
    r = requests.get(url, params=params).json()
    for v in r[:5]:
        print(f"Version: {v['version_number']} (Date: {v['date_published']})")

check_voicechat()
