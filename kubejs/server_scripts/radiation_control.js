// Radiation control for Flesh & Steel
// Makes radiation biome- and temperature-dependent instead of feeling global.

LevelEvents.tick(event => {
    // Run only on server and not every tick for performance
    if (event.level.isClientSide()) return;
    if (event.level.time % 20 !== 0) return; // once per second

    event.level.players.forEach(player => {
        if (!player) return;

        let radiation = player.getPotionEffect('radiach:radiation');
        if (!radiation) return;

        // Sample biome and temperature at player position
        let { x, y, z } = player;
        let biome = event.level.getBiome(x, y, z).value();
        let temp = biome.getTemperature();

        // DESIGN:
        // - Very cold biomes (temp <= 0.2): treated as low-radiation safe zones -> clear effect.
        // - Mild biomes (0.2 < temp <= 0.6): allow only low radiation (amplifier <= 1).
        // - Hot / harsh biomes (temp > 0.6): keep full Radiach behaviour.

        // Safe / low-radiation zones
        if (temp <= 0.2) {
            player.removePotionEffect('radiach:radiation');
            return;
        }

        // Clamp radiation strength in milder climates
        if (temp <= 0.6 && radiation.amplifier > 1) {
            player.addPotionEffect(
                'radiach:radiation',
                radiation.duration,
                1,
                radiation.ambient,
                radiation.visible
            );
        }
    });
});

