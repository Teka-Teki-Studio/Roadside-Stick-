import json, copy

PROJECT = r"c:\Users\DELL\Downloads\Proffesionalsss\TTS\Roadside-Stick-\game.json"

with open(PROJECT, 'r', encoding='utf-8') as f:
    g = json.load(f)

# 1. Register new resources
new_images = [
    ("bg_lobby.png", "ASSETS/LOBBY/bg_lobby.png"),
    ("robi_lobby_waistup.png", "ASSETS/CHARACTER/PLAYER/robi_lobby_waistup.png"),
    ("btn_play_normal.png", "ASSETS/UI/BUTTONS/btn_play_normal.png"),
    ("btn_play_hover.png", "ASSETS/UI/BUTTONS/btn_play_hover.png"),
    ("btn_play_pressed.png", "ASSETS/UI/BUTTONS/btn_play_pressed.png"),
    ("btn_shop_normal.png", "ASSETS/UI/BUTTONS/btn_shop_normal.png"),
    ("btn_shop_hover.png", "ASSETS/UI/BUTTONS/btn_shop_hover.png"),
    ("btn_shop_pressed.png", "ASSETS/UI/BUTTONS/btn_shop_pressed.png"),
    ("btn_index_normal.png", "ASSETS/UI/BUTTONS/btn_index_normal.png"),
    ("btn_index_hover.png", "ASSETS/UI/BUTTONS/btn_index_hover.png"),
    ("btn_index_pressed.png", "ASSETS/UI/BUTTONS/btn_index_pressed.png"),
    ("btn_upgrade_normal.png", "ASSETS/UI/BUTTONS/btn_upgrade_normal.png"),
    ("btn_upgrade_hover.png", "ASSETS/UI/BUTTONS/btn_upgrade_hover.png"),
    ("btn_upgrade_pressed.png", "ASSETS/UI/BUTTONS/btn_upgrade_pressed.png"),
]

existing_res_names = {r.get('name') for r in g['resources']['resources']}
for name, file_path in new_images:
    if name not in existing_res_names:
        g['resources']['resources'].append({
            "alwaysLoaded": False,
            "file": file_path,
            "kind": "image",
            "metadata": "",
            "name": name,
            "smoothed": False,
            "userAdded": True
        })
        existing_res_names.add(name)

