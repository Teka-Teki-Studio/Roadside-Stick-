import json
import os
import uuid

def make_uuid():
    return str(uuid.uuid4())

def make_inst(type_val, params, inverted=False, sub_instructions=None):
    inst = {
        "type": {
            "value": type_val
        },
        "parameters": params
    }
    if inverted:
        inst["inverted"] = True
    if sub_instructions:
        inst["subInstructions"] = sub_instructions
    return inst

def make_event(conditions=None, actions=None, sub_events=None):
    return {
        "type": "BuiltinCommonInstructions::Standard",
        "disabled": False,
        "folded": False,
        "conditions": conditions if conditions is not None else [],
        "actions": actions if actions is not None else [],
        "events": sub_events if sub_events is not None else []
    }

# 1. Project Global Properties
project = {
    "firstLayout": "Main_World",
    "gdVersion": {
        "build": 287,
        "major": 5,
        "minor": 6,
        "revision": 0
    },
    "properties": {
        "adaptGameResolutionAtRuntime": False,
        "antialiasingMode": "none",
        "antialisingEnabledOnMobile": False,
        "folderProject": False,
        "orientation": "landscape",
        "packageName": "com.stickscavenger.game",
        "pixelsRounding": True,
        "projectUuid": make_uuid(),
        "scaleMode": "nearest",
        "sizeOnStartupMode": "",
        "templateSlug": "",
        "version": "0.1.0",
        "name": "Stick Scavenger",
        "description": "Stick Scavenger - Sprint 1 Core Loop MVP",
        "author": "Antigravity Senior Engineer",
        "windowWidth": 640,
        "windowHeight": 360,
        "latestCompilationDirectory": "",
        "maxFPS": 60,
        "minFPS": 20,
        "verticalSync": False,
        "loadingScreen": {
            "backgroundColor": 0,
            "backgroundFadeInDuration": 0.2,
            "backgroundImageResourceName": "",
            "gdevelopLogoStyle": "light",
            "logoAndProgressFadeInDuration": 0.2,
            "logoAndProgressLogoFadeInDelay": 0,
            "minDuration": 0.5,
            "progressBarColor": 16777215,
            "progressBarHeight": 20,
            "progressBarMaxWidth": 200,
            "progressBarMinWidth": 40,
            "progressBarWidthPercent": 30,
            "showGDevelopSplash": False,
            "showProgressBar": False
        },
        "watermark": {
            "placement": "bottom-left",
            "showWatermark": False
        },
        "authorIds": [],
        "authorUsernames": [],
        "categories": ["Action", "Platformer", "Pixel Art"],
        "playableDevices": ["keyboard"],
        "extensionProperties": [],
        "platforms": [
            {
                "name": "GDevelop JS platform"
            }
        ],
        "currentPlatform": "GDevelop JS platform"
    },
    "resources": {
        "resources": []
    },
    "objects": [],
    "objectsFolderStructure": {
        "folderName": "__ROOT__"
    },
    "objectsGroups": [],
    "variables": [],
    "layouts": [],
    "layoutsFolderStructure": {
        "folderName": "__ROOT__"
    },
    "externalEvents": [],
    "externalEventsFolderStructure": {
        "folderName": "__ROOT__"
    },
    "tests": [],
    "testsFolderStructure": {
        "folderName": "__ROOT__"
    },
    "eventsFunctionsExtensions": [],
    "externalLayouts": [],
    "externalLayoutsFolderStructure": {
        "folderName": "__ROOT__"
    }
}

# 2. Register all resources from assets/dummy/ with smoothed: false
DUMMY_DIR = "assets/dummy"
resource_files = []
for root, dirs, files in os.walk(DUMMY_DIR):
    for f in sorted(files):
        if f.endswith(".png"):
            full_p = os.path.join(root, f).replace("\\", "/")
            resource_files.append(full_p)

for rf in sorted(resource_files):
    project["resources"]["resources"].append({
        "file": rf,
        "kind": "image",
        "metadata": "",
        "name": rf,
        "smoothed": False,
        "userAdded": True
    })

# 3. Scene "Main_World" Objects
# A. Ground_Floor (TiledSprite)
ground_floor_obj = {
    "assetStoreId": "",
    "behaviors": [
        {
            "name": "Platform",
            "type": "PlatformBehavior::PlatformBehavior",
            "canBeGrabbed": False,
            "platformType": "NormalPlatform",
            "yGrabOffset": 0
        }
    ],
    "effects": [],
    "height": 64,
    "name": "Ground_Floor",
    "texture": "assets/dummy/env/ground_tile.png",
    "type": "TiledSpriteObject::TiledSprite",
    "variables": [],
    "width": 8400
}

# B. Wall_Left (Dinding pembatas kiri)
wall_left_obj = {
    "assetStoreId": "",
    "behaviors": [
        {
            "name": "Platform",
            "type": "PlatformBehavior::PlatformBehavior",
            "canBeGrabbed": False,
            "platformType": "NormalPlatform",
            "yGrabOffset": 0
        }
    ],
    "effects": [],
    "height": 360,
    "name": "Wall_Left",
    "texture": "assets/dummy/env/ground_tile.png",
    "type": "TiledSpriteObject::TiledSprite",
    "variables": [],
    "width": 32
}

# C. Home_Base (Sprite)
home_base_obj = {
    "assetStoreId": "",
    "name": "Home_Base",
    "type": "Sprite",
    "variables": [],
    "behaviors": [],
    "effects": [],
    "animations": [
        {
            "name": "Default",
            "useMultipleDirections": False,
            "directions": [
                {
                    "looping": False,
                    "timeBetweenFrames": 1,
                    "sprites": [
                        {
                            "hasCustomCollisionMask": False,
                            "customCollisionMask": [],
                            "image": "assets/dummy/env/home_base.png",
                            "points": [],
                            "originPoint": {"name": "origine", "x": 0, "y": 0},
                            "centerPoint": {"automatic": True, "name": "centre", "x": 0, "y": 0}
                        }
                    ]
                }
            ]
        }
    ]
}

