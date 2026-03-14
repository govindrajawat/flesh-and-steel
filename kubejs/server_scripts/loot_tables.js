// ============================================================
// FLESH & STEEL - Loot Table Tuning
// ============================================================

LootJS.modifiers((event) => {
    // Add gun components to exploration chests
    event
        .addLootTableModifier(/minecraft:chests\/(simple_dungeon|pillager_outpost|abandoned_mineshaft)/)
        .addLoot('immersive-guns:component_pistol')
        .randomChance(0.25);

    // Add "Unidentified Radio Disc" to loot
    // This item will be identify a random song from the audio_player folder when used
    event
        .addLootTableModifier(/minecraft:chests\/(simple_dungeon|pillager_outpost|village\/village_weaponsmith)/)
        .addLoot(Item.of('minecraft:music_disc_fragment5', '{display:{Name:\'{"text":"Mysterious Radio Disc","color":"gold","italic":true}\',Lore:[\'{"text":"Right-click to identify...","color":"gray","italic":false}\']},UnidentifiedRadio:true}'))
        .randomChance(0.15); // 15% chance in chests

    event
        .addLootTypeModifier(LootType.ENTITY)
        .addLoot(Item.of('minecraft:music_disc_fragment5', '{display:{Name:\'{"text":"Mysterious Radio Disc","color":"gold","italic":true}\',Lore:[\'{"text":"Right-click to identify...","color":"gray","italic":false}\']},UnidentifiedRadio:true}'))
        .randomChance(0.01); // 1% chance from monsters
});