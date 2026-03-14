// Biomechanical Haze: Yellowish-Green Fog in toxic / irradiated conditions
RenderEvents.fogColor(event => {
    // Use the camera entity directly for performance (avoids searching the world every frame)
    const entity = event.entity;
    if (!entity || !entity.player) return;
    const player = entity;

    // Check if player is actually irradiated
    const radiation = player.getPotionEffect('radiach:radiation');
    const isVeryHot = player.persistentData.getInt('tempScale') >= 10;
    
    if (!radiation && !isVeryHot) return;

    // Base fog color (vanilla)
    let r = event.red;
    let g = event.green;
    let b = event.blue;

    // 1. Radiation (Toxic Green)
    if (radiation) {
        const amp = Math.min(radiation.amplifier + 1, 4);
        const intensity = 0.15 * amp;
        const hazeR = 0.85; const hazeG = 0.95; const hazeB = 0.25;
        r = r * (1 - intensity) + hazeR * intensity;
        g = g * (1 - intensity) + hazeG * intensity;
        b = b * (1 - intensity) + hazeB * intensity;
    }

    // 2. Heat (Scorched Red)
    if (isVeryHot) {
        const intensity = 0.1;
        r = r * (1 - intensity) + 1.0 * intensity;
        g = g * (1 - intensity) + 0.4 * intensity;
        b = b * (1 - intensity) + 0.2 * intensity;
    }

    event.red = r;
    event.green = g;
    event.blue = b;
});

// Muffled Audio when radiated
// We simulate the 'ear ringing' while heavily irradiated
LevelEvents.tick(event => {
    let player = Client.player;
    if (!player) return;

    // Find radiation effect
    let radiation = player.getPotionEffect('radiach:radiation')
    if (!radiation) return

    // High radiation = play a faint ringing sound every few seconds
    if (radiation.amplifier > 1 && event.level.time % 120 == 0) {
        player.playSound('minecraft:block.beacon.ambient', 0.15, 2.0)
    }
})

// Visual Overlay for "The Gore" Theme
// If player is choosing 'Flesh' over 'Steel' (detected by inventory)
// we could apply a slight reddish vignette.
