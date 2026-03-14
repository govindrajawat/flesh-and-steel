// Biomechanical Haze: Yellowish-Green Fog in toxic / irradiated conditions
RenderEvents.fogColor(event => {
    const level = event.level;
    const player = level.getNearestPlayer(event.camera.getPosition().x, event.camera.getPosition().y, event.camera.getPosition().z, 64);
    if (!player) return;

    // Only apply in Overworld
    if (!level.dimension || String(level.dimension) !== "minecraft:overworld") return;

    // Check if player is actually irradiated
    const radiation = player.getPotionEffect('radiach:radiation');
    if (!radiation) return;

    // Base fog color (vanilla)
    let r = event.red;
    let g = event.green;
    let b = event.blue;

    // Increase strength with amplifier (up to a cap)
    const amp = Math.min(radiation.amplifier + 1, 4);
    const intensity = 0.12 * amp; // how strong the tint is

    // Yellow-green smog tint
    const hazeR = 0.85;
    const hazeG = 0.95;
    const hazeB = 0.25;

    r = r * (1 - intensity) + hazeR * intensity;
    g = g * (1 - intensity) + hazeG * intensity;
    b = b * (1 - intensity) + hazeB * intensity;

    event.red = r;
    event.green = g;
    event.blue = b;
});

// Muffled Audio when radiated
// We simulate the 'ear ringing' while heavily irradiated
LevelEvents.tick(event => {
    if (!event.level.isClientSide()) return
    let player = event.level.players[0]
    if (!player) return

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
