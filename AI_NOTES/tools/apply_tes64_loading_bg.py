"""
apply_tes64_loading_bg.py
Ganti background Loading scene menjadi Tes64.png
"""
import json

PROJECT = r"c:\Users\DELL\Downloads\Proffesionalsss\TTS\Roadside-Stick-\game.json"

with open(PROJECT, "r", encoding="utf-8") as f:
    g = json.load(f)

# 1. Register resource Tes64.png
existing_res = {r["name"]: r for r in g["resources"]["resources"]}

if "Tes64.png" not in existing_res:
    g["resources"]["resources"].append({
        "alwaysLoaded": False,
        "file": "ASSETS/BOOT/LOADING/Tes64.png",
        "kind": "image",
        "metadata": "",
        "name": "Tes64.png",
        "smoothed": False,
        "userAdded": True
    })
    print("Resource Tes64.png added (smoothed=False)")
else:
    existing_res["Tes64.png"]["file"] = "ASSETS/BOOT/LOADING/Tes64.png"
    existing_res["Tes64.png"]["smoothed"] = False
    print("Resource Tes64.png updated")

# 2. Update Loading layout
for sc in g["layouts"]:
    if sc["name"] == "Loading":
        # Update Spr_LoadingBg object animation
        for obj in sc.get("objects", []):
            if obj.get("name") == "Spr_LoadingBg":
                for anim in obj.get("animations", []):
                    for d in anim.get("directions", []):
                        for spr in d.get("sprites", []):
                            spr["image"] = "Tes64.png"
                            print("Spr_LoadingBg sprite image set to Tes64.png")

        # Update instance to cover 1024x576
        for inst in sc.get("instances", []):
            if inst.get("name") == "Spr_LoadingBg":
                inst["x"] = 0
                inst["y"] = 0
                inst["width"] = 1024
                inst["height"] = 576
                inst["customSize"] = True
                print("Spr_LoadingBg instance updated: 1024x576 at (0,0)")

# 3. Write back
with open(PROJECT, "w", encoding="utf-8") as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print("game.json updated successfully with Tes64.png!")
