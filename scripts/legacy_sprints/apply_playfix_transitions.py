import json
import uuid
import os

PROJECT_PATH = "StickScavenger.json"

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

def apply_playfix_and_transitions():
    print("=" * 70)
    print("APPLYING PLAYFIX & SEAMLESS SCENE TRANSITION SYSTEM")
    print("=" * 70)

    with open(PROJECT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Register assets/sprint4/ui/fade_black.png in resources
    fade_res_file = "assets/sprint4/ui/fade_black.png"
    resources_list = data["resources"]["resources"]
    if not any(r.get("file") == fade_res_file for r in resources_list):
        resources_list.append({
            "alwaysLoaded": False,
            "file": fade_res_file,
            "kind": "image",
            "metadata": "",
            "name": fade_res_file,
            "smoothed": False,
            "userAdded": False
        })
        print("Registered fade_black.png in resources.")

    # Definition of Transition_Fade sprite object
    fade_obj_def = {
        "assetStoreId": "",
        "name": "Transition_Fade",
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
                                "image": fade_res_file,
                                "points": [],
                                "originPoint": {
                                    "name": "origine",
                                    "x": 0,
                                    "y": 0
                                },
                                "centerPoint": {
                                    "automatic": True,
                                    "name": "centre",
                                    "x": 16,
                                    "y": 16
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # Definition of UI layer (for Title_Screen)
    ui_layer_def = {
        "ambientLightColorB": 0,
        "ambientLightColorG": 0,
        "ambientLightColorR": 0,
        "camera3DFairDistance": 10000,
        "camera3DFieldOfView": 45,
        "camera3DNearDistance": 1,
        "cameraType": "",
        "effects": [],
        "followBaseLayerCamera": False,
        "isLightingLayer": False,
        "isLocked": False,
        "name": "UI",
        "renderingType": "",
        "visibility": True
    }

    title_screen = next(l for l in data["layouts"] if l["name"] == "Title_Screen")
    main_world = next(l for l in data["layouts"] if l["name"] == "Main_World")

    # =========================================================================
    # STEP 1: Setup Title_Screen Layers, Objects, Instances & Variables
    # =========================================================================
    # Ensure "UI" layer exists in Title_Screen
    if not any(ly.get("name") == "UI" for ly in title_screen["layers"]):
        title_screen["layers"].append(dict(ui_layer_def))
        print("Added 'UI' layer to Title_Screen.")

    # Add Transition_Fade object
    if not any(o.get("name") == "Transition_Fade" for o in title_screen["objects"]):
        title_screen["objects"].append(dict(fade_obj_def))
        print("Added 'Transition_Fade' object to Title_Screen.")

    # Add Transition_Fade instance
    title_screen["instances"] = [i for i in title_screen["instances"] if i.get("name") != "Transition_Fade"]
    title_screen["instances"].append({
        "angle": 0,
        "customSize": True,
        "height": 360,
        "keepRatio": False,
        "layer": "UI",
        "locked": False,
        "name": "Transition_Fade",
        "persistentUuid": str(uuid.uuid4()),
        "width": 640,
        "x": 0,
        "y": 0,
        "zOrder": 999,
        "numberProperties": [],
        "stringProperties": [],
        "initialVariables": []
    })
    print("Placed 'Transition_Fade' instance in Title_Screen (layer: UI, zOrder: 999).")

    # Add fade variables in Title_Screen
    ts_vars = {v["name"]: v for v in title_screen["variables"]}
    if "fade_state" not in ts_vars:
        title_screen["variables"].append({"name": "fade_state", "type": "number", "value": 1})
    else:
        ts_vars["fade_state"]["value"] = 1
    if "fade_alpha" not in ts_vars:
        title_screen["variables"].append({"name": "fade_alpha", "type": "number", "value": 255})
    else:
        ts_vars["fade_alpha"]["value"] = 255

    # =========================================================================
    # STEP 2: Setup Main_World Objects, Instances & Variables
    # =========================================================================
    # Add Transition_Fade object in Main_World
    if not any(o.get("name") == "Transition_Fade" for o in main_world["objects"]):
        main_world["objects"].append(dict(fade_obj_def))
        print("Added 'Transition_Fade' object to Main_World.")

    # Add Transition_Fade instance in Main_World
    main_world["instances"] = [i for i in main_world["instances"] if i.get("name") != "Transition_Fade"]
    main_world["instances"].append({
        "angle": 0,
        "customSize": True,
        "height": 360,
        "keepRatio": False,
        "layer": "UI",
        "locked": False,
        "name": "Transition_Fade",
        "persistentUuid": str(uuid.uuid4()),
        "width": 640,
        "x": 0,
        "y": 0,
        "zOrder": 999,
        "numberProperties": [],
        "stringProperties": [],
        "initialVariables": []
    })
    print("Placed 'Transition_Fade' instance in Main_World (layer: UI, zOrder: 999).")

    # Add fade variables in Main_World
    mw_vars = {v["name"]: v for v in main_world["variables"]}
    if "fade_state" not in mw_vars:
        main_world["variables"].append({"name": "fade_state", "type": "number", "value": 1})
    else:
        mw_vars["fade_state"]["value"] = 1
    if "fade_alpha" not in mw_vars:
        main_world["variables"].append({"name": "fade_alpha", "type": "number", "value": 255})
    else:
        mw_vars["fade_alpha"]["value"] = 255

    # =========================================================================
    # STEP 3: Build Robust Event Sheets with Fade System
    # =========================================================================

    # --- Title_Screen Events ---
    title_screen["events"] = [
        # Event 0: Ambient Title Menu Pulses & Background Scroll
        make_event(
            conditions=[],
            actions=[
                make_inst("ModVarScene", ["menu_pulse_time", "+", "TimeDelta()"]),
                make_inst("ModVarScene", ["menu_scroll_x", "+", "12 * TimeDelta()"])
            ],
            sub_events=[
                make_event(
                    actions=[
                        make_inst("TextObject::Opacity", ["Txt_Title_Start", "=", "180 + 75 * cos(Variable(menu_pulse_time) * 4)"]),
                        make_inst("TextObject::Opacity", ["Txt_Title_Hint", "=", "120 + 80 * cos(Variable(menu_pulse_time) * 3)"]),
                        make_inst("SetY", ["Menu_Cursor", "=", "183 + 2 * cos(Variable(menu_pulse_time) * 5)"])
                    ]
                )
            ]
        ),
        # Event 1: At the beginning of the scene (DepartScene)
        make_event(
            conditions=[make_inst("DepartScene", [""])],
            actions=[
                make_inst("ChangeTimeScale", ["", "1"]),
                make_inst("ModVarScene", ["fade_state", "=", "1"]),
                make_inst("ModVarScene", ["fade_alpha", "=", "255"]),
                make_inst("Show", ["Transition_Fade", ""]),
                make_inst("Opacity", ["Transition_Fade", "=", "255"]),
                make_inst("TextObject::String", ["Txt_Title_Start", "=", "\"Mulai [Klik / Space]\""]),
                make_inst("TextObject::String", ["Txt_Title_Hint", "=", "\"[A]/[D] Gerak  *  [Space] Lompat  *  [E] Ambil  *  [Q] Lepas\""]),
                make_inst("TextObject::String", ["Txt_Title_Credits", "=", "\"\""])
            ],
            sub_events=[
                make_event(
                    conditions=[
                        make_inst("GroupExists", ['"StickScavengerSave"', '"high_score"'])
                    ],
                    actions=[
                        make_inst("LireFichierExp", ['"StickScavengerSave"', '"high_score"', "", "high_score"])
                    ]
                )
            ]
        ),
        # Event 2: Update High Score Display
        make_event(
            conditions=[],
            actions=[
                make_inst("TextObject::String", ["Txt_Title_High", "=", "\"Rekor: \" + ToString(Variable(high_score))"])
            ]
        ),
        # Event 3: Input Trigger (Mouse Click, Space, Enter) -> Fade-Out to Main_World
        make_event(
            conditions=[
                make_inst("VarScene", ["fade_state", "<=", "1"]),
                make_inst("BuiltinCommonInstructions::Once", []),
                make_inst("BuiltinCommonInstructions::Or", [], sub_instructions=[
                    make_inst("SourisBouton", ["", "Left"]),
                    make_inst("KeyPressed", ["", "Space"]),
                    make_inst("KeyPressed", ["", "Return"])
                ])
            ],
            actions=[
                make_inst("PlaySound", ["", "assets/audio/sfx_menu_select.wav", "no", "70", "1"]),
                make_inst("ModVarScene", ["fade_state", "=", "2"])
            ]
        ),
        # Event 4: Transition State Machine
        make_event(
            conditions=[],
            actions=[],
            sub_events=[
                # Sub 0: fade_state == 1 (Fade-In)
                make_event(
                    conditions=[make_inst("VarScene", ["fade_state", "=", "1"])],
                    actions=[
                        make_inst("Show", ["Transition_Fade", ""]),
                        make_inst("ModVarScene", ["fade_alpha", "=", "max(0, Variable(fade_alpha) - 730 * max(0.016, TimeDelta()))"]),
                        make_inst("Opacity", ["Transition_Fade", "=", "Variable(fade_alpha)"])
                    ],
                    sub_events=[
                        make_event(
                            conditions=[make_inst("VarScene", ["fade_alpha", "<=", "0"])],
                            actions=[
                                make_inst("ModVarScene", ["fade_state", "=", "0"]),
                                make_inst("Hide", ["Transition_Fade"])
                            ]
                        )
                    ]
                ),
                # Sub 1: fade_state == 2 (Fade-Out -> Main_World)
                make_event(
                    conditions=[make_inst("VarScene", ["fade_state", "=", "2"])],
                    actions=[
                        make_inst("Show", ["Transition_Fade", ""]),
                        make_inst("ModVarScene", ["fade_alpha", "=", "min(255, Variable(fade_alpha) + 850 * max(0.016, TimeDelta()))"]),
                        make_inst("Opacity", ["Transition_Fade", "=", "Variable(fade_alpha)"])
                    ],
                    sub_events=[
                        make_event(
                            conditions=[
                                make_inst("VarScene", ["fade_alpha", ">=", "255"]),
                                make_inst("BuiltinCommonInstructions::Once", [])
                            ],
                            actions=[
                                make_inst("Scene", ["", "\"Main_World\"", "no"])
                            ]
                        )
                    ]
                )
            ]
        )
    ]
    print("Rebuilt Title_Screen event sheet with anti-deadlock fade transitions.")

    # --- Main_World Events ---
    # First, let's create the dedicated DepartScene event at the top of Main_World
    mw_depart_event = make_event(
        conditions=[make_inst("DepartScene", [""])],
        actions=[
            make_inst("ChangeTimeScale", ["", "1"]),
            make_inst("ModVarScene", ["fade_state", "=", "1"]),
            make_inst("ModVarScene", ["fade_alpha", "=", "255"]),
            make_inst("Show", ["Transition_Fade", ""]),
            make_inst("Opacity", ["Transition_Fade", "=", "255"]),
            make_inst("ChangeAnimation", ["Ground_Stick", "=", "Ground_Stick.Variable(tier) - 1"]),
            make_inst("SetZOrder", ["Ground_Stick", "=", "15"]),
            make_inst("Opacity", ["Ground_Stick", "=", "255"]),
            make_inst("Show", ["Ground_Stick", ""]),
            make_inst("Hide", ["Txt_Warning_Banner"])
        ],
        sub_events=[
            make_event(
                conditions=[
                    make_inst("GroupExists", ['"StickScavengerSave"', '"high_score"'])
                ],
                actions=[
                    make_inst("LireFichierExp", ['"StickScavengerSave"', '"high_score"', "", "high_score"])
                ]
            )
        ]
    )

    # Transition State Machine event for Main_World
    mw_fade_event = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Sub 0: fade_state == 1 (Fade-In)
            make_event(
                conditions=[make_inst("VarScene", ["fade_state", "=", "1"])],
                actions=[
                    make_inst("Show", ["Transition_Fade", ""]),
                    make_inst("ModVarScene", ["fade_alpha", "=", "max(0, Variable(fade_alpha) - 730 * max(0.016, TimeDelta()))"]),
                    make_inst("Opacity", ["Transition_Fade", "=", "Variable(fade_alpha)"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["fade_alpha", "<=", "0"])],
                        actions=[
                            make_inst("ModVarScene", ["fade_state", "=", "0"]),
                            make_inst("Hide", ["Transition_Fade"])
                        ]
                    )
                ]
            ),
            # Sub 1: fade_state == 2 (Fade-Out -> Restart Main_World)
            make_event(
                conditions=[make_inst("VarScene", ["fade_state", "=", "2"])],
                actions=[
                    make_inst("Show", ["Transition_Fade", ""]),
                    make_inst("ModVarScene", ["fade_alpha", "=", "min(255, Variable(fade_alpha) + 850 * max(0.016, TimeDelta()))"]),
                    make_inst("Opacity", ["Transition_Fade", "=", "Variable(fade_alpha)"])
                ],
                sub_events=[
                    make_event(
                        conditions=[
                            make_inst("VarScene", ["fade_alpha", ">=", "255"]),
                            make_inst("BuiltinCommonInstructions::Once", [])
                        ],
                        actions=[
                            make_inst("Scene", ["", "\"Main_World\"", "no"])
                        ]
                    )
                ]
            ),
            # Sub 2: fade_state == 3 (Fade-Out -> Return to Title_Screen)
            make_event(
                conditions=[make_inst("VarScene", ["fade_state", "=", "3"])],
                actions=[
                    make_inst("Show", ["Transition_Fade", ""]),
                    make_inst("ModVarScene", ["fade_alpha", "=", "min(255, Variable(fade_alpha) + 850 * max(0.016, TimeDelta()))"]),
                    make_inst("Opacity", ["Transition_Fade", "=", "Variable(fade_alpha)"])
                ],
                sub_events=[
                    make_event(
                        conditions=[
                            make_inst("VarScene", ["fade_alpha", ">=", "255"]),
                            make_inst("BuiltinCommonInstructions::Once", [])
                        ],
                        actions=[
                            make_inst("Scene", ["", "\"Title_Screen\"", "no"])
                        ]
                    )
                ]
            )
        ]
    )

    # Clean Pause System Event for Main_World (Event 16)
    mw_pause_event = make_event(
        conditions=[
            make_inst("VarScene", ["fade_state", "=", "0"]),
            make_inst("KeyPressed", ["", "Escape"]),
            make_inst("BuiltinCommonInstructions::Once", [])
        ],
        actions=[
            make_inst("ModVarScene", ["is_paused", "=", "1 - Variable(is_paused)"]),
            make_inst("PlaySound", ["", "assets/audio/sfx_pause.wav", "no", "70", "1"])
        ],
        sub_events=[
            make_event(
                conditions=[make_inst("VarScene", ["is_paused", "=", "1"])],
                actions=[
                    make_inst("Show", ["Pause_Overlay", ""]),
                    make_inst("Show", ["Txt_Pause", ""]),
                    make_inst("Show", ["Txt_Pause_Sub", ""]),
                    make_inst("TextObject::String", ["Txt_Pause_Sub", "=", "\"[Escape] Lanjut  *  [R] Ulang  *  [M] Menu\""]),
                    make_inst("ChangeTimeScale", ["", "0"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["is_paused", "=", "0"])],
                actions=[
                    make_inst("Hide", ["Pause_Overlay"]),
                    make_inst("Hide", ["Txt_Pause"]),
                    make_inst("Hide", ["Txt_Pause_Sub"]),
                    make_inst("ChangeTimeScale", ["", "1"])
                ]
            )
        ]
    )

    # Restart [R] Event for Main_World
    mw_restart_event = make_event(
        conditions=[
            make_inst("VarScene", ["fade_state", "=", "0"]),
            make_inst("KeyPressed", ["", "r"]),
            make_inst("BuiltinCommonInstructions::Once", [])
        ],
        actions=[
            make_inst("ModVarScene", ["is_paused", "=", "0"]),
            make_inst("ChangeTimeScale", ["", "1"]),
            make_inst("ModVarScene", ["fade_state", "=", "2"])
        ]
    )

    # Return to Menu [M] Event for Main_World (during pause)
    mw_menu_event = make_event(
        conditions=[
            make_inst("VarScene", ["fade_state", "=", "0"]),
            make_inst("VarScene", ["is_paused", "=", "1"]),
            make_inst("KeyPressed", ["", "m"]),
            make_inst("BuiltinCommonInstructions::Once", [])
        ],
        actions=[
            make_inst("ModVarScene", ["is_paused", "=", "0"]),
            make_inst("ChangeTimeScale", ["", "1"]),
            make_inst("ModVarScene", ["fade_state", "=", "3"])
        ]
    )

    # Reassemble Main_World events:
    # 1. Prepend mw_depart_event at the beginning
    # 2. In existing events, update Event 16 (pause), Event 22 (restart), remove Event 23 (duplicate pause)
    # 3. Append mw_menu_event and mw_fade_event
    updated_mw_events = [mw_depart_event]

    for idx, ev in enumerate(main_world["events"]):
        # Skip duplicate pause event (idx 23)
        if idx == 23 and any(c.get("parameters", ["", ""])[1] == "Escape" for c in ev.get("conditions", [])):
            print(f"Skipping duplicate pause event at index {idx}.")
            continue
        # Replace Event 16 with clean locked pause event
        if idx == 16 and any(c.get("parameters", ["", ""])[1] == "Escape" for c in ev.get("conditions", [])):
            updated_mw_events.append(mw_pause_event)
            print("Replaced Event 16 with locked anti-deadlock pause system.")
            continue
        # Replace Event 22 with restart event that triggers fade_state = 2
        if idx == 22 and any(c.get("parameters", ["", ""])[1] == "r" for c in ev.get("conditions", [])):
            updated_mw_events.append(mw_restart_event)
            print("Replaced Event 22 with fade restart event.")
            continue

        updated_mw_events.append(ev)

    updated_mw_events.append(mw_menu_event)
    updated_mw_events.append(mw_fade_event)

    main_world["events"] = updated_mw_events
    print(f"Main_World events reassembled (Total: {len(main_world['events'])} top-level events).")

    with open(PROJECT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("SUCCESS: StickScavenger.json updated with complete fade transition system.")

if __name__ == "__main__":
    apply_playfix_and_transitions()