# D. Bg_Sky (TiledSprite)
bg_sky_obj = {
    "assetStoreId": "",
    "behaviors": [],
    "effects": [],
    "height": 360,
    "name": "Bg_Sky",
    "texture": "assets/dummy/env/bg_sky.png",
    "type": "TiledSpriteObject::TiledSprite",
    "variables": [],
    "width": 9000
}

# E. Bg_Mid (TiledSprite)
bg_mid_obj = {
    "assetStoreId": "",
    "behaviors": [],
    "effects": [],
    "height": 368,
    "name": "Bg_Mid",
    "texture": "assets/dummy/env/bg_mid.png",
    "type": "TiledSpriteObject::TiledSprite",
    "variables": [],
    "width": 9000
}

# F. Player (Sprite)
player_obj = {
    "assetStoreId": "",
    "name": "Player",
    "type": "Sprite",
    "variables": [],
    "behaviors": [
        {
            "name": "PlatformerObjectBehavior",
            "type": "PlatformBehavior::PlatformerObjectBehavior",
            "acceleration": 1200,
            "canGoDownFromJumpthru": True,
            "canGrabPlatforms": False,
            "canGrabWithoutMoving": False,
            "deceleration": 1200,
            "gravity": 1000,
            "ignoreDefaultControls": False,
            "jumpSpeed": 380,
            "jumpSustainTime": 0.2,
            "ladderClimbingSpeed": 200,
            "maxFallingSpeed": 800,
            "maxSpeed": 160,
            "slopeMaxAngle": 60,
            "useLegacyTrajectory": False,
            "xGrabTolerance": 10,
            "yGrabOffset": 0
        }
    ],
    "effects": [],
    "animations": [
        # 0: Idle (loop true, 0.15s)
        {
            "name": "Idle",
            "useMultipleDirections": False,
            "directions": [
                {
                    "looping": True,
                    "timeBetweenFrames": 0.15,
                    "sprites": [
                        {
                            "hasCustomCollisionMask": False,
                            "customCollisionMask": [],
                            "image": f"assets/dummy/player/player-idle-{i}.png",
                            "points": [],
                            "originPoint": {"name": "origine", "x": 16.5, "y": 32},
                            "centerPoint": {"automatic": False, "name": "centre", "x": 16.5, "y": 16}
                        }
                        for i in range(1, 5)
                    ]
                }
            ]
        },
        # 1: Run (loop true, 0.10s)
        {
            "name": "Run",
            "useMultipleDirections": False,
            "directions": [
                {
                    "looping": True,
                    "timeBetweenFrames": 0.10,
                    "sprites": [
                        {
                            "hasCustomCollisionMask": False,
                            "customCollisionMask": [],
                            "image": f"assets/dummy/player/player-run-{i}.png",
                            "points": [],
                            "originPoint": {"name": "origine", "x": 16.5, "y": 32},
                            "centerPoint": {"automatic": False, "name": "centre", "x": 16.5, "y": 16}
                        }
                        for i in range(1, 7)
                    ]
                }
            ]
        },
        # 2: Jump (loop false, 0.15s)
        {
            "name": "Jump",
            "useMultipleDirections": False,
            "directions": [
                {
                    "looping": False,
                    "timeBetweenFrames": 0.15,
                    "sprites": [
                        {
                            "hasCustomCollisionMask": False,
                            "customCollisionMask": [],
                            "image": f"assets/dummy/player/player-jump-{i}.png",
                            "points": [],
                            "originPoint": {"name": "origine", "x": 16.5, "y": 32},
                            "centerPoint": {"automatic": False, "name": "centre", "x": 16.5, "y": 16}
                        }
                        for i in range(1, 3)
                    ]
                }
            ]
        }
    ]
}

# G. Held_Stick (Sprite with 4 animations)
held_stick_obj = {
    "assetStoreId": "",
    "name": "Held_Stick",
    "type": "Sprite",
    "variables": [],
    "behaviors": [],
    "effects": [],
    "animations": [
        {
            "name": f"Tier{t}",
            "useMultipleDirections": False,
            "directions": [
                {
                    "looping": False,
                    "timeBetweenFrames": 1,
                    "sprites": [
                        {
                            "hasCustomCollisionMask": False,
                            "customCollisionMask": [],
                            "image": f"assets/dummy/sticks/stick_t{t}.png",
                            "points": [],
                            "originPoint": {"name": "origine", "x": 8, "y": 8},
                            "centerPoint": {"automatic": True, "name": "centre", "x": 8, "y": 8}
                        }
                    ]
                }
            ]
        }
        for t in range(1, 5)
    ]
}

# H. Ground_Stick (Sprite with same 4 animations & instance variables)
ground_stick_obj = {
    "assetStoreId": "",
    "name": "Ground_Stick",
    "type": "Sprite",
    "variables": [
        {"name": "tier", "type": "number", "value": 1},
        {"name": "base_value", "type": "number", "value": 10},
        {"name": "chunk_id", "type": "number", "value": 0}
    ],
    "behaviors": [],
    "effects": [],
    "animations": [
        {
            "name": f"Tier{t}",
            "useMultipleDirections": False,
            "directions": [
                {
                    "looping": False,
                    "timeBetweenFrames": 1,
                    "sprites": [
                        {
                            "hasCustomCollisionMask": False,
                            "customCollisionMask": [],
                            "image": f"assets/dummy/sticks/stick_t{t}.png",
                            "points": [],
                            "originPoint": {"name": "origine", "x": 8, "y": 16},
                            "centerPoint": {"automatic": True, "name": "centre", "x": 8, "y": 8}
                        }
                    ]
                }
            ]
        }
        for t in range(1, 5)
    ]
}

