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

def generate_sprint3():
    with open("data/game_balance.json", "r", encoding="utf-8") as f:
        balance = json.load(f)

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
            "version": "0.3.0",
            "name": "Stick Scavenger",
            "description": "Stick Scavenger - Sprint 3 Push-Your-Luck Risk System (AI Thief, Chaser Beast, Brambles, Stagger, Emergency Drop [Q], Threat Indicator)",
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

    # Gather resources from dummy, sprint2, and sprint3
    all_resource_files = []
    for d in ["assets/dummy", "assets/sprint2", "assets/sprint3"]:
        for root, dirs, files in os.walk(d):
            for f in sorted(files):
                if f.endswith(".png"):
                    full_p = os.path.join(root, f).replace("\\", "/")
                    all_resource_files.append(full_p)

    for rf in sorted(set(all_resource_files)):
        project["resources"]["resources"].append({
            "file": rf,
            "kind": "image",
            "metadata": "",
            "name": rf,
            "smoothed": False,
            "userAdded": True
        })

    # Objects Definition
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

    home_base_obj = {
        "assetStoreId": "",
        "name": "Home_Base",
        "type": "Sprite",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "animations": [
            {
                "name": "Base",
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
                                "centerPoint": {"automatic": True, "name": "centre", "x": 43, "y": 54}
                            }
                        ]
                    }
                ]
            }
        ]
    }

    player_obj = {
        "assetStoreId": "",
        "name": "Player",
        "type": "Sprite",
        "variables": [],
        "behaviors": [
            {
                "name": "PlatformerObjectBehavior",
                "type": "PlatformBehavior::PlatformerObjectBehavior",
                "acceleration": 1500,
                "canGrabPlatforms": False,
                "deceleration": 1500,
                "gravity": 850,
                "ignoreDefaultControls": True,
                "jumpAbortDeceleration": 0,
                "jumpSustainTime": 0.15,
                "jumpSpeed": 380,
                "maxFallingSpeed": 600,
                "maxSpeed": 160,
                "roundCoordinates": True,
                "slopeMaxAngle": 45,
                "xGrabTolerance": 10,
                "yGrabOffset": 0
            }
        ],
        "effects": [],
        "animations": [
            {
                "name": "Idle",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": True,
                        "timeBetweenFrames": 0.18,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": f"assets/dummy/player/player-idle-{i}.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 16, "y": 16}
                            }
                            for i in range(1, 5)
                        ]
                    }
                ]
            },
            {
                "name": "Run",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": True,
                        "timeBetweenFrames": 0.12,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": f"assets/dummy/player/player-run-{i}.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 16, "y": 16}
                            }
                            for i in range(1, 7)
                        ]
                    }
                ]
            },
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
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 16, "y": 16}
                            }
                            for i in range(1, 3)
                        ]
                    }
                ]
            }
        ]
    }

    held_stick_obj = {
        "assetStoreId": "",
        "name": "Held_Stick",
        "type": "Sprite",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "animations": [
            {
                "name": f"Tier_{i}",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": f"assets/dummy/sticks/stick_t{i}.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 8, "y": 8}
                            }
                        ]
                    }
                ]
            }
            for i in range(1, 5)
        ]
    }

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
                "name": f"Tier_{i}",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": f"assets/dummy/sticks/stick_t{i}.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 8, "y": 8}
                            }
                        ]
                    }
                ]
            }
            for i in range(1, 5)
        ]
    }

    bg_l0_sky_obj = {
        "assetStoreId": "",
        "effects": [],
        "height": 360,
        "name": "Bg_L0_Sky",
        "texture": "assets/sprint2/bg_L0_sky.png",
        "type": "TiledSpriteObject::TiledSprite",
        "variables": [],
        "width": 10000
    }

    bg_l1_far_obj = {
        "assetStoreId": "",
        "effects": [],
        "height": 360,
        "name": "Bg_L1_Far",
        "texture": "assets/sprint2/bg_L1_far.png",
        "type": "TiledSpriteObject::TiledSprite",
        "variables": [],
        "width": 10000
    }

    bg_l2_mid_obj = {
        "assetStoreId": "",
        "effects": [],
        "height": 360,
        "name": "Bg_L2_Mid",
        "texture": "assets/sprint2/bg_L2_mid.png",
        "type": "TiledSpriteObject::TiledSprite",
        "variables": [],
        "width": 10000
    }

    bg_l3_near_obj = {
        "assetStoreId": "",
        "effects": [],
        "height": 360,
        "name": "Bg_L3_Near",
        "texture": "assets/sprint2/bg_L3_near.png",
        "type": "TiledSpriteObject::TiledSprite",
        "variables": [],
        "width": 10000
    }

    fg_l5_overlay_obj = {
        "assetStoreId": "",
        "effects": [],
        "height": 360,
        "name": "Fg_L5_Overlay",
        "texture": "assets/sprint2/fg_L5_overlay.png",
        "type": "TiledSpriteObject::TiledSprite",
        "variables": [],
        "width": 10000
    }

    zone_tint_overlay_obj = {
        "assetStoreId": "",
        "effects": [],
        "height": 360,
        "name": "Zone_Tint_Overlay",
        "texture": "assets/sprint2/zone_tint_overlay.png",
        "type": "TiledSpriteObject::TiledSprite",
        "variables": [],
        "width": 640
    }

    ui_slot_frame_obj = {
        "assetStoreId": "",
        "name": "UI_Slot_Frame",
        "type": "Sprite",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "animations": [
            {
                "name": "Frame",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint2/ui/ui_slot_frame.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 14, "y": 14}
                            }
                        ]
                    }
                ]
            }
        ]
    }

    ui_slot_icon_obj = {
        "assetStoreId": "",
        "name": "UI_Slot_Icon",
        "type": "Sprite",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "animations": [
            {
                "name": "Empty",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint2/ui/ui_icon_empty.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 8, "y": 8}
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Tier1",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint2/ui/ui_icon_t1.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 8, "y": 8}
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Tier2",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint2/ui/ui_icon_t2.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 8, "y": 8}
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Tier3",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint2/ui/ui_icon_t3.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 8, "y": 8}
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Tier4",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint2/ui/ui_icon_t4.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 8, "y": 8}
                            }
                        ]
                    }
                ]
            }
        ]
    }

    zone_sign_obj = {
        "assetStoreId": "",
        "name": "Zone_Sign",
        "type": "Sprite",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "animations": [
            {
                "name": "Zone1",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint2/ui/ui_zone_sign_z1.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 12, "y": 16}
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Zone2",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint2/ui/ui_zone_sign_z2.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 12, "y": 16}
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Zone3",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint2/ui/ui_zone_sign_z3.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 12, "y": 16}
                            }
                        ]
                    }
                ]
            }
        ]
    }

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
            "outlineThickness": 2,
            "shadowAngle": 90,
            "shadowBlurRadius": 2,
            "shadowColor": "0;0;0",
            "shadowDistance": 1,
            "shadowOpacity": 128,
            "text": "[E] AMBIL KAYU",
            "textAlignment": "left",
            "underlined": False,
            "verticalTextAlignment": "top"
        }
    }

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
            "text": "SKOR: 0 | ZONA: 0 | MAX DIST: 0 px",
            "textAlignment": "left",
            "underlined": False,
            "verticalTextAlignment": "top"
        }
    }

    txt_slot_label_obj = {
        "name": "Txt_Slot_Label",
        "type": "TextObject::Text",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "content": {
            "bold": True,
            "characterSize": 11,
            "color": "240;240;240",
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
            "text": "SLOT: KOSONG (Tangan Bebas)",
            "textAlignment": "left",
            "underlined": False,
            "verticalTextAlignment": "top"
        }
    }

    txt_zone_banner_obj = {
        "name": "Txt_Zone_Banner",
        "type": "TextObject::Text",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "content": {
            "bold": True,
            "characterSize": 15,
            "color": "255;235;100",
            "font": "",
            "isOutlineEnabled": True,
            "isShadowEnabled": False,
            "italic": False,
            "lineHeight": 0,
            "outlineColor": "0;0;0",
            "outlineThickness": 2.5,
            "shadowAngle": 90,
            "shadowBlurRadius": 2,
            "shadowColor": "0;0;0",
            "shadowDistance": 1,
            "shadowOpacity": 128,
            "text": "~ ZONA 1: PINGGIRAN AMAN ~",
            "textAlignment": "center",
            "underlined": False,
            "verticalTextAlignment": "top"
        }
    }

    txt_floating_gain_obj = {
        "name": "Txt_Floating_Gain",
        "type": "TextObject::Text",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "content": {
            "bold": True,
            "characterSize": 13,
            "color": "100;255;120",
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

    # SPRINT 3 OBJECTS
    hazard_bramble_obj = {
        "assetStoreId": "",
        "name": "Hazard_Bramble",
        "type": "Sprite",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "animations": [
            {
                "name": "Bramble",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint3/hazards/hazard_bramble.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 16, "y": 10}
                            }
                        ]
                    }
                ]
            }
        ]
    }

    safe_barrier_obj = {
        "assetStoreId": "",
        "name": "Safe_Barrier",
        "type": "Sprite",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "animations": [
            {
                "name": "Totem",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint3/hazards/safe_barrier.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 10, "y": 24}
                            }
                        ]
                    }
                ]
            }
        ]
    }

    enemy_thief_obj = {
        "assetStoreId": "",
        "name": "Enemy_Thief",
        "type": "Sprite",
        "variables": [
            {"name": "thief_state", "type": "number", "value": 0},
            {"name": "thief_dir", "type": "number", "value": 1},
            {"name": "thief_flee_timer", "type": "number", "value": 0},
            {"name": "thief_stun_timer", "type": "number", "value": 0},
            {"name": "stolen_tier", "type": "number", "value": 0},
            {"name": "stolen_value", "type": "number", "value": 0}
        ],
        "behaviors": [],
        "effects": [],
        "animations": [
            {
                "name": "Patrol",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": True,
                        "timeBetweenFrames": 0.25,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": f"assets/sprint3/enemies/thief_patrol_{i}.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 12, "y": 12}
                            }
                            for i in [1, 2]
                        ]
                    }
                ]
            },
            {
                "name": "Stalk",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": True,
                        "timeBetweenFrames": 0.15,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": f"assets/sprint3/enemies/thief_stalk_{i}.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 12, "y": 12}
                            }
                            for i in [1, 2]
                        ]
                    }
                ]
            },
            {
                "name": "Flee",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": True,
                        "timeBetweenFrames": 0.15,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": f"assets/sprint3/enemies/thief_flee_{i}.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 12, "y": 12}
                            }
                            for i in [1, 2]
                        ]
                    }
                ]
            },
            {
                "name": "Stun",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": True,
                        "timeBetweenFrames": 0.30,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": f"assets/sprint3/enemies/thief_stun_{i}.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 12, "y": 12}
                            }
                            for i in [1, 2]
                        ]
                    }
                ]
            }
        ]
    }

    enemy_chaser_obj = {
        "assetStoreId": "",
        "name": "Enemy_Chaser",
        "type": "Sprite",
        "variables": [
            {"name": "chaser_state", "type": "number", "value": 0},
            {"name": "chaser_telegraph_timer", "type": "number", "value": 0},
            {"name": "chaser_cooldown", "type": "number", "value": 0}
        ],
        "behaviors": [],
        "effects": [],
        "animations": [
            {
                "name": "Telegraph",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": True,
                        "timeBetweenFrames": 0.15,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": f"assets/sprint3/enemies/chaser_telegraph_{i}.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 16, "y": 16}
                            }
                            for i in [1, 2]
                        ]
                    }
                ]
            },
            {
                "name": "Chase",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": True,
                        "timeBetweenFrames": 0.12,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": f"assets/sprint3/enemies/chaser_chase_{i}.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 16, "y": 16}
                            }
                            for i in [1, 2]
                        ]
                    }
                ]
            },
            {
                "name": "Retreat",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint3/enemies/chaser_retreat_1.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 16, "y": 16}
                            }
                        ]
                    }
                ]
            }
        ]
    }

    ui_alert_indicator_obj = {
        "assetStoreId": "",
        "name": "UI_Alert_Indicator",
        "type": "Sprite",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "animations": [
            {
                "name": "Safe",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint3/ui/ui_alert_safe.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 10, "y": 10}
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Caution",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint3/ui/ui_alert_caution.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 10, "y": 10}
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Danger",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint3/ui/ui_alert_danger.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 10, "y": 10}
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Panic",
                "useMultipleDirections": False,
                "directions": [
                    {
                        "looping": False,
                        "timeBetweenFrames": 1,
                        "sprites": [
                            {
                                "hasCustomCollisionMask": False,
                                "customCollisionMask": [],
                                "image": "assets/sprint3/ui/ui_alert_panic.png",
                                "points": [],
                                "originPoint": {"name": "origine", "x": 0, "y": 0},
                                "centerPoint": {"automatic": True, "name": "centre", "x": 10, "y": 10}
                            }
                        ]
                    }
                ]
            }
        ]
    }

    alert_vignette_obj = {
        "assetStoreId": "",
        "effects": [],
        "height": 360,
        "name": "Alert_Vignette",
        "texture": "assets/sprint3/ui/alert_vignette.png",
        "type": "TiledSpriteObject::TiledSprite",
        "variables": [],
        "width": 640
    }

    txt_warning_banner_obj = {
        "name": "Txt_Warning_Banner",
        "type": "TextObject::Text",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "content": {
            "bold": True,
            "characterSize": 14,
            "color": "255;70;70",
            "font": "",
            "isOutlineEnabled": True,
            "isShadowEnabled": True,
            "italic": False,
            "lineHeight": 0,
            "outlineColor": "40;0;0",
            "outlineThickness": 2,
            "shadowAngle": 90,
            "shadowBlurRadius": 2,
            "shadowColor": "0;0;0",
            "shadowDistance": 1,
            "shadowOpacity": 200,
            "text": "PERINGATAN: ENTITAS BAYANGAN MENDEKAT!",
            "textAlignment": "center",
            "underlined": False,
            "verticalTextAlignment": "top"
        }
    }

    txt_combat_feedback_obj = {
        "name": "Txt_Combat_Feedback",
        "type": "TextObject::Text",
        "variables": [],
        "behaviors": [],
        "effects": [],
        "content": {
            "bold": True,
            "characterSize": 12,
            "color": "255;220;120",
            "font": "",
            "isOutlineEnabled": True,
            "isShadowEnabled": True,
            "italic": False,
            "lineHeight": 0,
            "outlineColor": "20;20;20",
            "outlineThickness": 2,
            "shadowAngle": 90,
            "shadowBlurRadius": 2,
            "shadowColor": "0;0;0",
            "shadowDistance": 1,
            "shadowOpacity": 180,
            "text": "",
            "textAlignment": "center",
            "underlined": False,
            "verticalTextAlignment": "top"
        }
    }

    all_scene_objects = [
        ground_floor_obj, wall_left_obj, home_base_obj,
        bg_l0_sky_obj, bg_l1_far_obj, bg_l2_mid_obj, bg_l3_near_obj,
        fg_l5_overlay_obj, zone_tint_overlay_obj, player_obj,
        held_stick_obj, ground_stick_obj, zone_sign_obj,
        ui_slot_frame_obj, ui_slot_icon_obj, txt_interact_obj,
        txt_hud_obj, txt_slot_label_obj, txt_zone_banner_obj,
        txt_floating_gain_obj,
        # Sprint 3 additions
        hazard_bramble_obj, safe_barrier_obj, enemy_thief_obj,
        enemy_chaser_obj, ui_alert_indicator_obj, alert_vignette_obj,
        txt_warning_banner_obj, txt_combat_feedback_obj
    ]

    initial_instances = [
        {
            "angle": 0, "customSize": True, "depth": 1, "height": 360, "keepRatio": False,
            "layer": "Parallax_L0", "locked": True, "name": "Bg_L0_Sky", "persistentUuid": make_uuid(),
            "width": 10000, "x": -1000, "y": 0, "zOrder": 0,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": True, "depth": 1, "height": 360, "keepRatio": False,
            "layer": "Parallax_L1", "locked": True, "name": "Bg_L1_Far", "persistentUuid": make_uuid(),
            "width": 10000, "x": -1000, "y": 0, "zOrder": 1,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": True, "depth": 1, "height": 360, "keepRatio": False,
            "layer": "Parallax_L2", "locked": True, "name": "Bg_L2_Mid", "persistentUuid": make_uuid(),
            "width": 10000, "x": -1000, "y": 0, "zOrder": 2,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": True, "depth": 1, "height": 360, "keepRatio": False,
            "layer": "Parallax_L3", "locked": True, "name": "Bg_L3_Near", "persistentUuid": make_uuid(),
            "width": 10000, "x": -1000, "y": 0, "zOrder": 3,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
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
        {
            "angle": 0, "customSize": False, "height": 108, "keepRatio": True,
            "layer": "", "locked": False, "name": "Home_Base", "persistentUuid": make_uuid(),
            "width": 87, "x": 24, "y": 188, "zOrder": 2,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        # Safe Barrier Totem at X=180
        {
            "angle": 0, "customSize": False, "height": 48, "keepRatio": True,
            "layer": "", "locked": False, "name": "Safe_Barrier", "persistentUuid": make_uuid(),
            "width": 20, "x": 180, "y": 248, "zOrder": 4,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        # Zone Signs
        {
            "angle": 0, "customSize": False, "height": 32, "keepRatio": True,
            "layer": "", "locked": False, "name": "Zone_Sign", "persistentUuid": make_uuid(),
            "width": 24, "x": 640, "y": 264, "zOrder": 3,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 32, "keepRatio": True,
            "layer": "", "locked": False, "name": "Zone_Sign", "persistentUuid": make_uuid(),
            "width": 24, "x": 1920, "y": 264, "zOrder": 3,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 32, "keepRatio": True,
            "layer": "", "locked": False, "name": "Zone_Sign", "persistentUuid": make_uuid(),
            "width": 24, "x": 4480, "y": 264, "zOrder": 3,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        # Bramble Hazards in Zone 2 & Zone 3
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "", "locked": False, "name": "Hazard_Bramble", "persistentUuid": make_uuid(),
            "width": 32, "x": 2280, "y": 276, "zOrder": 4,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "", "locked": False, "name": "Hazard_Bramble", "persistentUuid": make_uuid(),
            "width": 32, "x": 2880, "y": 276, "zOrder": 4,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "", "locked": False, "name": "Hazard_Bramble", "persistentUuid": make_uuid(),
            "width": 32, "x": 3560, "y": 276, "zOrder": 4,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "", "locked": False, "name": "Hazard_Bramble", "persistentUuid": make_uuid(),
            "width": 32, "x": 4160, "y": 276, "zOrder": 4,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "", "locked": False, "name": "Hazard_Bramble", "persistentUuid": make_uuid(),
            "width": 32, "x": 4880, "y": 276, "zOrder": 4,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "", "locked": False, "name": "Hazard_Bramble", "persistentUuid": make_uuid(),
            "width": 32, "x": 5560, "y": 276, "zOrder": 4,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "", "locked": False, "name": "Hazard_Bramble", "persistentUuid": make_uuid(),
            "width": 32, "x": 6280, "y": 276, "zOrder": 4,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "", "locked": False, "name": "Hazard_Bramble", "persistentUuid": make_uuid(),
            "width": 32, "x": 6980, "y": 276, "zOrder": 4,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "", "locked": False, "name": "Hazard_Bramble", "persistentUuid": make_uuid(),
            "width": 32, "x": 7680, "y": 276, "zOrder": 4,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        # Enemy Thief
        {
            "angle": 0, "customSize": False, "height": 24, "keepRatio": True,
            "layer": "", "locked": False, "name": "Enemy_Thief", "persistentUuid": make_uuid(),
            "width": 24, "x": 2100, "y": 272, "zOrder": 8,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        # Enemy Chaser (starts dormant offscreen)
        {
            "angle": 0, "customSize": False, "height": 32, "keepRatio": True,
            "layer": "", "locked": False, "name": "Enemy_Chaser", "persistentUuid": make_uuid(),
            "width": 32, "x": -1000, "y": 264, "zOrder": 9,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        # Player and Held Stick
        {
            "angle": 0, "customSize": False, "height": 32, "keepRatio": True,
            "layer": "", "locked": False, "name": "Player", "persistentUuid": make_uuid(),
            "width": 33, "x": 100, "y": 260, "zOrder": 10,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 16, "keepRatio": True,
            "layer": "", "locked": False, "name": "Held_Stick", "persistentUuid": make_uuid(),
            "width": 16, "x": 100, "y": 260, "zOrder": 11,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        # Foreground Layer
        {
            "angle": 0, "customSize": True, "depth": 1, "height": 360, "keepRatio": False,
            "layer": "Foreground_L5", "locked": True, "name": "Fg_L5_Overlay", "persistentUuid": make_uuid(),
            "width": 10000, "x": -1000, "y": 0, "zOrder": 1,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        # In-game Floating Texts
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "", "locked": False, "name": "Txt_Floating_Gain", "persistentUuid": make_uuid(),
            "width": 120, "x": 50, "y": 160, "zOrder": 25,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "", "locked": False, "name": "Txt_Interact", "persistentUuid": make_uuid(),
            "width": 120, "x": 0, "y": 0, "zOrder": 20,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "", "locked": False, "name": "Txt_Combat_Feedback", "persistentUuid": make_uuid(),
            "width": 200, "x": 0, "y": 0, "zOrder": 26,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        # UI Layer Elements
        {
            "angle": 0, "customSize": True, "depth": 1, "height": 360, "keepRatio": False,
            "layer": "UI", "locked": True, "name": "Zone_Tint_Overlay", "persistentUuid": make_uuid(),
            "width": 640, "x": 0, "y": 0, "zOrder": 1,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": True, "depth": 1, "height": 360, "keepRatio": False,
            "layer": "UI", "locked": True, "name": "Alert_Vignette", "persistentUuid": make_uuid(),
            "width": 640, "x": 0, "y": 0, "zOrder": 2,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 28, "keepRatio": True,
            "layer": "UI", "locked": True, "name": "UI_Slot_Frame", "persistentUuid": make_uuid(),
            "width": 28, "x": 12, "y": 32, "zOrder": 15,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 16, "keepRatio": True,
            "layer": "UI", "locked": True, "name": "UI_Slot_Icon", "persistentUuid": make_uuid(),
            "width": 16, "x": 18, "y": 38, "zOrder": 16,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "UI", "locked": True, "name": "UI_Alert_Indicator", "persistentUuid": make_uuid(),
            "width": 20, "x": 16, "y": 66, "zOrder": 17,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 20, "keepRatio": True,
            "layer": "UI", "locked": True, "name": "Txt_Slot_Label", "persistentUuid": make_uuid(),
            "width": 380, "x": 44, "y": 36, "zOrder": 18,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 24, "keepRatio": True,
            "layer": "UI", "locked": True, "name": "Txt_HUD", "persistentUuid": make_uuid(),
            "width": 550, "x": 12, "y": 10, "zOrder": 20,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 24, "keepRatio": True,
            "layer": "UI", "locked": True, "name": "Txt_Zone_Banner", "persistentUuid": make_uuid(),
            "width": 320, "x": 160, "y": 64, "zOrder": 22,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        },
        {
            "angle": 0, "customSize": False, "height": 24, "keepRatio": True,
            "layer": "UI", "locked": True, "name": "Txt_Warning_Banner", "persistentUuid": make_uuid(),
            "width": 320, "x": 160, "y": 88, "zOrder": 23,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        }
    ]

    scene_vars = [
        # Sprint 1 & 2 variables
        {"name": "facing_dir", "type": "number", "value": 1},
        {"name": "held_tier", "type": "number", "value": 0},
        {"name": "held_value", "type": "number", "value": 0},
        {"name": "swap_cooldown", "type": "number", "value": 0},
        {"name": "total_score", "type": "number", "value": 0},
        {"name": "max_dist_x", "type": "number", "value": 0},
        {"name": "current_chunk", "type": "number", "value": 0},
        {"name": "current_zone", "type": "number", "value": 0},
        {"name": "prev_zone", "type": "number", "value": 0},
        {"name": "banner_timer", "type": "number", "value": 0},
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
        {"name": "gain_timer", "type": "number", "value": 0},
        {"name": "val_diff", "type": "number", "value": 0},
        # Sprint 3 variables (ALL NUMBERS)
        {"name": "stagger_timer", "type": "number", "value": 0},
        {"name": "invuln_timer", "type": "number", "value": 0},
        {"name": "shake_timer", "type": "number", "value": 0},
        {"name": "shake_x", "type": "number", "value": 0},
        {"name": "shake_y", "type": "number", "value": 0},
        {"name": "thief_state", "type": "number", "value": 0},
        {"name": "thief_dir", "type": "number", "value": 1},
        {"name": "thief_flee_timer", "type": "number", "value": 0},
        {"name": "thief_stun_timer", "type": "number", "value": 0},
        {"name": "stolen_tier", "type": "number", "value": 0},
        {"name": "stolen_value", "type": "number", "value": 0},
        {"name": "chaser_state", "type": "number", "value": 0},
        {"name": "chaser_telegraph_timer", "type": "number", "value": 0},
        {"name": "chaser_cooldown", "type": "number", "value": 0},
        {"name": "chaser_speed", "type": "number", "value": 124},
        {"name": "warning_timer", "type": "number", "value": 0},
        {"name": "alert_level", "type": "number", "value": 0},
        {"name": "alert_pulse_time", "type": "number", "value": 0},
        {"name": "barrier_flash_timer", "type": "number", "value": 0},
        {"name": "is_slowed", "type": "number", "value": 0},
        {"name": "emergency_drop_cooldown", "type": "number", "value": 0},
        {"name": "combat_feedback_timer", "type": "number", "value": 0}
    ]

    layers = [
        {
            "ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0,
            "camera3DFairDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearDistance": 1,
            "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False,
            "isLocked": False, "name": "Parallax_L0", "renderingType": "", "visibility": True
        },
        {
            "ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0,
            "camera3DFairDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearDistance": 1,
            "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False,
            "isLocked": False, "name": "Parallax_L1", "renderingType": "", "visibility": True
        },
        {
            "ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0,
            "camera3DFairDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearDistance": 1,
            "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False,
            "isLocked": False, "name": "Parallax_L2", "renderingType": "", "visibility": True
        },
        {
            "ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0,
            "camera3DFairDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearDistance": 1,
            "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False,
            "isLocked": False, "name": "Parallax_L3", "renderingType": "", "visibility": True
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
            "isLocked": False, "name": "Foreground_L5", "renderingType": "", "visibility": True
        },
        {
            "ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0,
            "camera3DFairDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearDistance": 1,
            "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False,
            "isLocked": False, "name": "UI", "renderingType": "", "visibility": True
        }
    ]

    events = []

    # 1. Frame Updates (Timers, Zones, Tracking, Floating Text)
    ev_frame_updates = make_event(
        conditions=[],
        actions=[
            make_inst("ModVarScene", ["swap_cooldown", "=", "max(0, Variable(swap_cooldown) - TimeDelta())"]),
            make_inst("ModVarScene", ["gain_timer", "=", "max(0, Variable(gain_timer) - TimeDelta())"]),
            make_inst("ModVarScene", ["current_chunk", "=", "floor(max(0, Player.CenterX()) / 640)"]),
            # Sprint 3 timers update
            make_inst("ModVarScene", ["stagger_timer", "=", "max(0, Variable(stagger_timer) - TimeDelta())"]),
            make_inst("ModVarScene", ["invuln_timer", "=", "max(0, Variable(invuln_timer) - TimeDelta())"]),
            make_inst("ModVarScene", ["shake_timer", "=", "max(0, Variable(shake_timer) - TimeDelta())"]),
            make_inst("ModVarScene", ["warning_timer", "=", "max(0, Variable(warning_timer) - TimeDelta())"]),
            make_inst("ModVarScene", ["barrier_flash_timer", "=", "max(0, Variable(barrier_flash_timer) - TimeDelta())"]),
            make_inst("ModVarScene", ["emergency_drop_cooldown", "=", "max(0, Variable(emergency_drop_cooldown) - TimeDelta())"]),
            make_inst("ModVarScene", ["combat_feedback_timer", "=", "max(0, Variable(combat_feedback_timer) - TimeDelta())"]),
            make_inst("ModVarScene", ["alert_pulse_time", "+", "TimeDelta()"])
        ],
        sub_events=[
            # Floating gain text
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
            # Floating combat feedback text
            make_event(
                conditions=[make_inst("VarScene", ["combat_feedback_timer", ">", "0"])],
                actions=[
                    make_inst("SetY", ["Txt_Combat_Feedback", "-", "20 * TimeDelta()"]),
                    make_inst("Show", ["Txt_Combat_Feedback", ""])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["combat_feedback_timer", "<=", "0"])],
                actions=[
                    make_inst("Hide", ["Txt_Combat_Feedback"])
                ]
            ),
            # Zone triggers
            make_event(
                conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<=", "160"])],
                actions=[make_inst("ModVarScene", ["current_zone", "=", "0"])]
            ),
            make_event(
                conditions=[
                    make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">", "160"]),
                    make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<", "1920"])
                ],
                actions=[make_inst("ModVarScene", ["current_zone", "=", "1"])]
            ),
            make_event(
                conditions=[
                    make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">=", "1920"]),
                    make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<", "4480"])
                ],
                actions=[make_inst("ModVarScene", ["current_zone", "=", "2"])]
            ),
            make_event(
                conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">=", "4480"])],
                actions=[make_inst("ModVarScene", ["current_zone", "=", "3"])]
            ),
            make_event(
                conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">", "Variable(max_dist_x)"])],
                actions=[make_inst("ModVarScene", ["max_dist_x", "=", "Player.CenterX()"])]
            )
        ]
    )
    events.append(ev_frame_updates)

    # 2. Bramble Hazard Collision Check
    ev_brambles_hazard = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            make_event(
                conditions=[
                    make_inst("CollisionNP", ["Player", "Hazard_Bramble", "", "no"])
                ],
                actions=[
                    make_inst("ModVarScene", ["is_slowed", "=", "1"])
                ]
            ),
            make_event(
                conditions=[
                    make_inst("CollisionNP", ["Player", "Hazard_Bramble", "", "no"], inverted=True)
                ],
                actions=[
                    make_inst("ModVarScene", ["is_slowed", "=", "0"])
                ]
            )
        ]
    )
    events.append(ev_brambles_hazard)

    # 3. Player Speed Calculation (Weight + Brambles)
    ev_player_speed = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Tier 0 / Tier 1 (Base Speed 160)
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "<=", "1"])],
                actions=[],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "0"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "160"])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "1"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "88"])]
                    )
                ]
            ),
            # Tier 2 (Base Speed 152)
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "2"])],
                actions=[],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "0"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "152"])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "1"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "84"])]
                    )
                ]
            ),
            # Tier 3 (Base Speed 144)
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "3"])],
                actions=[],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "0"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "144"])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "1"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "79"])]
                    )
                ]
            ),
            # Tier 4 (Base Speed 136)
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "4"])],
                actions=[],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "0"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "136"])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "1"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "75"])]
                    )
                ]
            )
        ]
    )
    events.append(ev_player_speed)

    # 4. Player Stagger & Invulnerability State
    ev_stagger_and_invuln = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Stagger active: knockback and red tint
            make_event(
                conditions=[make_inst("VarScene", ["stagger_timer", ">", "0"])],
                actions=[
                    make_inst("SetX", ["Player", "-", "135 * TimeDelta()"]),
                    make_inst("SetX", ["Player", "=", "max(16, Player.X())"]),
                    make_inst("SetColor", ["Player", "\"255;100;100\""])
                ]
            ),
            # Stagger ended: check invulnerability blink
            make_event(
                conditions=[make_inst("VarScene", ["stagger_timer", "<=", "0"])],
                actions=[],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["invuln_timer", ">", "0"])],
                        actions=[
                            make_inst("SetOpacity", ["Player", "=", "130 + 120 * cos(Variable(invuln_timer) * 25)"]),
                            make_inst("SetColor", ["Player", "\"255;255;255\""])
                        ]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["invuln_timer", "<=", "0"])],
                        actions=[
                            make_inst("SetOpacity", ["Player", "=", "255"]),
                            make_inst("SetColor", ["Player", "\"255;255;255\""])
                        ]
                    )
                ]
            )
        ]
    )
    events.append(ev_stagger_and_invuln)

    # 5. Zone Triggers & Banners
    ev_zone_triggers = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            make_event(
                conditions=[
                    make_inst("BuiltinCommonInstructions::CompareNumbers", ["Variable(current_zone)", "!=", "Variable(prev_zone)"])
                ],
                actions=[
                    make_inst("ModVarScene", ["prev_zone", "=", "Variable(current_zone)"]),
                    make_inst("ModVarScene", ["banner_timer", "=", "2.5"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["current_zone", "=", "0"])],
                        actions=[make_inst("TextObject::String", ["Txt_Zone_Banner", "=", "\"~ ZONA AMAN: HOME BASE ~\""])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["current_zone", "=", "1"])],
                        actions=[make_inst("TextObject::String", ["Txt_Zone_Banner", "=", "\"~ ZONA 1: PINGGIRAN AMAN ~\""])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["current_zone", "=", "2"])],
                        actions=[make_inst("TextObject::String", ["Txt_Zone_Banner", "=", "\"~ ZONA 2: HUTAN BERBISIK ~\""])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["current_zone", "=", "3"])],
                        actions=[make_inst("TextObject::String", ["Txt_Zone_Banner", "=", "\"~ ZONA 3: WILAYAH TERLARANG ~\""])]
                    )
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["banner_timer", ">", "0"])],
                actions=[
                    make_inst("ModVarScene", ["banner_timer", "=", "max(0, Variable(banner_timer) - TimeDelta())"]),
                    make_inst("Show", ["Txt_Zone_Banner", ""])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["banner_timer", "<=", "0"])],
                actions=[
                    make_inst("Hide", ["Txt_Zone_Banner"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["current_zone", "=", "0"])],
                actions=[
                    make_inst("TiledSpriteObject::SetOpacity", ["Zone_Tint_Overlay", "=", "0"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["current_zone", "=", "1"])],
                actions=[
                    make_inst("TiledSpriteObject::SetColor", ["Zone_Tint_Overlay", "\"220;255;230\""]),
                    make_inst("TiledSpriteObject::SetOpacity", ["Zone_Tint_Overlay", "=", "18"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["current_zone", "=", "2"])],
                actions=[
                    make_inst("TiledSpriteObject::SetColor", ["Zone_Tint_Overlay", "\"240;190;130\""]),
                    make_inst("TiledSpriteObject::SetOpacity", ["Zone_Tint_Overlay", "=", "35"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["current_zone", "=", "3"])],
                actions=[
                    make_inst("TiledSpriteObject::SetColor", ["Zone_Tint_Overlay", "\"160;100;220\""]),
                    make_inst("TiledSpriteObject::SetOpacity", ["Zone_Tint_Overlay", "=", "50"])
                ]
            )
        ]
    )
    events.append(ev_zone_triggers)

    # 6. Player Controls (D/Right) - Gated by Stagger
    ev_right = make_event(
        conditions=[
            make_inst("VarScene", ["stagger_timer", "<=", "0"]),
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

    # 7. Player Controls (A/Left) - Gated by Stagger
    ev_left = make_event(
        conditions=[
            make_inst("VarScene", ["stagger_timer", "<=", "0"]),
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

    # 8. Player Controls (Jump) - Gated by Stagger
    ev_jump = make_event(
        conditions=[
            make_inst("VarScene", ["stagger_timer", "<=", "0"]),
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

    # 9. Player Animations
    ev_anim = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            make_event(
                conditions=[
                    make_inst("PlatformBehavior::IsOnFloor", ["Player", "PlatformerObjectBehavior"]),
                    make_inst("PlatformBehavior::IsMoving", ["Player", "PlatformerObjectBehavior"])
                ],
                actions=[make_inst("ChangeAnimation", ["Player", "=", "1"])]
            ),
            make_event(
                conditions=[
                    make_inst("PlatformBehavior::IsOnFloor", ["Player", "PlatformerObjectBehavior"]),
                    make_inst("PlatformBehavior::IsMoving", ["Player", "PlatformerObjectBehavior"], inverted=True)
                ],
                actions=[make_inst("ChangeAnimation", ["Player", "=", "0"])]
            ),
            make_event(
                conditions=[
                    make_inst("PlatformBehavior::IsOnFloor", ["Player", "PlatformerObjectBehavior"], inverted=True)
                ],
                actions=[make_inst("ChangeAnimation", ["Player", "=", "2"])]
            )
        ]
    )
    events.append(ev_anim)

    # 10. Emergency Drop [Q]
    ev_emergency_drop = make_event(
        conditions=[
            make_inst("KeyPressed", ["", "q"]),
            make_inst("BuiltinCommonInstructions::Once", []),
            make_inst("VarScene", ["held_tier", ">", "0"]),
            make_inst("VarScene", ["emergency_drop_cooldown", "<=", "0"])
        ],
        actions=[
            make_inst("Create", ["", "Ground_Stick", "Player.CenterX() - 8", "296 - 16", "\"\""]),
            make_inst("ModVarObjet", ["Ground_Stick", "tier", "=", "Variable(held_tier)"]),
            make_inst("ModVarObjet", ["Ground_Stick", "base_value", "=", "Variable(held_value)"]),
            make_inst("ModVarObjet", ["Ground_Stick", "chunk_id", "=", "floor(Player.CenterX() / 640)"]),
            make_inst("ChangeAnimation", ["Ground_Stick", "=", "Variable(held_tier) - 1"]),
            make_inst("SetZOrder", ["Ground_Stick", "=", "5"]),
            make_inst("ModVarScene", ["held_tier", "=", "0"]),
            make_inst("ModVarScene", ["held_value", "=", "0"]),
            make_inst("ModVarScene", ["emergency_drop_cooldown", "=", "0.30"]),
            make_inst("TextObject::String", ["Txt_Combat_Feedback", "=", "\"[Q] EMERGENCY DROP! LARI!\""]),
            make_inst("SetXY", ["Txt_Combat_Feedback", "=", "Player.CenterX() - 60", "=", "Player.Y() - 24"]),
            make_inst("Show", ["Txt_Combat_Feedback", ""]),
            make_inst("ModVarScene", ["combat_feedback_timer", "=", "1.2"])
        ]
    )
    events.append(ev_emergency_drop)

    # 11. Camera Shake & Parallax Integration (Rule 6)
    ev_parallax_camera = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Shake timer update
            make_event(
                conditions=[make_inst("VarScene", ["shake_timer", ">", "0"])],
                actions=[
                    make_inst("ModVarScene", ["shake_x", "=", "RandomInRange(-4, 4)"]),
                    make_inst("ModVarScene", ["shake_y", "=", "RandomInRange(-3, 3)"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["shake_timer", "<=", "0"])],
                actions=[
                    make_inst("ModVarScene", ["shake_x", "=", "0"]),
                    make_inst("ModVarScene", ["shake_y", "=", "0"])
                ]
            ),
            # Camera Position Base Layer + Shake Offset & Parallax Layers
            make_event(
                conditions=[],
                actions=[
                    make_inst("ZoomCamera", ["", "1", "\"\"", "0"]),
                    make_inst("SetCameraCenterX", ["", "=", "round(clamp(Player.CenterX() + Variable(facing_dir) * 48, 320, 8000)) + Variable(shake_x)", "\"\"", "0"]),
                    make_inst("SetCameraCenterY", ["", "=", "180 + Variable(shake_y)", "\"\"", "0"]),
                    make_inst("SetCameraCenterX", ["", "=", "round(CameraX(\"\", 0) * 0.05)", "\"Parallax_L0\"", "0"]),
                    make_inst("SetCameraCenterY", ["", "=", "180", "\"Parallax_L0\"", "0"]),
                    make_inst("SetCameraCenterX", ["", "=", "round(CameraX(\"\", 0) * 0.15)", "\"Parallax_L1\"", "0"]),
                    make_inst("SetCameraCenterY", ["", "=", "180", "\"Parallax_L1\"", "0"]),
                    make_inst("SetCameraCenterX", ["", "=", "round(CameraX(\"\", 0) * 0.35)", "\"Parallax_L2\"", "0"]),
                    make_inst("SetCameraCenterY", ["", "=", "180", "\"Parallax_L2\"", "0"]),
                    make_inst("SetCameraCenterX", ["", "=", "round(CameraX(\"\", 0) * 0.65)", "\"Parallax_L3\"", "0"]),
                    make_inst("SetCameraCenterY", ["", "=", "180", "\"Parallax_L3\"", "0"]),
                    make_inst("SetCameraCenterX", ["", "=", "round(CameraX(\"\", 0) * 1.15)", "\"Foreground_L5\"", "0"]),
                    make_inst("SetCameraCenterY", ["", "=", "180", "\"Foreground_L5\"", "0"])
                ]
            )
        ]
    )
    events.append(ev_parallax_camera)

    # 12. Held Stick Visual
    ev_held_stick = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "0"])],
                actions=[make_inst("Hide", ["Held_Stick"])]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", ">", "0"])],
                actions=[
                    make_inst("Show", ["Held_Stick", ""]),
                    make_inst("ChangeAnimation", ["Held_Stick", "=", "Variable(held_tier) - 1"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["facing_dir", "=", "1"])],
                        actions=[
                            make_inst("FlipX", ["Held_Stick", "no"]),
                            make_inst("SetXY", ["Held_Stick", "=", "Player.CenterX() + 8", "=", "Player.CenterY() + 1"])
                        ]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["facing_dir", "=", "-1"])],
                        actions=[
                            make_inst("FlipX", ["Held_Stick", "yes"]),
                            make_inst("SetXY", ["Held_Stick", "=", "Player.CenterX() - 8", "=", "Player.CenterY() + 1"])
                        ]
                    )
                ]
            )
        ]
    )
    events.append(ev_held_stick)

    # 13. AI Pencuri (Thief AI) System
    ev_thief_ai = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Safe Barrier Repulsion: cannot go past X=180
            make_event(
                conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Enemy_Thief.X()", "<", "180"])],
                actions=[
                    make_inst("SetX", ["Enemy_Thief", "=", "180"]),
                    make_inst("ModVarScene", ["thief_dir", "=", "1"]),
                    make_inst("FlipX", ["Enemy_Thief", "no"])
                ]
            ),
            # State 0: Patrol
            make_event(
                conditions=[make_inst("VarScene", ["thief_state", "=", "0"])],
                actions=[
                    make_inst("ChangeAnimation", ["Enemy_Thief", "=", "0"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["thief_dir", "=", "1"])],
                        actions=[
                            make_inst("SetX", ["Enemy_Thief", "+", "65 * TimeDelta()"]),
                            make_inst("FlipX", ["Enemy_Thief", "no"])
                        ],
                        sub_events=[
                            make_event(
                                conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Enemy_Thief.X()", ">=", "2500"])],
                                actions=[make_inst("ModVarScene", ["thief_dir", "=", "-1"])]
                            )
                        ]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["thief_dir", "=", "-1"])],
                        actions=[
                            make_inst("SetX", ["Enemy_Thief", "-", "65 * TimeDelta()"]),
                            make_inst("FlipX", ["Enemy_Thief", "yes"])
                        ],
                        sub_events=[
                            make_event(
                                conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Enemy_Thief.X()", "<=", "1950"])],
                                actions=[make_inst("ModVarScene", ["thief_dir", "=", "1"])]
                            )
                        ]
                    ),
                    # Detection Check: Player within 220px, beyond barrier, carrying stick
                    make_event(
                        conditions=[
                            make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">", "180"]),
                            make_inst("Distance", ["Enemy_Thief", "Player", "220", ""]),
                            make_inst("VarScene", ["held_tier", ">", "0"])
                        ],
                        actions=[
                            make_inst("ModVarScene", ["thief_state", "=", "1"]),
                            make_inst("TextObject::String", ["Txt_Combat_Feedback", "=", "\"PENCURI MENGINCAR KAYUMU!\""]),
                            make_inst("SetXY", ["Txt_Combat_Feedback", "=", "Enemy_Thief.CenterX() - 60", "=", "Enemy_Thief.Y() - 20"]),
                            make_inst("Show", ["Txt_Combat_Feedback", ""]),
                            make_inst("ModVarScene", ["combat_feedback_timer", "=", "1.5"])
                        ]
                    )
                ]
            ),
            # State 1: Stalk / Pursuing Player
            make_event(
                conditions=[make_inst("VarScene", ["thief_state", "=", "1"])],
                actions=[
                    make_inst("ChangeAnimation", ["Enemy_Thief", "=", "1"])
                ],
                sub_events=[
                    # If player dropped stick, thief loses interest
                    make_event(
                        conditions=[make_inst("VarScene", ["held_tier", "=", "0"])],
                        actions=[make_inst("ModVarScene", ["thief_state", "=", "0"])]
                    ),
                    # If player still carries stick, pursue
                    make_event(
                        conditions=[make_inst("VarScene", ["held_tier", ">", "0"])],
                        actions=[],
                        sub_events=[
                            make_event(
                                conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">", "Enemy_Thief.CenterX()"])],
                                actions=[
                                    make_inst("SetX", ["Enemy_Thief", "+", "118 * TimeDelta()"]),
                                    make_inst("FlipX", ["Enemy_Thief", "no"])
                                ]
                            ),
                            make_event(
                                conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<", "Enemy_Thief.CenterX()"])],
                                actions=[
                                    make_inst("SetX", ["Enemy_Thief", "-", "118 * TimeDelta()"]),
                                    make_inst("FlipX", ["Enemy_Thief", "yes"])
                                ]
                            ),
                            # Steal collision check
                            make_event(
                                conditions=[
                                    make_inst("Distance", ["Enemy_Thief", "Player", "22", ""]),
                                    make_inst("VarScene", ["invuln_timer", "<=", "0"])
                                ],
                                actions=[
                                    make_inst("ModVarScene", ["stolen_tier", "=", "Variable(held_tier)"]),
                                    make_inst("ModVarScene", ["stolen_value", "=", "Variable(held_value)"]),
                                    make_inst("ModVarScene", ["held_tier", "=", "0"]),
                                    make_inst("ModVarScene", ["held_value", "=", "0"]),
                                    make_inst("ModVarScene", ["thief_state", "=", "2"]),
                                    make_inst("ModVarScene", ["thief_flee_timer", "=", "6.0"]),
                                    make_inst("ModVarScene", ["stagger_timer", "=", "0.70"]),
                                    make_inst("ModVarScene", ["invuln_timer", "=", "1.60"]),
                                    make_inst("ModVarScene", ["shake_timer", "=", "0.35"]),
                                    make_inst("TextObject::String", ["Txt_Combat_Feedback", "=", "\"KAYU DICURI! KEJAR PENCURI!\""]),
                                    make_inst("SetXY", ["Txt_Combat_Feedback", "=", "Player.CenterX() - 65", "=", "Player.Y() - 24"]),
                                    make_inst("Show", ["Txt_Combat_Feedback", ""]),
                                    make_inst("ModVarScene", ["combat_feedback_timer", "=", "2.0"])
                                ]
                            )
                        ]
                    )
                ]
            ),
            # State 2: Fleeing with Loot
            make_event(
                conditions=[make_inst("VarScene", ["thief_state", "=", "2"])],
                actions=[
                    make_inst("ChangeAnimation", ["Enemy_Thief", "=", "2"]),
                    make_inst("ModVarScene", ["thief_flee_timer", "=", "max(0, Variable(thief_flee_timer) - TimeDelta())"])
                ],
                sub_events=[
                    # Run away from player
                    make_event(
                        conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<=", "Enemy_Thief.CenterX()"])],
                        actions=[
                            make_inst("SetX", ["Enemy_Thief", "+", "134 * TimeDelta()"]),
                            make_inst("FlipX", ["Enemy_Thief", "no"])
                        ]
                    ),
                    make_event(
                        conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">", "Enemy_Thief.CenterX()"])],
                        actions=[
                            make_inst("SetX", ["Enemy_Thief", "-", "134 * TimeDelta()"]),
                            make_inst("FlipX", ["Enemy_Thief", "yes"])
                        ]
                    ),
                    # Recapture mechanic
                    make_event(
                        conditions=[
                            make_inst("Distance", ["Player", "Enemy_Thief", "34", ""]),
                            make_inst("VarScene", ["stagger_timer", "<=", "0"])
                        ],
                        actions=[
                            make_inst("ModVarScene", ["thief_state", "=", "3"]),
                            make_inst("ModVarScene", ["thief_stun_timer", "=", "8.0"]),
                            # Drop the stolen stick on ground
                            make_inst("Create", ["", "Ground_Stick", "Enemy_Thief.CenterX() - 8", "296 - 16", "\"\""]),
                            make_inst("ModVarObjet", ["Ground_Stick", "tier", "=", "Variable(stolen_tier)"]),
                            make_inst("ModVarObjet", ["Ground_Stick", "base_value", "=", "Variable(stolen_value)"]),
                            make_inst("ModVarObjet", ["Ground_Stick", "chunk_id", "=", "floor(Enemy_Thief.CenterX() / 640)"]),
                            make_inst("ChangeAnimation", ["Ground_Stick", "=", "Variable(stolen_tier) - 1"]),
                            make_inst("SetZOrder", ["Ground_Stick", "=", "5"]),
                            make_inst("ModVarScene", ["stolen_tier", "=", "0"]),
                            make_inst("ModVarScene", ["stolen_value", "=", "0"]),
                            make_inst("TextObject::String", ["Txt_Combat_Feedback", "=", "\"KAYU BERHASIL DIREBUT KEMBALI!\""]),
                            make_inst("SetXY", ["Txt_Combat_Feedback", "=", "Enemy_Thief.CenterX() - 65", "=", "Enemy_Thief.Y() - 24"]),
                            make_inst("Show", ["Txt_Combat_Feedback", ""]),
                            make_inst("ModVarScene", ["combat_feedback_timer", "=", "1.8"]),
                            make_inst("ModVarScene", ["shake_timer", "=", "0.20"])
                        ]
                    ),
                    # Escape timeout
                    make_event(
                        conditions=[make_inst("VarScene", ["thief_flee_timer", "<=", "0"])],
                        actions=[
                            make_inst("SetXY", ["Enemy_Thief", "=", "2200", "=", "272"]),
                            make_inst("ModVarScene", ["thief_state", "=", "0"]),
                            make_inst("ModVarScene", ["stolen_tier", "=", "0"]),
                            make_inst("ModVarScene", ["stolen_value", "=", "0"]),
                            make_inst("TextObject::String", ["Txt_Combat_Feedback", "=", "\"PENCURI KABUR MEMBAWA KAYUMU...\""]),
                            make_inst("SetXY", ["Txt_Combat_Feedback", "=", "Player.CenterX() - 60", "=", "Player.Y() - 24"]),
                            make_inst("Show", ["Txt_Combat_Feedback", ""]),
                            make_inst("ModVarScene", ["combat_feedback_timer", "=", "2.0"])
                        ]
                    )
                ]
            ),
            # State 3: Stunned
            make_event(
                conditions=[make_inst("VarScene", ["thief_state", "=", "3"])],
                actions=[
                    make_inst("ChangeAnimation", ["Enemy_Thief", "=", "3"]),
                    make_inst("ModVarScene", ["thief_stun_timer", "=", "max(0, Variable(thief_stun_timer) - TimeDelta())"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["thief_stun_timer", "<=", "0"])],
                        actions=[make_inst("ModVarScene", ["thief_state", "=", "0"])]
                    )
                ]
            )
        ]
    )
    events.append(ev_thief_ai)

    # 14. AI Entitas Pengejar (Chaser AI) System
    ev_chaser_ai = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Activation Check
            make_event(
                conditions=[
                    make_inst("VarScene", ["chaser_state", "=", "0"]),
                    make_inst("VarScene", ["chaser_cooldown", "<=", "0"]),
                    make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">=", "1920"]),
                    make_inst("BuiltinCommonInstructions::Or", [], False, [
                        make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">=", "4800"]),
                        make_inst("BuiltinCommonInstructions::And", [], False, [
                            make_inst("VarScene", ["held_tier", ">=", "3"]),
                            make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">=", "2500"])
                        ])
                    ])
                ],
                actions=[
                    make_inst("ModVarScene", ["chaser_state", "=", "1"]),
                    make_inst("ModVarScene", ["chaser_telegraph_timer", "=", "1.2"]),
                    make_inst("ModVarScene", ["warning_timer", "=", "2.0"]),
                    make_inst("SetXY", ["Enemy_Chaser", "=", "clamp(Player.CenterX() + 270, 200, 7800)", "=", "264"]),
                    make_inst("Show", ["Enemy_Chaser", ""]),
                    make_inst("ChangeAnimation", ["Enemy_Chaser", "=", "0"]),
                    make_inst("ModVarScene", ["shake_timer", "=", "0.35"]),
                    make_inst("TextObject::String", ["Txt_Warning_Banner", "=", "\"PERINGATAN: ENTITAS BAYANGAN MENDEKAT!\""]),
                    make_inst("Show", ["Txt_Warning_Banner", ""])
                ]
            ),
            # State 1: Telegraphing
            make_event(
                conditions=[make_inst("VarScene", ["chaser_state", "=", "1"])],
                actions=[
                    make_inst("ModVarScene", ["chaser_telegraph_timer", "=", "max(0, Variable(chaser_telegraph_timer) - TimeDelta())"]),
                    make_inst("SetOpacity", ["Enemy_Chaser", "=", "120 + 120 * cos(Variable(chaser_telegraph_timer) * 30)"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["chaser_telegraph_timer", "<=", "0"])],
                        actions=[
                            make_inst("ModVarScene", ["chaser_state", "=", "2"]),
                            make_inst("SetOpacity", ["Enemy_Chaser", "=", "255"]),
                            make_inst("ChangeAnimation", ["Enemy_Chaser", "=", "1"]),
                            make_inst("ModVarScene", ["shake_timer", "=", "0.30"]),
                            make_inst("ModVarScene", ["warning_timer", "=", "2.5"]),
                            make_inst("TextObject::String", ["Txt_Warning_Banner", "=", "\"LARI! ENTITAS BAYANGAN MENGEJAR!\""])
                        ]
                    )
                ]
            ),
            # State 2: Relentless Chasing
            make_event(
                conditions=[make_inst("VarScene", ["chaser_state", "=", "2"])],
                actions=[],
                sub_events=[
                    # Chaser speed based on zone
                    make_event(
                        conditions=[make_inst("VarScene", ["current_zone", "<=", "2"])],
                        actions=[make_inst("ModVarScene", ["chaser_speed", "=", "124"])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["current_zone", ">=", "3"])],
                        actions=[make_inst("ModVarScene", ["chaser_speed", "=", "131"])]
                    ),
                    # Move toward player
                    make_event(
                        conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">", "Enemy_Chaser.CenterX()"])],
                        actions=[
                            make_inst("SetX", ["Enemy_Chaser", "+", "Variable(chaser_speed) * TimeDelta()"]),
                            make_inst("FlipX", ["Enemy_Chaser", "no"])
                        ]
                    ),
                    make_event(
                        conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<", "Enemy_Chaser.CenterX()"])],
                        actions=[
                            make_inst("SetX", ["Enemy_Chaser", "-", "Variable(chaser_speed) * TimeDelta()"]),
                            make_inst("FlipX", ["Enemy_Chaser", "yes"])
                        ]
                    ),
                    # Safe Barrier Repulsion at X=180
                    make_event(
                        conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Enemy_Chaser.CenterX()", "<=", "180"])],
                        actions=[
                            make_inst("ModVarScene", ["barrier_flash_timer", "=", "0.8"]),
                            make_inst("ModVarScene", ["shake_timer", "=", "0.35"]),
                            make_inst("ModVarScene", ["chaser_state", "=", "3"]),
                            make_inst("ModVarScene", ["chaser_cooldown", "=", "10.0"]),
                            make_inst("SetXY", ["Enemy_Chaser", "=", "-1000", "=", "264"]),
                            make_inst("Hide", ["Enemy_Chaser"]),
                            make_inst("TextObject::String", ["Txt_Combat_Feedback", "=", "\"BARRIER SUCI MENAHAN ENTITAS!\""]),
                            make_inst("SetXY", ["Txt_Combat_Feedback", "=", "180", "=", "240"]),
                            make_inst("Show", ["Txt_Combat_Feedback", ""]),
                            make_inst("ModVarScene", ["combat_feedback_timer", "=", "2.0"])
                        ]
                    ),
                    # Catch Player Attack
                    make_event(
                        conditions=[
                            make_inst("Distance", ["Enemy_Chaser", "Player", "24", ""]),
                            make_inst("VarScene", ["invuln_timer", "<=", "0"])
                        ],
                        actions=[
                            make_inst("ModVarScene", ["stagger_timer", "=", "0.70"]),
                            make_inst("ModVarScene", ["invuln_timer", "=", "1.60"]),
                            make_inst("ModVarScene", ["shake_timer", "=", "0.50"])
                        ],
                        sub_events=[
                            make_event(
                                conditions=[make_inst("VarScene", ["held_tier", ">", "0"])],
                                actions=[
                                    make_inst("Create", ["", "Ground_Stick", "Player.CenterX() - 16", "296 - 16", "\"\""]),
                                    make_inst("ModVarObjet", ["Ground_Stick", "tier", "=", "Variable(held_tier)"]),
                                    make_inst("ModVarObjet", ["Ground_Stick", "base_value", "=", "Variable(held_value)"]),
                                    make_inst("ModVarObjet", ["Ground_Stick", "chunk_id", "=", "floor(Player.CenterX() / 640)"]),
                                    make_inst("ChangeAnimation", ["Ground_Stick", "=", "Variable(held_tier) - 1"]),
                                    make_inst("SetZOrder", ["Ground_Stick", "=", "5"]),
                                    make_inst("ModVarScene", ["held_tier", "=", "0"]),
                                    make_inst("ModVarScene", ["held_value", "=", "0"])
                                ]
                            ),
                            make_event(
                                conditions=[],
                                actions=[
                                    make_inst("TextObject::String", ["Txt_Combat_Feedback", "=", "\"TERSERANG ENTITAS! STAGGER!\""]),
                                    make_inst("SetXY", ["Txt_Combat_Feedback", "=", "Player.CenterX() - 65", "=", "Player.Y() - 25"]),
                                    make_inst("Show", ["Txt_Combat_Feedback", ""]),
                                    make_inst("ModVarScene", ["combat_feedback_timer", "=", "2.0"]),
                                    make_inst("ModVarScene", ["chaser_state", "=", "3"]),
                                    make_inst("ModVarScene", ["chaser_cooldown", "=", "10.0"]),
                                    make_inst("SetXY", ["Enemy_Chaser", "=", "-1000", "=", "264"]),
                                    make_inst("Hide", ["Enemy_Chaser"])
                                ]
                            )
                        ]
                    )
                ]
            ),
            # State 3: Cooldown
            make_event(
                conditions=[make_inst("VarScene", ["chaser_state", "=", "3"])],
                actions=[
                    make_inst("Hide", ["Enemy_Chaser"]),
                    make_inst("ModVarScene", ["chaser_cooldown", "=", "max(0, Variable(chaser_cooldown) - TimeDelta())"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["chaser_cooldown", "<=", "0"])],
                        actions=[make_inst("ModVarScene", ["chaser_state", "=", "0"])]
                    )
                ]
            )
        ]
    )
    events.append(ev_chaser_ai)

    # 15. Safe Barrier Visual Glow
    ev_safe_barrier_visual = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            make_event(
                conditions=[make_inst("VarScene", ["barrier_flash_timer", ">", "0"])],
                actions=[make_inst("SetColor", ["Safe_Barrier", "\"100;255;255\""])]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["barrier_flash_timer", "<=", "0"])],
                actions=[make_inst("SetColor", ["Safe_Barrier", "\"255;255;255\""])]
            )
        ]
    )
    events.append(ev_safe_barrier_visual)

    # 16. Threat / Alert Level & Danger HUD System
    ev_alert_indicator = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Determine Alert Level
            make_event(
                conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<=", "180"])],
                actions=[make_inst("ModVarScene", ["alert_level", "=", "0"])]
            ),
            make_event(
                conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">", "180"])],
                actions=[],
                sub_events=[
                    make_event(
                        conditions=[
                            make_inst("BuiltinCommonInstructions::Or", [], False, [
                                make_inst("VarScene", ["chaser_state", "=", "2"]),
                                make_inst("VarScene", ["stagger_timer", ">", "0"])
                            ])
                        ],
                        actions=[make_inst("ModVarScene", ["alert_level", "=", "3"])]
                    ),
                    make_event(
                        conditions=[
                            make_inst("VarScene", ["chaser_state", "!=", "2"]),
                            make_inst("VarScene", ["stagger_timer", "<=", "0"]),
                            make_inst("VarScene", ["chaser_state", "=", "1"])
                        ],
                        actions=[make_inst("ModVarScene", ["alert_level", "=", "2"])]
                    ),
                    make_event(
                        conditions=[
                            make_inst("VarScene", ["chaser_state", "<=", "0"]),
                            make_inst("VarScene", ["stagger_timer", "<=", "0"]),
                            make_inst("BuiltinCommonInstructions::Or", [], False, [
                                make_inst("VarScene", ["thief_state", "=", "1"]),
                                make_inst("VarScene", ["thief_state", "=", "2"])
                            ])
                        ],
                        actions=[make_inst("ModVarScene", ["alert_level", "=", "1"])]
                    ),
                    make_event(
                        conditions=[
                            make_inst("VarScene", ["chaser_state", "<=", "0"]),
                            make_inst("VarScene", ["stagger_timer", "<=", "0"]),
                            make_inst("VarScene", ["thief_state", "!=", "1"]),
                            make_inst("VarScene", ["thief_state", "!=", "2"])
                        ],
                        actions=[make_inst("ModVarScene", ["alert_level", "=", "0"])]
                    )
                ]
            ),
            # UI Alert Indicator Frame Update
            make_event(
                conditions=[],
                actions=[make_inst("ChangeAnimation", ["UI_Alert_Indicator", "=", "Variable(alert_level)"])]
            ),
            # Warning Banner Visibility
            make_event(
                conditions=[make_inst("VarScene", ["warning_timer", ">", "0"])],
                actions=[make_inst("Show", ["Txt_Warning_Banner", ""])]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["warning_timer", "<=", "0"])],
                actions=[make_inst("Hide", ["Txt_Warning_Banner"])]
            ),
            # Alert Vignette Pulsing
            make_event(
                conditions=[make_inst("VarScene", ["alert_level", "=", "3"])],
                actions=[
                    make_inst("TiledSpriteObject::SetColor", ["Alert_Vignette", "\"255;0;0\""]),
                    make_inst("TiledSpriteObject::SetOpacity", ["Alert_Vignette", "=", "100 + 60 * cos(Variable(alert_pulse_time) * 12)"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["alert_level", "=", "2"])],
                actions=[
                    make_inst("TiledSpriteObject::SetColor", ["Alert_Vignette", "\"255;120;0\""]),
                    make_inst("TiledSpriteObject::SetOpacity", ["Alert_Vignette", "=", "50 + 30 * cos(Variable(alert_pulse_time) * 8)"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["alert_level", "<=", "1"])],
                actions=[
                    make_inst("TiledSpriteObject::SetOpacity", ["Alert_Vignette", "=", "0"])
                ]
            )
        ]
    )
    events.append(ev_alert_indicator)

    # Zone RNG generator helper for stick spawning
    def make_zone_rng_subevents(chunk_num):
        if chunk_num <= 2:
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
        elif chunk_num <= 6:
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

    zone_signs_init = [
        make_event(
            conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Zone_Sign.X()", "<", "1000"])],
            actions=[make_inst("ChangeAnimation", ["Zone_Sign", "=", "0"])]
        ),
        make_event(
            conditions=[
                make_inst("BuiltinCommonInstructions::CompareNumbers", ["Zone_Sign.X()", ">=", "1000"]),
                make_inst("BuiltinCommonInstructions::CompareNumbers", ["Zone_Sign.X()", "<", "3000"])
            ],
            actions=[make_inst("ChangeAnimation", ["Zone_Sign", "=", "1"])]
        ),
        make_event(
            conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Zone_Sign.X()", ">=", "3000"])],
            actions=[make_inst("ChangeAnimation", ["Zone_Sign", "=", "2"])]
        )
    ]

    # 17. Scene Start Initialization
    ev_scene_start = make_event(
        conditions=[make_inst("DepartScene", [""])],
        actions=[
            make_inst("ModVarScene", ["swap_cooldown", "=", "0"]),
            make_inst("ModVarScene", ["respawn_timer", "=", "0"]),
            make_inst("ModVarScene", ["banner_timer", "=", "0"]),
            make_inst("ModVarScene", ["prev_zone", "=", "0"]),
            make_inst("Hide", ["Txt_Zone_Banner"]),
            make_inst("Hide", ["Txt_Warning_Banner"]),
            make_inst("Hide", ["Txt_Combat_Feedback"]),
            make_inst("Hide", ["Enemy_Chaser"]),
            make_inst("TiledSpriteObject::SetOpacity", ["Zone_Tint_Overlay", "=", "0"]),
            make_inst("TiledSpriteObject::SetOpacity", ["Alert_Vignette", "=", "0"]),
            # Sprint 3 variable resets
            make_inst("ModVarScene", ["stagger_timer", "=", "0"]),
            make_inst("ModVarScene", ["invuln_timer", "=", "0"]),
            make_inst("ModVarScene", ["shake_timer", "=", "0"]),
            make_inst("ModVarScene", ["shake_x", "=", "0"]),
            make_inst("ModVarScene", ["shake_y", "=", "0"]),
            make_inst("ModVarScene", ["thief_state", "=", "0"]),
            make_inst("ModVarScene", ["thief_dir", "=", "1"]),
            make_inst("ModVarScene", ["thief_flee_timer", "=", "0"]),
            make_inst("ModVarScene", ["thief_stun_timer", "=", "0"]),
            make_inst("ModVarScene", ["stolen_tier", "=", "0"]),
            make_inst("ModVarScene", ["stolen_value", "=", "0"]),
            make_inst("ModVarScene", ["chaser_state", "=", "0"]),
            make_inst("ModVarScene", ["chaser_telegraph_timer", "=", "0"]),
            make_inst("ModVarScene", ["chaser_cooldown", "=", "0"]),
            make_inst("ModVarScene", ["warning_timer", "=", "0"]),
            make_inst("ModVarScene", ["alert_level", "=", "0"]),
            make_inst("ModVarScene", ["alert_pulse_time", "=", "0"]),
            make_inst("ModVarScene", ["barrier_flash_timer", "=", "0"]),
            make_inst("ModVarScene", ["is_slowed", "=", "0"]),
            make_inst("ModVarScene", ["emergency_drop_cooldown", "=", "0"]),
            make_inst("ModVarScene", ["combat_feedback_timer", "=", "0"])
        ],
        sub_events=initial_chunk_subevents + zone_signs_init
    )
    events.append(ev_scene_start)

    # 18. Respawn System
    ev_respawn = make_event(
        conditions=[],
        actions=[
            make_inst("ModVarScene", ["respawn_timer", "+", "TimeDelta()"])
        ],
        sub_events=[
            make_event(
                conditions=[make_inst("VarScene", ["respawn_timer", ">=", "30.0"])],
                actions=[
                    make_inst("ModVarScene", ["respawn_timer", "=", "0"])
                ],
                sub_events=[
                    make_event(
                        conditions=[
                            make_inst("BuiltinCommonInstructions::CompareNumbers", ["Variable(current_chunk)", ">=", "1"]),
                            make_inst("BuiltinCommonInstructions::CompareNumbers", ["Variable(current_chunk)", "<=", "12"])
                        ],
                        actions=[
                            make_inst("PickAll", ["Ground_Stick"]),
                            make_event() # dummy placeholder if needed, or actions below
                        ] if False else [
                            make_inst("ModVarScene", ["spawn_x", "=", "Variable(current_chunk) * 640 + RandomInRange(100, 540)"]),
                            make_inst("ModVarScene", ["rng_roll", "=", "RandomInRange(1, 100)"])
                        ],
                        sub_events=[
                            make_event(
                                conditions=[make_inst("VarScene", ["current_chunk", "<=", "2"])],
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
                            make_event(
                                conditions=[
                                    make_inst("VarScene", ["current_chunk", ">", "2"]),
                                    make_inst("VarScene", ["current_chunk", "<=", "6"])
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
                            make_event(
                                conditions=[make_inst("VarScene", ["current_chunk", ">", "6"])],
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
                            make_event(
                                conditions=[],
                                actions=[
                                    make_inst("Create", ["", "Ground_Stick", "Variable(spawn_x)", "296 - 16", "\"\""]),
                                    make_inst("ModVarObjet", ["Ground_Stick", "tier", "=", "Variable(spawn_tier)"]),
                                    make_inst("ModVarObjet", ["Ground_Stick", "base_value", "=", "Variable(spawn_val)"]),
                                    make_inst("ModVarObjet", ["Ground_Stick", "chunk_id", "=", "Variable(current_chunk)"]),
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

    # 19. Smart Comparison Prompt
    ev_smart_comparison_prompt = make_event(
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
                    make_inst("SetXY", ["Txt_Interact", "=", "Ground_Stick.CenterX() - 65", "=", "Ground_Stick.Y() - 24"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["held_tier", "=", "0"])],
                        actions=[
                            make_inst("TextObject::String", [
                                "Txt_Interact",
                                "=",
                                "\"[E] AMBIL TIER \" + ToString(Ground_Stick.Variable(tier)) + \" (+\" + ToString(Ground_Stick.Variable(base_value)) + \" POIN)\""
                            ])
                        ]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["held_tier", ">", "0"])],
                        actions=[
                            make_inst("ModVarScene", ["val_diff", "=", "Ground_Stick.Variable(base_value) - Variable(held_value)"])
                        ],
                        sub_events=[
                            make_event(
                                conditions=[make_inst("VarScene", ["val_diff", ">", "0"])],
                                actions=[
                                    make_inst("TextObject::String", [
                                        "Txt_Interact",
                                        "=",
                                        "\"[E] TUKAR KE T\" + ToString(Ground_Stick.Variable(tier)) + \" (UPGRADE +\" + ToString(Variable(val_diff)) + \" POIN!)\""
                                    ])
                                ]
                            ),
                            make_event(
                                conditions=[make_inst("VarScene", ["val_diff", "=", "0"])],
                                actions=[
                                    make_inst("TextObject::String", [
                                        "Txt_Interact",
                                        "=",
                                        "\"[E] TUKAR T\" + ToString(Ground_Stick.Variable(tier)) + \" (NILAI SAMA)\""
                                    ])
                                ]
                            ),
                            make_event(
                                conditions=[make_inst("VarScene", ["val_diff", "<", "0"])],
                                actions=[
                                    make_inst("TextObject::String", [
                                        "Txt_Interact",
                                        "=",
                                        "\"[E] TUKAR KE T\" + ToString(Ground_Stick.Variable(tier)) + \" (DOWNGRADE \" + ToString(Variable(val_diff)) + \" POIN)\""
                                    ])
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    events.append(ev_smart_comparison_prompt)

    # 20. Pickup & Swap System
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
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "0"])],
                actions=[
                    make_inst("ModVarScene", ["held_tier", "=", "Ground_Stick.Variable(tier)"]),
                    make_inst("ModVarScene", ["held_value", "=", "Ground_Stick.Variable(base_value)"]),
                    make_inst("Delete", ["Ground_Stick", ""]),
                    make_inst("ModVarScene", ["swap_cooldown", "=", "0.25"])
                ]
            ),
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

    # 21. Extraction & Scoring System
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

    # 22. HUD and Inventory Slots
    ev_hud_and_slots = make_event(
        conditions=[],
        actions=[
            make_inst("TextObject::String", [
                "Txt_HUD",
                "=",
                "\"SKOR: \" + ToString(Variable(total_score)) + \" | ZONA: \" + ToString(Variable(current_zone)) + \" (Chunk \" + ToString(Variable(current_chunk)) + \") | MAX EXP: \" + ToString(round(Variable(max_dist_x))) + \" px\""
            ])
        ],
        sub_events=[
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "0"])],
                actions=[
                    make_inst("ChangeAnimation", ["UI_Slot_Icon", "=", "0"]),
                    make_inst("TextObject::String", ["Txt_Slot_Label", "=", "\"SLOT: KOSONG (Tangan Bebas)\""])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "1"])],
                actions=[
                    make_inst("ChangeAnimation", ["UI_Slot_Icon", "=", "1"]),
                    make_inst("TextObject::String", ["Txt_Slot_Label", "=", "\"SLOT: T1 - Ranting Rapuh (10 Poin | 1.00x Lari) [Q] Lepas\""])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "2"])],
                actions=[
                    make_inst("ChangeAnimation", ["UI_Slot_Icon", "=", "2"]),
                    make_inst("TextObject::String", ["Txt_Slot_Label", "=", "\"SLOT: T2 - Kayu Keras (30 Poin | 0.95x Lari) [Q] Lepas\""])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "3"])],
                actions=[
                    make_inst("ChangeAnimation", ["UI_Slot_Icon", "=", "3"]),
                    make_inst("TextObject::String", ["Txt_Slot_Label", "=", "\"SLOT: T3 - Kayu Damar (85 Poin | 0.90x Lari) [Q] Lepas\""])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "4"])],
                actions=[
                    make_inst("ChangeAnimation", ["UI_Slot_Icon", "=", "4"]),
                    make_inst("TextObject::String", ["Txt_Slot_Label", "=", "\"SLOT: T4 - Akar Kristal (250 Poin | 0.85x Lari) [Q] Lepas\""])
                ]
            )
        ]
    )
    events.append(ev_hud_and_slots)

    # 23. Scene Reset (R Key)
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
            "zoomFactor": 1
        },
        "objectsFolderStructure": {
            "folderName": "__ROOT__"
        },
        "behaviorsSharedData": [],
        "layers": layers,
        "variables": scene_vars,
        "objects": all_scene_objects,
        "instances": initial_instances,
        "events": events
    }

    project["layouts"].append(layout)

    out_file = "StickScavenger.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(project, f, indent=2)
    print(f"Generated {out_file} successfully!")

if __name__ == "__main__":
    generate_sprint3()
