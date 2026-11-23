"""
apply_gameplay_zoom_and_cleanup.py
1. Set Gameplay scene background color to sky blue (r=99, g=155, b=255)
2. Apply Camera Zoom 2.8x on Base, BG_Village, and BG_Sky layers
3. Set Camera Y to 410 (focused close-up on Robi and the grass terrain)
4. Update Camera X minimum to 183 px (half-width of 2.8x viewport)
5. Expand terrain tiles from 16 to 24 tiles (up to X: 6144)
6. Expand Sky and Village backdrops along the journey
"""
import json

PROJECT = r"c:\Users\DELL\Downloads\Proffesionalsss\TTS\Roadside-Stick-\game.json"

with open(PROJECT, "r", encoding="utf-8") as f:
    g = json.load(f)

for sc in g["layouts"]:
    if sc["name"] != "Gameplay":
        continue

    # 1. Background color of scene -> Sky Blue (99, 155, 255)
    sc["r"] = 99
    sc["g"] = 155
    sc["b"] = 255
    print("Gameplay: background color set to sky blue (99, 155, 255)")

    # 2. Expand instances for terrain, sky, and village
    # Keep Player and HUD instances, rebuild world instances
    keep_instances = [inst for inst in sc.get("instances", [])
                      if inst.get("name") in ("Spr_Player", "Txt_HUDLevel", "Txt_HUDTimer", "Txt_HUDControls")]

    new_world_instances = []

    # Sky (height 450 to cover sky down to ground)
    for k in range(6):
        new_world_instances.append({
            "name": "Spr_Sky", "x": k * 1024, "y": 0, "width": 1024, "height": 450,
            "customSize": True, "layer": "BG_Sky", "zOrder": 1, "angle": 0, "locked": False
        })

    # Village (Y=192, height 256)
    for k in range(4):
        new_world_instances.append({
            "name": "Spr_Village", "x": k * 1536, "y": 192, "width": 1536, "height": 256,
            "customSize": True, "layer": "BG_Village", "zOrder": 2, "angle": 0, "locked": False
        })

    # Terrain tiles (24 tiles = 6144 px) alternating Rumput1..3
    for idx in range(24):
        new_world_instances.append({
            "name": "Spr_Terrain", "x": idx * 256, "y": 448, "width": 256, "height": 128,
            "customSize": True, "layer": "", "zOrder": 5, "angle": 0, "locked": False,
            "initialNumAnim": idx % 3
        })

    sc["instances"] = new_world_instances + keep_instances
    print(f"Gameplay: updated instances (6 sky, 4 village, 24 terrain)")

    # 3. Update Gameplay Events: Zoom and Camera position
    for ev in sc.get("events", []):
        # Update Init Group: add ZoomCamera on start
        if ev.get("title") == "[T9] Gameplay — Inisialisasi & Timer":
            for sub in ev.get("events", []):
                conds = sub.get("conditions", [])
                if any(c.get("type", {}).get("value") == "DepartScene" for c in conds):
                    # Add Zoom actions on DepartScene
                    acts = sub.setdefault("actions", [])
                    # Clean previous zoom actions if any
                    sub["actions"] = [a for a in acts if a.get("type", {}).get("value") != "ZoomCamera"]
                    # ZoomCamera: [currentScene="", expression="2.8", layer="", camera="0"]
                    sub["actions"].extend([
                        {"type": {"value": "ZoomCamera"}, "parameters": ["", "2.8", "\"\"", "0"]},
                        {"type": {"value": "ZoomCamera"}, "parameters": ["", "2.8", "\"BG_Village\"", "0"]},
                        {"type": {"value": "ZoomCamera"}, "parameters": ["", "2.8", "\"BG_Sky\"", "0"]}
                    ])
                    print("Gameplay: added ZoomCamera 2.8x on scene start")
                    break

        # Update Camera Group: SetCameraX & SetCameraY focused on player at Y=410
        if ev.get("title") == "[T9] Gameplay — Kamera & Parallax":
            ev["events"] = [
                {
                    "type": "BuiltinCommonInstructions::Standard",
                    "conditions": [],
                    "actions": [
                        # Base layer camera: Center on player X (min 185 px), Y=410
                        {"type": {"value": "SetCameraX"}, "parameters": ["", "=", "max(185, Spr_Player.X() + 64)", "\"\"", "0"]},
                        {"type": {"value": "SetCameraY"}, "parameters": ["", "=", "410", "\"\"", "0"]},
                        # BG_Village parallax camera
                        {"type": {"value": "SetCameraX"}, "parameters": ["", "=", "185 + (max(185, Spr_Player.X() + 64) - 185) * 0.5", "\"BG_Village\"", "0"]},
                        {"type": {"value": "SetCameraY"}, "parameters": ["", "=", "410", "\"BG_Village\"", "0"]},
                        # BG_Sky camera
                        {"type": {"value": "SetCameraY"}, "parameters": ["", "=", "410", "\"BG_Sky\"", "0"]}
                    ]
                }
            ]
            print("Gameplay: Camera X & Y events updated for 2.8x zoom close-up")

# Write back
with open(PROJECT, "w", encoding="utf-8") as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print("game.json updated successfully!")
