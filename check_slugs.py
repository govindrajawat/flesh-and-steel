import requests
import json

MODRINTH_API = "https://api.modrinth.com/v2"

slugs = ["supermartijn642corelib", "supermartijn642s-core-lib", "supermartijn642configlib", "supermartijn642s-config-lib", "resourcefullib", "athena", "terrablender", "balm"]
for s in slugs:
    r = requests.get(f"{MODRINTH_API}/project/{s}")
    print(f"{s}: {r.status_code}")
