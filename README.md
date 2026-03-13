# Flesh & Steel — Biomechanical Tech Modpack

Minecraft 1.20.1 · Forge 47.4.10

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
├── local_mods/           # Manually-provided mod jars (bundled into builds)
│   ├── common/           # Included in both client and server packs
│   ├── client/           # Client-only local jars
│   └── server/           # Server-only local jars
│
├── scripts/             # Server deployment scripts
│   ├── install.sh       # Forge server installer
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
├── requirements.txt     # Python dependencies
└── .gitignore
```

## How to Build

### Prerequisites
```bash
pip install -r requirements.txt
```

### 1. Build the Modpack
```bash
python build_pack.py
```
This will:
- Download all mods from Modrinth into `mods/common/`, `mods/client/`, `mods/server/`
- Bundle any jars present in `local_mods/` into the client `.mrpack` and server `.zip`
- Build `build/client-pack/flesh-and-steel.mrpack` (import in Prism/Modrinth App)
- Build `build/server-pack/` (complete server directory)

### 2. Deploy the Server
```bash
cd build/server-pack/
./install.sh    # Downloads Forge installer, runs it, accepts EULA
./start.sh      # Starts the server
```

## Mod Categorization

All mod definitions live in `pack-config/mods.json`:

- **common**: Installed on both client and server (~120 mods)
- **client**: Client-only mods — shaders, UI, audio (~17 mods)
- **server**: Server-only mods (none currently, but ready for future additions)

Version pins for Create ecosystem compatibility are also defined in `mods.json`.

## Fabric → Forge Migration Notes

Key substitutions made when converting from Fabric:

| Removed (Fabric-only) | Added (Forge equivalent) |
|---|---|
| Fabric API | Forge (built-in) |
| Fabric Language Kotlin | Kotlin for Forge |
| Trinkets / Accessories | Curios API |
| Lithium | Embeddium (includes Rubidium/Sodium optimizations) |
| Sodium (client) | Embeddium (common) |
| Iris (client) | Oculus (client) |
| Mod Menu (client) | Catalogue (client) |
| Dynamic FPS | FPS Reducer |
| Presence Footsteps | Dynamic Surroundings |
| Zenith (Apotheosis Fabric) | Apotheosis |
| Farmer's Delight Refabricated | Farmer's Delight (original) |
| Universal Graves | Graves |
| Create Enchantment Industry (legacy slug) | create-enchantment-industry |
| Repurposed Structures Fabric | repurposed-structures |

Fabric-only mods with no Forge equivalent that were **removed**:
Modern Industrialization, Chest Cavity, Dungeonz, Integrated Stronghold/API,
Villagers & Pillages, Custom Villager Trades, Rot N' Putrid, Forsaken Corpses,
Nature's Spirit, BioButcher's Delight, Dahmer's Delight, Spectrum, Somatogenesis,
Simple Quests, Amendments, Styled Chat, Krypton, Noisium, C2ME, ServerCore,
Athena, Cardinal Components API, Porting Lib, FakerLib, Zenith Attributes,
Accessories (replaced by Curios), owo-lib, Revelationary, Impersonate,
Attribute Helpers, EnvironmentZ, AutoTag, MidnightLib, Library Ferret, Kambrik,
Obscure API, Indium.
