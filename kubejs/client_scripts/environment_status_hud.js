// Client-side HUD for Flesh & Steel - Radioactive Mod Edition
// Displays Temperature and Radiation scales (0-10) in the GUI.

let fs_env_status = {
    text: '',
};

ClientEvents.tick(event => {
    const player = event.player;
    if (!player) return;

    // Retrieve scales stored in persistentData by radiation_control.js
    const tScale = player.persistentData.getInt('tempScale') || 5;
    const rScale = player.persistentData.getInt('radScale') || 0;

    // 1. Temperature Labeling
    let tColor = '§a'; let tLabel = 'Norm';
    if (tScale <= 1) { tColor = '§b'; tLabel = 'V.Cold'; }
    else if (tScale <= 4) { tColor = '§9'; tLabel = 'Cold'; }
    else if (tScale >= 9) { tColor = '§4'; tLabel = 'V.Hot'; }
    else if (tScale >= 8) { tColor = '§6'; tLabel = 'Hot'; }

    // 2. Radiation Labeling
    let rColor = '§a'; let rLabel = 'Safe';
    if (rScale >= 9) { rColor = '§5'; rLabel = 'LETHAL'; }
    else if (rScale >= 7) { rColor = '§c'; rLabel = 'HEAVY'; }
    else if (rScale >= 4) { rColor = '§6'; rLabel = 'WARN'; }
    else if (rScale >= 1) { rColor = '§e'; rLabel = 'LOW'; }

    // 3. Status Matrix
    let status = '';
    if (tScale >= 5 && tScale <= 7 && rScale <= 3) {
        status = ' §k| §2§lVITALITY';
    } else if (rScale >= 7 || tScale >= 9 || tScale <= 1) {
        status = ' §k| §c§lHAZARD';
    }

    const tempPart = `${tColor}Temp: ${tScale}/10`;
    const radPart = `${rColor}Rad: ${rScale}/10`;

    fs_env_status.text = `§7[ ${tempPart}  §7|  ${radPart} §7]${status}`;
});

ClientEvents.paintScreen(event => {
    const width = event.graphics.guiScaledWidth;
    const height = event.graphics.guiScaledHeight;
    const textWidth = font.width(fs_env_status.text);

    // Position at top center
    const x = (width - textWidth) / 2;
    const y = 10; 
    
    // Background shadow for readability
    gui.fill(x - 4, y - 4, x + textWidth + 4, y + 10, 0xCC111111);
    gui.drawString(font, fs_env_status.text, x, y, 0xFFFFFF, false);
});