# 2. Helper to create 3-state Button Object
def create_button_object(btn_name, prefix, w, h):
    return {
        "assetStoreId": "",
        "name": btn_name,
        "type": "Sprite",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "animations": [
            {
                "name": "Normal",
                "useMultipleDirections": False,
                "directions": [{
                    "looping": False,
                    "timeBetweenFrames": 1,
                    "sprites": [{
                        "hasCustomCollisionMask": False,
                        "customCollisionMask": [],
                        "image": f"{prefix}_normal.png",
                        "points": [],
                        "originPoint": {"name": "origine", "x": 0, "y": 0},
                        "centerPoint": {"automatic": True, "name": "centre", "x": w//2, "y": h//2}
                    }]
                }]
            },
            {
                "name": "Hover",
                "useMultipleDirections": False,
                "directions": [{
                    "looping": False,
                    "timeBetweenFrames": 1,
                    "sprites": [{
                        "hasCustomCollisionMask": False,
                        "customCollisionMask": [],
                        "image": f"{prefix}_hover.png",
                        "points": [],
                        "originPoint": {"name": "origine", "x": 0, "y": 0},
                        "centerPoint": {"automatic": True, "name": "centre", "x": w//2, "y": h//2}
                    }]
                }]
            },
            {
                "name": "Pressed",
                "useMultipleDirections": False,
                "directions": [{
                    "looping": False,
                    "timeBetweenFrames": 1,
                    "sprites": [{
                        "hasCustomCollisionMask": False,
                        "customCollisionMask": [],
                        "image": f"{prefix}_pressed.png",
                        "points": [],
                        "originPoint": {"name": "origine", "x": 0, "y": 0},
                        "centerPoint": {"automatic": True, "name": "centre", "x": w//2, "y": h//2}
                    }]
                }]
            }
        ]
    }

# 3. Helper to create Text Object
def create_text_object(name, initial_str, size=24, align="center"):
    return {
        "assetStoreId": "",
        "name": name,
        "type": "TextObject::Text",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "bold": True,
        "italic": False,
        "underlined": False,
        "color": "255;255;255",
        "fontResourceName": "vcr.ttf",
        "size": size,
        "string": initial_str,
        "isOutlineEnabled": False,
        "outlineThickness": 0,
        "outlineColor": "0;0;0",
        "isShadowEnabled": False,
        "shadowAngle": 90,
        "shadowDistance": 0,
        "shadowColor": "0;0;0",
        "shadowOpacity": 0
    }

# Find Lobby layout
lobby = None
for sc in g['layouts']:
    if sc['name'] == 'Lobby':
        lobby = sc
        break

if not lobby:
    print("Scene Lobby not found!")
    exit(1)

# Ensure layers: Base, UI, Modals
existing_layer_names = [l.get('name') for l in lobby.get('layers', [])]
if 'Base' not in existing_layer_names:
    lobby.setdefault('layers', []).insert(0, {
        "ambientLightColorR": 255, "ambientLightColorG": 255, "ambientLightColorB": 255,
        "camera3DFarPlaneDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearPlaneDistance": 0.1,
        "cameraType": "", "effects": [], "isLightingLayer": False, "isLocked": False,
        "name": "Base", "renderingType": "", "timeScale": 1, "visibility": True,
        "cameras": [{"defaultSize": True, "defaultViewport": True, "height": 0, "viewportBottom": 1, "viewportLeft": 0, "viewportRight": 1, "viewportTop": 0, "width": 0}]
    })
if 'UI' not in existing_layer_names:
    lobby.setdefault('layers', []).append({
        "ambientLightColorR": 255, "ambientLightColorG": 255, "ambientLightColorB": 255,
        "camera3DFarPlaneDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearPlaneDistance": 0.1,
        "cameraType": "", "effects": [], "isLightingLayer": False, "isLocked": False,
        "name": "UI", "renderingType": "", "timeScale": 1, "visibility": True,
        "cameras": [{"defaultSize": True, "defaultViewport": True, "height": 0, "viewportBottom": 1, "viewportLeft": 0, "viewportRight": 1, "viewportTop": 0, "width": 0}]
    })

# Configure objects in Lobby
lobby_objects = [
    # Background
    {
        "assetStoreId": "",
        "name": "Spr_LobbyBg",
        "type": "Sprite",
        "variables": [], "behaviors": [], "effects": [],
        "animations": [{
            "name": "Normal", "useMultipleDirections": False,
            "directions": [{"looping": False, "timeBetweenFrames": 1, "sprites": [{
                "hasCustomCollisionMask": False, "customCollisionMask": [], "image": "bg_lobby.png",
                "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 836, "y": 470}
            }]}]
        }]
    },
    # Player Idle portrait bust
    {
        "assetStoreId": "",
        "name": "Spr_PlayerLobby",
        "type": "Sprite",
        "variables": [], "behaviors": [], "effects": [],
        "animations": [{
            "name": "Idle", "useMultipleDirections": False,
            "directions": [{"looping": False, "timeBetweenFrames": 1, "sprites": [{
                "hasCustomCollisionMask": False, "customCollisionMask": [], "image": "robi_lobby_waistup.png",
                "points": [], "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 12, "y": 10}
            }]}]
        }]
    },
    # Buttons
    create_button_object("Btn_Play", "btn_play", 420, 64),
    create_button_object("Btn_Shop", "btn_shop", 200, 56),
    create_button_object("Btn_Index", "btn_index", 200, 56),
    create_button_object("Btn_Upgrade", "btn_upgrade", 420, 64),
    # Texts
    create_text_object("Txt_BtnPlay", "MAINKAN", 28),
    create_text_object("Txt_BtnShop", "TOKO", 22),
    create_text_object("Txt_BtnIndex", "KOLEKSI", 22),
    create_text_object("Txt_BtnUpgrade", "UPGRADE", 28),
    create_text_object("Txt_LobbyMoney", "$0", 24, "right"),
    create_text_object("Txt_LobbyLevel", "CURRENT JOURNEY: LEVEL 01", 20, "left"),
]

lobby['objects'] = lobby_objects

# Configure Instances in Lobby Layout
instances = [
    # Background
    {"name": "Spr_LobbyBg", "x": 0, "y": 0, "width": 1024, "height": 576, "customSize": True, "layer": "Base", "zOrder": 0, "angle": 0, "locked": True},
    
    # Karakter Idle di kiri (kepala - pinggang, zoom besar)
    {"name": "Spr_PlayerLobby", "x": 60, "y": 170, "width": 360, "height": 300, "customSize": True, "layer": "UI", "zOrder": 5, "angle": 0, "locked": False},
    
    # Tombol Mainkan (Kuning 3D, atas)
    {"name": "Btn_Play", "x": 520, "y": 140, "width": 420, "height": 64, "customSize": True, "layer": "UI", "zOrder": 10, "angle": 0, "locked": False},
    {"name": "Txt_BtnPlay", "x": 670, "y": 156, "width": 140, "height": 36, "customSize": False, "layer": "UI", "zOrder": 15, "angle": 0, "locked": False},
    
    # Tombol Toko (Kiri bawah Mainkan, Kuning)
    {"name": "Btn_Shop", "x": 520, "y": 224, "width": 200, "height": 56, "customSize": True, "layer": "UI", "zOrder": 10, "angle": 0, "locked": False},
    {"name": "Txt_BtnShop", "x": 585, "y": 238, "width": 80, "height": 30, "customSize": False, "layer": "UI", "zOrder": 15, "angle": 0, "locked": False},
    
    # Tombol Koleksi (Kanan bawah Mainkan, Ungu)
    {"name": "Btn_Index", "x": 740, "y": 224, "width": 200, "height": 56, "customSize": True, "layer": "UI", "zOrder": 10, "angle": 0, "locked": False},
    {"name": "Txt_BtnIndex", "x": 790, "y": 238, "width": 100, "height": 30, "customSize": False, "layer": "UI", "zOrder": 15, "angle": 0, "locked": False},
    
    # Tombol Upgrade (Bawah, Kuning 3D, sama besar dengan Mainkan)
    {"name": "Btn_Upgrade", "x": 520, "y": 300, "width": 420, "height": 64, "customSize": True, "layer": "UI", "zOrder": 10, "angle": 0, "locked": False},
    {"name": "Txt_BtnUpgrade", "x": 670, "y": 316, "width": 140, "height": 36, "customSize": False, "layer": "UI", "zOrder": 15, "angle": 0, "locked": False},
    
    # HUD: Level & Money
    {"name": "Txt_LobbyLevel", "x": 48, "y": 28, "width": 400, "height": 32, "customSize": False, "layer": "UI", "zOrder": 10, "angle": 0, "locked": False},
    {"name": "Txt_LobbyMoney", "x": 860, "y": 28, "width": 120, "height": 32, "customSize": False, "layer": "UI", "zOrder": 10, "angle": 0, "locked": False},
]

lobby['instances'] = instances

# Add Object Group Grp_Buttons to Lobby
button_group = {
    "name": "Grp_Buttons",
    "objects": [
        {"name": "Btn_Play"},
        {"name": "Btn_Shop"},
        {"name": "Btn_Index"},
        {"name": "Btn_Upgrade"}
    ]
}
lobby['objectsGroups'] = [button_group]

# 4. Lobby Events (Initialization & Hover/Pressed feedback)
def build_button_event(btn_obj):
    return {
        "type": "BuiltinCommonInstructions::Standard",
        "conditions": [
            {
                "type": {"value": "IsCursorOnObject"},
                "parameters": [btn_obj, "", ""]
            }
        ],
        "actions": [],
        "events": [
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {
                        "type": {"value": "MouseButtonPressed"},
                        "parameters": ["", "Left"]
                    }
                ],
                "actions": [
                    {
                        "type": {"value": "ChangeAnimation"},
                        "parameters": [btn_obj, "=", "2"]
                    }
                ]
            },
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {
                        "type": {"value": "MouseButtonPressed", "inverted": True},
                        "parameters": ["", "Left"]
                    }
                ],
                "actions": [
                    {
                        "type": {"value": "ChangeAnimation"},
                        "parameters": [btn_obj, "=", "1"]
                    }
                ]
            }
        ]
    }

