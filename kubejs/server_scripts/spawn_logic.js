EntityEvents.spawned('minecraft:zombie', event => {
    let entity = event.entity
    let level = entity.level

    // Use the entity's own block position (already a BlockPos)
    let pos = entity.blockPosition()
    let lightLevel = level.getMaxLocalRawBrightness(pos)

    if (lightLevel > 7) {
        event.cancel()
        return
    }

    // Temperature check: Cold-Dwelling mutants only spawn in cold/mild biomes.
    // We use dynamic temperature to support 100+ modded biomes from BOP/BYG automatically.
    let biome = level.getBiome(pos);
    let temp = biome.value().getTemperature(pos);
    
    // If it's too warm (> 0.4 represents mild/hot climates), cancel the spawn.
    if (temp > 0.4) {
        event.cancel()
    }
})

EntityEvents.spawned('minecraft:husk', event => {
    // Husks are sun-resistant, which breaks the 'Zombies only in dark/cold' theme.
    event.cancel()
})

// Special logic: If a player is in a 'High Radiation' zone (detected via potion effect),
// we might want to force some 'Malignant' spawns, but for now, we stick to the user's rule.
