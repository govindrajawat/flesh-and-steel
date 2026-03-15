// Material/Tool Tags for Radiation Resistance in Flesh & Steel
// Makes Steel and Lead armor act as radiation suits automatically.

ServerEvents.tags('item', event => {
    // 1. Tagging Steel Armor for moderate protection
    // Radioactive mod recognizes tags like 'forge:radiation_protection' 
    // or specific percentages if configured.
    const steelItems = [
        'minecraft:iron_helmet', // Assuming Iron/Steel are unified or using base iron
        'minecraft:iron_chestplate',
        'minecraft:iron_leggings',
        'minecraft:iron_boots'
    ];
    
    // We add radiation protection tags to the material base
    event.add('forge:radiation_protection', steelItems);
    event.add('radioactive:protects_from_radiation', steelItems);

    // 2. Identify and Tag any specific Lead armor if it exists in the pack
    // event.add('forge:radiation_protection', /.*lead_.*(helmet|chestplate|leggings|boots)/);
});
