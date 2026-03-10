import os
import json
from pathlib import Path

quest_dir = Path("overrides") / "global_data_packs" / "FleshAndSteelQuests"

# 1. pack.mcmeta
os.makedirs(quest_dir, exist_ok=True)
with open(quest_dir / "pack.mcmeta", "w", encoding="utf-8") as f:
    json.dump({"pack": {"pack_format": 15, "description": "Flesh & Steel Quests"}}, f, indent=2)

# 2. Add some simple quests
sq_dir = quest_dir / "data" / "simplequests" / "quests"
os.makedirs(sq_dir, exist_ok=True)

q1 = {
  "name": "The Beginning of the End",
  "category": "flesh_and_steel",
  "description": [
    "Welcome to Flesh & Steel.",
    "Your first task: gather the basic materials for survival."
  ],
  "tasks": [
    {
      "type": "simplequests:item",
      "predicate": {"items": ["minecraft:log"]},
      "amount": 16
    }
  ],
  "loot_table": "minecraft:chests/village/village_toolsmith",
  "icon": "minecraft:iron_pickaxe"
}

q2 = {
  "name": "Harvesting the Flesh",
  "category": "flesh_and_steel",
  "description": [
    "Harvesting rotten flesh will be key to survival."
  ],
  "tasks": [
    {
      "type": "simplequests:item",
      "predicate": {"items": ["minecraft:rotten_flesh"]},
      "amount": 32
    }
  ],
  "loot_table": "minecraft:chests/simple_dungeon",
  "icon": "minecraft:rotten_flesh",
  "parent": "simplequests:q1_start"
}

q3 = {
  "name": "The Spark of Creation",
  "category": "flesh_and_steel",
  "description": [
    "The Create mod allows you to automate everything.",
    "Craft your first Andesite Alloy."
  ],
  "tasks": [
    {
      "type": "simplequests:item",
      "predicate": {"items": ["create:andesite_alloy"]},
      "amount": 8
    }
  ],
  "loot_table": "minecraft:chests/abandoned_mineshaft",
  "icon": "create:andesite_alloy",
  "parent": "simplequests:q1_start"
}

with open(sq_dir / "q1_start.json", "w", encoding="utf-8") as f:
    json.dump(q1, f, indent=2)
with open(sq_dir / "q2_flesh.json", "w", encoding="utf-8") as f:
    json.dump(q2, f, indent=2)
with open(sq_dir / "q3_create.json", "w", encoding="utf-8") as f:
    json.dump(q3, f, indent=2)

print("Quests generated.")
