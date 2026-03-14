// Create Steam Engine Heat Integration for Cold Sweat
// This script makes Create Steam Engines emit heat that affects the player's temperature.

LevelEvents.tick(event => {
    // Optimization: Only run every 20 ticks (1 second)
    if (event.level.time % 20 != 0) return;

    event.level.players.forEach(player => {
        let { x, y, z } = player;

        // Count nearby heat sources instead of just a boolean.
        let heatScore = 0;

        // Optimized search: Check a small 7x5x7 area around the player
        for (let dx = -3; dx <= 3; dx++) {
            for (let dy = -1; dy <= 2; dy++) {
                for (let dz = -3; dz <= 3; dz++) {
                    let block = event.level.getBlock(x + dx, y + dy, z + dz);
                    let id = block.id;

                    // Strong industrial heat sources
                    if (id == 'create:steam_engine' || id == 'createnuclear:reactor_casing') {
                        heatScore += 3;
                    }

                    // Ambient heat sources (fire / light)
                    if (
                        id == 'minecraft:torch' ||
                        id == 'minecraft:wall_torch' ||
                        id == 'minecraft:soul_torch' ||
                        id == 'minecraft:campfire' ||
                        id == 'minecraft:soul_campfire' ||
                        id == 'minecraft:lantern' ||
                        id == 'minecraft:soul_lantern'
                    ) {
                        heatScore += 1;
                    }
                }
            }
        }

        if (heatScore > 0) {
            // Translate heatScore into a Cold Sweat 'heat' effect amplifier.
            // 1–3 = mild, 4–7 = medium, 8+ = intense.
            let amp = 0;
            if (heatScore >= 8) {
                amp = 2;
            } else if (heatScore >= 4) {
                amp = 1;
            }

            // Apply Heat effect from Cold Sweat
            // We use the effect 'cold_sweat:heat' which makes the player feel warmer.
            player.addPotionEffect('cold_sweat:heat', 60, amp, false, false);
        }
    });
});
