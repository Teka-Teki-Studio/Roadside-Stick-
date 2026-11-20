"""
Sprint 4 Patcher — patches StickScavenger.json IN-PLACE.
Adds: Title_Screen layout, Save/Load, Mini-Radar, Game Juice,
      Audio SFX, Pause Menu to existing Main_World.
Preserves ALL Sprint 1-3 content (objects, events, layers, resources).
"""
import json
import os
import uuid

def make_uuid():
    return str(uuid.uuid4())

def make_inst(type_val, params, inverted=False, sub_instructions=None):
    inst = {"type": {"value": type_val}, "parameters": params}
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

def patch_sprint4():
    with open("StickScavenger.json", "r", encoding="utf-8") as f:
        project = json.load(f)

    # ================================================================
    # A. ADD NEW RESOURCES (images + audio)
    # ================================================================
    existing_res = {r["file"] for r in project["resources"]["resources"]}

    # Gather new image resources
    for d in ["assets/sprint4", "assets/audio"]:
        for root, dirs, files in os.walk(d):
            for fn in sorted(files):
                fp = os.path.join(root, fn).replace("\\", "/")
                if fp not in existing_res:
                    kind = "audio" if fn.endswith(".wav") else "image"
                    project["resources"]["resources"].append({
                        "file": fp,
                        "kind": kind,
                        "metadata": "",
                        "name": fp,
                        "smoothed": False,
                        "userAdded": True
                    })

    # ================================================================
    # B. HELPER: Sprite frame dict
    # ================================================================
    def sprite_frame(image_path, cx=None, cy=None):
        return {
            "hasCustomCollisionMask": False,
            "customCollisionMask": [],
            "image": image_path,
            "points": [],
            "originPoint": {"name": "origine", "x": 0, "y": 0},
            "centerPoint": {"automatic": True, "name": "centre",
                            "x": cx if cx else 0, "y": cy if cy else 0}
        }

    def anim(name, looping, tbf, frames):
        return {
            "name": name,
            "useMultipleDirections": False,
            "directions": [{
                "looping": looping,
                "timeBetweenFrames": tbf,
                "sprites": frames
            }]
        }

    def sprite_obj(name, animations, variables=None, behaviors=None):
        return {
            "assetStoreId": "",
            "name": name,
            "type": "Sprite",
            "variables": variables or [],
            "behaviors": behaviors or [],
            "effects": [],
            "animations": animations
        }

    def tiled_obj(name, texture, w, h):
        return {
            "assetStoreId": "",
            "effects": [],
            "height": h,
            "name": name,
            "texture": texture,
            "type": "TiledSpriteObject::TiledSprite",
            "variables": [],
            "width": w
        }

    def text_obj(name, text, size, color, bold=True, outline=True, ol_color="0;0;0", ol_thick=2, align="left"):
        return {
            "name": name,
            "type": "TextObject::Text",
            "variables": [],
            "behaviors": [],
            "effects": [],
            "content": {
                "bold": bold,
                "characterSize": size,
                "color": color,
                "font": "",
                "isOutlineEnabled": outline,
                "isShadowEnabled": False,
                "italic": False,
                "lineHeight": 0,
                "outlineColor": ol_color,
                "outlineThickness": ol_thick,
                "shadowAngle": 90,
                "shadowBlurRadius": 2,
                "shadowColor": "0;0;0",
                "shadowDistance": 1,
                "shadowOpacity": 128,
                "text": text,
                "textAlignment": align,
                "underlined": False,
                "verticalTextAlignment": "top"
            }
        }

    def inst(name, x, y, w, h, layer="", zOrder=0, locked=False, customSize=False, keepRatio=True, extra=None):
        d = {
            "angle": 0, "customSize": customSize, "height": h, "keepRatio": keepRatio,
            "layer": layer, "locked": locked, "name": name, "persistentUuid": make_uuid(),
            "width": w, "x": x, "y": y, "zOrder": zOrder,
            "numberProperties": [], "stringProperties": [], "initialVariables": []
        }
        if customSize:
            d["depth"] = 1
        if extra:
            d.update(extra)
        return d

    # ================================================================
    # C. FIND Main_World layout
    # ================================================================
    main_world = None
    for layout in project["layouts"]:
        if layout["name"] == "Main_World":
            main_world = layout
            break
    assert main_world is not None, "Main_World layout not found!"

    # ================================================================
    # D. ADD NEW OBJECTS TO Main_World (Sprint 4)
    # ================================================================
    existing_obj_names = {o["name"] for o in main_world["objects"]}

    new_objects = []

    if "Dust_Particle" not in existing_obj_names:
        new_objects.append(sprite_obj("Dust_Particle", [
            anim("Puff", False, 0.12, [
                sprite_frame("assets/sprint4/particles/dust_1.png", 3, 3),
                sprite_frame("assets/sprint4/particles/dust_2.png", 3, 3)
            ])
        ]))

    if "Glint_Sparkle" not in existing_obj_names:
        new_objects.append(sprite_obj("Glint_Sparkle", [
            anim("Sparkle", True, 0.15, [
                sprite_frame("assets/sprint4/particles/glint_1.png", 4, 4),
                sprite_frame("assets/sprint4/particles/glint_2.png", 4, 4)
            ])
        ]))

    if "Radar_Frame" not in existing_obj_names:
        new_objects.append(sprite_obj("Radar_Frame", [
            anim("Frame", False, 1, [
                sprite_frame("assets/sprint4/ui/radar_frame.png", 50, 10)
            ])
        ]))

    if "Radar_Dot" not in existing_obj_names:
        new_objects.append(sprite_obj("Radar_Dot", [
            anim("Dot", False, 1, [
                sprite_frame("assets/sprint4/ui/radar_dot.png", 2, 2)
            ])
        ]))

    if "Pause_Overlay" not in existing_obj_names:
        new_objects.append(tiled_obj("Pause_Overlay",
            "assets/sprint4/ui/pause_overlay.png", 640, 360))

    if "Save_Icon" not in existing_obj_names:
        new_objects.append(sprite_obj("Save_Icon", [
            anim("Icon", False, 1, [
                sprite_frame("assets/sprint4/ui/save_icon.png", 8, 8)
            ])
        ]))

    if "Txt_Pause" not in existing_obj_names:
        new_objects.append(text_obj("Txt_Pause", "PAUSE", 24,
            "255;255;255", align="center", ol_thick=3))

    if "Txt_Pause_Sub" not in existing_obj_names:
        new_objects.append(text_obj("Txt_Pause_Sub",
            "[ESC] Lanjut  |  [R] Restart", 11, "200;200;200", align="center"))

    if "Txt_Save_Toast" not in existing_obj_names:
        new_objects.append(text_obj("Txt_Save_Toast",
            "REKOR TERSIMPAN!", 11, "100;255;120", align="left"))

    main_world["objects"].extend(new_objects)

    # ================================================================
    # E. ADD NEW INSTANCES TO Main_World
    # ================================================================
    new_instances = [
        inst("Radar_Frame", 530, 65, 100, 20, "UI", 24, True),
        inst("Radar_Dot", 530, 73, 4, 4, "UI", 25, False),
        inst("Pause_Overlay", 0, 0, 640, 360, "UI", 90, True, customSize=True),
        inst("Txt_Pause", 240, 140, 160, 30, "UI", 91, True),
        inst("Txt_Pause_Sub", 200, 175, 240, 20, "UI", 91, True),
        inst("Save_Icon", 540, 320, 16, 16, "UI", 26, False),
        inst("Txt_Save_Toast", 560, 322, 80, 14, "UI", 26, False),
    ]
    main_world["instances"].extend(new_instances)

    # ================================================================
    # F. ADD NEW SCENE VARIABLES TO Main_World
    # ================================================================
    existing_var_names = {v["name"] for v in main_world["variables"]}
    new_vars = [
        ("is_paused", 0),
        ("pause_cooldown", 0),
        ("hitstop_timer", 0),
        ("dust_spawn_timer", 0),
        ("step_sfx_timer", 0),
        ("glint_pulse_time", 0),
        ("save_toast_timer", 0),
        ("menu_pulse_time", 0),
        ("high_score", 0),
        ("radar_player_px", 0),
    ]
    for vn, vv in new_vars:
        if vn not in existing_var_names:
            main_world["variables"].append({"name": vn, "type": "number", "value": vv})

    # ================================================================
    # G. PATCH CAMERA EVENT — add shake offset (verify not already patched)
    # ================================================================
    # The camera is already integrated with shake_x/shake_y from Sprint 3.
    # No camera patching needed.

    # ================================================================
    # H. ADD NEW EVENTS TO Main_World (appended after existing 23 root events)
    # ================================================================

    # ----- EVENT: Pause System (ESC key) -----
    ev_pause_system = make_event(
        conditions=[],
        actions=[
            make_inst("ModVarScene", ["pause_cooldown", "=", "max(0, Variable(pause_cooldown) - TimeDelta())"])
        ],
        sub_events=[
            # Toggle Pause
            make_event(
                conditions=[
                    make_inst("KeyPressed", ["", "Escape"]),
                    make_inst("BuiltinCommonInstructions::Once", []),
                    make_inst("VarScene", ["pause_cooldown", "<=", "0"])
                ],
                actions=[],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["is_paused", "=", "0"])],
                        actions=[
                            make_inst("ModVarScene", ["is_paused", "=", "1"]),
                            make_inst("ModVarScene", ["pause_cooldown", "=", "0.3"]),
                            make_inst("PauseScene", ["\"Main_World\""]),
                            make_inst("Show", ["Pause_Overlay", ""]),
                            make_inst("Show", ["Txt_Pause", ""]),
                            make_inst("Show", ["Txt_Pause_Sub", ""]),
                            make_inst("PlaySound", ["assets/audio/sfx_pause.wav", "", "no", "70", "1", "1"])
                        ]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["is_paused", "=", "1"])],
                        actions=[
                            make_inst("ModVarScene", ["is_paused", "=", "0"]),
                            make_inst("ModVarScene", ["pause_cooldown", "=", "0.3"]),
                            make_inst("UnpauseScene", ["\"Main_World\""]),
                            make_inst("Hide", ["Pause_Overlay"]),
                            make_inst("Hide", ["Txt_Pause"]),
                            make_inst("Hide", ["Txt_Pause_Sub"]),
                            make_inst("PlaySound", ["assets/audio/sfx_pause.wav", "", "no", "70", "1", "1"])
                        ]
                    )
                ]
            ),
            # Hide pause UI when not paused
            make_event(
                conditions=[make_inst("VarScene", ["is_paused", "=", "0"])],
                actions=[
                    make_inst("Hide", ["Pause_Overlay"]),
                    make_inst("Hide", ["Txt_Pause"]),
                    make_inst("Hide", ["Txt_Pause_Sub"])
                ]
            )
        ]
    )

    # ----- EVENT: Save/Load High Score -----
    ev_save_load = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Load high score at scene start (use the existing DepartScene approach)
            # Read from storage on every frame if high_score is 0 (once-like)
            make_event(
                conditions=[make_inst("VarScene", ["high_score", "=", "0"])],
                actions=[
                    make_inst("ReadNumberFromJSONFile", ["\"StickScavengerSave\"", "\"high_score\"", "high_score", "\"\""])
                ]
            ),
            # Save toast visibility
            make_event(
                conditions=[make_inst("VarScene", ["save_toast_timer", ">", "0"])],
                actions=[
                    make_inst("ModVarScene", ["save_toast_timer", "=", "max(0, Variable(save_toast_timer) - TimeDelta())"]),
                    make_inst("Show", ["Save_Icon", ""]),
                    make_inst("Show", ["Txt_Save_Toast", ""])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["save_toast_timer", "<=", "0"])],
                actions=[
                    make_inst("Hide", ["Save_Icon"]),
                    make_inst("Hide", ["Txt_Save_Toast"])
                ]
            )
        ]
    )

    # ----- EVENT: Mini-Radar Position Update -----
    ev_radar = make_event(
        conditions=[],
        actions=[
            # Map player X (0–8000) to radar pixel X (530–630)
            make_inst("ModVarScene", ["radar_player_px", "=",
                "530 + clamp(Player.CenterX() / 8000, 0, 1) * 96"]),
            make_inst("SetX", ["Radar_Dot", "=", "Variable(radar_player_px)"])
        ]
    )

    # ----- EVENT: Foot Dust Particles -----
    ev_dust_particles = make_event(
        conditions=[],
        actions=[
            make_inst("ModVarScene", ["dust_spawn_timer", "=",
                "max(0, Variable(dust_spawn_timer) - TimeDelta())"])
        ],
        sub_events=[
            # Spawn dust when running on floor
            make_event(
                conditions=[
                    make_inst("PlatformBehavior::IsOnFloor", ["Player", "PlatformerObjectBehavior"]),
                    make_inst("PlatformBehavior::IsMoving", ["Player", "PlatformerObjectBehavior"]),
                    make_inst("VarScene", ["dust_spawn_timer", "<=", "0"]),
                    make_inst("VarScene", ["is_paused", "=", "0"])
                ],
                actions=[
                    make_inst("Create", ["", "Dust_Particle",
                        "Player.CenterX() + RandomInRange(-6, 6)",
                        "Player.Y() + 26", "\"\""]),
                    make_inst("SetZOrder", ["Dust_Particle", "=", "9"]),
                    make_inst("ModVarScene", ["dust_spawn_timer", "=", "0.18"])
                ]
            ),
            # Animate and kill dust particles after lifetime
            make_event(
                conditions=[],
                actions=[
                    make_inst("SetOpacity", ["Dust_Particle", "-",
                        "800 * TimeDelta()"]),
                    make_inst("SetY", ["Dust_Particle", "-", "15 * TimeDelta()"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers",
                            ["Dust_Particle.Opacity()", "<=", "10"])],
                        actions=[make_inst("Delete", ["Dust_Particle", ""])]
                    )
                ]
            )
        ]
    )

    # ----- EVENT: Glint on High-Tier Ground Sticks -----
    ev_glint = make_event(
        conditions=[],
        actions=[
            make_inst("ModVarScene", ["glint_pulse_time", "+", "TimeDelta()"])
        ],
        sub_events=[
            # Create glints near tier 3/4 sticks periodically
            make_event(
                conditions=[
                    make_inst("BuiltinCommonInstructions::CompareNumbers",
                        ["Variable(glint_pulse_time)", ">", "1.2"])
                ],
                actions=[
                    make_inst("ModVarScene", ["glint_pulse_time", "=", "0"])
                ],
                sub_events=[
                    make_event(
                        conditions=[
                            make_inst("BuiltinCommonInstructions::CompareNumbers",
                                ["Ground_Stick.Variable(tier)", ">=", "3"])
                        ],
                        actions=[
                            make_inst("Create", ["", "Glint_Sparkle",
                                "Ground_Stick.CenterX() + RandomInRange(-6, 6)",
                                "Ground_Stick.CenterY() + RandomInRange(-6, 2)", "\"\""]),
                            make_inst("SetZOrder", ["Glint_Sparkle", "=", "6"])
                        ]
                    )
                ]
            ),
            # Kill glints after their animation completes
            make_event(
                conditions=[
                    make_inst("AnimationEnded", ["Glint_Sparkle"])
                ],
                actions=[make_inst("Delete", ["Glint_Sparkle", ""])]
            )
        ]
    )

    # ----- EVENT: Audio SFX System -----
    ev_audio = make_event(
        conditions=[],
        actions=[
            make_inst("ModVarScene", ["step_sfx_timer", "=",
                "max(0, Variable(step_sfx_timer) - TimeDelta())"])
        ],
        sub_events=[
            # Footstep sound when running on floor
            make_event(
                conditions=[
                    make_inst("PlatformBehavior::IsOnFloor", ["Player", "PlatformerObjectBehavior"]),
                    make_inst("PlatformBehavior::IsMoving", ["Player", "PlatformerObjectBehavior"]),
                    make_inst("VarScene", ["step_sfx_timer", "<=", "0"]),
                    make_inst("VarScene", ["is_paused", "=", "0"])
                ],
                actions=[
                    make_inst("PlaySound", ["assets/audio/sfx_step.wav", "", "no", "40", "1", "1"]),
                    make_inst("ModVarScene", ["step_sfx_timer", "=", "0.24"])
                ]
            )
        ]
    )

    # ----- EVENT: Hitstop (brief freeze) on combat/rare swap -----
    ev_hitstop = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            make_event(
                conditions=[make_inst("VarScene", ["hitstop_timer", ">", "0"])],
                actions=[
                    make_inst("ModVarScene", ["hitstop_timer", "=",
                        "max(0, Variable(hitstop_timer) - TimeDelta())"]),
                    make_inst("ChangeTimeScale", ["0.05"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["hitstop_timer", "<=", "0"])],
                actions=[],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["is_paused", "=", "0"])],
                        actions=[make_inst("ChangeTimeScale", ["1"])]
                    )
                ]
            )
        ]
    )

    # Now add SFX triggers to existing events by patching
    # Instead of patching inline (risky), we add wrapper events that trigger sounds

    # ----- EVENT: SFX Triggers (pickup, extraction, steal, etc.) -----
    ev_sfx_triggers = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Pickup SFX on E key + near stick + swap_cooldown just triggered
            make_event(
                conditions=[
                    make_inst("KeyPressed", ["", "e"]),
                    make_inst("BuiltinCommonInstructions::Once", []),
                    make_inst("Distance", ["Player", "Ground_Stick", "28", ""])
                ],
                actions=[
                    make_inst("PlaySound", ["assets/audio/sfx_pickup.wav", "", "no", "70", "1", "1"])
                ],
                sub_events=[
                    # Hitstop on tier 3+ swap
                    make_event(
                        conditions=[
                            make_inst("BuiltinCommonInstructions::CompareNumbers",
                                ["Ground_Stick.Variable(tier)", ">=", "3"])
                        ],
                        actions=[
                            make_inst("ModVarScene", ["hitstop_timer", "=", "0.05"])
                        ]
                    )
                ]
            ),
            # Emergency Drop SFX
            make_event(
                conditions=[
                    make_inst("KeyPressed", ["", "q"]),
                    make_inst("BuiltinCommonInstructions::Once", []),
                    make_inst("VarScene", ["held_tier", ">", "0"])
                ],
                actions=[
                    make_inst("PlaySound", ["assets/audio/sfx_drop.wav", "", "no", "70", "1", "1"])
                ]
            ),
            # Extraction SFX + Save High Score
            make_event(
                conditions=[
                    make_inst("BuiltinCommonInstructions::CompareNumbers",
                        ["Player.CenterX()", "<=", "160"]),
                    make_inst("VarScene", ["held_tier", ">", "0"])
                ],
                actions=[
                    make_inst("PlaySound", ["assets/audio/sfx_extraction.wav", "", "no", "70", "1", "1"])
                ],
                sub_events=[
                    # Check & save high score
                    make_event(
                        conditions=[
                            make_inst("BuiltinCommonInstructions::CompareNumbers",
                                ["Variable(total_score) + Variable(earned)", ">", "Variable(high_score)"])
                        ],
                        actions=[
                            make_inst("ModVarScene", ["high_score", "=",
                                "Variable(total_score) + Variable(earned)"]),
                            make_inst("WriteNumberToJSONFile",
                                ["Variable(high_score)", "\"StickScavengerSave\"", "\"high_score\"", "\"\""]),
                            make_inst("TextObject::String", ["Txt_Save_Toast", "=",
                                "\"REKOR BARU: \" + ToString(Variable(high_score))"]),
                            make_inst("ModVarScene", ["save_toast_timer", "=", "2.4"])
                        ]
                    )
                ]
            ),
            # Combat Hit SFX (stagger triggered)
            make_event(
                conditions=[
                    make_inst("VarScene", ["stagger_timer", ">", "0.65"]),
                    make_inst("VarScene", ["stagger_timer", "<=", "0.70"])
                ],
                actions=[
                    make_inst("PlaySound", ["assets/audio/sfx_hit.wav", "", "no", "70", "1", "1"]),
                    make_inst("ModVarScene", ["hitstop_timer", "=", "0.07"])
                ]
            ),
            # Alert SFX (chaser telegraph just started)
            make_event(
                conditions=[
                    make_inst("VarScene", ["chaser_state", "=", "1"]),
                    make_inst("VarScene", ["chaser_telegraph_timer", ">", "1.1"])
                ],
                actions=[
                    make_inst("PlaySound", ["assets/audio/sfx_alert.wav", "", "no", "60", "1", "1"])
                ]
            ),
            # Steal SFX
            make_event(
                conditions=[
                    make_inst("VarScene", ["thief_state", "=", "2"]),
                    make_inst("VarScene", ["thief_flee_timer", ">", "5.9"])
                ],
                actions=[
                    make_inst("PlaySound", ["assets/audio/sfx_steal.wav", "", "no", "70", "1", "1"])
                ]
            ),
            # Recapture SFX
            make_event(
                conditions=[
                    make_inst("VarScene", ["thief_state", "=", "3"]),
                    make_inst("VarScene", ["thief_stun_timer", ">", "7.9"])
                ],
                actions=[
                    make_inst("PlaySound", ["assets/audio/sfx_recapture.wav", "", "no", "70", "1", "1"])
                ]
            )
        ]
    )

    # Append all new events to Main_World
    main_world["events"].extend([
        ev_pause_system,
        ev_save_load,
        ev_radar,
        ev_dust_particles,
        ev_glint,
        ev_audio,
        ev_hitstop,
        ev_sfx_triggers,
    ])

    # Also patch scene_start (first DepartScene event) to init new vars
    for ev in main_world["events"]:
        if ev.get("conditions"):
            for cond in ev["conditions"]:
                if cond.get("type", {}).get("value") == "DepartScene":
                    # This is the scene start event — add initialization actions
                    ev["actions"].extend([
                        make_inst("ModVarScene", ["is_paused", "=", "0"]),
                        make_inst("ModVarScene", ["pause_cooldown", "=", "0"]),
                        make_inst("ModVarScene", ["hitstop_timer", "=", "0"]),
                        make_inst("ModVarScene", ["dust_spawn_timer", "=", "0"]),
                        make_inst("ModVarScene", ["step_sfx_timer", "=", "0"]),
                        make_inst("ModVarScene", ["glint_pulse_time", "=", "0"]),
                        make_inst("ModVarScene", ["save_toast_timer", "=", "0"]),
                        make_inst("ModVarScene", ["menu_pulse_time", "=", "0"]),
                        make_inst("ModVarScene", ["radar_player_px", "=", "530"]),
                        make_inst("Hide", ["Pause_Overlay"]),
                        make_inst("Hide", ["Txt_Pause"]),
                        make_inst("Hide", ["Txt_Pause_Sub"]),
                        make_inst("Hide", ["Save_Icon"]),
                        make_inst("Hide", ["Txt_Save_Toast"]),
                        make_inst("ChangeTimeScale", ["1"]),
                    ])
                    break

    # ================================================================
    # I. CREATE Title_Screen LAYOUT
    # ================================================================
    title_objects = [
        tiled_obj("Title_Bg", "assets/sprint4/title/title_bg.png", 640, 360),
        sprite_obj("Title_Logo", [
            anim("Logo", False, 1, [
                sprite_frame("assets/sprint4/title/title_logo.png", 160, 30)
            ])
        ]),
        sprite_obj("Menu_Cursor", [
            anim("Arrow", False, 1, [
                sprite_frame("assets/sprint4/title/menu_cursor.png", 6, 6)
            ])
        ]),
        text_obj("Txt_Title_Start", "MULAI PETUALANGAN", 13,
            "255;240;180", align="center", ol_thick=2),
        text_obj("Txt_Title_High", "REKOR TERTINGGI: 0", 10,
            "180;200;255", align="center"),
        text_obj("Txt_Title_Hint", "[ENTER / SPACE] untuk Mulai", 9,
            "150;150;170", align="center"),
        text_obj("Txt_Title_Credits", "Stick Scavenger v0.4 — Sprint 4", 8,
            "80;80;100", align="center"),
    ]

    title_instances = [
        inst("Title_Bg", 0, 0, 640, 360, "", 0, True, customSize=True),
        inst("Title_Logo", 160, 80, 320, 60, "", 5),
        inst("Menu_Cursor", 180, 183, 12, 12, "", 10),
        inst("Txt_Title_Start", 200, 178, 240, 20, "", 8),
        inst("Txt_Title_High", 220, 220, 200, 16, "", 8),
        inst("Txt_Title_Hint", 210, 260, 220, 14, "", 8),
        inst("Txt_Title_Credits", 220, 335, 200, 12, "", 3),
    ]

    title_vars = [
        {"name": "menu_pulse_time", "type": "number", "value": 0},
        {"name": "menu_scroll_x", "type": "number", "value": 0},
        {"name": "transition_timer", "type": "number", "value": 0},
        {"name": "high_score", "type": "number", "value": 0},
    ]

    title_events = []

    # Title Frame Update
    title_events.append(make_event(
        conditions=[],
        actions=[
            make_inst("ModVarScene", ["menu_pulse_time", "+", "TimeDelta()"]),
            make_inst("ModVarScene", ["menu_scroll_x", "+", "8 * TimeDelta()"]),
        ],
        sub_events=[
            # Pulsing text opacity
            make_event(
                conditions=[],
                actions=[
                    make_inst("SetOpacity", ["Txt_Title_Start", "=",
                        "180 + 75 * cos(Variable(menu_pulse_time) * 4)"]),
                    make_inst("SetOpacity", ["Txt_Title_Hint", "=",
                        "120 + 100 * cos(Variable(menu_pulse_time) * 3)"]),
                    # Cursor bob
                    make_inst("SetY", ["Menu_Cursor", "=",
                        "183 + 2 * cos(Variable(menu_pulse_time) * 5)"])
                ]
            )
        ]
    ))

    # Load high score
    title_events.append(make_event(
        conditions=[make_inst("DepartScene", [""])],
        actions=[
            make_inst("ReadNumberFromJSONFile",
                ["\"StickScavengerSave\"", "\"high_score\"", "high_score", "\"\""]),
            make_inst("ModVarScene", ["transition_timer", "=", "0"])
        ]
    ))

    # Display high score
    title_events.append(make_event(
        conditions=[],
        actions=[
            make_inst("TextObject::String", ["Txt_Title_High", "=",
                "\"REKOR TERTINGGI: \" + ToString(Variable(high_score))"])
        ]
    ))

    # Start Game (Enter / Space)
    title_events.append(make_event(
        conditions=[
            make_inst("VarScene", ["transition_timer", "<=", "0"]),
            make_inst("BuiltinCommonInstructions::Or", [], False, [
                make_inst("KeyPressed", ["", "Return"]),
                make_inst("KeyPressed", ["", "Space"])
            ])
        ],
        actions=[
            make_inst("ModVarScene", ["transition_timer", "=", "0.5"]),
            make_inst("PlaySound", ["assets/audio/sfx_menu_select.wav", "", "no", "70", "1", "1"])
        ]
    ))

    # Transition countdown & scene change
    title_events.append(make_event(
        conditions=[make_inst("VarScene", ["transition_timer", ">", "0"])],
        actions=[
            make_inst("ModVarScene", ["transition_timer", "=",
                "max(0, Variable(transition_timer) - TimeDelta())"])
        ],
        sub_events=[
            make_event(
                conditions=[make_inst("VarScene", ["transition_timer", "<=", "0.01"])],
                actions=[
                    make_inst("Scene", ["", "\"Main_World\"", "no"])
                ]
            )
        ]
    ))

    title_layers = [
        {
            "ambientLightColorB": 0, "ambientLightColorG": 0, "ambientLightColorR": 0,
            "camera3DFairDistance": 10000, "camera3DFieldOfView": 45, "camera3DNearDistance": 1,
            "cameraType": "", "effects": [], "followBaseLayerCamera": False, "isLightingLayer": False,
            "isLocked": False, "name": "", "renderingType": "", "visibility": True
        }
    ]

    title_layout = {
        "b": 10,
        "disableInputWhenNotFocused": False,
        "mangledName": "Title_95Screen",
        "name": "Title_Screen",
        "r": 10,
        "renderer3DWorldScale": 100,
        "standardSortMethod": True,
        "stopSoundsOnStartup": True,
        "title": "Title Screen",
        "v": 15,
        "uiSettings": {
            "grid": False, "gridType": "isometric",
            "gridWidth": 32, "gridHeight": 32, "gridDepth": 32,
            "gridColor": 10401023, "gridAlpha": 0.8,
            "snap": False, "zoomFactor": 1
        },
        "objectsFolderStructure": {"folderName": "__ROOT__"},
        "behaviorsSharedData": [],
        "layers": title_layers,
        "variables": title_vars,
        "objects": title_objects,
        "instances": title_instances,
        "events": title_events
    }

    # Check if Title_Screen already exists
    title_exists = any(l["name"] == "Title_Screen" for l in project["layouts"])
    if not title_exists:
        project["layouts"].insert(0, title_layout)

    # Set firstLayout to Title_Screen
    project["firstLayout"] = "Title_Screen"

    # Update version
    project["properties"]["version"] = "0.4.0"
    project["properties"]["description"] = (
        "Stick Scavenger - Sprint 4 Title Screen, Save/Load, Mini-Radar, "
        "Game Juice, Chiptune SFX, Pause Menu"
    )

    # ================================================================
    # J. SAVE PATCHED PROJECT
    # ================================================================
    with open("StickScavenger.json", "w", encoding="utf-8") as f:
        json.dump(project, f, indent=2)

    print("Sprint 4 patch applied successfully!")

if __name__ == "__main__":
    patch_sprint4()
