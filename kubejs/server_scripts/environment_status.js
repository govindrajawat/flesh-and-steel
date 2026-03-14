// Server-side environmental debuffs based on temperature and radiation
// - Cold biomes apply Mining Fatigue and increase thirst pressure
// - High radiation applies Poison

LevelEvents.tick(event => {
    // Run once per second
    if (event.level.time % 20 != 0) return;

    event.level.players.forEach(player => {
        if (!player) return;

        let pos = player.blockPosition();
        const biome = event.level.getBiome(pos);
        const temp = biome.getTemperature(pos);

        // --- UNIVERSAL 10-POINT SCALING ---
        let tScale = 5;
        if (temp <= -0.2) tScale = 0; 
        else if (temp < 0) tScale = 1;
        else if (temp <= 0.2) tScale = 2;
        else if (temp <= 0.4) tScale = 4;
        else if (temp <= 0.7) tScale = 6;
        else if (temp <= 0.9) tScale = 8;
        else if (temp <= 1.2) tScale = 9;
        else tScale = 10;

        const rad = player.getPotionEffect('radiach:radiation');
        let rScale = rad ? (rad.amplifier + 1) * 2 : 0; 
        // Note: rScale is calculated from potion amp to stay synced with radiation_control.js

        // --- HAZARD MATRIX & SYNERGY ---

        // 🌟 THE GOOD ZONES (Optimal Habitats)
        // If Temp is Normal (5-7) AND Rad is Low (0-3)
        if (tScale >= 5 && tScale <= 7 && rScale <= 3) {
            // "Abundance" Buffs
            player.addPotionEffect('minecraft:regeneration', 100, 0, false, false);
            player.addPotionEffect('minecraft:haste', 100, 0, false, false);
            if (rScale == 0) { // Truly Pristine
                player.addPotionEffect('minecraft:saturation', 100, 0, false, false);
            }
            // Clear all environmental badness
            player.removePotionEffect('minecraft:poison');
            player.removePotionEffect('minecraft:slowness');
            player.removePotionEffect('minecraft:mining_fatigue');
            player.removePotionEffect('minecraft:darkness');
            player.removePotionEffect('minecraft:wither');
        }

        // 🟢 ZONE A: VERY COLD (0-1) - Frostbite & Lethargy
        else if (tScale <= 1) {
            player.addPotionEffect('minecraft:slowness', 60, 1, false, false);
            player.addPotionEffect('minecraft:mining_fatigue', 60, 1, false, false);
            if (rScale >= 7) { // Arctic Madness
                player.addPotionEffect('minecraft:darkness', 60, 0, false, false);
                player.addPotionEffect('minecraft:wither', 60, 0, false, false);
            }
        }

        // ❄️ ZONE B: COLD (2-4) - Stiffness
        else if (tScale <= 4) {
            player.addPotionEffect('minecraft:mining_fatigue', 60, 0, false, false);
            if (rScale >= 7) { 
                player.addPotionEffect('minecraft:weakness', 60, 0, false, false);
                player.addPotionEffect('minecraft:hunger', 60, 0, false, false);
            }
        }

        // 🟠 ZONE C: HOT (8-9) - Fever & Exhaustion
        else if (tScale >= 8 && tScale <= 9) {
            player.addPotionEffect('minecraft:hunger', 60, 0, false, false);
            if (rScale >= 4) { 
                player.addPotionEffect('minecraft:poison', 60, 0, false, false);
                player.addPotionEffect('minecraft:weakness', 60, 0, false, false);
            }
        }

        // 🔥 ZONE D: VERY HOT (10) - Melting Point
        else if (tScale == 10) {
            player.addPotionEffect('minecraft:mining_fatigue', 60, 1, false, false);
            player.addPotionEffect('minecraft:slowness', 60, 0, false, false);
            if (rScale >= 7) { // Nuclear Incineration
                player.addPotionEffect('minecraft:wither', 60, 1, false, false);
                player.addPotionEffect('minecraft:blindness', 60, 0, false, false);
            } else {
                player.addPotionEffect('minecraft:poison', 60, 1, false, false);
            }
        }

        // ☢️ ZONE E: TOXIC NORMAL (Temp 5-7 + High Rad)
        else if (rScale >= 9) {
            player.addPotionEffect('minecraft:poison', 60, 1, false, false);
            player.addPotionEffect('minecraft:nausea', 120, 0, false, false);
            player.addPotionEffect('minecraft:glowing', 120, 0, false, false); // Radioactive Glow
        }
    });
});