def build_button_leave_event(btn_obj):
    return {
        "type": "BuiltinCommonInstructions::Standard",
        "conditions": [
            {
                "type": {"value": "IsCursorOnObject", "inverted": True},
                "parameters": [btn_obj, "", ""]
            }
        ],
        "actions": [
            {
                "type": {"value": "ChangeAnimation"},
                "parameters": [btn_obj, "=", "0"]
            }
        ]
    }

button_names = ["Btn_Play", "Btn_Shop", "Btn_Index", "Btn_Upgrade"]
button_sub_events = []
for b in button_names:
    button_sub_events.append(build_button_event(b))
    button_sub_events.append(build_button_leave_event(b))

lobby_events = [
    {
        "type": "BuiltinCommonInstructions::Group",
        "title": "[T3] Lobby — Inisialisasi Tampilan & Variabel",
        "parameters": [""],
        "events": [
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {
                        "type": {"value": "DepartScene"},
                        "parameters": [""]
                    }
                ],
                "actions": [
                    {
                        "type": {"value": "TextObject::String"},
                        "parameters": ["Txt_LobbyMoney", "=", '"$" + ToString(Variable(Save.money))']
                    },
                    {
                        "type": {"value": "TextObject::String"},
                        "parameters": ["Txt_LobbyLevel", "=", '"CURRENT JOURNEY: LEVEL 0" + ToString(Variable(Save.level))']
                    }
                ]
            }
        ]
    },
    {
        "type": "BuiltinCommonInstructions::Group",
        "title": "[T3] Lobby — Interaksi Tombol (Hover & Pressed 3D Feedback)",
        "parameters": [""],
        "events": button_sub_events
    }
]

lobby['events'] = lobby_events

with open(PROJECT, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print("Lobby scene updated successfully!")
