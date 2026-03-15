// Server-side environmental status & buffs for Flesh & Steel
// Updated for Radioactive mod compatibility

LevelEvents.tick(event => {
    if (event.level.time % 20 != 0) return;

    event.level.players.forEach(player => {
        if (!player) return;

        // Retrieve current scales from persistentData (set in radiation_control.js)
        const tScale = player.persistentData.getInt('tempScale') || 5;
        const rScale = player.persistentData.getInt('radScale') || 0;

        // --- THE VITALITY SYSTEM ---
        // Biomes with Normal Temp (5-7) and Low Rad (0-3) are "Safe Havens"
        if (tScale >= 5 && tScale <= 7 && rScale <= 3) {
            player.potionEffects.add('minecraft:regeneration', 100, 0, false, false);
            player.potionEffects.add('minecraft:haste', 100, 0, false, false);
            
            if (rScale == 0) { // Pristine environment
                player.potionEffects.add('minecraft:saturation', 100, 0, false, false);
            }

            // Clear environmental debuffs
            player.removeEffect('minecraft:slowness');
            player.removeEffect('minecraft:mining_fatigue');
            player.removeEffect('minecraft:weakness');
        }

        // --- ENVIRONMENTAL DEBUFFS ---
        
        // Lethal Cold (Zone A)
        else if (tScale <= 1) {
            player.potionEffects.add('minecraft:slowness', 80, 1, false, false);
            player.potionEffects.add('minecraft:mining_fatigue', 80, 1, false, false);
        }

        // Severe Heat (Zone D)
        else if (tScale >= 9) {
            player.potionEffects.add('minecraft:hunger', 80, 0, false, false);
            player.potionEffects.add('minecraft:weakness', 80, 0, false, false);
        }

        // Extreme Radiation (High Rad Scale)
        if (rScale >= 7) {
            player.potionEffects.add('minecraft:poison', 80, 0, false, false);
            player.potionEffects.add('minecraft:nausea', 160, 0, false, false);
        }
    });
});
