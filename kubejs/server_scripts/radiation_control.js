// Radiation control for Flesh & Steel
// Makes radiation biome- and temperature-dependent instead of feeling global.

LevelEvents.tick(event => {
    // Run only on server
    if (event.level.isClientSide()) return;

    const isSecond = event.level.time % 20 === 0;

    event.level.players.forEach(player => {
        if (!player) return;

        // Sample biome and temperature at player position
        let { x, y, z } = player;
        let biome = event.level.getBiome(x, y, z).value();
        let temp = biome.getTemperature();

        // DESIGN:
        // - Safe Zones (temp < 0.85): AGGRESSIVELY clear radiation and associated debuffs.
        // - Harsh Zones (temp >= 0.85): Allow radiation (Hot biomes like Deserts/Savannas).

        // Clear radiation in safe/normal zones (Temperate, Cold, Mild)
        // Running this EVERY tick ensures that even if the mod re-applies it, we kill it immediately.
        if (temp < 0.85) {
            player.removePotionEffect('radiach:radiation');
            player.removePotionEffect('minecraft:poison');
            player.removePotionEffect('minecraft:slowness');
            return;
        }

        // Further logic runs only once per second for performance
        if (!isSecond) return;

        // If we are in a harsh zone, check if player has radiation to manage it
        let radiation = player.getPotionEffect('radiach:radiation');
        if (!radiation) return;

        // Keep radiation in Hot zones, but clamp it if it's not extreme (0.85 to 1.0)
        // This prevents immediate death while still giving a sense of danger.
        if (temp < 1.0 && radiation.amplifier > 0) {
            player.potionEffects.add('radiach:radiation', radiation.duration, 0, radiation.ambient, radiation.visible);
        }
    });
});

