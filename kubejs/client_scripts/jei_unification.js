// JEI Unification Hiding for Flesh & Steel
// Hides duplicate ores and items to make the pack feel more "AAA"

JEIEvents.hideItems(event => {
    // Hide duplicate ores from mods that aren't the primary ones
    // We prioritize Create and Minecraft (Vanilla)
    
    // Example: Hiding duplicate copper ingots from other mods
    // event.hide('othermod:copper_ingot')
    
    // We can also hide items that are disabled by our scripts
    // event.hide('naturescompass:natures_compass') // If we replaced it with a different one
})


