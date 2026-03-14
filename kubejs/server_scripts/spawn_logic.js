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
    // Direct Biome temperature methods are not accessible in KJS 1.20.1 Forge,
    // so we use a blocklist of warm/hot biome IDs instead.
    const HOT_BIOMES = [
        'minecraft:desert',
        'minecraft:badlands',
        'minecraft:eroded_badlands',
        'minecraft:wooded_badlands',
        'minecraft:savanna',
        'minecraft:savanna_plateau',
        'minecraft:windswept_savanna',
        'minecraft:warm_ocean',
        'minecraft:jungle',
        'minecraft:sparse_jungle',
        'minecraft:bamboo_jungle',
    ]
    let biomeId = level.getBiome(pos).key().location().toString()
    if (HOT_BIOMES.includes(biomeId)) {
        event.cancel()
    }
})

EntityEvents.spawned('minecraft:husk', event => {
    // Husks are sun-resistant, which breaks the 'Zombies only in dark/cold' theme.
    event.cancel()
})

// Special logic: If a player is in a 'High Radiation' zone (detected via potion effect),
// we might want to force some 'Malignant' spawns, but for now, we stick to the user's rule.
