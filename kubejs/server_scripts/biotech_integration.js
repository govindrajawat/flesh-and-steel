// ============================================================
// FLESH & STEEL - Biotech Integration (1.20.1)
// Integrating Create, Biomancy, and Create: Bio-Factory
// ============================================================

ServerEvents.recipes(event => {
    // 1. Nutrient Fluid via Create Spouting
    // Allow players to spout nutrient fluid onto mechanical parts for "Living" variants
    
    // Example: Spouting nutrient fluid onto a shaft makes it a "Living Shaft" (purely thematic or custom item)
    // If Create: Bio-Factory doesn't add many items, we focus on recipe shortcuts.

    // 2. Convering Biomancy items to Create fluids
    // Use the Digester or Mixer to create Bio-Factory fluids
    
    // Create: Bio-Factory already adds many of these, we just ensure they are visible.

    // 3. Tetra x Biomancy Integration
    // Allow using bone fragments and sinew in Tetra weapon crafting
    // (Note: This is usually done via tags, but we add custom recipes for materials)
    
    event.custom({
        type: 'create:mixing',
        ingredients: [
            { item: 'biomancy:flesh_bits' },
            { item: 'biomancy:flesh_bits' },
            { fluid: 'minecraft:water', amount: 1000 }
        ],
        results: [
            { fluid: 'biofactory:nutrient_paste_fluid', amount: 500 }
        ],
        heatRequirement: 'heated'
    }).id('flesh_and_steel:mix_nutrient_fluid')

    // 4. Point Blank Gun Crafting Integration
    // Make Gunmetal craftable via Create Mixing (Alloy)
    event.custom({
        type: 'create:mixing',
        ingredients: [
            { item: 'minecraft:iron_ingot' },
            { item: 'minecraft:coal' },
            { item: 'biomancy:bone_fragments' } // Biological hardening
        ],
        results: [
            { item: 'pointblank:gunmetal_ingot', count: 2 }
        ],
        heatRequirement: 'heated'
    }).id('flesh_and_steel:mix_gunmetal')
})
