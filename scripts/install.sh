#!/usr/bin/env bash
# ============================================================
# Flesh & Steel - Fabric Server Installer
# Minecraft 1.20.1 | Fabric Loader 0.18.4
# ============================================================
set -euo pipefail

MINECRAFT_VERSION="1.20.1"
FABRIC_LOADER_VERSION="0.18.4"
FABRIC_INSTALLER_VERSION="1.0.1"
FABRIC_INSTALLER_URL="https://meta.fabricmc.net/v2/versions/loader/${MINECRAFT_VERSION}/${FABRIC_LOADER_VERSION}/${FABRIC_INSTALLER_VERSION}/server/jar"

SERVER_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SERVER_DIR"

echo "============================================"
echo " Flesh & Steel — Fabric Server Installer"
echo " Minecraft ${MINECRAFT_VERSION}"
echo " Fabric Loader ${FABRIC_LOADER_VERSION}"
echo "============================================"
echo ""

# ------------------------------------
# 1. Check Java
# ------------------------------------
if ! command -v java &>/dev/null; then
    echo "❌ Java not found. Please install Java 17+ and try again."
    echo "   Ubuntu/Debian: sudo apt install openjdk-17-jre-headless"
    echo "   Fedora:        sudo dnf install java-17-openjdk-headless"
    echo "   Arch:          sudo pacman -S jre-openjdk-headless"
    exit 1
fi

JAVA_VER=$(java -version 2>&1 | head -n1 | awk -F'"' '{print $2}' | cut -d. -f1)
if [ "$JAVA_VER" -lt 17 ] 2>/dev/null; then
    echo "⚠️  Java 17+ is required. Detected version: $JAVA_VER"
    echo "   Please update Java and try again."
    exit 1
fi
echo "✅ Java $JAVA_VER detected"

# ------------------------------------
# 2. Download Fabric Server Launcher
# ------------------------------------
if [ ! -f "fabric-server-launch.jar" ]; then
    echo "📥 Downloading Fabric server launcher..."
    curl -sSL -o fabric-server-launch.jar "$FABRIC_INSTALLER_URL"
    echo "✅ Fabric server launcher downloaded"
else
    echo "✅ Fabric server launcher already exists"
fi

# ------------------------------------
# 3. Accept EULA
# ------------------------------------
if [ ! -f "eula.txt" ] || ! grep -q "eula=true" eula.txt 2>/dev/null; then
    echo ""
    echo "📜 Minecraft EULA: https://aka.ms/MinecraftEULA"
    read -rp "Do you accept the Minecraft EULA? (y/N): " accept
    if [[ "$accept" =~ ^[Yy]$ ]]; then
        echo "eula=true" > eula.txt
        echo "✅ EULA accepted"
    else
        echo "❌ You must accept the EULA to run a Minecraft server."
        exit 1
    fi
fi

# ------------------------------------
# 4. Generate default server.properties if missing
# ------------------------------------
if [ ! -f "server.properties" ]; then
    echo "📝 Generating server.properties with Flesh & Steel defaults..."
    cat > server.properties << 'PROPS'
# Flesh & Steel Server Configuration
# Minecraft 1.20.1 Fabric

# NETWORK
server-port=25565
server-ip=
max-players=20
network-compression-threshold=256
rate-limit=0

# WORLD
level-name=world
level-seed=
level-type=minecraft\:normal
generator-settings={}
max-world-size=29999984
view-distance=12
simulation-distance=10
generate-structures=true
allow-nether=true

# GAMEPLAY
gamemode=survival
difficulty=hard
hardcore=false
pvp=true
force-gamemode=false
spawn-protection=16
spawn-npcs=true
spawn-animals=true
spawn-monsters=true
allow-flight=false
max-tick-time=60000
player-idle-timeout=0

# SERVER
motd=\u00a76\u00a7l⚙ Flesh & Steel \u00a7r\u00a77— Biomechanical Tech
online-mode=false
white-list=false
enforce-whitelist=false
enable-command-block=true
op-permission-level=4
function-permission-level=2
enable-status=true
enable-query=false
enable-rcon=false
rcon.port=25575
rcon.password=

# RESOURCE PACK (leave blank or set your own)
resource-pack=
resource-pack-sha1=
require-resource-pack=false
resource-pack-prompt=

# PERFORMANCE
sync-chunk-writes=true
entity-broadcast-range-percentage=100
PROPS
    echo "✅ server.properties created"
else
    echo "✅ server.properties already exists"
fi

# ------------------------------------
# 5. Copy mods (symlink or copy from server_mods)
# ------------------------------------
echo ""
echo "📦 Checking mods directory..."
MOD_COUNT=$(find mods/ -name "*.jar" 2>/dev/null | wc -l)
if [ "$MOD_COUNT" -gt 0 ]; then
    echo "✅ Found $MOD_COUNT mods in mods/"
else
    echo "⚠️  No mods found in mods/ directory!"
    echo "   Run the populate_server.py script to copy server-side mods."
fi

echo ""
echo "============================================"
echo " ✅ Installation complete!"
echo ""
echo " To start the server, run:"
echo "   ./start.sh"
echo ""
echo " To configure memory, edit start.sh"
echo "============================================"
