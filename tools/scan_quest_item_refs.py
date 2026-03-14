import glob
import json
import os
import re


def main() -> None:
    root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

    mods_path = os.path.join(root, "pack-config", "mods.json")
    with open(mods_path, "r", encoding="utf-8") as f:
        mods = json.load(f)

    slugs = set()
    for group in ("common", "client", "server"):
        for m in mods["mods"].get(group, []):
            slug = m.get("slug")
            if slug:
                slugs.add(slug)

    # SNBT isn't strict JSON; this is a heuristic: extract modid from fields we know contain IDs.
    snbt_files = glob.glob(os.path.join(root, "config", "ftbquests", "quests", "chapters", "*.snbt"))
    # Matches e.g. item: "modid:name", icon: "modid:name", entity: "modid:name"
    # NOTE: Skip nested item stacks like item: { id: "modid:name", ... } by not matching bare `id:`.
    pat = re.compile(r'\b(?:item|icon|to_observe|entity):\s*(?:\{|\")?\s*\"?([a-z0-9_]+):')

    modids = set()
    refs: list[tuple[str, str]] = []
    for path in snbt_files:
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        for m in pat.finditer(txt):
            modid = m.group(1)
            modids.add(modid)
            refs.append((modid, os.path.basename(path)))

    allowed = {"minecraft", "forge", "ftbquests", "kubejs"}
    missing = sorted([m for m in modids if m not in slugs and m not in allowed])

    print("Potentially missing modids referenced by quests:")
    for modid in missing:
        files = sorted({fn for m, fn in refs if m == modid})
        print(f"- {modid}: {', '.join(files)}")


if __name__ == "__main__":
    main()