# I. Txt_Interact
txt_interact_obj = {
    "name": "Txt_Interact",
    "type": "TextObject::Text",
    "variables": [],
    "behaviors": [],
    "effects": [],
    "content": {
        "bold": True,
        "characterSize": 11,
        "color": "255;255;255",
        "font": "",
        "isOutlineEnabled": True,
        "isShadowEnabled": False,
        "italic": False,
        "lineHeight": 0,
        "outlineColor": "0;0;0",
        "outlineThickness": 1.5,
        "shadowAngle": 90,
        "shadowBlurRadius": 2,
        "shadowColor": "0;0;0",
        "shadowDistance": 1,
        "shadowOpacity": 128,
        "text": "[E] Ambil T1",
        "textAlignment": "center",
        "underlined": False,
        "verticalTextAlignment": "top"
    }
}

# J. Txt_HUD
txt_hud_obj = {
    "name": "Txt_HUD",
    "type": "TextObject::Text",
    "variables": [],
    "behaviors": [],
    "effects": [],
    "content": {
        "bold": True,
        "characterSize": 12,
        "color": "255;255;255",
        "font": "",
        "isOutlineEnabled": True,
        "isShadowEnabled": False,
        "italic": False,
        "lineHeight": 0,
        "outlineColor": "0;0;0",
        "outlineThickness": 2,
        "shadowAngle": 90,
        "shadowBlurRadius": 2,
        "shadowColor": "0;0;0",
        "shadowDistance": 1,
        "shadowOpacity": 128,
        "text": "SKOR AMAN: 0 | ZONA: 0 (Chunk 0) | BAWAAN: Tier 0 (Val: 0)",
        "textAlignment": "left",
        "underlined": False,
        "verticalTextAlignment": "top"
    }
}

# K. Txt_Floating_Gain
txt_gain_obj = {
    "name": "Txt_Floating_Gain",
    "type": "TextObject::Text",
    "variables": [],
    "behaviors": [],
    "effects": [],
    "content": {
        "bold": True,
        "characterSize": 14,
        "color": "255;215;0",
        "font": "",
        "isOutlineEnabled": True,
        "isShadowEnabled": False,
        "italic": False,
        "lineHeight": 0,
        "outlineColor": "0;0;0",
        "outlineThickness": 2,
        "shadowAngle": 90,
        "shadowBlurRadius": 2,
        "shadowColor": "0;0;0",
        "shadowDistance": 1,
        "shadowOpacity": 128,
        "text": "+0 POIN AMAN!",
        "textAlignment": "center",
        "underlined": False,
        "verticalTextAlignment": "top"
    }
}

scene_objects = [
    ground_floor_obj,
    wall_left_obj,
    home_base_obj,
    bg_sky_obj,
    bg_mid_obj,
    player_obj,
    held_stick_obj,
    ground_stick_obj,
    txt_interact_obj,
    txt_hud_obj,
    txt_gain_obj
]

# 4. Scene Instances
scene_instances = [
    # Parallax Background
    {
        "angle": 0, "customSize": True, "depth": 1, "height": 360, "keepRatio": False,
        "layer": "Background", "locked": True, "name": "Bg_Sky", "persistentUuid": make_uuid(),
        "width": 9000, "x": 0, "y": 0, "zOrder": 0,
        "numberProperties": [], "stringProperties": [], "initialVariables": []
    },
    {
        "angle": 0, "customSize": True, "depth": 1, "height": 368, "keepRatio": False,
        "layer": "Background", "locked": True, "name": "Bg_Mid", "persistentUuid": make_uuid(),
        "width": 9000, "x": 0, "y": 0, "zOrder": 1,
        "numberProperties": [], "stringProperties": [], "initialVariables": []
    },
    # Ground Floor & Left Wall
    {
        "angle": 0, "customSize": True, "depth": 1, "height": 64, "keepRatio": False,
        "layer": "", "locked": True, "name": "Ground_Floor", "persistentUuid": make_uuid(),
        "width": 8400, "x": -64, "y": 296, "zOrder": 1,
        "numberProperties": [], "stringProperties": [], "initialVariables": []
    },
    {
        "angle": 0, "customSize": True, "depth": 1, "height": 360, "keepRatio": False,
        "layer": "", "locked": True, "name": "Wall_Left", "persistentUuid": make_uuid(),
        "width": 32, "x": -32, "y": 0, "zOrder": 1,
        "numberProperties": [], "stringProperties": [], "initialVariables": []
    },
    # Home Base
    {
        "angle": 0, "customSize": False, "height": 108, "keepRatio": True,
        "layer": "", "locked": False, "name": "Home_Base", "persistentUuid": make_uuid(),
        "width": 87, "x": 24, "y": 188, "zOrder": 2,
        "numberProperties": [], "stringProperties": [], "initialVariables": []
    },
    # Player
    {
        "angle": 0, "customSize": False, "height": 32, "keepRatio": True,
        "layer": "", "locked": False, "name": "Player", "persistentUuid": make_uuid(),
        "width": 33, "x": 100, "y": 260, "zOrder": 10,
        "numberProperties": [], "stringProperties": [], "initialVariables": []
    },
    # Held Stick
    {
        "angle": 0, "customSize": False, "height": 16, "keepRatio": True,
        "layer": "", "locked": False, "name": "Held_Stick", "persistentUuid": make_uuid(),
        "width": 16, "x": 100, "y": 260, "zOrder": 11,
        "numberProperties": [], "stringProperties": [], "initialVariables": []
    },
    # Floating Gain text
    {
        "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
        "layer": "", "locked": False, "name": "Txt_Floating_Gain", "persistentUuid": make_uuid(),
        "width": 120, "x": 50, "y": 160, "zOrder": 25,
        "numberProperties": [], "stringProperties": [], "initialVariables": []
    },
    # Interact text
    {
        "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
        "layer": "", "locked": False, "name": "Txt_Interact", "persistentUuid": make_uuid(),
        "width": 120, "x": 0, "y": 0, "zOrder": 20,
        "numberProperties": [], "stringProperties": [], "initialVariables": []
    },
    # HUD text
    {
        "angle": 0, "customSize": False, "height": 24, "keepRatio": True,
        "layer": "UI", "locked": True, "name": "Txt_HUD", "persistentUuid": make_uuid(),
        "width": 550, "x": 12, "y": 10, "zOrder": 10,
        "numberProperties": [], "stringProperties": [], "initialVariables": []
    }
]

