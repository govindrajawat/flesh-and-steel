## `local_mods/` — JARs bundled into builds

Put mod `.jar` files here when they **cannot be downloaded from Modrinth** by the build scripts (example: CurseForge-only mods like Apotheosis).

### Folder layout

- `local_mods/common/`: included in both client `.mrpack` and server `.zip`
- `local_mods/client/`: included only in client `.mrpack`
- `local_mods/server/`: included only in server `.zip`

### How it works

- Client build: jars are embedded into the `.mrpack` as `overrides/mods/*.jar`
- Server build: jars are copied into `build/server-pack/mods/` and included in the server `.zip`

### Licensing note

Only bundle jars here if you have the right to redistribute them (private pack / permissions / allowed license).
