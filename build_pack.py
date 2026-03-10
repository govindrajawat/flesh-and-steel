import requests
import json
import zipfile
import os
import time
import concurrent.futures
from pathlib import Path

# SETTINGS
MINECRAFT_VERSION = "1.20.1"
FABRIC_LOADER_VERSION = "0.18.4"
MODRINTH_API = "https://api.modrinth.com/v2"

MOD_LIST = [
    # CORE TECH & BIOMECHANICAL
    ("create-fabric", "Create Fabric"),
    ("modern-industrialization", "Modern Industrialization"),
    ("ae2", "Applied Energistics 2"),
    ("techreborn", "Tech Reborn"),
    ("advanced-netherite", "Advanced Netherite"),
    ("mythic-upgrades", "Mythic Upgrades"),
    ("toms-storage", "Tom's Simple Storage"),
    
    # CREATE ADDONS & THEME
    ("bellsandwhistles", "Create: Bells & Whistles"),
    ("chest-cavity", "Chest Cavity"),
    ("createaddition", "Create Crafts & Additions"),
    ("create-deco", "Create Deco"),
    ("create-enchantment-industry-fabric-legacy", "Create Enchantment Industry"),
    
    # COMBAT & WEAPONS
    ("bettercombat", "Better Combat"),
    ("simplyswords", "Simply Swords"),
    ("immersive-guns", "Immersive Guns"),
    ("artifacts", "Artifacts"),
    ("carry-on", "Carry On"),
    ("nyfsspiders", "Nyf's Spiders"),

    # WORLD & TERRAIN
    ("terralith", "Terralith"),
    ("incendium", "Incendium"),
    ("yungsapi", "YUNG's API"),
    ("waystones", "Waystones"),
    ("travelersbackpack", "Traveler's Backpack"),
    ("veinmining", "Vein Mining"),

    # STRUCTURES & DUNGEONS
    ("dungeons_arise", "When Dungeons Arise"),
    ("explorify", "Explorify"),
    ("dungeons-and-taverns", "Dungeons and Taverns"),
    ("integrated_stronghold", "Integrated Stronghold"),
    ("integrated_api", "Integrated API"),
    ("repurposed-structures-fabric", "Repurposed Structures"),
    ("create-structures", "Create: Structures"),
    ("graveyard", "The Graveyard (Fabric)"),
    ("aquamirae", "Aquamirae"),
    ("betterdungeons", "YUNG's Better Dungeons"),
    ("bettermineshafts", "YUNG's Better Mineshafts"),
    ("betterstrongholds", "YUNG's Better Strongholds"),
    ("betteroceanmonuments", "YUNG's Better Ocean Monuments"),
    ("betterfortresses", "YUNG's Better Nether Fortresses"),
    ("betterdeserttemples", "YUNG's Better Desert Temples"),
    ("betterjungletemples", "YUNG's Better Jungle Temples"),
    ("betterwitchhuts", "YUNG's Better Witch Huts"),
    ("yungsextras", "YUNG's Extras"),
    ("structory", "Structory"),
    ("structory_towers", "Structory: Towers"),
    ("dungeonz", "Dungeonz"),
    ("lootr", "Lootr"),

    # VILLAGES
    ("towns-and-towers", "Towns and Towers"),
    ("better-village", "Better Village"),
    ("villagesandpillages", "Villages & Pillages"),
    ("villager-names-serilum", "Villager Names"),
    ("custom-villager-trades", "Custom Villager Trades"),
    ("bountiful", "Bountiful"),

    # BLOOD & FLESH THEME
    ("sanguine", "Sanguine Blood Particles"),
    ("rotnputrid", "Rot N' Putrid"),
    ("flesh-to-leather", "Flesh to Leather"),
    ("forsaken_corpses", "Forsaken Corpses"),
    ("gigeresque", "Gigeresque"),
    ("somatogenesis", "Somatogenesis"),
    ("farmers-delight-refabricated", "Farmer's Delight (Fabric)"),
    ("natures-spirit", "Nature's Spirit"),
    ("biobutchers-delight", "BioButcher's Delight"),
    ("dahmersdelight", "Dahmer's Delight"),

    ("bosses_of_mass_destruction", "Bosses of Mass Destruction"),
    ("mutantmonsters", "Mutant Monsters"),
    ("zombie-awareness", "Zombie Awareness"),

    # ELDRITCH & OCCULT THEME
    ("eldritch-mobs", "Eldritch Mobs"),
    ("spectrum", "Spectrum (Otherworldly Magic)"),
    ("tftg", "The Flesh That Grows"),
    ("whisperwoods", "Whisperwoods (Creepy Mobs)"),

    # ECONOMY & PROGRESSION
    ("numismatics", "Numismatics"),
    ("origins", "Origins"),

    # SURVIVAL QOL
    ("universal-graves", "Universal Graves"),
    ("simplequests", "Simple Quests"),
    ("globalpacks", "GlobalPacks"),
    ("comforts", "Comforts"),

    # ATMOSPHERE & IMMERSION
    ("sound-physics-remastered", "Sound Physics Remastered"),
    ("ambientsounds", "AmbientSounds"),
    ("creativecore", "CreativeCore"),
    ("presencefootsteps", "Presence Footsteps"),
    ("visuality", "Visuality"),
    ("effective", "Effective"),
    ("supplementaries", "Supplementaries"),
    ("amendments", "Amendments"),

    # UI & QOL
    ("jei", "Just Enough Items"),
    ("jade", "Jade"),
    ("xaerominimap", "Xaero's Minimap"),
    ("xaeroworldmap", "Xaero's World Map"),
    ("appleskin", "AppleSkin"),
    ("inventoryprofilesnext", "Inventory Profiles Next"),
    ("explorerscompass", "Explorer's Compass"),
    ("naturescompass", "Nature's Compass"),
    ("mousetweaks", "Mouse Tweaks"),
    ("controlling", "Controlling"),
    ("clumps", "Clumps"),
    ("enchdesc", "Enchantment Descriptions"),
    ("betterthirdperson", "Better Third Person"),
    ("chipped", "Chipped"),
    ("storagedrawers", "Storage Drawers"),

    # MULTIPLAYER SOCIAL & FUN
    ("voicechat", "Simple Voice Chat"),
    ("emotecraft", "Emotecraft"),
    ("simplehats", "Simple Hats"),
    ("chat_heads", "Chat Heads"),
    ("styled-chat", "Styled Chat"),

    # PERFORMANCE - CLIENT
    ("sodium", "Sodium"),
    ("iris", "Iris"),
    ("indium", "Indium"),
    ("entityculling", "Entity Culling"),
    ("immediatelyfast", "ImmediatelyFast"),
    ("memoryleakfix", "Memory Leak Fix"),

    # PERFORMANCE - SERVER/SHARED
    ("lithium", "Lithium"),
    ("krypton", "Krypton"),
    ("modernfix", "ModernFix"),
    ("dynamic-fps", "Dynamic FPS"),
    ("noisium", "Noisium"),
    ("ferritecore", "FerriteCore"),
    ("c2me-fabric", "C2ME"),
    ("servercore", "ServerCore"),


    # UTILITIES
    ("spark", "Spark Profiler"),
    ("chunky", "Chunky"),
    ("modmenu", "Mod Menu"),
    ("purely-framework", "Framework"),

    # LIBRARY DEPENDENCIES
    ("fabric-api", "Fabric API"),
    ("cloth-config", "Cloth Config"),
    ("architectury", "Architectury API"),
    ("resourcefullib", "Resourceful Lib"),
    ("athena", "Athena"),
    ("terrablender", "TerraBlender"),
    ("balm", "Balm"),
    ("trinkets", "Trinkets"),
    ("fabric-language-kotlin", "Fabric Language Kotlin"),
    ("libipn", "libIPN"),
    ("fusion", "Fusion (Connected Textures)"),
    ("ponder", "Ponder for KubeJS"),
    ("kubejs", "KubeJS"),
    ("rhino", "Rhino"),
    ("playeranimator", "playerAnimator"),
    ("geckolib", "GeckoLib"),
    ("moonlight", "Moonlight Lib"),
    ("pehkui", "Pehkui"),
    ("lootjs", "LootJS"),
    ("morejs", "MoreJS"),
    ("obscure-api", "Obscure API"),
    ("searchables", "Searchables"),
    ("bookshelf", "Bookshelf"),
    ("azurelib", "AzureLib"),
    ("smartbrainlib", "SmartBrainLib"),
    ("puzzleslib", "Puzzles Lib"),
    ("library-ferret", "Library Ferret"),
    ("kambrik", "Kambrik"),
    ("owo-lib", "owo-lib"),
    ("revelationary", "Revelationary"),
    ("midnightlib", "MidnightLib"),
    ("accessories", "Accessories"),
    ("modonomicon", "Modonomicon"),
    ("patchouli", "Patchouli"),
    ("impersonate", "Impersonate"),
    ("cristellib", "Cristel Lib"),
    ("coroutil", "CoroUtil"),
    ("collective", "Collective (Library)"),

]