# 5. Scene Variables (all type number)
scene_vars = [
    {"name": "facing_dir", "type": "number", "value": 1},
    {"name": "held_tier", "type": "number", "value": 0},
    {"name": "held_value", "type": "number", "value": 0},
    {"name": "swap_cooldown", "type": "number", "value": 0},
    {"name": "total_score", "type": "number", "value": 0},
    {"name": "max_dist_x", "type": "number", "value": 0},
    {"name": "current_chunk", "type": "number", "value": 0},
    {"name": "current_zone", "type": "number", "value": 0},
    {"name": "respawn_timer", "type": "number", "value": 0},
    {"name": "rng_roll", "type": "number", "value": 0},
    {"name": "spawn_x", "type": "number", "value": 0},
    {"name": "spawn_tier", "type": "number", "value": 1},
    {"name": "spawn_val", "type": "number", "value": 10},
    {"name": "c", "type": "number", "value": 0},
    {"name": "temp_tier", "type": "number", "value": 0},
    {"name": "temp_val", "type": "number", "value": 0},
    {"name": "drop_x", "type": "number", "value": 0},
    {"name": "drop_y", "type": "number", "value": 0},
    {"name": "drop_chunk", "type": "number", "value": 0},
    {"name": "dist_bonus_mult", "type": "number", "value": 1},
    {"name": "earned", "type": "number", "value": 0},
    {"name": "gain_timer", "type": "number", "value": 0}
]

# 6. Layers
scene_layers = [
    {
        "ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0,
        "camera3DFairDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearDistance": 1,
        "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False,
        "isLocked": False, "name": "Background", "renderingType": "", "visibility": True
    },
    {
        "ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0,
        "camera3DFairDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearDistance": 1,
        "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False,
        "isLocked": False, "name": "", "renderingType": "", "visibility": True
    },
    {
        "ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0,
        "camera3DFairDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearDistance": 1,
        "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False,
        "isLocked": False, "name": "UI", "renderingType": "", "visibility": True
    }
]

# 7. SPRINT 1 EVENTS IMPLEMENTATION
events = []

# -------------------------------------------------------------
# BLOCK A: Movement Controller, Bobot Muatan & Kamera Pixel-Snap
# -------------------------------------------------------------

# A1. Every Frame Updates: Cooldowns, Gain timer, Chunk & Zone, Distance
ev_frame_updates = make_event(
    conditions=[],
    actions=[
        make_inst("ModVarScene", ["swap_cooldown", "=", "max(0, Variable(swap_cooldown) - TimeDelta())"]),
        make_inst("ModVarScene", ["gain_timer", "=", "max(0, Variable(gain_timer) - TimeDelta())"]),
        make_inst("ModVarScene", ["current_chunk", "=", "floor(max(0, Player.CenterX()) / 640)"])
    ],
    sub_events=[
        # Floating gain text animation
        make_event(
            conditions=[make_inst("VarScene", ["gain_timer", ">", "0"])],
            actions=[
                make_inst("SetY", ["Txt_Floating_Gain", "-", "25 * TimeDelta()"]),
                make_inst("Show", ["Txt_Floating_Gain", ""])
            ]
        ),
        make_event(
            conditions=[make_inst("VarScene", ["gain_timer", "<=", "0"])],
            actions=[
                make_inst("Hide", ["Txt_Floating_Gain"])
            ]
        ),
        # Zone 0: Home Safe Zone (Player.CenterX() <= 160)
        make_event(
            conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<=", "160"])],
            actions=[make_inst("ModVarScene", ["current_zone", "=", "0"])]
        ),
        # Zone 1: Near Home (Player.CenterX() > 160 and current_chunk <= 3)
        make_event(
            conditions=[
                make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">", "160"]),
                make_inst("VarScene", ["current_chunk", "<=", "3"])
            ],
            actions=[make_inst("ModVarScene", ["current_zone", "=", "1"])]
        ),
        # Zone 2: Mid Forest (current_chunk >= 4 and current_chunk <= 7)
        make_event(
            conditions=[
                make_inst("VarScene", ["current_chunk", ">=", "4"]),
                make_inst("VarScene", ["current_chunk", "<=", "7"])
            ],
            actions=[make_inst("ModVarScene", ["current_zone", "=", "2"])]
        ),
        # Zone 3: Deep Territory (current_chunk >= 8)
        make_event(
            conditions=[make_inst("VarScene", ["current_chunk", ">=", "8"])],
            actions=[make_inst("ModVarScene", ["current_zone", "=", "3"])]
        ),
        # Track max distance achieved during this run
        make_event(
            conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">", "Variable(max_dist_x)"])],
            actions=[make_inst("ModVarScene", ["max_dist_x", "=", "Player.CenterX()"])]
        ),
        # Weight speed modifier
        make_event(
            conditions=[make_inst("VarScene", ["held_tier", "<=", "1"])],
            actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "160"])]
        ),
        make_event(
            conditions=[make_inst("VarScene", ["held_tier", "=", "2"])],
            actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "152"])]
        ),
        make_event(
            conditions=[make_inst("VarScene", ["held_tier", "=", "3"])],
            actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "144"])]
        ),
        make_event(
            conditions=[make_inst("VarScene", ["held_tier", "=", "4"])],
            actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "136"])]
        )
    ]
)
events.append(ev_frame_updates)

