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
PlayerEvents.loggedIn(event => {
    const { player } = event;

    if (!player.persistentData.contains('flesh_steel_starter_given')) {
        player.persistentData.putBoolean('flesh_steel_starter_given', true);

        // Robust Starter Kit: Give each item safely to prevent script crashes
        const giveSafe = (item, count) => {
            try {
                if (count > 1) {
                    player.give(`${count}x ${item}`);
                } else {
                    player.give(item);
                }
            } catch (e) {
                console.log(`Failed to give starter item ${item}: Mod might be missing.`);
            }
        };

        giveSafe('minecraft:cooked_beef', 16);
        giveSafe('minecraft:torch', 32);
        
        // Potion handling (NBT can be tricky in KJS 1.20.1)
        try {
            player.give(Item.of('minecraft:potion', 12, '{Potion:"minecraft:water"}'));
        } catch (e) {
            console.log("Failed to give water potions.");
        }

        giveSafe('minecraft:iron_sword', 1);

        // Sophisticated Backpacks was missing, replacing with a Vanilla alternative if needed 
        // Or simply omitting if no backpack mod is present.
        
        player.tell('§aWelcome to Flesh & Steel! Your starter kit has been provided.');
    }
});

// Admin command to reset starter kit for testing
ServerEvents.commandRegistry(event => {
    const { commands: Commands, arguments: Arguments } = event;
    event.register(
        Commands.literal('resetstarter')
        .requires(s => s.hasPermission(2))
        .executes(c => {
            c.source.player.persistentData.remove('flesh_steel_starter_given');
            c.source.player.tell('§eStarter kit reset. Relog to receive it again.');
            return 1;
        })
    );
});
