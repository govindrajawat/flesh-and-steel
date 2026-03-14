EntityEvents.spawned('minecraft:zombie', event => {
    let { entity, level, x, y, z } = event
    
    // 1. Light Level Check: Zombies only spawn in darkness
    if (level.getLightLevel(x, y, z) > 7) {
        event.cancel()
        return
    }

    // 2. Temperature Check (Cold Sweat Integration)
    // Zombies in this pack are 'Cold-Dwelling' mutants. 
    // They only spawn if the local temperature is below a certain threshold.
    // getBiome(x, y, z).value().getTemperature() is the base biome temp.
    let biomeTemp = level.getBiome(x, y, z).value().getTemperature()
    
    // If it's too warm (like a desert or high-noon in summer), cancel the spawn.
    if (biomeTemp > 0.4) {
        event.cancel()
    }
})

EntityEvents.spawned('minecraft:husk', event => {
    // Husks are sun-resistant, which breaks the 'Zombies only in dark/cold' theme.
    event.cancel() 
})

// Special logic: If a player is in a 'High Radiation' zone (detected via potion effect), 
// we might want to force some 'Malignant' spawns, but for now, we stick to the user's rule.