# A2. Player Controls & Movement
# Move Right (D or Right arrow)
ev_right = make_event(
    conditions=[
        make_inst("BuiltinCommonInstructions::Or", [], False, [
            make_inst("KeyPressed", ["", "d"]),
            make_inst("KeyPressed", ["", "Right"])
        ])
    ],
    actions=[
        make_inst("PlatformBehavior::SimulateRightKey", ["Player", "PlatformerObjectBehavior"]),
        make_inst("FlipX", ["Player", "no"]),
        make_inst("ModVarScene", ["facing_dir", "=", "1"])
    ]
)
events.append(ev_right)

# Move Left (A or Left arrow)
ev_left = make_event(
    conditions=[
        make_inst("BuiltinCommonInstructions::Or", [], False, [
            make_inst("KeyPressed", ["", "a"]),
            make_inst("KeyPressed", ["", "Left"])
        ])
    ],
    actions=[
        make_inst("PlatformBehavior::SimulateLeftKey", ["Player", "PlatformerObjectBehavior"]),
        make_inst("FlipX", ["Player", "yes"]),
        make_inst("ModVarScene", ["facing_dir", "=", "-1"])
    ]
)
events.append(ev_left)

# Jump (W, Up arrow, or Space)
ev_jump = make_event(
    conditions=[
        make_inst("BuiltinCommonInstructions::Or", [], False, [
            make_inst("KeyPressed", ["", "w"]),
            make_inst("KeyPressed", ["", "Up"]),
            make_inst("KeyPressed", ["", "Space"])
        ])
    ],
    actions=[
        make_inst("PlatformBehavior::SimulateJumpKey", ["Player", "PlatformerObjectBehavior"])
    ]
)
events.append(ev_jump)

# Player Animation Logic
ev_anim = make_event(
    conditions=[],
    actions=[],
    sub_events=[
        # Run (On floor and moving)
        make_event(
            conditions=[
                make_inst("PlatformBehavior::IsOnFloor", ["Player", "PlatformerObjectBehavior"]),
                make_inst("PlatformBehavior::IsMoving", ["Player", "PlatformerObjectBehavior"])
            ],
            actions=[make_inst("ChangeAnimation", ["Player", "=", "1"])]
        ),
        # Idle (On floor and not moving)
        make_event(
            conditions=[
                make_inst("PlatformBehavior::IsOnFloor", ["Player", "PlatformerObjectBehavior"]),
                make_inst("PlatformBehavior::IsMoving", ["Player", "PlatformerObjectBehavior"], inverted=True)
            ],
            actions=[make_inst("ChangeAnimation", ["Player", "=", "0"])]
        ),
        # Jump (In the air)
        make_event(
            conditions=[
                make_inst("PlatformBehavior::IsOnFloor", ["Player", "PlatformerObjectBehavior"], inverted=True)
            ],
            actions=[make_inst("ChangeAnimation", ["Player", "=", "2"])]
        )
    ]
)
events.append(ev_anim)

# A3. Camera Pixel-Snap & Look-Ahead & Parallax
ev_camera = make_event(
    conditions=[],
    actions=[
        make_inst("ZoomCamera", ["", "1", "\"\"", "0"]),
        make_inst("SetCameraCenterX", ["", "=", "round(clamp(Player.CenterX() + Variable(facing_dir) * 48, 320, 8000))", "\"\"", "0"]),
        make_inst("SetCameraCenterY", ["", "=", "180", "\"\"", "0"]),
        make_inst("SetCameraCenterX", ["", "=", "round(CameraX(\"\", 0) * 0.3)", "\"Background\"", "0"]),
        make_inst("SetCameraCenterY", ["", "=", "180", "\"Background\"", "0"])
    ]
)
events.append(ev_camera)

# A4. Synchronize Held Stick on Player
ev_held_stick = make_event(
    conditions=[],
    actions=[],
    sub_events=[
        # Empty hand: hide
        make_event(
            conditions=[make_inst("VarScene", ["held_tier", "=", "0"])],
            actions=[make_inst("Hide", ["Held_Stick"])]
        ),
        # Carrying stick: show, match animation, attach to hand, match flip
        make_event(
            conditions=[make_inst("VarScene", ["held_tier", ">", "0"])],
            actions=[
                make_inst("Show", ["Held_Stick", ""]),
                make_inst("ChangeAnimation", ["Held_Stick", "=", "Variable(held_tier) - 1"]),
                make_inst("SetXY", ["Held_Stick", "=", "Player.CenterX() + (Variable(facing_dir) * 10)", "=", "Player.CenterY() - 2"])
            ],
            sub_events=[
                make_event(
                    conditions=[make_inst("VarScene", ["facing_dir", "=", "1"])],
                    actions=[make_inst("FlipX", ["Held_Stick", "no"])]
                ),
                make_event(
                    conditions=[make_inst("VarScene", ["facing_dir", "=", "-1"])],
                    actions=[make_inst("FlipX", ["Held_Stick", "yes"])]
                )
            ]
        )
    ]
)
events.append(ev_held_stick)

# -------------------------------------------------------------
# BLOCK B: Chunk Spawner & Weighted RNG Stick
# -------------------------------------------------------------

