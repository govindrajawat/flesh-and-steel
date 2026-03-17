#!/usr/bin/env python3
"""
Flesh & Steel — Update Script
Updates a deployed server or dev environment from a release zip.

Sources:
  --zip <path>          Local server pack .zip or .mrpack file
  --github [tag]        Download from GitHub releases (latest if no tag given)

Usage:
    python update.py --github                  # latest release
    python update.py --github v3.2.1           # specific tag
    python update.py --zip path/to/server.zip
    python update.py --zip path/to/pack.mrpack

Options:
    --target <dir>      Directory to update (default: current working directory)
    --no-backup         Skip backup of replaced directories
    --dry-run           Show what would change without applying anything
"""

import argparse
import json
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' is required. Run: pip install requests")
    sys.exit(1)

GITHUB_REPO = "govindrajawat/flesh-and-steel"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases"

# Directories/files to update from a server pack zip
SERVER_UPDATE_DIRS = ["mods", "config", "kubejs", "global_data_packs", "audio_player"]
SERVER_UPDATE_FILES = ["install.sh", "start.sh", "README.md"]

# Overrides directories inside a .mrpack
MRPACK_OVERRIDES = ["config", "kubejs", "global_data_packs", "mods"]


# ---------------------------------------------------------------------------
# GitHub helpers
# ---------------------------------------------------------------------------

def fetch_release(tag: str | None) -> dict:
    url = f"{GITHUB_API}/latest" if tag is None else f"{GITHUB_API}/tags/{tag}"
    print(f"  Fetching release info from GitHub ({tag or 'latest'})...")
    r = requests.get(url, timeout=15)
    if r.status_code == 404:
        sys.exit(f"ERROR: Release '{tag}' not found on GitHub.")
    r.raise_for_status()
    return r.json()


def pick_asset(release: dict) -> tuple[str, str]:
    """Return (download_url, filename) for the best asset in a release."""
    assets = release.get("assets", [])
    tag = release.get("tag_name", "")

    # Prefer server zip, fall back to mrpack
    for priority in (".zip", ".mrpack"):
        for asset in assets:
            if asset["name"].endswith(priority):
                return asset["browser_download_url"], asset["name"]

    sys.exit(
        f"ERROR: No .zip or .mrpack asset found in release {tag}.\n"
        f"Available assets: {[a['name'] for a in assets]}"
    )


def download_asset(url: str, dest: Path) -> None:
    print(f"  Downloading {dest.name}...")
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=65536):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 // total
                    print(f"\r    {pct}% ({downloaded // 1024} / {total // 1024} KB)", end="", flush=True)
        print()


# ---------------------------------------------------------------------------
# Zip inspection
# ---------------------------------------------------------------------------

def detect_zip_type(zip_path: Path) -> str:
    """Return 'server' or 'mrpack'."""
    if zip_path.suffix == ".mrpack":
        return "mrpack"
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
    if any(n == "modrinth.index.json" or n.startswith("overrides/") for n in names):
        return "mrpack"
    return "server"


def read_pack_version_from_zip(zip_path: Path, zip_type: str) -> str | None:
    """Try to extract pack version from the zip."""
    try:
        with zipfile.ZipFile(zip_path) as zf:
            if zip_type == "mrpack" and "modrinth.index.json" in zf.namelist():
                data = json.loads(zf.read("modrinth.index.json"))
                return data.get("versionId")
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Backup
# ---------------------------------------------------------------------------

def backup_targets(target_dir: Path, items: list[str], dry_run: bool) -> Path | None:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = target_dir / f"_update_backup_{ts}"
    existing = [i for i in items if (target_dir / i).exists()]
    if not existing:
        return None
    print(f"\n  Backing up {len(existing)} item(s) to {backup_dir.name}/")
    if dry_run:
        for item in existing:
            print(f"    [dry-run] would backup: {item}")
        return backup_dir
    backup_dir.mkdir(parents=True, exist_ok=True)
    for item in existing:
        src = target_dir / item
        dst = backup_dir / item
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        print(f"    backed up: {item}")
    return backup_dir


# ---------------------------------------------------------------------------
# Apply update — server pack
# ---------------------------------------------------------------------------

