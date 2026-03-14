// Radiation control for Flesh & Steel
// Makes radiation biome- and temperature-dependent instead of feeling global.

LevelEvents.tick(event => {
    if (event.level.isClientSide()) return;
    if (event.level.time % 20 !== 0) return; // once per second

    event.level.players.forEach(player => {
        if (!player) return;

        // Use activeEffects map to avoid a hard registry lookup crash
        // if the radiach mod effect isn't registered yet / not installed.
        const effectMap = player.activeEffects;
        let radiation = null;
        effectMap.forEach((instance, effect) => {
            if (effect.registryName && effect.registryName.toString() === 'radiach:radiation') {
                radiation = instance;
            }
        });
        if (!radiation) return;

        // Sample biome at player position
        let pos = player.blockPosition();
        let biomeId = event.level.getBiome(pos).key().location().toString();

        // Biome-based radiation zones (direct temperature methods not accessible in KJS 1.20.1)
        const COLD_BIOMES = [
            'minecraft:snowy_plains', 'minecraft:ice_spikes', 'minecraft:snowy_taiga',
            'minecraft:snowy_beach', 'minecraft:snowy_slopes', 'minecraft:frozen_peaks',
            'minecraft:jagged_peaks', 'minecraft:frozen_river', 'minecraft:frozen_ocean',
            'minecraft:deep_frozen_ocean', 'minecraft:grove',
        ];
        const HOT_BIOMES = [
            'minecraft:desert', 'minecraft:badlands', 'minecraft:eroded_badlands',
            'minecraft:wooded_badlands', 'minecraft:savanna', 'minecraft:savanna_plateau',
            'minecraft:windswept_savanna', 'minecraft:warm_ocean', 'minecraft:jungle',
            'minecraft:sparse_jungle', 'minecraft:bamboo_jungle',
        ];

        // DESIGN:
        // - Cold biomes: treated as low-radiation safe zones -> clear effect.
        // - Hot / harsh biomes: keep full Radiach behaviour.
        // - Everything else (mild): clamp to low radiation (amplifier <= 1).

        // Safe / low-radiation zones
        if (COLD_BIOMES.includes(biomeId)) {
            player.removeEffect(radiation.effect);
            return;
        }

        // Clamp radiation strength in mild climates
        if (!HOT_BIOMES.includes(biomeId) && radiation.amplifier > 1) {
            player.potionEffects.add(radiation.effect, radiation.duration, 1, radiation.ambient, radiation.showParticles);
        }
    });
});
