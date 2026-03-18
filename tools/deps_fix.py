import os
import urllib.request
import json

req_headers = {'User-Agent': 'FleshAndSteel/4.0 (contact@example.com)'}

dest_prism = r'C:\Users\govind\AppData\Roaming\PrismLauncher\instances\flesh-and-steel\minecraft\mods'
dest_local = r'd:\home_clone\flesh-and-steel\local_mods\common'

# 1. Delete Corrupted / Wrong Version Files
files_to_delete = [
    'LongNbtKiller-Forge-1.20.2-1.0.0.jar',
    'item-filters-forge-2001.1.0-build.53.jar',
    'no_moon-1.5.6-forge-1.20.1.jar' # Just in case it's still lingering
]

for folder in [dest_prism, dest_local]:
    for file in files_to_delete:
        path = os.path.join(folder, file)
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"Deleted broken/outdated file: {file} from {folder}")
            except Exception as e:
                print(f"Could not delete {file}: {e}")

# 2. Download Correct / Working Files
def download_mod(slug):
    url = f"https://api.modrinth.com/v2/project/{slug}/version"
    try:
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            
            for v in data:
                if 'forge' in v['loaders'] and '1.20.1' in v['game_versions']:
                    file_info = v['files'][0]
                    dl_url = file_info['url']
                    dl_name = file_info['filename']
                    
                    print(f"Downloading working {dl_name}...")
                    
                    req_dl = urllib.request.Request(dl_url, headers=req_headers)
                    with urllib.request.urlopen(req_dl) as dl:
                        content = dl.read()
                        with open(os.path.join(dest_prism, dl_name), 'wb') as f: f.write(content)
                        with open(os.path.join(dest_local, dl_name), 'wb') as f: f.write(content)
                    
                    print(f"Success! Saved to Prism and local_mods.")
                    return True
            print(f"Could not find a 1.20.1 Forge version for {slug}.")
    except Exception as e:
        print(f"Error downloading {slug}: {e}")
    return False

# Download correct item filters and no_moon from Modrinth
download_mod("item-filters")
download_mod("no-moon")

print("All crash-causing mods removed and updated completely!")