CLIENT_ONLY_MODS = [
    "sodium", "iris", "indium", "modmenu",
    "xaerominimap", "xaeroworldmap", "appleskin",
    "entityculling", "immediatelyfast", "memoryleakfix",
    "sound-physics-remastered", "ambientsounds", "presencefootsteps",
    "visuality", "effective", "chat_heads",
]


def get_best_version(project_id_or_slug):
    url = f"{MODRINTH_API}/project/{project_id_or_slug}/version"
    params = {"game_versions": json.dumps([MINECRAFT_VERSION])}
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            versions = r.json()
            if not versions: return None
            
            # Create Mod Ecosystem: Pin to stable 0.5.1-j era for compatibility with PonderJS and Addons
            if project_id_or_slug == "create-fabric":
                v_stable = [v for v in versions if "0.5.1-j" in v["version_number"].lower()]
                if v_stable: return v_stable[0]
            
            if project_id_or_slug == "createaddition":
                # Version 1.3.4+ require Create 6.x. Stay on 1.2.6 for Create 0.5.1 compatibility
                v_stable = [v for v in versions if "1.2.6" in v["version_number"].lower() and any(l.lower() in ["fabric", "quilt"] for l in v.get("loaders", []))]
                if v_stable: return v_stable[0]

            
            if project_id_or_slug == "create-deco":
                # Version 2.1.1+ is for Create 0.6.x. Stay on 2.0.2 for Create 0.5.1
                v_stable = [v for v in versions if "2.0.2" in v["version_number"].lower() and any(l.lower() in ["fabric", "quilt"] for l in v.get("loaders", []))]
                if v_stable: return v_stable[0]
            
            if project_id_or_slug in ["create-bells-and-whistles", "bellsandwhistles"]:
                v_stable = [v for v in versions if "0.4.5" in v["version_number"].lower() and any(l.lower() in ["fabric", "quilt"] for l in v.get("loaders", []))]
                if v_stable: return v_stable[0]

                
            if project_id_or_slug == "azurelib":
                # Gigeresque and Immersive Guns crash on the newer 3.x rewrites of azurelib.
                v_stable = [v for v in versions if v["version_number"].startswith("2.0.") and "forge" not in v["version_number"].lower() and any(l.lower() in ["fabric", "quilt"] for l in v.get("loaders", []))]
                if v_stable: return v_stable[0]

            if project_id_or_slug == "geckolib":
                # Gigeresque 0.5.72 was built against an old GeckoLib where GeoEntityRenderer
                # took GeoModel in its constructor. 4.7+ renamed this to EntityType, breaking
                # Gigeresque's mixin. We must stay on the 4.4.x branch.
                v_stable = [v for v in versions if v["version_number"].startswith("4.4.") and any(l.lower() in ["fabric", "quilt"] for l in v.get("loaders", []))]
                if v_stable: return v_stable[0]

            if project_id_or_slug == "numismatics":
                # 1.0.15 requires Create 6.x. Stay on 1.0.11 for Create 0.5.1 compatibility
                v_stable = [v for v in versions if "1.0.11" in v["version_number"] and any(l.lower() in ["fabric", "quilt"] for l in v.get("loaders", []))]
                if v_stable: return v_stable[0]

            if project_id_or_slug == "immersive-guns":
                # Pin to a version compatible with Azurelib 2.0
                v_stable = [v for v in versions if "0.1.1-fabric" in v["version_number"].lower()]
                if v_stable: return v_stable[0]

            if project_id_or_slug == "comforts":
                 v_stable = [v for v in versions if any(l.lower() in ["fabric", "quilt"] for l in v.get("loaders", []))]
                 if v_stable: return v_stable[0]


            # STRICTLY Prioritize Fabric/Quilt and Ignore Forge unless it's a multi-platform build
            fabric = [v for v in versions if any(l.lower() in ["fabric", "quilt"] for l in v.get("loaders", []))]
            if fabric: return fabric[0]
            
            minecraft = [v for v in versions if "minecraft" in [l.lower() for l in v.get("loaders", [])]] # Resource packs
            if minecraft: return minecraft[0]

            
            # Disable Forge fallback for a Fabric pack
            # forge = [v for v in versions if any(l.lower() in ["forge", "neoforge"] for l in v.get("loaders", []))]
            # if forge: return forge[0]
    except: pass
    return None

