"""
apply_fixes_v4.py
1. Clean frame 0 of idle animation (remove yellow 'IDLE' text stray pixels)
2. Scale down Boot logo (480x108, centered)
3. Update Loading scene:
   - BG -> BGLoadingPX.png (256x144 pixel-art sharp, instance 1024x576)
   - Add Game Logo -> Logo Gam.png in top-left with margin (x=36, y=28, 280x180)
4. Update Lobby scene:
   - Remove Robi breathe effect (SetX, SetY)
   - Zoom Robi waist-up (scale 16x, centered waist-up on left screen)
"""
import json, os, shutil
from PIL import Image

PROJECT = r"c:\Users\DELL\Downloads\Proffesionalsss\TTS\Roadside-Stick-\game.json"

# -------------------------------------------------------------
# 1. CLEAN & RE-GENERATE 10 IDLE FRAMES
# -------------------------------------------------------------
sheet_path = r"ASSETS\CHARACTER\PLAYER\robi_sd.png"
out_dir = r"ASSETS\CHARACTER\PLAYER\idle_frames"
os.makedirs(out_dir, exist_ok=True)

sheet = Image.open(sheet_path)
for col in range(10):
    cell = sheet.crop((col * 128, 128, col * 128 + 128, 256))
    if col == 0:
        # Clear stray yellow label pixels in x < 48
        pix = cell.load()
        for x in range(48):
            for y in range(128):
                pix[x, y] = (0, 0, 0, 0)
    out_file = os.path.join(out_dir, f"robi_idle_{col:02d}.png")
    cell.save(out_file)
    print(f"Saved clean idle frame: {out_file}")

# -------------------------------------------------------------
# 2. UPDATE GAME.JSON
# -------------------------------------------------------------
with open(PROJECT, "r", encoding="utf-8") as f:
    g = json.load(f)

# Resources check
existing_res = {r["name"] for r in g["resources"]["resources"]}

def add_resource(name, file_path, kind="image"):
    if name not in existing_res:
        entry = {
            "alwaysLoaded": False,
            "file": file_path,
            "kind": kind,
            "metadata": "",
            "name": name,
            "userAdded": True
        }
        if kind == "image":
            entry["smoothed"] = False
        g["resources"]["resources"].append(entry)
        existing_res.add(name)
        print(f"  + Resource added: {name}")

add_resource("BGLoadingPX.png", "ASSETS/BOOT/LOADING/BGLoadingPX.png", "image")
add_resource("Logo Gam.png", "ASSETS/BOOT/LOADING/Logo Gam.png", "image")

# -------------------------------------------------------------
# 3. BOOT SCENE: KECILKAN LOGO DEVELOPER
# -------------------------------------------------------------
for sc in g["layouts"]:
    if sc["name"] == "Boot":
        # Logo asli 2213x496. Jadikan 480x108 px (proporsional), centered di 1024x576
        # X: (1024 - 480) / 2 = 272, Y: (576 - 108) / 2 = 234
        for inst in sc.get("instances", []):
            if inst.get("name") == "Spr_BootLogo":
                inst["x"] = 272
                inst["y"] = 234
                inst["width"] = 480
                inst["height"] = 108
                inst["customSize"] = True
                print(f"Boot logo resized: pos ({inst['x']},{inst['y']}) size {inst['width']}x{inst['height']}")

# -------------------------------------------------------------
# 4. LOADING SCENE: BG KOSONGAN + LOGO GAME DI KIRI ATAS
# -------------------------------------------------------------
for sc in g["layouts"]:
    if sc["name"] == "Loading":
        # 1. Update background image -> BGLoadingPX.png
        for obj in sc.get("objects", []):
            if obj.get("name") == "Spr_LoadingBg":
                for anim in obj.get("animations", []):
                    for d in anim.get("directions", []):
                        for spr in d.get("sprites", []):
                            spr["image"] = "BGLoadingPX.png"
                            print("Loading BG updated to BGLoadingPX.png")

        # 2. Add Spr_LoadingLogo object if not exists
        has_logo_obj = any(o.get("name") == "Spr_LoadingLogo" for o in sc.get("objects", []))
        if not has_logo_obj:
            logo_obj = {
                "assetStoreId": "",
                "name": "Spr_LoadingLogo",
                "type": "Sprite",
                "variables": [], "behaviors": [], "effects": [],
                "animations": [{
                    "name": "Normal",
                    "useMultipleDirections": False,
                    "directions": [{
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [{
                            "hasCustomCollisionMask": False,
                            "customCollisionMask": [],
                            "image": "Logo Gam.png",
                            "points": [],
                            "originPoint": {"name": "origine", "x": 0, "y": 0},
                            "centerPoint": {"automatic": True, "name": "centre", "x": 166, "y": 107}
                        }]
                    }]
                }]
            }
            sc.setdefault("objects", []).append(logo_obj)
            print("Created Spr_LoadingLogo object")

        # 3. Add instance for Spr_LoadingLogo at top-left with margin
        # Original size: 333x214. Scale to ~260x167 with margin (x=36, y=28)
        has_logo_inst = any(i.get("name") == "Spr_LoadingLogo" for i in sc.get("instances", []))
        if not has_logo_inst:
            sc.setdefault("instances", []).append({
                "name": "Spr_LoadingLogo",
                "x": 36, "y": 28,
                "width": 260, "height": 167,
                "customSize": True,
                "layer": "Base",
                "zOrder": 10,
                "angle": 0,
                "locked": False
            })
            print("Added Spr_LoadingLogo instance at (36, 28) size 260x167")

# -------------------------------------------------------------
# 5. LOBBY SCENE: ROBI ZOOM WAIST-UP & HAPUS EFEK NAFAS
# -------------------------------------------------------------
for sc in g["layouts"]:
    if sc["name"] == "Lobby":
        # 1. Update instance Spr_PlayerLobby to zoom waist-up
        # Robi in 128x128 cell: head y=48, waist y=74 (height 26).
        # We want scale ~17x: width = 2176, height = 2176
        # When y_char = 48 -> top of screen y=110: y_inst = 110 - (48 * 17) = 110 - 816 = -706
        # When x_char = 52 -> left screen x=30: x_inst = 30 - (52 * 17) = 30 - 884 = -854
        for inst in sc.get("instances", []):
            if inst.get("name") == "Spr_PlayerLobby":
                inst["x"] = -854
                inst["y"] = -706
                inst["width"] = 2176
                inst["height"] = 2176
                inst["customSize"] = True
                print(f"Lobby Robi instance zoomed waist-up: pos ({inst['x']},{inst['y']}) size {inst['width']}x{inst['height']}")

        # 2. Remove breath/float movement (SetX, SetY) from VFX group
        lobby_events = sc.get("events", [])
        for ev in lobby_events:
            if ev.get("title") == "[T3] Lobby — VFX & Efek Hidup":
                # Filter out SetX and SetY actions on Spr_PlayerLobby
                ev["events"] = [sub for sub in ev.get("events", [])
                                if not any(a.get("type", {}).get("value") in ("SetX", "SetY")
                                           for a in sub.get("actions", []))]
                print("Removed breathe/float effect from Lobby VFX")
                break

# -------------------------------------------------------------
# 6. WRITE BACK TO GAME.JSON
# -------------------------------------------------------------
with open(PROJECT, "w", encoding="utf-8") as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print("game.json updated successfully!")
