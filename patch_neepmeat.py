import requests, zipfile, io, json, os
from pathlib import Path

# Remove neepmeat from MOD_LIST later in build_pack.py
url = requests.get('https://api.modrinth.com/v2/project/neepmeat/version', params={'game_versions':json.dumps(['1.20.1'])}).json()[0]['files'][0]['url']
print("Downloading neepmeat...")
jar_data = requests.get(url).content

print("Patching neepmeat JAR...")
out_buffer = io.BytesIO()

with zipfile.ZipFile(io.BytesIO(jar_data), "r") as zin:
    with zipfile.ZipFile(out_buffer, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)
            
            # If this is the bundled modern flywheel JAR, we need to patch ITS fabric.mod.json
            if item.filename.endswith(".jar") and "flywheel" in item.filename:
                print(f"Patching embedded JAR: {item.filename}")
                inner_in = io.BytesIO(content)
                inner_out = io.BytesIO()
                
                with zipfile.ZipFile(inner_in, "r") as inner_zin:
                    with zipfile.ZipFile(inner_out, "w", zipfile.ZIP_DEFLATED) as inner_zout:
                        for inner_item in inner_zin.infolist():
                            inner_content = inner_zin.read(inner_item.filename)
                            if inner_item.filename == "fabric.mod.json":
                                inner_fmj = json.loads(inner_content)
                                if inner_fmj.get("id") == "flywheel":
                                    print("Changing mod ID from 'flywheel' to 'flywheel_engine_room'")
                                    inner_fmj["id"] = "flywheel_engine_room"
                                    # Also change it in provides if any
                                    if "provides" in inner_fmj and "flywheel" in inner_fmj["provides"]:
                                        inner_fmj["provides"].remove("flywheel")
                                    inner_content = json.dumps(inner_fmj, indent=2).encode('utf-8')
                            inner_zout.writestr(inner_item, inner_content)
                
                content = inner_out.getvalue()
                
            # If this is neepmeat's fabric.mod.json, update it to use the new nested mod id?
            # Actually fabric loader just loads whatever is in "jars" array natively.
            # But the "jars" array points to the filename. We didn't change the filename.
            # Wait, do we need to update neepmeat's dependencies if it specifically requires "flywheel"?
            if item.filename == "fabric.mod.json":
                fmj = json.loads(content)
                if "depends" in fmj and "flywheel" in fmj["depends"]:
                    fmj["depends"]["flywheel_engine_room"] = fmj["depends"]["flywheel"]
                    del fmj["depends"]["flywheel"]
                content = json.dumps(fmj, indent=2).encode('utf-8')
                
            zout.writestr(item, content)

os.makedirs("overrides/mods", exist_ok=True)
with open("overrides/mods/neepmeat-0.25.3-fixed.jar", "wb") as f:
    f.write(out_buffer.getvalue())
print("Saved patched neepmeat to overrides/mods/neepmeat-0.25.3-fixed.jar")
