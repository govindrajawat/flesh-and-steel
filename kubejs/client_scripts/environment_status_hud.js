// Client-side environment status HUD for Flesh & Steel
// Optimized for independent Temperature and Radiation tracking.

let fs_env_status = {
    text: '',
    color: 0xffffff,
};

ClientEvents.tick(event => {
    const player = event.player;
    if (!player) return;

    const level = player.level;
    if (!level) return;

    let pos = player.blockPosition();
    let biome = level.getBiome(pos).value();
    // --- UNIVERSAL 10-POINT HUD ---
    
    // 1. Temperature Calculation (Standardized with Server)
    let tScale = 5;
    let tColor = '§7';
    let tLabel = 'Normal';
    if (temp <= -0.2) { tScale = 0; tColor = '§b'; tLabel = 'V.Cold'; }
    else if (temp < 0) { tScale = 1; tColor = '§3'; tLabel = 'V.Cold'; }
    else if (temp <= 0.2) { tScale = 2; tColor = '§9'; tLabel = 'Cold'; }
    else if (temp <= 0.4) { tScale = 4; tColor = '§1'; tLabel = 'Cold'; }
    else if (temp <= 0.7) { tScale = 6; tColor = '§a'; tLabel = 'Normal'; }
    else if (temp <= 0.9) { tScale = 8; tColor = '§6'; tLabel = 'Hot'; }
    else if (temp <= 1.2) { tScale = 9; tColor = '§c'; tLabel = 'Hot'; }
    else { tScale = 10; tColor = '§4'; tLabel = 'V.Hot'; }

    // 2. Radiation Calculation (Standardized with Server)
    const rad = player.getPotionEffect('radiach:radiation');
    let rScale = rad ? (rad.amplifier + 1) * 2 : 0;
    let rColor = '§f';
    let rLabel = 'Low';
    
    if (rScale == 0) { rColor = '§a'; rLabel = 'Safe'; }
    else if (rScale <= 3) { rColor = '§e'; rLabel = 'Low'; }
    else if (rScale <= 6) { rColor = '§6'; rLabel = 'Normal'; }
    else if (rScale <= 8) { rColor = '§c'; rLabel = 'High'; }
    else { rColor = '§4'; rLabel = 'V.High'; }

    // 3. Hazard Matrix Display & Labeling
    let status = '';
    if (tScale >= 8 && rScale >= 7) status = ' §k| §4LETHAL'; // Nuclear Fire
    else if (tScale <= 1 && rScale >= 7) status = ' §b| §8VOID'; // Freezing Cold
    else if (rScale >= 9) status = ' §4| MELTDOWN';
    else if (tScale >= 5 && tScale <= 7 && rScale <= 3) status = ' §2| VITALITY'; // Buff active
    else if (rScale == 0 && tScale >= 5 && tScale <= 7) status = ' §d| OPTIMAL';

    let tempText = `${tColor}Temp: ${tScale}/10`;
    let radText = `${rColor}Rad: ${rScale}/10`;

    fs_env_status.text = `§7[ ${tempText}  §7|  ${radText} §7]${status}`;
});

RenderEvents.overlay(event => {
    const mc = event.minecraft;
    const gui = event.getGuiGraphics();
    const font = mc.font;

    const width = event.getWindow().getGuiScaledWidth();
    const height = event.getWindow().getGuiScaledHeight();
    const textWidth = font.width(fs_env_status.text);

    // Bottom-center positioning (above hotbar)
    const x = (width - textWidth) / 2;
    const y = height - 55; // Elevated above the hotbar items
    
    // Slight shadow rect for readability
    gui.fill(x - 2, y - 2, x + textWidth + 2, y + 10, 0x88000000);
    gui.drawString(font, fs_env_status.text, x, y, 0xFFFFFF, false);
});
