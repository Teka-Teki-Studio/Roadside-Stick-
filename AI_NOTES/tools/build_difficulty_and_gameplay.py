"""
build_difficulty_and_gameplay.py
1. Register walk frames & environment resources to game.json
2. Setup Difficulty Modal in Lobby scene:
   - Panel background, 5 difficulty levels (Peaceful, Easy, Normal, Hard, Super Hard)
   - Left/Right arrow selector & text description
   - Confirm button -> Change Scene to Gameplay
   - Back button -> Close modal
3. Setup Gameplay scene:
   - Layers: BG_Sky, BG_Village, World, HUD
   - Backgrounds: Langit_Pagi.png, Rumah dan Pohon.png
   - Terrain: Rumput1, Rumput2, Rumput3 tiled along ground (Y=448)
   - Player object (Spr_Player) with Idle & Walk animations
   - Movement events (A/D to move & walk, Idle when stopped)
   - Camera follow player
   - HUD text (Timer, Controls, Difficulty name)
"""
import json, os

PROJECT = r"c:\Users\DELL\Downloads\Proffesionalsss\TTS\Roadside-Stick-\game.json"

with open(PROJECT, "r", encoding="utf-8") as f:
    g = json.load(f)

# -------------------------------------------------------------------
# 1. REGISTER RESOURCES
# -------------------------------------------------------------------
existing_res = {r["name"]: r for r in g["resources"]["resources"]}

def add_res(name, file_path, kind="image"):
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
        existing_res[name] = entry
        print(f"  + Resource added: {name}")

# Walk frames
for i in range(10):
    add_res(f"robi_walk_{i:02d}.png", f"ASSETS/CHARACTER/PLAYER/walk_frames/robi_walk_{i:02d}.png", "image")

# Environment
add_res("Rumput1.png", "ASSETS/ENVIRONMENT/Rumput1.png", "image")
add_res("Rumput2.png", "ASSETS/ENVIRONMENT/Rumput2.png", "image")
add_res("Rumput3.png", "ASSETS/ENVIRONMENT/Rumput3.png", "image")
add_res("Rumah_dan_Pohon.png", "ASSETS/ENVIRONMENT/Rumah dan Pohon.png", "image")
add_res("Langit_Pagi.png", "ASSETS/ENVIRONMENT/SKY/Langit_Pagi.png", "image")

