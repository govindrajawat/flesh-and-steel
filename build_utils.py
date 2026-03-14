#!/usr/bin/env python3
"""
Flesh & Steel — Shared Build Utilities
"""

import requests
import json
import zipfile
import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
PACK_CONFIG = PROJECT_ROOT / "pack-config" / "mods.json"
MODRINTH_API = "https://api.modrinth.com/v2"
LOCAL_MODS_DIR = PROJECT_ROOT / "local_mods"


def _iter_local_jars(*dirs: Path):
    for d in dirs:
        if not d.exists():
            continue
        for jar in sorted(d.glob("*.jar")):
            yield jar


def _collect_local_jars(*dirs: Path):
    """
    Collect local jars uniquely by filename.
    Earlier directories win (common should override client/server if duplicated).
    """
    by_name: dict[str, Path] = {}
    for jar in _iter_local_jars(*dirs):
        by_name.setdefault(jar.name, jar)
    return [by_name[name] for name in sorted(by_name.keys())]


def load_config():
    with open(PACK_CONFIG) as f:
        return json.load(f)


def get_best_version(slug, mc_version, version_pins):
    """Resolve the best Modrinth version for a mod slug (Forge loader)."""
    url = f"{MODRINTH_API}/project/{slug}/version"
    params = {"game_versions": json.dumps([mc_version])}
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code != 200:
            return None
        versions = r.json()
        if not versions:
            return None

        # Check for pinned version — prefer Forge/NeoForge match first
        pin = version_pins.get(slug)
        if pin:
            pinned_forge = [
                v for v in versions
                if pin in v["version_number"].lower()
                   and any(l.lower() in ["forge", "neoforge"] for l in v.get("loaders", []))
            ]
            if pinned_forge:
                return pinned_forge[0]
            # Prefix fallback ignoring loader
            pinned = [v for v in versions if v["version_number"].startswith(pin)]
            if pinned:
                return pinned[0]

        # Prefer Forge/NeoForge builds
        forge = [
            v for v in versions
            if any(l.lower() in ["forge", "neoforge"] for l in v.get("loaders", []))
        ]
        if forge:
            return forge[0]

        # Resource packs / datapacks use "minecraft" loader
        minecraft = [
            v for v in versions
            if "minecraft" in [l.lower() for l in v.get("loaders", [])]
        ]
        if minecraft:
            return minecraft[0]

    except Exception as e:
        print(f"\nError fetching versions for {slug}: {e}")
    return None


def download_file(url, dest):
    """Download a file from a URL to a local path."""
    try:
        print(f"  Downloading {dest.name}...")
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with open(dest, "wb") as f:
                f.write(r.content)
            return True
    except Exception as e:
        print(f"\nError downloading {url}: {e}")
    return False


def resolve_and_download(slug, name, side, mc_version, version_pins, mods_dir):
    """Resolve a mod version and download it. Returns (slug, name, side, entry_or_None)."""
    version = get_best_version(slug, mc_version, version_pins)

    # Fallback: try search
    if not version:
        try:
            search_url = f"{MODRINTH_API}/search"
            params = {"query": name, "facets": json.dumps([[f"versions:{mc_version}"]])}
            hits = requests.get(search_url, params=params, timeout=10).json().get("hits", [])
            if hits:
                version = get_best_version(hits[0]["project_id"], mc_version, version_pins)
        except Exception as e:
            print(f"\nError searching for {name}: {e}")

    if not version:
        return slug, name, side, None

    file_info = version["files"][0]
    filename = file_info["filename"]
    dest_dir = mods_dir / side
    dest_path = dest_dir / filename

    if not dest_path.exists():
        download_file(file_info["url"], dest_path)

    entry = {
        "filename": filename,
        "path": f"mods/{filename}",
        "hashes": file_info["hashes"],
        "downloads": [file_info["url"]],
        "fileSize": file_info["size"],
        "env": {
            "client": "unsupported" if side == "server" else "required",
            "server": "unsupported" if side == "client" else "required"
        },
    }
    return slug, name, side, entry


