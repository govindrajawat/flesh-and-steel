// Create & Nuclear Machine Hazards (Heat & Radiation)
// This script makes industrial machines emit both heat (Cold Sweat) and radiation (Radiach).

LevelEvents.tick(event => {
    // Optimization: Only run every 20 ticks (1 second)
    if (event.level.time % 20 != 0) return;

    event.level.players.forEach(player => {
        let { x, y, z } = player;

        let heatScore = 0;
        let radiationScore = 0;

        // Search area around player
        for (let dx = -4; dx <= 4; dx++) {
            for (let dy = -2; dy <= 3; dy++) {
                for (let dz = -4; dz <= 4; dz++) {
                    let block = event.level.getBlock(Math.floor(x + dx), Math.floor(y + dy), Math.floor(z + dz));
                    let id = block.id;

                    // Nuclear Reactors: High Heat + High Radiation
                    if (id == 'createnuclear:reactor_casing' || id == 'createnuclear:reactor_controller') {
                        heatScore += 5;
                        radiationScore += 10;
                    }

                    // Steam Engines: High Heat + Low Radiation (Industrial Leakage)
                    if (id == 'create:steam_engine') {
                        heatScore += 3;
                        radiationScore += 1;
                    }

                    // Ambient heat sources (fire / light)
                    if (id.contains('torch') || id.contains('campfire') || id.contains('lantern')) {
                        heatScore += 1;
                    }
                }
            }
        }

        // Apply Heat (Cold Sweat)
        if (heatScore > 0) {
            let amp = heatScore >= 12 ? 2 : (heatScore >= 6 ? 1 : 0);
            player.addPotionEffect('cold_sweat:heat', 60, amp, false, false);
        }

        // Apply Radiation (Radiach)
        if (radiationScore > 0) {
            let amp = radiationScore >= 15 ? 2 : (radiationScore >= 5 ? 1 : 0);
            player.addPotionEffect('radiach:radiation', 60, amp, false, false);
        }
    });
});

