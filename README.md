# Flesh & Steel — Biomechanical Tech Modpack

Minecraft 1.20.1 · Fabric

## Project Structure

```
flesh-and-steel/
│
├── mods/
│   ├── common/          # Mods for both client & server (downloaded by build script)
│   ├── client/          # Client-only mods (rendering, UI, audio)
│   └── server/          # Server-only mods (if any)
│
├── config/              # Game config overrides (toml, json5, etc.)
│
├── kubejs/
│   ├── server_scripts/  # KubeJS server-side scripts (recipes, loot, etc.)
│   └── startup_scripts/ # KubeJS startup scripts (worldgen, etc.)
│
├── global_data_packs/   # GlobalPacks data packs (quests, etc.)
│
├── resourcepacks/       # Resource packs (if any)
│
├── scripts/             # Server deployment scripts
│   ├── install.sh       # Fabric server installer
│   ├── start.sh         # Server start script (Aikar's flags)
│   └── README.md        # Server setup notes
│
├── pack-config/
│   └── mods.json        # Single source of truth for all mods & versions
│
├── build/               # Build outputs (gitignored)
│   ├── client-pack/     # → flesh-and-steel.mrpack
│   └── server-pack/     # → ready-to-deploy server directory
│
├── build_pack.py        # Main build script (downloads mods, builds packs)
├── patch_neepmeat.py    # Patches neepmeat JAR (flywheel mod ID conflict)
├── requirements.txt     # Python dependencies
└── .gitignore
```

## How to Build

### Prerequisites
```bash
pip install -r requirements.txt
```

### 1. Patch Neepmeat (first time only)
```bash
python patch_neepmeat.py
```
This downloads and patches the neepmeat mod, saving it to `mods/common/`.

### 2. Build the Modpack
```bash
python build_pack.py
```
This will:
- Download all mods from Modrinth into `mods/common/`, `mods/client/`, `mods/server/`
- Build `build/client-pack/flesh-and-steel.mrpack` (import in Prism/Modrinth App)
- Build `build/server-pack/` (complete server directory)

### 3. Deploy the Server
```bash
cd build/server-pack/
./install.sh    # Downloads Fabric launcher, accepts EULA
./start.sh      # Starts the server
```

## Mod Categorization

All mod definitions live in `pack-config/mods.json`:

- **common**: Installed on both client and server (~150 mods)
- **client**: Client-only mods — rendering, shaders, UI, audio (~22 mods)
- **server**: Server-only mods (none currently, but ready for future additions)

Version pins for Create ecosystem compatibility are also defined in `mods.json`.

