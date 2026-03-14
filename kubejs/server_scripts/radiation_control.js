// Radiation control for Flesh & Steel
// Separates Temperature and Radiation into independent mechanics.
// Radiation is now based on Biome Tags and refined "Toxic" biome IDs.

LevelEvents.tick(event => {
    // Standardizing floor/ceil counts to ensure consistency
    if (event.level.clientSide || event.level.time % 20 != 0) return;

    event.level.players.forEach(player => {
        if (!player) return;

        let pos = player.blockPosition();
        let biome = event.level.getBiome(pos);
        let biomeId = biome.id.toString();
        let temp = biome.getTemperature(pos);

        // Safe Effect Lookup
        const effectMap = player.activeEffects;
        let radiationInst = null;
        effectMap.forEach((instance, effect) => {
            if (effect.registryName && effect.registryName.toString() === 'radiach:radiation') {
                radiationInst = instance;
            }
        });

        // --- ENHANCED RADIATION LOGIC ---
        // We categorize biomes into Rad Levels: 0 (None), 1 (Low), 2 (Medium), 3 (High)
        let naturalRadLevel = 0;

        // --- UNIVERSAL 10-POINT SCALING ---
        
        // 1. RADIATION SCALE (0-10)
        let naturalRadScale = 0;
        if (biomeId.contains('atomic') || biomeId.contains('nuclear') || biomeId.contains('withered') || biomeId.contains('null')) {
            naturalRadScale = 10;
        } else if (biomeId.contains('corrupted') || biomeId.contains('wasteland') || biomeId.contains('volcanic')) {
            naturalRadScale = 8;
        } else if (biomeId.contains('dead') || biomeId.contains('abandoned') || biomeId.contains('quagmire')) {
            naturalRadScale = 7;
        } else if (biomeId.contains('desert') || biomeId.contains('badlands') || biomeId.contains('dunes')) {
            naturalRadScale = 6;
        } else if (biomeId.contains('savanna') || biomeId.contains('mesa') || biomeId.contains('scrubland')) {
            naturalRadScale = 4;
        } else if (biomeId.contains('swamp') || biomeId.contains('bog') || biomeId.contains('fen') || biomeId.contains('marsh')) {
            naturalRadScale = 3;
        } else if (biomeId.contains('jungle') || biomeId.contains('mangrove')) {
            naturalRadScale = 1;
        }

        // 2. TEMPERATURE SCALE (0-10) mapping
        else tempScale = 10; // Very Hot

        // Store for client-side use (fog/HUD/etc)
        player.persistentData.putInt('tempScale', tempScale);
        player.persistentData.putInt('radScale', naturalRadScale);

        // --- CLEARING LOGIC ---
        // Biomes with Normal Temp (5-7) and Low Rad (0) are "Sanitized"
        if (naturalRadScale == 0 && tempScale >= 5 && tempScale <= 7) {
            player.removePotionEffect('radiach:radiation');
            player.removePotionEffect('minecraft:poison');
        } 
        // Otherwise apply radiation if present
        else if (naturalRadScale > 0) {
            // Mapping 0-10 to potion amplifier (roughly scale/2 for intensity)
            // 7-8 is High Rad (amp 2-3), 9-10 is Very High (amp 4-5)
            let amp = Math.floor(naturalRadScale / 2);
            player.addPotionEffect('radiach:radiation', 60, amp, false, false);
        }
    });
});
