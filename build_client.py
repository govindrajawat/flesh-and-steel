#!/usr/bin/env python3
"""
Flesh & Steel — Client Pack Build Script (Forge)
Reads mod definitions from pack-config/mods.json, downloads them into
mods/common/ and mods/client/, then assembles:
  - build/client-pack/flesh-and-steel.mrpack  (Modrinth client pack)
Usage:
    python build_client.py
"""

import build_utils as utils


def main():
    print("🛠️  Flesh & Steel — Client Pack Build System (Forge)")
    print("=" * 50)

    mods_dir = utils.PROJECT_ROOT / "mods"
    build_dir = utils.PROJECT_ROOT / "build"
    client_pack_dir = build_dir / "client-pack"

    config = utils.load_config()
    sides = ["common", "client"]
    for side in sides:
        (mods_dir / side).mkdir(parents=True, exist_ok=True)
    client_pack_dir.mkdir(parents=True, exist_ok=True)

    # Resolve mods and build the client pack
    mrpack_files, log_lines = utils.resolve_mods(config, sides, mods_dir)

    # Build .mrpack
    print("\n📦 Building client .mrpack...")
    mrpack_path = client_pack_dir / "flesh-and-steel.mrpack"
    utils.build_mrpack(config, mrpack_files, utils.PROJECT_ROOT, mrpack_path)
    print(f"  ✅ {mrpack_path}")

    # Write build log
    log_path = build_dir / "install-log-client.txt"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    print(f"\n{'=' * 50}")
    print("✅ Client build complete!")
    print(f"   Client pack: {mrpack_path}")
    print(f"   Build log:   {log_path}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()