def resolve_mods(config, sides, mods_dir):
    """Resolve and download mods for the given sides ('common', 'client', 'server')."""
    mc_version = config["minecraft_version"]
    version_pins = config.get("version_pins", {})

    all_mods_to_resolve = []
    for side in sides:
        for mod in config["mods"].get(side, []):
            all_mods_to_resolve.append((mod["slug"], mod["name"], side))

    mrpack_files = []
    log_lines = []
    processed = set()

    print(f"\n📦 Resolving {len(all_mods_to_resolve)} mods for sides: {sides}...\n")

    for slug, name, side in all_mods_to_resolve:
        if slug in processed:
            continue
        processed.add(slug)

        print(f"  Resolving {name} ({side})...", end=" ", flush=True)
        _, _, _, entry = resolve_and_download(slug, name, side, mc_version, version_pins, mods_dir)

        if entry:
            mrpack_files.append(entry)
            print("✅")
            log_lines.append(f"[OK] {name} ({side}) -> {entry['filename']}")
        else:
            print("❌ NOT FOUND")
            log_lines.append(f"[FAIL] {name} ({side}) not found on Modrinth for {mc_version}")
    return mrpack_files, log_lines


def build_mrpack(config, mrpack_files, project_root, output_path):
    """Build a .mrpack (Modrinth format) from resolved mod entries."""
    index = {
        "formatVersion": 1,
        "game": "minecraft",
        "versionId": config["pack_version"],
        "name": config["pack_name"],
        "summary": config["pack_summary"],
        "files": mrpack_files,
        "dependencies": {
            "minecraft": config["minecraft_version"],
            "forge": config["forge_version"],
        },
    }

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("modrinth.index.json", json.dumps(index, indent=2))

        # Include overrides: config, kubejs, global_data_packs, patched mods
        overrides_map = {
            project_root / "config": "overrides/config",
            project_root / "kubejs": "overrides/kubejs",
            project_root / "global_data_packs": "overrides/global_data_packs",
        }
        for src_dir, arc_prefix in overrides_map.items():
            if not src_dir.exists():
                continue
            for root, _, files in os.walk(src_dir):
                for fn in files:
                    file_path = Path(root) / fn
                    arcname = f"{arc_prefix}/{file_path.relative_to(src_dir)}"
                    zf.write(file_path, arcname=arcname)

        # Include local mods (e.g. CurseForge-only mods) directly in the pack.
        # These will be copied into the instance's `mods/` folder on install.
        local_common = LOCAL_MODS_DIR / "common"
        local_client = LOCAL_MODS_DIR / "client"
        for jar in _collect_local_jars(local_common, local_client):
            zf.write(jar, arcname=f"overrides/mods/{jar.name}")

def build_server_pack(config, project_root, output_dir):
    """Assemble the server pack directory from common + server mods + configs."""
    mods_dir = project_root / "mods"

    # Clean and recreate mods destination
    server_mods_dest = output_dir / "mods"
    if server_mods_dest.exists():
        shutil.rmtree(server_mods_dest)
    server_mods_dest.mkdir(parents=True, exist_ok=True)

    # Copy common mods
    for jar in sorted((mods_dir / "common").glob("*.jar")):
        shutil.copy2(jar, server_mods_dest / jar.name)

    # Copy server-only mods
    server_dir = mods_dir / "server"
    if server_dir.exists():
        for jar in sorted(server_dir.glob("*.jar")):
            shutil.copy2(jar, server_mods_dest / jar.name)

    # Copy local mods into server pack
    local_common = LOCAL_MODS_DIR / "common"
    local_server = LOCAL_MODS_DIR / "server"
    for jar in _collect_local_jars(local_common, local_server):
        shutil.copy2(jar, server_mods_dest / jar.name)

    # Copy config, KubeJS, data packs, and scripts
    copy_map = {
        project_root / "config": output_dir / "config",
        project_root / "global_data_packs": output_dir / "global_data_packs",
        project_root / "audio_player": output_dir / "audio_player",
    }
    for src, dest in copy_map.items():
        if dest.exists():
            shutil.rmtree(dest)
        if src.exists():
            shutil.copytree(src, dest)

    # Copy KubeJS (server + startup scripts only)
    dest_kubejs = output_dir / "kubejs"
    if dest_kubejs.exists():
        shutil.rmtree(dest_kubejs)
    src_kubejs = project_root / "kubejs"
    if src_kubejs.exists():
        for subdir in ["server_scripts", "startup_scripts"]:
            src_sub = src_kubejs / subdir
            dest_sub = dest_kubejs / subdir
            if src_sub.exists():
                shutil.copytree(src_sub, dest_sub, dirs_exist_ok=True)

    # Copy server deployment scripts
    scripts_dir = project_root / "scripts"
    if scripts_dir.exists():
        for f in scripts_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, output_dir / f.name)

    # Zip the entire server pack directory
    zip_path = output_dir.parent / f"{config['pack_name']}-server.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(output_dir):
            for fn in files:
                file_path = Path(root) / fn
                arcname = file_path.relative_to(output_dir)
                zf.write(file_path, arcname=arcname)
    return zip_path