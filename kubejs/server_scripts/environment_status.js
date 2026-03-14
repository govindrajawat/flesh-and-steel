// Server-side environmental debuffs based on temperature and radiation
// - Cold biomes apply Mining Fatigue and increase thirst pressure
// - High radiation applies Poison

LevelEvents.tick(event => {
    // Run once per second
    if (event.level.time % 20 != 0) return;

    event.level.players.forEach(player => {
        if (!player) return;

        const { x, y, z } = player;
        const biome = event.level.getBiome(x, y, z).value();
        const temp = biome.getTemperature();

        // Temperature band based on biome temperature
        let tempBand = 'Mild';
        if (temp <= 0.15) tempBand = 'Very Cold';
        else if (temp <= 0.4) tempBand = 'Cold';
        else if (temp <= 0.8) tempBand = 'Warm';
        else tempBand = 'Hot';

        // Radiation band from Radiach potion effect
        const rad = player.getPotionEffect('radiach:radiation');
        let radAmp = rad ? rad.amplifier : -1;

        // --- COLD EFFECTS: Mining Fatigue (soft in Cold, stronger in Very Cold) ---
        if (tempBand === 'Cold' || tempBand === 'Very Cold') {
            const mfAmp = tempBand === 'Very Cold' ? 1 : 0;
            // 3 seconds, refreshed each tick
            player.addPotionEffect('minecraft:mining_fatigue', 60, mfAmp, false, false);
        }

        // --- RADIATION EFFECTS: Poison scales with radiation amplifier ---
        // Only applies in Harsh zones (Hot biomes) where radiation is intended to be active.
        if (radAmp >= 0 && temp >= 0.85) {
            let poisonAmp = -1;
            // Very low radiation: no poison, just audio/visual cues
            if (radAmp === 1) {
                poisonAmp = 0; // light poison
            } else if (radAmp >= 2) {
                poisonAmp = 1; // stronger poison at high radiation
            }

            if (poisonAmp >= 0) {
                player.addPotionEffect('minecraft:poison', 60, poisonAmp, false, false);
            }
        }
    });
});