# -------------------------------------------------------------------
# 2. LOBBY SCENE: SETUP DIFFICULTY MODAL
# -------------------------------------------------------------------
for sc in g["layouts"]:
    if sc["name"] != "Lobby":
        continue

    # Ensure layer 'Modals' exists
    layer_names = [l["name"] for l in sc.get("layers", [])]
    if "Modals" not in layer_names:
        sc["layers"].append({
            "ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0,
            "camera3DFarPlaneDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearPlaneDistance": 0.1,
            "cameraType": "", "effects": [], "followBaseLayerCamera": False,
            "isLightingLayer": False, "name": "Modals", "renderingType": "", "visibility": True,
            "cameras": [{"defaultAspectRatio": True, "defaultSize": True, "height": 0, "viewportBottom": 1,
                         "viewportLeft": 0, "viewportRight": 1, "viewportTop": 0, "width": 0}]
        })
        print("Lobby: layer 'Modals' added")

    obj_names = {o["name"] for o in sc.get("objects", [])}

    # Modal Dim / Background Panel (Sprite)
    if "Pnl_ModalDim" not in obj_names:
        sc["objects"].append({
            "assetStoreId": "", "name": "Pnl_ModalDim", "type": "Sprite",
            "variables": [], "behaviors": [], "effects": [],
            "animations": [{
                "name": "Normal", "useMultipleDirections": False,
                "directions": [{
                    "looping": False, "timeBetweenFrames": 1,
                    "sprites": [{
                        "hasCustomCollisionMask": False, "customCollisionMask": [],
                        "image": "DraftLoadingPXFix.png", # fallback texture
                        "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0},
                        "centerPoint": {"automatic": True, "name": "centre", "x": 640, "y": 360}
                    }]
                }]
            }]
        })

    # Difficulty Card Panel
    if "Pnl_DifficultyCard" not in obj_names:
        sc["objects"].append({
            "assetStoreId": "", "name": "Pnl_DifficultyCard", "type": "Sprite",
            "variables": [], "behaviors": [], "effects": [],
            "animations": [{
                "name": "Normal", "useMultipleDirections": False,
                "directions": [{
                    "looping": False, "timeBetweenFrames": 1,
                    "sprites": [{
                        "hasCustomCollisionMask": False, "customCollisionMask": [],
                        "image": "btn_upgrade_normal.png",
                        "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0},
                        "centerPoint": {"automatic": True, "name": "centre", "x": 210, "y": 32}
                    }]
                }]
            }]
        })

    # Text Objects for Difficulty Modal
    text_objs = [
        ("Txt_DiffTitle", "PILIH KESULITAN", 36),
        ("Txt_DiffCurrent", "NORMAL", 32),
        ("Txt_DiffDesc", "Waktu 1.7x | Tantangan Seimbang", 18),
        ("Txt_BtnConfirm", "MULAI (CONFIRM)", 20),
        ("Txt_BtnBack", "BATAL (BACK)", 18),
        ("Txt_BtnLeft", "<", 32),
        ("Txt_BtnRight", ">", 32)
    ]
    for tobj, default_text, sz in text_objs:
        if tobj not in obj_names:
            sc["objects"].append({
                "assetStoreId": "", "name": tobj, "type": "TextObject::Text",
                "variables": [], "behaviors": [], "effects": [],
                "content": {
                    "bold": True, "italic": False, "underlined": False,
                    "characterSize": sz, "color": "255;255;255",
                    "font": "vcr.ttf", "text": default_text
                }
            })

    # Buttons for Modal
    modal_btns = [
        ("Btn_DiffConfirm", "btn_play_normal.png", "btn_play_hover.png", "btn_play_pressed.png"),
        ("Btn_DiffBack", "btn_index_normal.png", "btn_index_hover.png", "btn_index_pressed.png"),
        ("Btn_DiffPrev", "btn_shop_normal.png", "btn_shop_hover.png", "btn_shop_pressed.png"),
        ("Btn_DiffNext", "btn_shop_normal.png", "btn_shop_hover.png", "btn_shop_pressed.png"),
    ]
    for bname, norm, hov, prs in modal_btns:
        if bname not in obj_names:
            sc["objects"].append({
                "assetStoreId": "", "name": bname, "type": "Sprite",
                "variables": [], "behaviors": [], "effects": [],
                "animations": [
                    {"name": "Normal", "useMultipleDirections": False, "directions": [{"looping": False, "timeBetweenFrames": 1, "sprites": [{"hasCustomCollisionMask": False, "customCollisionMask": [], "image": norm, "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 32, "y": 16}}]}]},
                    {"name": "Hover", "useMultipleDirections": False, "directions": [{"looping": False, "timeBetweenFrames": 1, "sprites": [{"hasCustomCollisionMask": False, "customCollisionMask": [], "image": hov, "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 32, "y": 16}}]}]},
                    {"name": "Pressed", "useMultipleDirections": False, "directions": [{"looping": False, "timeBetweenFrames": 1, "sprites": [{"hasCustomCollisionMask": False, "customCollisionMask": [], "image": prs, "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 32, "y": 16}}]}]}
                ]
            })

    # Add modal instances on layer 'Modals' (hidden by default)
    # Centered in 1024x576
    modal_instances = [
        # Dim overlay
        {"name": "Pnl_ModalDim", "x": 0, "y": 0, "width": 1024, "height": 576, "layer": "Modals", "zOrder": 1, "customSize": True},
        # Center Box
        {"name": "Pnl_DifficultyCard", "x": 232, "y": 108, "width": 560, "height": 360, "layer": "Modals", "zOrder": 2, "customSize": True},
        # Title
        {"name": "Txt_DiffTitle", "x": 360, "y": 136, "layer": "Modals", "zOrder": 3, "customSize": False},
        # Selector Left / Right
        {"name": "Btn_DiffPrev", "x": 310, "y": 210, "width": 64, "height": 56, "layer": "Modals", "zOrder": 3, "customSize": True},
        {"name": "Txt_BtnLeft", "x": 332, "y": 218, "layer": "Modals", "zOrder": 4, "customSize": False},
        {"name": "Txt_DiffCurrent", "x": 450, "y": 218, "layer": "Modals", "zOrder": 3, "customSize": False},
        {"name": "Btn_DiffNext", "x": 650, "y": 210, "width": 64, "height": 56, "layer": "Modals", "zOrder": 3, "customSize": True},
        {"name": "Txt_BtnRight", "x": 672, "y": 218, "layer": "Modals", "zOrder": 4, "customSize": False},
        # Description
        {"name": "Txt_DiffDesc", "x": 310, "y": 286, "layer": "Modals", "zOrder": 3, "customSize": False},
        # Confirm & Back Buttons
        {"name": "Btn_DiffConfirm", "x": 524, "y": 360, "width": 240, "height": 56, "layer": "Modals", "zOrder": 3, "customSize": True},
        {"name": "Txt_BtnConfirm", "x": 554, "y": 376, "layer": "Modals", "zOrder": 4, "customSize": False},
        {"name": "Btn_DiffBack", "x": 260, "y": 360, "width": 220, "height": 56, "layer": "Modals", "zOrder": 3, "customSize": True},
        {"name": "Txt_BtnBack", "x": 300, "y": 378, "layer": "Modals", "zOrder": 4, "customSize": False},
    ]

    # Clean previous modal instances if any
    modal_inst_names = {i["name"] for i in modal_instances}
    sc["instances"] = [inst for inst in sc.get("instances", []) if inst.get("name") not in modal_inst_names]
    for minst in modal_instances:
        sc["instances"].append({
            "name": minst["name"], "x": minst["x"], "y": minst["y"],
            "width": minst.get("width", 100), "height": minst.get("height", 30),
            "customSize": minst["customSize"], "layer": minst["layer"],
            "zOrder": minst["zOrder"], "angle": 0, "locked": False
        })
    print(f"Lobby: {len(modal_instances)} modal instances placed on layer 'Modals'")

    # Setup Lobby Events for Difficulty Modal
    # Scene Variables needed:
    # ModalOpen (0/1), SelectedDiff (0..4)
    # Check scene variables
    s_vars = {v["name"]: v for v in sc.get("variables", [])}
    if "ModalOpen" not in s_vars:
        sc["variables"].append({"name": "ModalOpen", "value": 0})
    if "SelectedDiff" not in s_vars:
        sc["variables"].append({"name": "SelectedDiff", "value": 2}) # 2 = Normal

    # Remove previous difficulty event group if any
    sc["events"] = [ev for ev in sc.get("events", []) if ev.get("title") != "[T5] Lobby — Modal Difficulty"]

    diff_group = {
        "type": "BuiltinCommonInstructions::Group",
        "title": "[T5] Lobby — Modal Difficulty",
        "parameters": [""],
        "events": [
            # 1. On Start: Hide layer Modals, set dim opacity to 200
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [{"type": {"value": "DepartScene"}, "parameters": []}],
                "actions": [
                    {"type": {"value": "HideLayer"}, "parameters": ["", "\"Modals\""]},
                    {"type": {"value": "ChangeOpacity"}, "parameters": ["Pnl_ModalDim", "=", "200"]}
                ]
            },
            # 2. Click Btn_Play -> Open Modal Difficulty
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {"type": {"value": "SourisSurObjet"}, "parameters": ["Btn_Play", "", "", ""]},
                    {"type": {"value": "MouseButtonReleased"}, "parameters": ["", "Left"]},
                    {"type": {"value": "VarScene"}, "parameters": ["ModalOpen", "=", "0"]}
                ],
                "actions": [
                    {"type": {"value": "ModVarScene"}, "parameters": ["ModalOpen", "=", "1"]},
                    {"type": {"value": "ShowLayer"}, "parameters": ["", "\"Modals\""]}
                ]
            },
            # 3. Click Btn_DiffBack -> Close Modal
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {"type": {"value": "SourisSurObjet"}, "parameters": ["Btn_DiffBack", "", "", ""]},
                    {"type": {"value": "MouseButtonReleased"}, "parameters": ["", "Left"]},
                    {"type": {"value": "VarScene"}, "parameters": ["ModalOpen", "=", "1"]}
                ],
                "actions": [
                    {"type": {"value": "ModVarScene"}, "parameters": ["ModalOpen", "=", "0"]},
                    {"type": {"value": "HideLayer"}, "parameters": ["", "\"Modals\""]}
                ]
            },
            # 4. Click Prev (<) Difficulty
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {"type": {"value": "SourisSurObjet"}, "parameters": ["Btn_DiffPrev", "", "", ""]},
                    {"type": {"value": "MouseButtonReleased"}, "parameters": ["", "Left"]},
                    {"type": {"value": "VarScene"}, "parameters": ["ModalOpen", "=", "1"]},
                    {"type": {"value": "VarScene"}, "parameters": ["SelectedDiff", ">", "0"]}
                ],
                "actions": [
                    {"type": {"value": "ModVarScene"}, "parameters": ["SelectedDiff", "-", "1"]}
                ]
            },
            # 5. Click Next (>) Difficulty
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {"type": {"value": "SourisSurObjet"}, "parameters": ["Btn_DiffNext", "", "", ""]},
                    {"type": {"value": "MouseButtonReleased"}, "parameters": ["", "Left"]},
                    {"type": {"value": "VarScene"}, "parameters": ["ModalOpen", "=", "1"]},
                    {"type": {"value": "VarScene"}, "parameters": ["SelectedDiff", "<", "4"]}
                ],
                "actions": [
                    {"type": {"value": "ModVarScene"}, "parameters": ["SelectedDiff", "+", "1"]}
                ]
            },
            # 6. Update Difficulty Text based on SelectedDiff
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {"type": {"value": "VarScene"}, "parameters": ["SelectedDiff", "=", "0"]}
                ],
                "actions": [
                    {"type": {"value": "ChangeText"}, "parameters": ["Txt_DiffCurrent", "=", "\"PEACEFUL\""]},
                    {"type": {"value": "ChangeText"}, "parameters": ["Txt_DiffDesc", "=", "\"Waktu 3.0x | Santai tanpa tekanan\""]}
                ]
            },
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {"type": {"value": "VarScene"}, "parameters": ["SelectedDiff", "=", "1"]}
                ],
                "actions": [
                    {"type": {"value": "ChangeText"}, "parameters": ["Txt_DiffCurrent", "=", "\"EASY\""]},
                    {"type": {"value": "ChangeText"}, "parameters": ["Txt_DiffDesc", "=", "\"Waktu 2.2x | Cukup longgar\""]}
                ]
            },
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {"type": {"value": "VarScene"}, "parameters": ["SelectedDiff", "=", "2"]}
                ],
                "actions": [
                    {"type": {"value": "ChangeText"}, "parameters": ["Txt_DiffCurrent", "=", "\"NORMAL\""]},
                    {"type": {"value": "ChangeText"}, "parameters": ["Txt_DiffDesc", "=", "\"Waktu 1.7x | Tantangan seimbang\""]}
                ]
            },
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {"type": {"value": "VarScene"}, "parameters": ["SelectedDiff", "=", "3"]}
                ],
                "actions": [
                    {"type": {"value": "ChangeText"}, "parameters": ["Txt_DiffCurrent", "=", "\"HARD\""]},
                    {"type": {"value": "ChangeText"}, "parameters": ["Txt_DiffDesc", "=", "\"Waktu 1.35x | Waktu lebih ketat\""]}
                ]
            },
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {"type": {"value": "VarScene"}, "parameters": ["SelectedDiff", "=", "4"]}
                ],
                "actions": [
                    {"type": {"value": "ChangeText"}, "parameters": ["Txt_DiffCurrent", "=", "\"SUPER HARD\""]},
                    {"type": {"value": "ChangeText"}, "parameters": ["Txt_DiffDesc", "=", "\"Waktu 1.15x | Sangat terbatas!\""]}
                ]
            },
            # 7. Click Confirm -> Save difficulty & ChangeScene to Gameplay
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {"type": {"value": "SourisSurObjet"}, "parameters": ["Btn_DiffConfirm", "", "", ""]},
                    {"type": {"value": "MouseButtonReleased"}, "parameters": ["", "Left"]},
                    {"type": {"value": "VarScene"}, "parameters": ["ModalOpen", "=", "1"]}
                ],
                "actions": [
                    {"type": {"value": "ModVarGlobal"}, "parameters": ["Run.difficulty", "=", "Variable(SelectedDiff)"]},
                    {"type": {"value": "PushScene"}, "parameters": ["", "\"Gameplay\""]}
                ]
            }
        ]
    }
    sc["events"].append(diff_group)
    print("Lobby: Difficulty modal events configured!")


