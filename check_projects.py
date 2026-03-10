import requests
import json

def check_project(slug):
    url = f"https://api.modrinth.com/v2/project/{slug}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        print(f"--- {slug} ---")
        print(f"Title: {data['title']}")
        print(f"Categories: {data['categories']}")
        print(f"Server Side: {data['server_side']}")
        print(f"Client Side: {data['client_side']}")

check_project("ftb-quests")
check_project("ftb-quests-fabric")
check_project("ftb-library")
check_project("ftb-library-fabric")
check_project("ftb-teams")
check_project("ftb-teams-fabric")
check_project("biomancy")
check_project("victus")
check_project("integrated-stronghold")
check_project("better-stronghold")
check_project("when-dungeons-arise")
check_project("create-steam-n-rails")
