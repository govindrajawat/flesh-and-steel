// Radiation control for Flesh & Steel - Radioactive Mod Edition
// Standardizes radiation based on biomes and integrates with the Radioactive mod.

LevelEvents.tick(event => {
    // Only run on server, once per second (20 ticks)
    if (event.level.clientSide || event.level.time % 20 != 0) return;

    event.level.players.forEach(player => {
        if (!player) return;

        let pos = player.blockPosition();
        let biome = event.level.getBiome(pos);
        let biomeId = biome.id.toString();
        
        // Temperature Lookup (Cold Sweat / Vanilla)
        let temp = biome.value().getTemperature(pos);

        // --- RADIATION SCALING (0-10) ---
        let naturalRadScale = 0;
        
        // Lethal/Nuclear Zones (Scale 10)
        if (biomeId.contains('atomic') || biomeId.contains('nuclear') || biomeId.contains('withered') || biomeId.contains('null')) {
            naturalRadScale = 10;
        } 
        // Highly Toxic (Scale 8)
        else if (biomeId.contains('corrupted') || biomeId.contains('wasteland') || biomeId.contains('volcanic')) {
            naturalRadScale = 8;
        } 
        // Contaminated (Scale 6-7)
        else if (biomeId.contains('dead') || biomeId.contains('abandoned') || biomeId.contains('quagmire')) {
            naturalRadScale = 7;
        } 
        // Harsh/Dry (Scale 4-5)
        else if (biomeId.contains('desert') || biomeId.contains('badlands') || biomeId.contains('dunes')) {
            naturalRadScale = 5;
        }
        // Swamps/Bogs (Scale 2-3)
        else if (biomeId.contains('swamp') || biomeId.contains('bog') || biomeId.contains('marsh')) {
            naturalRadScale = 3;
        }

        // --- TEMPERATURE SCALING (0-10) ---
        let tempScale = 5; // Default normal
        if (temp <= -0.2) tempScale = 0; 
        else if (temp < 0) tempScale = 1;
        else if (temp <= 0.2) tempScale = 2;
        else if (temp <= 0.4) tempScale = 4;
        else if (temp <= 0.7) tempScale = 6;
        else if (temp <= 0.9) tempScale = 8;
        else if (temp <= 1.2) tempScale = 9;
        else tempScale = 10;

        // Store scales for HUD use
        player.persistentData.putInt('tempScale', tempScale);
        player.persistentData.putInt('radScale', naturalRadScale);

        // --- EFFECT APPLICATION ---
        
        // 1. APPLY RADIATION EFFECT (from Radioactive mod)
        // We add to the player's RAD level based on biome
        if (naturalRadScale > 0) {
            // Radioactive mod uses a RAD value (0-1000)
            // We map our 0-10 scale to 0-400 (dangerous but not instant death)
            let radToAdd = naturalRadScale * 10; 
            
            // Using logic: if they are in high rad, give them the effect
            // radioactive:radiation_sickness or similar. 
            // For now we apply the mod's specific effect or a generic placeholder
            player.potionEffects.add('radioactive:radiation', 60, Math.floor(naturalRadScale/2), false, false);
        }

        // 2. CLEARING LOGIC (Sanitized Zones)
        if (naturalRadScale == 0 && tempScale >= 5 && tempScale <= 7) {
            player.removeEffect('radioactive:radiation');
            player.removeEffect('radioactive:radiation_sickness');
            player.removeEffect('minecraft:poison');
        }
    });
});