# -------------------------------------------------------------------
# 3. GAMEPLAY SCENE SETUP
# -------------------------------------------------------------------
for sc in g["layouts"]:
    if sc["name"] != "Gameplay":
        continue

    # Setup layers: BG_Sky, BG_Village, World, HUD
    sc["layers"] = [
        {"ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0, "camera3DFarPlaneDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearPlaneDistance": 0.1, "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False, "name": "BG_Sky", "renderingType": "", "visibility": True, "cameras": [{"defaultAspectRatio": True, "defaultSize": True, "height": 0, "viewportBottom": 1, "viewportLeft": 0, "viewportRight": 1, "viewportTop": 0, "width": 0}]},
        {"ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0, "camera3DFarPlaneDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearPlaneDistance": 0.1, "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False, "name": "BG_Village", "renderingType": "", "visibility": True, "cameras": [{"defaultAspectRatio": True, "defaultSize": True, "height": 0, "viewportBottom": 1, "viewportLeft": 0, "viewportRight": 1, "viewportTop": 0, "width": 0}]},
        {"ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0, "camera3DFarPlaneDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearPlaneDistance": 0.1, "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False, "name": "", "renderingType": "", "visibility": True, "cameras": [{"defaultAspectRatio": True, "defaultSize": True, "height": 0, "viewportBottom": 1, "viewportLeft": 0, "viewportRight": 1, "viewportTop": 0, "width": 0}]},
        {"ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0, "camera3DFarPlaneDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearPlaneDistance": 0.1, "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False, "name": "HUD", "renderingType": "", "visibility": True, "cameras": [{"defaultAspectRatio": True, "defaultSize": True, "height": 0, "viewportBottom": 1, "viewportLeft": 0, "viewportRight": 1, "viewportTop": 0, "width": 0}]}
    ]

    # Gameplay Objects
    gp_objects = []

    # 1. Sky Background (Sprite stretched or repeating)
    gp_objects.append({
        "assetStoreId": "", "name": "Spr_Sky", "type": "Sprite",
        "variables": [], "behaviors": [], "effects": [],
        "animations": [{"name": "Normal", "useMultipleDirections": False, "directions": [{"looping": False, "timeBetweenFrames": 1, "sprites": [{"hasCustomCollisionMask": False, "customCollisionMask": [], "image": "Langit_Pagi.png", "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 512, "y": 128}}]}]}]
    })

    # 2. Village / Houses Background
    gp_objects.append({
        "assetStoreId": "", "name": "Spr_Village", "type": "Sprite",
        "variables": [], "behaviors": [], "effects": [],
        "animations": [{"name": "Normal", "useMultipleDirections": False, "directions": [{"looping": False, "timeBetweenFrames": 1, "sprites": [{"hasCustomCollisionMask": False, "customCollisionMask": [], "image": "Rumah_dan_Pohon.png", "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 768, "y": 128}}]}]}]
    })

    # 3. Terrain Tiles (Spr_Terrain with animations for Rumput1, Rumput2, Rumput3)
    gp_objects.append({
        "assetStoreId": "", "name": "Spr_Terrain", "type": "Sprite",
        "variables": [], "behaviors": [], "effects": [],
        "animations": [
            {"name": "Rumput1", "useMultipleDirections": False, "directions": [{"looping": False, "timeBetweenFrames": 1, "sprites": [{"hasCustomCollisionMask": False, "customCollisionMask": [], "image": "Rumput1.png", "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 128, "y": 64}}]}]},
            {"name": "Rumput2", "useMultipleDirections": False, "directions": [{"looping": False, "timeBetweenFrames": 1, "sprites": [{"hasCustomCollisionMask": False, "customCollisionMask": [], "image": "Rumput2.png", "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 128, "y": 64}}]}]},
            {"name": "Rumput3", "useMultipleDirections": False, "directions": [{"looping": False, "timeBetweenFrames": 1, "sprites": [{"hasCustomCollisionMask": False, "customCollisionMask": [], "image": "Rumput3.png", "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 128, "y": 64}}]}]}
        ]
    })

    # 4. Player Object (Spr_Player with Idle and Walk animations)
    idle_sprites = []
    for i in range(10):
        idle_sprites.append({"hasCustomCollisionMask": False, "customCollisionMask": [], "image": f"robi_idle_{i:02d}.png", "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 64, "y": 64}})

    walk_sprites = []
    for i in range(10):
        walk_sprites.append({"hasCustomCollisionMask": False, "customCollisionMask": [], "image": f"robi_walk_{i:02d}.png", "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 64, "y": 64}})

    gp_objects.append({
        "assetStoreId": "", "name": "Spr_Player", "type": "Sprite",
        "variables": [], "behaviors": [], "effects": [],
        "animations": [
            {"name": "Idle", "useMultipleDirections": False, "directions": [{"looping": True, "timeBetweenFrames": 0.12, "sprites": idle_sprites}]},
            {"name": "Walk", "useMultipleDirections": False, "directions": [{"looping": True, "timeBetweenFrames": 0.10, "sprites": walk_sprites}]}
        ]
    })

    # 5. HUD Text Objects
    hud_texts = [
        ("Txt_HUDTimer", "SISA WAKTU: 60s", 24),
        ("Txt_HUDControls", "KONTROL: [A/D] Jalan | [ESC] Pause", 16),
        ("Txt_HUDLevel", "PERJALANAN PULANG #1", 20)
    ]
    for hname, htxt, hsz in hud_texts:
        gp_objects.append({
            "assetStoreId": "", "name": hname, "type": "TextObject::Text",
            "variables": [], "behaviors": [], "effects": [],
            "content": {
                "bold": True, "italic": False, "underlined": False,
                "characterSize": hsz, "color": "255;255;255",
                "font": "vcr.ttf", "text": htxt
            }
        })

    sc["objects"] = gp_objects

    # Gameplay Instances
    gp_instances = []

    # Sky instances (cover 0 to 4000)
    for k in range(4):
        gp_instances.append({
            "name": "Spr_Sky", "x": k * 1024, "y": 0, "width": 1024, "height": 300,
            "customSize": True, "layer": "BG_Sky", "zOrder": 1, "angle": 0, "locked": False
        })

    # Village instances along the path (Y=192 so bottom sits at ground Y=448)
    for k in range(3):
        gp_instances.append({
            "name": "Spr_Village", "x": k * 1536, "y": 192, "width": 1536, "height": 256,
            "customSize": True, "layer": "BG_Village", "zOrder": 2, "angle": 0, "locked": False
        })

    # Terrain tiles (Rumput1, 2, 3 alternating) along ground Y=448 (width 256, height 128)
    # Covering X: 0 up to 3840 (15 tiles)
    for idx in range(16):
        gp_instances.append({
            "name": "Spr_Terrain", "x": idx * 256, "y": 448, "width": 256, "height": 128,
            "customSize": True, "layer": "", "zOrder": 5, "angle": 0, "locked": False
        })

    # Player instance
    # Player starts at x=150, y=368 (height 128, feet at 368+80=448 ground)
    gp_instances.append({
        "name": "Spr_Player", "x": 150, "y": 368, "width": 128, "height": 128,
        "customSize": False, "layer": "", "zOrder": 10, "angle": 0, "locked": False
    })

    # HUD instances
    gp_instances.append({
        "name": "Txt_HUDLevel", "x": 32, "y": 24, "width": 300, "height": 30,
        "customSize": False, "layer": "HUD", "zOrder": 1, "angle": 0, "locked": False
    })
    gp_instances.append({
        "name": "Txt_HUDTimer", "x": 740, "y": 24, "width": 250, "height": 30,
        "customSize": False, "layer": "HUD", "zOrder": 1, "angle": 0, "locked": False
    })
    gp_instances.append({
        "name": "Txt_HUDControls", "x": 32, "y": 64, "width": 400, "height": 24,
        "customSize": False, "layer": "HUD", "zOrder": 1, "angle": 0, "locked": False
    })

    sc["instances"] = gp_instances

    # Setup Gameplay Scene Variables
    sc["variables"] = [
        {"name": "TimeRemaining", "value": 60},
        {"name": "IsMoving", "value": 0}
    ]

    # Setup Gameplay Events
    sc["events"] = [
        # Group 1: Init Gameplay
        {
            "type": "BuiltinCommonInstructions::Group",
            "title": "[T9] Gameplay — Inisialisasi & Timer",
            "parameters": [""],
            "events": [
                {
                    "type": "BuiltinCommonInstructions::Standard",
                    "conditions": [{"type": {"value": "DepartScene"}, "parameters": []}],
                    "actions": [
                        # Set initial timer based on difficulty: 60s * multiplier
                        {"type": {"value": "ModVarScene"}, "parameters": ["TimeRemaining", "=", "75"]},
                        # Stop previous menu music, play gameplay ambiance
                        {"type": {"value": "StopMusicChannel"}, "parameters": ["", "1"]}
                    ]
                },
                # Countdown Timer every frame
                {
                    "type": "BuiltinCommonInstructions::Standard",
                    "conditions": [
                        {"type": {"value": "VarScene"}, "parameters": ["TimeRemaining", ">", "0"]}
                    ],
                    "actions": [
                        {"type": {"value": "ModVarScene"}, "parameters": ["TimeRemaining", "-", "TimeDelta()"]},
                        {"type": {"value": "ChangeText"}, "parameters": ["Txt_HUDTimer", "=", "\"SISA WAKTU: \" + ToString(ceil(Variable(TimeRemaining))) + \"s\""]}
                    ]
                }
            ]
        },
        # Group 2: Player Movement (A/D or Left/Right Arrow)
        {
            "type": "BuiltinCommonInstructions::Group",
            "title": "[T10] Gameplay — Kontrol Pergerakan Robi",
            "parameters": [""],
            "events": [
                # Reset IsMoving flag every frame
                {
                    "type": "BuiltinCommonInstructions::Standard",
                    "conditions": [],
                    "actions": [
                        {"type": {"value": "ModVarScene"}, "parameters": ["IsMoving", "=", "0"]}
                    ]
                },
                # Move Right (D or Right Key)
                {
                    "type": "BuiltinCommonInstructions::Standard",
                    "conditions": [
                        {"type": {"value": "KeyPressed"}, "parameters": ["", "d"]}
                    ],
                    "actions": [
                        {"type": {"value": "SetX"}, "parameters": ["Spr_Player", "+", "160 * TimeDelta()"]},
                        {"type": {"value": "SetAnimationName"}, "parameters": ["Spr_Player", "\"Walk\""]},
                        {"type": {"value": "FlipX"}, "parameters": ["Spr_Player", "no"]},
                        {"type": {"value": "ModVarScene"}, "parameters": ["IsMoving", "=", "1"]}
                    ]
                },
                # Move Left (A or Left Key)
                {
                    "type": "BuiltinCommonInstructions::Standard",
                    "conditions": [
                        {"type": {"value": "KeyPressed"}, "parameters": ["", "a"]}
                    ],
                    "actions": [
                        {"type": {"value": "SetX"}, "parameters": ["Spr_Player", "-", "160 * TimeDelta()"]},
                        {"type": {"value": "SetAnimationName"}, "parameters": ["Spr_Player", "\"Walk\""]},
                        {"type": {"value": "FlipX"}, "parameters": ["Spr_Player", "yes"]},
                        {"type": {"value": "ModVarScene"}, "parameters": ["IsMoving", "=", "1"]}
                    ]
                },
                # When not moving -> set animation to Idle
                {
                    "type": "BuiltinCommonInstructions::Standard",
                    "conditions": [
                        {"type": {"value": "VarScene"}, "parameters": ["IsMoving", "=", "0"]}
                    ],
                    "actions": [
                        {"type": {"value": "SetAnimationName"}, "parameters": ["Spr_Player", "\"Idle\""]}
                    ]
                },
                # Prevent player from going left beyond X=50
                {
                    "type": "BuiltinCommonInstructions::Standard",
                    "conditions": [
                        {"type": {"value": "XPosition"}, "parameters": ["Spr_Player", "<", "50"]}
                    ],
                    "actions": [
                        {"type": {"value": "SetX"}, "parameters": ["Spr_Player", "=", "50"]}
                    ]
                }
            ]
        },
        # Group 3: Camera Following Player
        {
            "type": "BuiltinCommonInstructions::Group",
            "title": "[T9] Gameplay — Kamera & Parallax",
            "parameters": [""],
            "events": [
                {
                    "type": "BuiltinCommonInstructions::Standard",
                    "conditions": [],
                    "actions": [
                        # Center camera on player X, minimum camera X = 512
                        {"type": {"value": "SetCameraX"}, "parameters": ["", "=", "max(512, Spr_Player.X() + 64)", "\"\"", "0"]},
                        # Camera for BG_Village with 0.5 parallax factor
                        {"type": {"value": "SetCameraX"}, "parameters": ["", "=", "512 + (max(512, Spr_Player.X() + 64) - 512) * 0.5", "\"BG_Village\"", "0"]}
                    ]
                }
            ]
        },
        # Group 4: Pause / Return to Lobby via ESC
        {
            "type": "BuiltinCommonInstructions::Group",
            "title": "[T12] Gameplay — Pause / Menu",
            "parameters": [""],
            "events": [
                {
                    "type": "BuiltinCommonInstructions::Standard",
                    "conditions": [
                        {"type": {"value": "KeyReleased"}, "parameters": ["", "Escape"]}
                    ],
                    "actions": [
                        {"type": {"value": "PushScene"}, "parameters": ["", "\"Lobby\""]}
                    ]
                }
            ]
        }
    ]

    print("Gameplay scene fully configured!")

# -------------------------------------------------------------------
# 4. SAVE BACK
# -------------------------------------------------------------------
with open(PROJECT, "w", encoding="utf-8") as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print("\nAll changes saved to game.json successfully!")
