// ============================================================
// FLESH & STEEL - Ore World Generation (1.20.1 KubeJS)
// NOTE: WorldgenEvents.add() is currently not supported in 1.20.1 KubeJS.
// We are leaving this commented out to prevent errors until the API is updated.
// ============================================================

/*
WorldgenEvents.add(event => {
  const { anchors } = event
  
  // surface hints (iron/copper)
  event.addOre(ore => {
    ore.id = 'flesh_and_steel:surface_iron'
    ore.target = 'minecraft:stone'
    ore.block = 'minecraft:iron_ore'
    ore.size = 5
    ore.count = 20
    ore.uniformHeight(anchors.absolute(50), anchors.absolute(128))
    ore.biomes = { not: 'minecraft:ocean' }
  })

  // deep rich iron
  event.addOre(ore => {
    ore.id = 'flesh_and_steel:deep_iron'
    ore.target = 'minecraft:deepslate'
    ore.block = 'minecraft:deepslate_iron_ore'
    ore.size = 12
    ore.count = 10
    ore.uniformHeight(anchors.absolute(-64), anchors.absolute(20))
  })

  // extra diamond deep down
  event.addOre(ore => {
    ore.id = 'flesh_and_steel:deep_diamond'
    ore.target = 'minecraft:deepslate'
    ore.block = 'minecraft:deepslate_diamond_ore'
    ore.size = 6
    ore.count = 6
    ore.uniformHeight(anchors.absolute(-64), anchors.absolute(-32))
  })

  // extra gold for tech
  event.addOre(ore => {
    ore.id = 'flesh_and_steel:deep_gold'
    ore.target = 'minecraft:deepslate'
    ore.block = 'minecraft:deepslate_gold_ore'
    ore.size = 10
    ore.count = 8
    ore.uniformHeight(anchors.absolute(-64), anchors.absolute(16))
  })

  // extra quartz in nether (AE2 dependency)
  event.addOre(ore => {
    ore.id = 'flesh_and_steel:extra_nether_quartz'
    ore.target = 'minecraft:netherrack'
    ore.block = 'minecraft:nether_quartz_ore'
    ore.size = 14
    ore.count = 20
    ore.uniformHeight(anchors.absolute(0), anchors.absolute(128))
    ore.worldgenLayer = 'underground_ores'
    // dimensions: "minecraft:the_nether"
  })
})
*/
