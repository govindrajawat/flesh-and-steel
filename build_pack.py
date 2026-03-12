#!/usr/bin/env python3
"""
Flesh & Steel — Modpack Build Script

Reads mod definitions from pack-config/mods.json, downloads them into
mods/common/, mods/client/, and mods/server/, then assembles:
  - build/client-pack/flesh-and-steel.mrpack  (Modrinth client pack)
  - build/server-pack/                         (ready-to-deploy server)

Usage:
    python build_pack.py
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


def load_config():
    with open(PACK_CONFIG) as f:
        return json.load(f)


def get_best_version(slug, mc_version, version_pins):
    """Resolve the best Modrinth version for a mod slug."""
    url = f"{MODRINTH_API}/project/{slug}/version"
    params = {"game_versions": json.dumps([mc_version])}
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code != 200:
            return None
        versions = r.json()
        if not versions:
            return None

        # Check for pinned version
        pin = version_pins.get(slug)
        if pin:
            pinned = [
                v for v in versions
                if pin in v["version_number"].lower()
                and any(l.lower() in ["fabric", "quilt"] for l in v.get("loaders", []))
            ]
            if pinned:
                return pinned[0]
            # Prefix match fallback
            pinned = [v for v in versions if v["version_number"].startswith(pin)]
            if pinned:
                return pinned[0]

        # Special handling for comforts (needs fabric filter)
        if slug == "comforts":
            fabric = [
                v for v in versions
                if any(l.lower() in ["fabric", "quilt"] for l in v.get("loaders", []))
            ]
            if fabric:
                return fabric[0]

        # Prefer Fabric/Quilt builds
        fabric = [
            v for v in versions
            if any(l.lower() in ["fabric", "quilt"] for l in v.get("loaders", []))
        ]
        if fabric:
            return fabric[0]

        # Resource packs use "minecraft" loader
        minecraft = [
            v for v in versions
            if "minecraft" in [l.lower() for l in v.get("loaders", [])]
        ]
        if minecraft:
            return minecraft[0]

    except Exception:
        pass
    return None


def download_file(url, dest):
    """Download a file from a URL to a local path."""
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with open(dest, "wb") as f:
                f.write(r.content)
            return True
    except Exception:
        pass
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
        except Exception:
            pass

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
            "client": "required",
            "server": "unsupported" if side == "client" else "required",
        },
    }
    return slug, name, side, entry


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
            "fabric-loader": config["fabric_loader_version"],
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

        # Include patched mods in overrides/mods/
        patched_filenames = {p["filename"] for p in config.get("patched_mods", [])}
        patched_dir = project_root / "mods" / "common"
        if patched_dir.exists():
            for jar in patched_dir.glob("*.jar"):
                if jar.name in patched_filenames:
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

    # Copy config
    src_config = project_root / "config"
    dest_config = output_dir / "config"
    if dest_config.exists():
        shutil.rmtree(dest_config)
    if src_config.exists():
        shutil.copytree(src_config, dest_config)

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
                dest_sub.mkdir(parents=True, exist_ok=True)
                for item in src_sub.rglob("*"):
                    if item.is_file():
                        rel = item.relative_to(src_sub)
                        target = dest_sub / rel
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, target)

    # Copy global data packs
    src_dp = project_root / "global_data_packs"
    dest_dp = output_dir / "global_data_packs"
    if dest_dp.exists():
        shutil.rmtree(dest_dp)
    if src_dp.exists():
        shutil.copytree(src_dp, dest_dp)

    # Copy server deployment scripts (install.sh, start.sh, README.md)
    scripts_dir = project_root / "scripts"
    if scripts_dir.exists():
        for f in scripts_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, output_dir / f.name)

    # Create a server mods zip
    zip_path = output_dir / "flesh-and-steel-server-mods.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for jar in sorted(server_mods_dest.glob("*.jar")):
            zf.write(jar, arcname=f"mods/{jar.name}")


def main():
    print("🛠️  Flesh & Steel — Build System")
    print("=" * 50)

    config = load_config()
    mc_version = config["minecraft_version"]
    version_pins = config.get("version_pins", {})
    mods_dir = PROJECT_ROOT / "mods"

    # Ensure mod dirs exist
    for side in ["common", "client", "server"]:
        (mods_dir / side).mkdir(parents=True, exist_ok=True)

    build_dir = PROJECT_ROOT / "build"
    client_pack_dir = build_dir / "client-pack"
    server_pack_dir = build_dir / "server-pack"
    client_pack_dir.mkdir(parents=True, exist_ok=True)
    server_pack_dir.mkdir(parents=True, exist_ok=True)

    # Collect all mods with their side
    all_mods = []
    for side in ["common", "client", "server"]:
        for mod in config["mods"].get(side, []):
            all_mods.append((mod["slug"], mod["name"], side))

    # Resolve and download all mods
    mrpack_files = []
    log_lines = []
    processed = set()

    print(f"\n📦 Resolving {len(all_mods)} mods...\n")

    for slug, name, side in all_mods:
        if slug in processed:
            continue
        processed.add(slug)

        print(f"  Resolving {name} ({side})...", end=" ", flush=True)
        _, _, _, entry = resolve_and_download(
            slug, name, side, mc_version, version_pins, mods_dir
        )

        if entry:
            mrpack_files.append(entry)
            print("✅")
            log_lines.append(f"[OK] {name} ({side}) -> {entry['filename']}")
        else:
            print("❌ NOT FOUND")
            log_lines.append(f"[FAIL] {name} ({side}) not found on Modrinth for {mc_version}")

    # Build .mrpack
    print("\n📦 Building client .mrpack...")
    mrpack_path = client_pack_dir / "flesh-and-steel.mrpack"
    build_mrpack(config, mrpack_files, PROJECT_ROOT, mrpack_path)
    print(f"  ✅ {mrpack_path}")

    # Build server pack
    print("\n📦 Building server pack...")
    build_server_pack(config, PROJECT_ROOT, server_pack_dir)
    print(f"  ✅ {server_pack_dir}")

    # Write build log
    log_path = build_dir / "install-log.txt"
    with open(log_path, "w") as f:
        f.write("\n".join(log_lines))

    print(f"\n{'=' * 50}")
    print("✅ Build complete!")
    print(f"   Client pack: {mrpack_path}")
    print(f"   Server pack: {server_pack_dir}")
    print(f"   Build log:   {log_path}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
