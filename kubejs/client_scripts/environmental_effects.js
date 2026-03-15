// Biomechanical Haze & Environmental Audio for Flesh & Steel
// Separated into safe events for KJS 6 compatibility

// 1. Environmental Audio & State Tracking
ClientEvents.tick(event => {
    const player = event.player;
    if (!player || event.level.time % 20 != 0) return;

    // Safe Radiation Effect lookup
    let radiation = null;
    try {
        player.potionEffects.active.forEach(effect => {
            if (effect.effect.id === 'radiach:radiation') {
                radiation = effect;
            }
        });
    } catch (e) {}

    // Audio Feedback: High radiation = play a faint ringing sound every few seconds
    if (radiation && radiation.amplifier > 1 && event.level.time % 120 == 0) {
        player.playSound('minecraft:block.beacon.ambient', 0.15, 2.0);
    }
});

// 2. Note on Fog: 
// ClientEvents.fogColor is currently unavailable in this build of KJS.
// We prioritize HUD visibility and Audio feedback until a stable fog hook is identified.
