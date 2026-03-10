// ============================================================
// FLESH & STEEL - Custom Villager Trades
// ============================================================

MoreJSEvents.villagerTrades((event) => {
    // The original script had an error, likely due to an invalid item ID,
    // which may be a side effect of other mod incompatibilities. This adds
    // a thematic trade for ammo.
    event.addTrade('minecraft:weaponsmith', 1, ['minecraft:emerald'], '8x immersive-guns:revolver_ammo');
    event.addTrade('minecraft:weaponsmith', 2, ['3x minecraft:emerald'], '8x immersive-guns:shotgun_ammo');
});