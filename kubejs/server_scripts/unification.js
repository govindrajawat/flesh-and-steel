// Basic Unification for Flesh & Steel
// Focuses on ensuring Create and Minecraft materials are prioritized.

ServerEvents.recipes(event => {
    // Unify all Zinc and Copper to Create/Minecraft versions
    // This prevents "dirty" ore processing from giving diverse ingots.
    
    // Unified metals
    event.replaceOutput({}, '#forge:ingots/copper', 'minecraft:copper_ingot')
    event.replaceOutput({}, '#forge:ingots/zinc', 'create:zinc_ingot')
    event.replaceOutput({}, '#forge:ingots/steel', 'pointblank:gunmetal_ingot') // Using gunmetal as high-grade steel
    
    // Nuggets
    event.replaceOutput({}, '#forge:nuggets/iron', 'create:iron_nugget')
    event.replaceOutput({}, '#forge:nuggets/copper', 'create:copper_nugget')
    
    // Plates (Sheets)
    event.replaceOutput({}, '#forge:plates/iron', 'create:iron_sheet')
    event.replaceOutput({}, '#forge:plates/copper', 'create:copper_sheet')
    event.replaceOutput({}, '#forge:plates/gold', 'create:golden_sheet')
})

// Hide duplicate ores from JEI if needed
// ClientEvents.reiHide() or JEIEvents.hideItems() would go in client_scripts
