#!/usr/bin/env python3
"""
Flesh & Steel — Server Pack Build Script (Forge)
Reads mod definitions from pack-config/mods.json, downloads them into
mods/common/ and mods/server/, then assembles:
  - build/server-pack/                         (ready-to-deploy server directory)
  - build/flesh-and-steel-server.zip           (zipped server pack)
Usage:
    python build_server.py
"""

import build_utils as utils


def main():
    print("🛠️  Flesh & Steel — Server Pack Build System (Forge)")
    print("=" * 50)

    mods_dir = utils.PROJECT_ROOT / "mods"
    build_dir = utils.PROJECT_ROOT / "build"
    server_pack_dir = build_dir / "server-pack"

    config = utils.load_config()
    sides = ["common", "server"]
    for side in sides:
        (mods_dir / side).mkdir(parents=True, exist_ok=True)
    server_pack_dir.mkdir(parents=True, exist_ok=True)

    # Resolve mods and build the server pack
    _, log_lines = utils.resolve_mods(config, sides, mods_dir)

    # Build server pack
    print("\n📦 Building server pack...")
    server_zip_path = utils.build_server_pack(config, utils.PROJECT_ROOT, server_pack_dir)
    print(f"  ✅ {server_zip_path}")

    # Write build log
    log_path = build_dir / "server-install-log.txt"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    print(f"\n{'=' * 50}")
    print("✅ Server build complete!")
    print(f"   Server pack: {server_zip_path}")
    print(f"   Build log:   {log_path}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()