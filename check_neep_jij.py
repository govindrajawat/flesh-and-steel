import requests, zipfile, io, json
r = requests.get('https://api.modrinth.com/v2/project/neepmeat/version', params={'game_versions':json.dumps(['1.20.1'])})
for v in r.json():
    ver = v['version_number']
    url = v['files'][0]['url']
    jar = requests.get(url).content
    with zipfile.ZipFile(io.BytesIO(jar)) as z:
        fmj = json.loads(z.read("fabric.mod.json"))
        jars = fmj.get("jars", [])
        flywheels = [j for j in jars if 'flywheel' in j['file'].lower()]
        print(f"neepmeat {ver} bundles: {flywheels}")
