// ============================================================
// FLESH & STEEL - Dynamic Radio Identification
// This script allows a "Mysterious Radio Disc" to turn into 
// ANY song currently in the audio_player folder without a restart.
// ============================================================

ItemEvents.rightClicked('minecraft:music_disc_fragment5', event => {
    const { item, player, world, server } = event;

    // Check if it's our special mysterious disc
    if (item.nbt && item.nbt.UnidentifiedRadio) {
        
        // 1. Get the list of songs from the audio_player folder
        // We use Java's File API to look at the folder directly at runtime
        let audioFolder = new java.io.File('audio_player');
        
        if (!audioFolder.exists() || !audioFolder.isDirectory()) {
            player.tell('§cError: audio_player folder not found on server.');
            return;
        }

        let files = audioFolder.listFiles();
        let songs = [];
        
        for (let file of files) {
            if (file.getName().endsWith('.ogg')) {
                songs.push(file.getName());
            }
        }

        if (songs.length === 0) {
            player.tell('§eThe disc remains silent... (No .ogg files found in audio_player folder)');
            return;
        }

        // 2. Pick a random song
        let randomSong = songs[Math.floor(Math.random() * songs.length)];
        let songTitle = randomSong.replace('.ogg', '').replace(/_/g, ' ').replace(/-/g, ' ').split(' ').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(' ');

        // 3. Create the identified disc
        let disc = Item.of('minecraft:music_disc_5', {
            MusicDisk: {
                audio_id: randomSong
            },
            display: {
                Name: JSON.stringify({
                    text: songTitle + " Radio Disc",
                    color: "gold",
                    italic: false
                })
            }
        });

        // 4. Swap the items
        item.count--;
        player.give(disc);
        
        // Effects
        player.playSound('minecraft:block.note_block.chime', 1.0, 1.2);
        player.tell(`§aYou identified the disc: §6${songTitle}`);
        
        // Cancel event to prevent default behavior
        event.cancel();
    }
});
