import zipfile
import json
import os

PACK_FILE = "flesh-and-steel.mrpack"

def verify_pack():
    if not os.path.exists(PACK_FILE):
        print(f"Error: {PACK_FILE} does not exist.")
        return

    try:
        with zipfile.ZipFile(PACK_FILE, 'r') as zf:
            print(f"Files in zip: {zf.namelist()}")
            if "modrinth.index.json" not in zf.namelist():
                print("Error: modrinth.index.json is missing!")
                return
            
            index_data = zf.read("modrinth.index.json")
            index = json.loads(index_data)
            
            print("\nManifest Schema Validation:")
            required_keys = ["formatVersion", "game", "versionId", "name", "files", "dependencies"]
            for key in required_keys:
                if key in index:
                    print(f"  [OK] {key}: {type(index[key])}")
                else:
                    print(f"  [MISSING] {key}!")
            
            print(f"\nTotal files in manifest: {len(index.get('files', []))}")
            if index.get('files'):
                first_file = index['files'][0]
                print(f"Sample file entry: {first_file['path']}")
                if 'hashes' not in first_file or 'sha1' not in first_file['hashes']:
                    print("  [ERROR] Hashes or sha1 missing in file entry!")

            print(f"\nDependencies: {index.get('dependencies')}")

    except Exception as e:
        print(f"Error reading zip: {e}")

if __name__ == "__main__":
    verify_pack()
