ServerEvents.recipes(event => {
    // Making Create Engineering require Biomancy "Flesh" parts
    
    // Shafts now require a bone fragment and andesite alloy
    event.remove({ output: 'create:shaft' })
    event.shaped('8x create:shaft', [
        'A',
        'B',
        'A'
    ], {
        A: 'create:andesite_alloy',
        B: 'biomancy:bone_fragments'
    })

    // Cogwheels (Small) require sinew
    event.remove({ output: 'create:cogwheel' })
    event.shaped('2x create:cogwheel', [
        ' S ',
        'SAS',
        ' S '
    ], {
        S: 'biomancy:sinew',
        A: 'create:andesite_alloy'
    })

    // Large Cogwheels require a regular cogwheel and bone fragments
    event.remove({ output: 'create:large_cogwheel' })
    event.shaped('create:large_cogwheel', [
        ' B ',
        'BCB',
        ' B '
    ], {
        B: 'biomancy:bone_fragments',
        C: 'create:cogwheel'
    })

    // Andesite Casing (The base of all early tech) requires Flesh Bits
    event.remove({ output: 'create:andesite_casing' })
    event.shaped('create:andesite_casing', [
        'WWW',
        'WFW',
        'WWW'
    ], {
        W: 'minecraft:andesite',
        F: 'biomancy:flesh_bits'
    })
})