def download_file(url, dest):
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with open(dest, 'wb') as f: f.write(r.content)
            return True
    except: pass
    return False

def main():
    print("🛠️ Generating Flesh & Steel Modpack...")
    mrpack_files = []
    log_lines = []
    
    server_mods_dir = Path("server_mods")
    server_mods_dir.mkdir(exist_ok=True)

    processed_slugs = set()
    
    for slug, name in MOD_LIST:
        if slug in processed_slugs: continue
        processed_slugs.add(slug)
        
        print(f"Resolving {name}...", end=" ", flush=True)
        version = get_best_version(slug)
        
        if not version:
            # Try search
            search_url = f"{MODRINTH_API}/search"
            params = {"query": name, "facets": json.dumps([[f"versions:{MINECRAFT_VERSION}"]])}
            try:
                hits = requests.get(search_url, params=params).json().get("hits", [])
                if hits: version = get_best_version(hits[0]["project_id"])
            except: pass

        if version:
            file = version["files"][0]
            is_resourcepack = "resourcepack" in [f.get("filename", "").lower() for f in version["files"]] or "fresh-animations" in slug or "pretty-pipes" in slug
            
            path = f"resourcepacks/{file['filename']}" if is_resourcepack else f"mods/{file['filename']}"
            
            entry = {
                "path": path,
                "hashes": file["hashes"],
                "downloads": [file["url"]],
                "fileSize": file["size"],
                "env": {
                    "client": "required",
                    "server": "unsupported" if slug in CLIENT_ONLY_MODS or is_resourcepack else "required"
                }
            }
            mrpack_files.append(entry)
            print("OK")
            
            # Download for server ZIP if applicable
            if entry["env"]["server"] == "required":
                dest = server_mods_dir / file["filename"]
                if not dest.exists():
                    download_file(file["url"], dest)
            
            log_lines.append(f"[OK] {name} -> {file['filename']}")
        else:
            print("NOT FOUND")
            log_lines.append(f"[FAIL] {name} not found on Modrinth for 1.20.1")

    # Final Manifest
    index = {
        "formatVersion": 1,
        "game": "minecraft",
        "versionId": "1.0.0",
        "name": "Flesh and Steel",
        "summary": "Biomechanical Tech Modpack",
        "files": mrpack_files,
        "dependencies": {
            "minecraft": MINECRAFT_VERSION,
            "fabric-loader": FABRIC_LOADER_VERSION
        }
    }

    # Write .mrpack (Modrinth format)
    with zipfile.ZipFile("flesh-and-steel.mrpack", "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("modrinth.index.json", json.dumps(index, indent=2))
        if os.path.exists("overrides"):
            for root, _, files in os.walk("overrides"):
                for fn in files:
                    file_path = os.path.join(root, fn)
                    zf.write(file_path, arcname=file_path)

    # Write server zip
    with zipfile.ZipFile("flesh-and-steel-server-mods.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for f in server_mods_dir.glob("*.jar"):
            zf.write(f, arcname=f"mods/{f.name}")

    with open("install-log.txt", "w") as f:
        f.write("\n".join(log_lines))

    print("\n✅ Build complete!")
    print(f"Artifacts ready:\n- flesh-and-steel.mrpack (Import this in Prism/Modrinth App)\n- flesh-and-steel-server-mods.zip (Server side mods)")

if __name__ == "__main__":
    main()
