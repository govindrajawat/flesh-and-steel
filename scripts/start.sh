#!/usr/bin/env bash
# ============================================================
# Flesh & Steel - Server Start Script (Forge)
# Adjust -Xmx and -Xms to fit your server's RAM
# ============================================================
set -euo pipefail

SERVER_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SERVER_DIR"

# ---- Memory Configuration ----
# Adjust these values based on your server's available RAM.
# Recommended: 6G minimum, 8G+ for best experience with this modpack.
MIN_RAM="4G"
MAX_RAM="8G"

# ---- JVM Flags (Aikar's flags, tuned for modded MC) ----
JVM_FLAGS=(
    -Xms${MIN_RAM}
    -Xmx${MAX_RAM}
    -XX:+UseG1GC
    -XX:+ParallelRefProcEnabled
    -XX:MaxGCPauseMillis=200
    -XX:+UnlockExperimentalVMOptions
    -XX:+DisableExplicitGC
    -XX:+AlwaysPreTouch
    -XX:G1NewSizePercent=30
    -XX:G1MaxNewSizePercent=40
    -XX:G1HeapRegionSize=8M
    -XX:G1ReservePercent=20
    -XX:G1HeapWastePercent=5
    -XX:G1MixedGCCountTarget=4
    -XX:InitiatingHeapOccupancyPercent=15
    -XX:G1MixedGCLiveThresholdPercent=90
    -XX:G1RSetUpdatingPauseTimePercent=5
    -XX:SurvivorRatio=32
    -XX:+PerfDisableSharedMem
    -XX:MaxTenuringThreshold=1
    -Dusing.aikars.flags=https://mcflags.emc.gs
    -Daikars.new.flags=true
)

# ---- Pre-flight Checks ----
# Forge generates a run.sh / run.bat after installation; fall back to the
# universal server jar if run.sh is not yet present.
if [ ! -f "run.sh" ] && ! ls forge-*-server.jar &>/dev/null 2>&1; then
    echo "❌ Forge server not found! Run ./install.sh first."
    exit 1
fi

if [ ! -f "eula.txt" ] || ! grep -q "eula=true" eula.txt; then
    echo "❌ EULA not accepted. Run ./install.sh first."
    exit 1
fi

echo "============================================"
echo " ⚙ Flesh & Steel — Starting Forge Server"
echo "   RAM: ${MIN_RAM} - ${MAX_RAM}"
echo "============================================"

# Forge 1.20.1 installs a run.sh wrapper — use it if present.
# JVM flags must be passed via USER_JVM_ARGS, not as arguments to run.sh.
if [ -f "run.sh" ]; then
    export USER_JVM_ARGS="${JVM_FLAGS[*]}"
    exec bash run.sh
else
    # Fallback: find the server jar directly
    SERVER_JAR=$(ls forge-*-server.jar 2>/dev/null | head -n1)
    exec java "${JVM_FLAGS[@]}" -jar "$SERVER_JAR" nogui
fi
