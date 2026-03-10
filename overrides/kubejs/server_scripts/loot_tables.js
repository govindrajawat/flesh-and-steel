// ============================================================
// FLESH & STEEL - Loot Table Tuning
// ============================================================

LootJS.modifiers((event) => {
    // The original script had an error using a function that does not exist.
    // This adds gun components to various dungeon chests to encourage exploration.
    event
        .addLootTableModifier(/minecraft:chests\/(simple_dungeon|pillager_outpost|abandoned_mineshaft)/)
        .addLoot('immersive-guns:component_pistol')
        .randomChance(0.25); // 25% chance to appear
});