def make_zone_rng_subevents(chunk_num):
    if chunk_num <= 3:
        # Zone 1: <= 80 Tier 1 (10), else Tier 2 (30)
        return [
            make_event(
                conditions=[make_inst("VarScene", ["rng_roll", "<=", "80"])],
                actions=[
                    make_inst("ModVarScene", ["spawn_tier", "=", "1"]),
                    make_inst("ModVarScene", ["spawn_val", "=", "10"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["rng_roll", ">", "80"])],
                actions=[
                    make_inst("ModVarScene", ["spawn_tier", "=", "2"]),
                    make_inst("ModVarScene", ["spawn_val", "=", "30"])
                ]
            )
        ]
    elif chunk_num <= 7:
        # Zone 2: <= 15 T1 (10), <= 65 T2 (30), else T3 (85)
        return [
            make_event(
                conditions=[make_inst("VarScene", ["rng_roll", "<=", "15"])],
                actions=[
                    make_inst("ModVarScene", ["spawn_tier", "=", "1"]),
                    make_inst("ModVarScene", ["spawn_val", "=", "10"])
                ]
            ),
            make_event(
                conditions=[
                    make_inst("VarScene", ["rng_roll", ">", "15"]),
                    make_inst("VarScene", ["rng_roll", "<=", "65"])
                ],
                actions=[
                    make_inst("ModVarScene", ["spawn_tier", "=", "2"]),
                    make_inst("ModVarScene", ["spawn_val", "=", "30"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["rng_roll", ">", "65"])],
                actions=[
                    make_inst("ModVarScene", ["spawn_tier", "=", "3"]),
                    make_inst("ModVarScene", ["spawn_val", "=", "85"])
                ]
            )
        ]
    else:
        # Zone 3: <= 20 T2 (30), <= 75 T3 (85), else T4 (250)
        return [
            make_event(
                conditions=[make_inst("VarScene", ["rng_roll", "<=", "20"])],
                actions=[
                    make_inst("ModVarScene", ["spawn_tier", "=", "2"]),
                    make_inst("ModVarScene", ["spawn_val", "=", "30"])
                ]
            ),
            make_event(
                conditions=[
                    make_inst("VarScene", ["rng_roll", ">", "20"]),
                    make_inst("VarScene", ["rng_roll", "<=", "75"])
                ],
                actions=[
                    make_inst("ModVarScene", ["spawn_tier", "=", "3"]),
                    make_inst("ModVarScene", ["spawn_val", "=", "85"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["rng_roll", ">", "75"])],
                actions=[
                    make_inst("ModVarScene", ["spawn_tier", "=", "4"]),
                    make_inst("ModVarScene", ["spawn_val", "=", "250"])
                ]
            )
        ]

def make_slot_event(chunk_num, x_expr):
    return make_event(
        conditions=[],
        actions=[
            make_inst("ModVarScene", ["spawn_x", "=", x_expr]),
            make_inst("ModVarScene", ["rng_roll", "=", "RandomInRange(1, 100)"])
        ],
        sub_events=make_zone_rng_subevents(chunk_num) + [
            make_event(
                conditions=[],
                actions=[
                    make_inst("Create", ["", "Ground_Stick", "Variable(spawn_x)", "296 - 16", "\"\""]),
                    make_inst("ModVarObjet", ["Ground_Stick", "tier", "=", "Variable(spawn_tier)"]),
                    make_inst("ModVarObjet", ["Ground_Stick", "base_value", "=", "Variable(spawn_val)"]),
                    make_inst("ModVarObjet", ["Ground_Stick", "chunk_id", "=", str(chunk_num)]),
                    make_inst("ChangeAnimation", ["Ground_Stick", "=", "Variable(spawn_tier) - 1"]),
                    make_inst("SetZOrder", ["Ground_Stick", "=", "5"])
                ]
            )
        ]
    )

# Initial Spawning across Chunk 1..12
initial_chunk_subevents = []
for c in range(1, 13):
    slot1 = make_slot_event(c, f"{c} * 640 + 110 + RandomInRange(-30, 30)")
    slot2 = make_slot_event(c, f"{c} * 640 + 320 + RandomInRange(-40, 40)")
    slot3 = make_slot_event(c, f"{c} * 640 + 530 + RandomInRange(-30, 30)")
    chunk_ev = make_event(
        conditions=[],
        actions=[make_inst("ModVarScene", ["c", "=", str(c)])],
        sub_events=[slot1, slot2, slot3]
    )
    initial_chunk_subevents.append(chunk_ev)

ev_scene_start = make_event(
    conditions=[make_inst("DepartScene", [""])],
    actions=[
        make_inst("ModVarScene", ["swap_cooldown", "=", "0"]),
        make_inst("ModVarScene", ["respawn_timer", "=", "0"])
    ],
    sub_events=initial_chunk_subevents
)
events.append(ev_scene_start)

# Periodic Respawn (every 30s) Anti Pop-in
ev_respawn = make_event(
    conditions=[],
    actions=[
        make_inst("ModVarScene", ["respawn_timer", "+", "TimeDelta()"])
    ],
    sub_events=[
        make_event(
            conditions=[make_inst("VarScene", ["respawn_timer", ">=", "30.0"])],
            actions=[
                make_inst("ModVarScene", ["respawn_timer", "=", "0"]),
                make_inst("ModVarScene", ["c", "=", "RandomInRange(1, 12)"])
            ],
            sub_events=[
                make_event(
                    conditions=[
                        make_inst("BuiltinCommonInstructions::CompareNumbers", ["abs((Variable(c) * 640 + 320) - Player.CenterX())", ">", "640"])
                    ],
                    actions=[
                        make_inst("ModVarScene", ["spawn_x", "=", "Variable(c) * 640 + RandomInRange(140, 500)"]),
                        make_inst("ModVarScene", ["rng_roll", "=", "RandomInRange(1, 100)"])
                    ],
                    sub_events=[
                        # Zone 1
                        make_event(
                            conditions=[make_inst("VarScene", ["c", "<=", "3"])],
                            actions=[],
                            sub_events=[
                                make_event(
                                    conditions=[make_inst("VarScene", ["rng_roll", "<=", "80"])],
                                    actions=[
                                        make_inst("ModVarScene", ["spawn_tier", "=", "1"]),
                                        make_inst("ModVarScene", ["spawn_val", "=", "10"])
                                    ]
                                ),
                                make_event(
                                    conditions=[make_inst("VarScene", ["rng_roll", ">", "80"])],
                                    actions=[
                                        make_inst("ModVarScene", ["spawn_tier", "=", "2"]),
                                        make_inst("ModVarScene", ["spawn_val", "=", "30"])
                                    ]
                                )
                            ]
                        ),
                        # Zone 2
                        make_event(
                            conditions=[
                                make_inst("VarScene", ["c", ">=", "4"]),
                                make_inst("VarScene", ["c", "<=", "7"])
                            ],
                            actions=[],
                            sub_events=[
                                make_event(
                                    conditions=[make_inst("VarScene", ["rng_roll", "<=", "15"])],
                                    actions=[
                                        make_inst("ModVarScene", ["spawn_tier", "=", "1"]),
                                        make_inst("ModVarScene", ["spawn_val", "=", "10"])
                                    ]
                                ),
                                make_event(
                                    conditions=[
                                        make_inst("VarScene", ["rng_roll", ">", "15"]),
                                        make_inst("VarScene", ["rng_roll", "<=", "65"])
                                    ],
                                    actions=[
                                        make_inst("ModVarScene", ["spawn_tier", "=", "2"]),
                                        make_inst("ModVarScene", ["spawn_val", "=", "30"])
                                    ]
                                ),
                                make_event(
                                    conditions=[make_inst("VarScene", ["rng_roll", ">", "65"])],
                                    actions=[
                                        make_inst("ModVarScene", ["spawn_tier", "=", "3"]),
                                        make_inst("ModVarScene", ["spawn_val", "=", "85"])
                                    ]
                                )
                            ]
                        ),
                        # Zone 3
                        make_event(
                            conditions=[make_inst("VarScene", ["c", ">=", "8"])],
                            actions=[],
                            sub_events=[
                                make_event(
                                    conditions=[make_inst("VarScene", ["rng_roll", "<=", "20"])],
                                    actions=[
                                        make_inst("ModVarScene", ["spawn_tier", "=", "2"]),
                                        make_inst("ModVarScene", ["spawn_val", "=", "30"])
                                    ]
                                ),
                                make_event(
                                    conditions=[
                                        make_inst("VarScene", ["rng_roll", ">", "20"]),
                                        make_inst("VarScene", ["rng_roll", "<=", "75"])
                                    ],
                                    actions=[
                                        make_inst("ModVarScene", ["spawn_tier", "=", "3"]),
                                        make_inst("ModVarScene", ["spawn_val", "=", "85"])
                                    ]
                                ),
                                make_event(
                                    conditions=[make_inst("VarScene", ["rng_roll", ">", "75"])],
                                    actions=[
                                        make_inst("ModVarScene", ["spawn_tier", "=", "4"]),
                                        make_inst("ModVarScene", ["spawn_val", "=", "250"])
                                    ]
                                )
                            ]
                        ),
                        # Create spawned stick
                        make_event(
                            conditions=[],
                            actions=[
                                make_inst("Create", ["", "Ground_Stick", "Variable(spawn_x)", "296 - 16", "\"\""]),
                                make_inst("ModVarObjet", ["Ground_Stick", "tier", "=", "Variable(spawn_tier)"]),
                                make_inst("ModVarObjet", ["Ground_Stick", "base_value", "=", "Variable(spawn_val)"]),
                                make_inst("ModVarObjet", ["Ground_Stick", "chunk_id", "=", "Variable(c)"]),
                                make_inst("ChangeAnimation", ["Ground_Stick", "=", "Variable(spawn_tier) - 1"]),
                                make_inst("SetZOrder", ["Ground_Stick", "=", "5"])
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
events.append(ev_respawn)

# -------------------------------------------------------------
# BLOCK C: Deteksi Item Terdekat, Pickup & Atomic Swap (Tombol E)
# -------------------------------------------------------------

# C1. Detect nearby stick & show floating interact prompt
ev_interact_prompt = make_event(
    conditions=[],
    actions=[
        make_inst("Hide", ["Txt_Interact"])
    ],
    sub_events=[
        make_event(
            conditions=[
                make_inst("Distance", ["Player", "Ground_Stick", "28", ""])
            ],
            actions=[
                make_inst("PickNearest", ["Ground_Stick", "Player.CenterX()", "Player.CenterY()"]),
                make_inst("Show", ["Txt_Interact", ""]),
                make_inst("SetXY", ["Txt_Interact", "=", "Ground_Stick.CenterX() - 45", "=", "Ground_Stick.Y() - 22"])
            ],
            sub_events=[
                make_event(
                    conditions=[make_inst("VarScene", ["held_tier", "=", "0"])],
                    actions=[
                        make_inst("TextObject::String", ["Txt_Interact", "=", "\"[E] Ambil T\" + ToString(Ground_Stick.Variable(tier))"])
                    ]
                ),
                make_event(
                    conditions=[make_inst("VarScene", ["held_tier", ">", "0"])],
                    actions=[
                        make_inst("TextObject::String", ["Txt_Interact", "=", "\"[E] Tukar T\" + ToString(Variable(held_tier)) + \" <-> T\" + ToString(Ground_Stick.Variable(tier))"])
                    ]
                )
            ]
        )
    ]
)
events.append(ev_interact_prompt)

# C2. Execute Pickup / Swap on key E
ev_pickup_swap = make_event(
    conditions=[
        make_inst("KeyPressed", ["", "e"]),
        make_inst("BuiltinCommonInstructions::Once", []),
        make_inst("VarScene", ["swap_cooldown", "<=", "0"]),
        make_inst("Distance", ["Player", "Ground_Stick", "28", ""])
    ],
    actions=[
        make_inst("PickNearest", ["Ground_Stick", "Player.CenterX()", "Player.CenterY()"])
    ],
    sub_events=[
        # Branch 1: Pickup (held_tier == 0)
        make_event(
            conditions=[make_inst("VarScene", ["held_tier", "=", "0"])],
            actions=[
                make_inst("ModVarScene", ["held_tier", "=", "Ground_Stick.Variable(tier)"]),
                make_inst("ModVarScene", ["held_value", "=", "Ground_Stick.Variable(base_value)"]),
                make_inst("Delete", ["Ground_Stick", ""]),
                make_inst("ModVarScene", ["swap_cooldown", "=", "0.25"])
            ]
        ),
        # Branch 2: Atomic Swap (held_tier > 0)
        make_event(
            conditions=[make_inst("VarScene", ["held_tier", ">", "0"])],
            actions=[
                make_inst("ModVarScene", ["temp_tier", "=", "Variable(held_tier)"]),
                make_inst("ModVarScene", ["temp_val", "=", "Variable(held_value)"]),
                make_inst("ModVarScene", ["drop_x", "=", "Ground_Stick.X()"]),
                make_inst("ModVarScene", ["drop_y", "=", "Ground_Stick.Y()"]),
                make_inst("ModVarScene", ["drop_chunk", "=", "Ground_Stick.Variable(chunk_id)"]),
                make_inst("ModVarScene", ["held_tier", "=", "Ground_Stick.Variable(tier)"]),
                make_inst("ModVarScene", ["held_value", "=", "Ground_Stick.Variable(base_value)"]),
                make_inst("Delete", ["Ground_Stick", ""]),
                make_inst("Create", ["", "Ground_Stick", "Variable(drop_x)", "Variable(drop_y)", "\"\""]),
                make_inst("ModVarObjet", ["Ground_Stick", "tier", "=", "Variable(temp_tier)"]),
                make_inst("ModVarObjet", ["Ground_Stick", "base_value", "=", "Variable(temp_val)"]),
                make_inst("ModVarObjet", ["Ground_Stick", "chunk_id", "=", "Variable(drop_chunk)"]),
                make_inst("ChangeAnimation", ["Ground_Stick", "=", "Variable(temp_tier) - 1"]),
                make_inst("SetZOrder", ["Ground_Stick", "=", "5"]),
                make_inst("ModVarScene", ["swap_cooldown", "=", "0.25"])
            ]
        )
    ]
)
events.append(ev_pickup_swap)

# -------------------------------------------------------------
# BLOCK D: Home Base Extraction (Pulang Mengamankan Muatan)
# -------------------------------------------------------------
ev_extraction = make_event(
    conditions=[
        make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<=", "160"]),
        make_inst("VarScene", ["held_tier", ">", "0"])
    ],
    actions=[
        make_inst("ModVarScene", ["dist_bonus_mult", "=", "1 + 0.15 * floor(Variable(max_dist_x) / 640)"]),
        make_inst("ModVarScene", ["earned", "=", "round(Variable(held_value) * Variable(dist_bonus_mult))"]),
        make_inst("ModVarScene", ["total_score", "+", "Variable(earned)"]),
        make_inst("TextObject::String", ["Txt_Floating_Gain", "=", "\"+\" + ToString(Variable(earned)) + \" POIN AMAN!\""]),
        make_inst("SetXY", ["Txt_Floating_Gain", "=", "Home_Base.CenterX() - 40", "=", "Home_Base.Y() - 15"]),
        make_inst("Show", ["Txt_Floating_Gain", ""]),
        make_inst("ModVarScene", ["gain_timer", "=", "1.5"]),
        make_inst("ModVarScene", ["held_tier", "=", "0"]),
        make_inst("ModVarScene", ["held_value", "=", "0"]),
        make_inst("ModVarScene", ["max_dist_x", "=", "0"])
    ]
)
events.append(ev_extraction)

# -------------------------------------------------------------
# BLOCK E: Update Teks HUD & Tombol Reset Testing (R)
# -------------------------------------------------------------
ev_hud = make_event(
    conditions=[],
    actions=[
        make_inst("TextObject::String", [
            "Txt_HUD",
            "=",
            "\"SKOR AMAN: \" + ToString(Variable(total_score)) + \" | ZONA: \" + ToString(Variable(current_zone)) + \" (Chunk \" + ToString(Variable(current_chunk)) + \") | BAWAAN: Tier \" + ToString(Variable(held_tier)) + \" (Val: \" + ToString(Variable(held_value)) + \")\""
        ])
    ]
)
events.append(ev_hud)

# Restart Scene on R key
ev_reset = make_event(
    conditions=[
        make_inst("KeyPressed", ["", "r"]),
        make_inst("BuiltinCommonInstructions::Once", [])
    ],
    actions=[
        make_inst("Scene", ["", "\"Main_World\"", "no"])
    ]
)
events.append(ev_reset)

# 8. Assemble Layout "Main_World"
layout = {
    "b": 100,
    "disableInputWhenNotFocused": False,
    "mangledName": "Main_95World",
    "name": "Main_World",
    "r": 100,
    "renderer3DWorldScale": 100,
    "standardSortMethod": True,
    "stopSoundsOnStartup": False,
    "title": "Main World",
    "v": 100,
    "uiSettings": {
        "grid": False,
        "gridType": "isometric",
        "gridWidth": 32,
        "gridHeight": 32,
        "gridDepth": 32,
        "gridColor": 10401023,
        "gridAlpha": 0.8,
        "snap": False,
        "zoomFactor": 1,
        "windowMask": False
    },
    "objectsGroups": [],
    "variables": scene_vars,
    "instances": scene_instances,
    "objects": scene_objects,
    "objectsFolderStructure": {
        "folderName": "__ROOT__"
    },
    "events": events,
    "layers": scene_layers,
    "behaviorsSharedData": [
        {
            "name": "Platform",
            "type": "PlatformBehavior::PlatformBehavior"
        },
        {
            "name": "PlatformerObjectBehavior",
            "type": "PlatformBehavior::PlatformerObjectBehavior"
        }
    ]
}

project["layouts"].append(layout)

# Save to StickScavenger.json
out_file = "StickScavenger.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(project, f, indent=2)
print(f"Generated {out_file} successfully.")

