// Client-side environment status HUD
// Shows Temp and Radiation bands in the top-left corner.

let fs_env_status = {
    text: '',
    color: 0xffffff,
};

ClientEvents.tick(event => {
    const player = event.player;
    if (!player) return;

    const level = player.level;
    if (!level) return;

    const x = player.x;
    const y = player.y;
    const z = player.z;

    const biome = level.getBiome(x, y, z).value();
    const temp = biome.getTemperature();

    // Temperature band based on biome temperature
    let tempBand = 'Mild';
    if (temp <= 0.15) tempBand = 'Very Cold';
    else if (temp <= 0.4) tempBand = 'Cold';
    else if (temp <= 0.8) tempBand = 'Warm';
    else tempBand = 'Hot';

    // Radiation band from Radiach potion effect
    const rad = player.getPotionEffect('radiach:radiation');
    let radBand = 'None';
    if (rad) {
        const amp = rad.amplifier;
        if (amp <= 0) radBand = 'Low';
        else if (amp <= 2) radBand = 'Medium';
        else radBand = 'High';
    }

    // Simple safe zone detection: comfortable temp & no radiation
    let zone = '';
    if (!rad && temp >= 0.2 && temp <= 0.8) {
        zone = ' | SAFE';
    }

    // Show debuff info if active
    const slow = player.getPotionEffect('minecraft:mining_fatigue');
    const poison = player.getPotionEffect('minecraft:poison');

    let tempInfo = `Temp: ${tempBand}`;
    if (slow) tempInfo += ' (Mining Fatigue)';

    let radInfo = `Rad: ${radBand}`;
    if (poison) radInfo += ' (Poison)';

    fs_env_status.text = `${tempInfo}  ${radInfo}${zone}`;
});

RenderEvents.overlay(event => {
    const mc = event.minecraft;
    const gui = event.getGuiGraphics();
    const font = mc.font;

    if (!fs_env_status.text) return;

    // Draw in the top-left corner with a subtle shadow
    const x = 4;
    const y = 4;
    gui.drawString(font, fs_env_status.text, x, y, fs_env_status.color, true);
});

