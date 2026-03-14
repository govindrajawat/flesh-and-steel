// ============================================================
// FLESH & STEEL - Gameplay Tuning (1.20.1 KJS)
// Tweaks to recipe, progression, and player experience
// ============================================================

ServerEvents.recipes((event) => {
    // Waystone - cheaper recipe using materials players find exploring
    event.shaped('waystones:waystone', [
        ' S ',
        'SWS',
        'SSS'
    ], {
        S: 'minecraft:stone',
        W: 'waystones:warp_stone'
    }).id('flesh_and_steel:cheap_waystone');

    // Remove original compass recipes to avoid duplicates
    event.remove({ id: 'explorerscompass:explorer_compass' })
    event.remove({ id: 'naturescompass:nature_compass' })

    // Quick crafting recipe for basic Create components from ore
    event.shaped('4x create:andesite_alloy', [
        'AA',
        'AA'
    ], {
        A: 'minecraft:andesite',
    }).id('flesh_and_steel:andesite_alloy_from_andesite');

    // Allow crafting simple compasses (for navigation mods)
    event.shaped('explorerscompass:explorers_compass', [
        ' I ',
        'ICI',
        ' I ',
    ], {
        I: 'minecraft:iron_ingot',
        C: 'minecraft:compass',
    }).id('flesh_and_steel:explorer_compass');

    event.shaped('naturescompass:natures_compass', [
        ' I ',
        'ILI',
        ' I ',
    ], {
        I: 'minecraft:iron_ingot',
        L: 'minecraft:oak_leaves',
    }).id('flesh_and_steel:nature_compass');
});

// ============================================================
// FLESH & STEEL - Starting Items for New Players
// Give players a better start so they can explore immediately
// ============================================================
PlayerEvents.loggedIn((event) => {
    const { player, server } = event;

    // Use persistentData (NBT) to ensure it survives restarts and is only given once
    if (!player.persistentData.contains('flesh_steel_starter_given')) {
        player.persistentData.putBoolean('flesh_steel_starter_given', true);

        // Give players a starter kit to begin exploring
        player.give('16x minecraft:cooked_beef');
        player.give('32x minecraft:torch');
        player.give('minecraft:iron_sword');
        player.give('travelersbackpack:standard');

        // Welcome message - Using a safe string format to avoid "Text" vs "Component" errors
        player.tell('§aWelcome to Flesh & Steel! Your starter kit has been provided.');
    }
});
