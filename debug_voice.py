
import sys
import os
import json

# Add current dir to path
sys.path.append(os.getcwd())

import build_pack

v = build_pack.get_best_version("simple-voice-chat")
if v:
    print(f"Slug found: {v['version_number']} - Loaders: {v['loaders']}")
    # print(json.dumps(v, indent=2))
else:
    print("Version not found!")

# Try search fallback logic
import requests
MODRINTH_API = "https://api.modrinth.com/v2"
name = "Simple Voice Chat"
search_url = f"{MODRINTH_API}/search"
params = {"query": name, "facets": json.dumps([["versions:1.20.1"]])}
hits = requests.get(search_url, params=params).json().get("hits", [])
if hits:
    print(f"First search hit: {hits[0]['slug']} (Title: {hits[0]['title']})")