def apply_server_update(zip_path: Path, target_dir: Path, dry_run: bool, no_backup: bool) -> None:
    print(f"\n  Pack type : server")
    print(f"  Target    : {target_dir}")

    all_items = SERVER_UPDATE_DIRS + SERVER_UPDATE_FILES

    if not no_backup:
        backup_targets(target_dir, all_items, dry_run)

    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        top_dirs = {n.split("/")[0] for n in names if "/" in n}
        root_files = {n for n in names if "/" not in n and n}

        # Replace directories
        for d in SERVER_UPDATE_DIRS:
            entries = [n for n in names if n.startswith(f"{d}/")]
            if not entries:
                print(f"  (skipping {d}/ — not in zip)")
                continue

            dest_dir = target_dir / d
            print(f"  Updating {d}/ ({len(entries)} files)...")
            if dry_run:
                continue

            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            dest_dir.mkdir(parents=True, exist_ok=True)

            for entry in entries:
                rel = Path(entry)
                out = target_dir / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                if not entry.endswith("/"):
                    out.write_bytes(zf.read(entry))

        # Replace root-level files
        for fname in SERVER_UPDATE_FILES:
            if fname in root_files:
                print(f"  Updating {fname}...")
                if not dry_run:
                    out = target_dir / fname
                    out.write_bytes(zf.read(fname))


# ---------------------------------------------------------------------------
# Apply update — mrpack
# ---------------------------------------------------------------------------

def apply_mrpack_update(zip_path: Path, target_dir: Path, dry_run: bool, no_backup: bool) -> None:
    print(f"\n  Pack type : mrpack (overrides only)")
    print(f"  Target    : {target_dir}")
    print("  Note      : mod JARs listed in modrinth.index.json must be managed by your launcher.")

    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()

    # Collect overrides subdirs that exist in the zip
    override_entries: dict[str, list[str]] = {}
    for name in names:
        if name.startswith("overrides/") and not name.endswith("/"):
            # e.g. overrides/config/foo.json  -> key "config"
            rest = name[len("overrides/"):]
            top = rest.split("/")[0]
            if top in MRPACK_OVERRIDES:
                override_entries.setdefault(top, []).append(name)

    if not override_entries:
        print("  No override directories found in mrpack.")
        return

    backup_items = list(override_entries.keys())
    if not no_backup:
        backup_targets(target_dir, backup_items, dry_run)

    with zipfile.ZipFile(zip_path) as zf:
        for subdir, entries in override_entries.items():
            dest_dir = target_dir / subdir
            print(f"  Updating {subdir}/ ({len(entries)} files)...")
            if dry_run:
                continue

            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            dest_dir.mkdir(parents=True, exist_ok=True)

            for entry in entries:
                rel = Path(entry[len("overrides/"):])
                out = target_dir / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(zf.read(entry))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Flesh & Steel — Modpack Update Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--zip", metavar="PATH", help="Local .zip or .mrpack file")
    source.add_argument(
        "--github",
        nargs="?",
        const=None,
        default=argparse.SUPPRESS,
        metavar="TAG",
        help="Download from GitHub releases (omit TAG for latest)",
    )
    parser.add_argument(
        "--target",
        metavar="DIR",
        default=".",
        help="Directory to update (default: current directory)",
    )
    parser.add_argument("--no-backup", action="store_true", help="Skip backup step")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change, do nothing")
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    if not target_dir.exists():
        sys.exit(f"ERROR: Target directory does not exist: {target_dir}")

    print("Flesh & Steel — Update Script")
    print("=" * 50)
    if args.dry_run:
        print("  [DRY RUN — no files will be modified]")

    # Resolve zip path
    if hasattr(args, "github"):
        tag = args.github  # None means latest
        release = fetch_release(tag)
        release_tag = release.get("tag_name", "unknown")
        release_name = release.get("name", release_tag)
        print(f"\n  Release   : {release_name} ({release_tag})")
        dl_url, asset_name = pick_asset(release)

        tmp_dir = Path(tempfile.mkdtemp())
        try:
            zip_path = tmp_dir / asset_name
            download_asset(dl_url, zip_path)
            _run_update(zip_path, target_dir, args.dry_run, args.no_backup)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
    else:
        zip_path = Path(args.zip).resolve()
        if not zip_path.exists():
            sys.exit(f"ERROR: File not found: {zip_path}")
        print(f"\n  Source    : {zip_path.name}")
        _run_update(zip_path, target_dir, args.dry_run, args.no_backup)

    print(f"\n{'=' * 50}")
    if args.dry_run:
        print("Dry run complete. No files were modified.")
    else:
        print("Update complete!")
    print("=" * 50)


def _run_update(zip_path: Path, target_dir: Path, dry_run: bool, no_backup: bool) -> None:
    zip_type = detect_zip_type(zip_path)
    version = read_pack_version_from_zip(zip_path, zip_type)
    if version:
        print(f"  Version   : {version}")

    if zip_type == "server":
        apply_server_update(zip_path, target_dir, dry_run, no_backup)
    else:
        apply_mrpack_update(zip_path, target_dir, dry_run, no_backup)


if __name__ == "__main__":
    main()