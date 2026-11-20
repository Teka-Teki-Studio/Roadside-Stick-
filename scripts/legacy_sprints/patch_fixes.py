import json
import uuid
import os

PROJECT_PATH = "StickScavenger.json"
BALANCE_PATH = "data/game_balance.json"

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

def update_game_balance():
    with open(BALANCE_PATH, "r", encoding="utf-8") as f:
        bal = json.load(f)

    # 1. Player combat & movement
    bal["player_combat"]["base_speed"] = 230
    bal["player_combat"]["tier_speeds"] = {
        "0": 230,
        "1": 230,
        "2": 220,
        "3": 208,
        "4": 195
    }
    bal["player_combat"]["acceleration"] = 1800
    bal["player_combat"]["deceleration"] = 1800
    bal["player_combat"]["jump_speed"] = 440
    bal["player_combat"]["gravity"] = 1150

    # 2. Hazards
    bal["hazards"]["bramble_slow_multiplier"] = 0.65

    # 3. Clean stick names
    bal["sticks"]["1"]["name"] = "Ranting"
    bal["sticks"]["2"]["name"] = "Kayu Oak"
    bal["sticks"]["3"]["name"] = "Kayu Damar"
    bal["sticks"]["4"]["name"] = "Kayu Tua"

    # 4. Clean zone names
    bal["zones"]["1"]["name"] = "Tepi Hutan"
    bal["zones"]["2"]["name"] = "Hutan Rimba"
    bal["zones"]["3"]["name"] = "Hutan Gelap"

    # 5. Enemies (chaser 4-phase)
    bal["enemies"]["chaser"]["hover_speed"] = 165
    bal["enemies"]["chaser"]["lunge_speed"] = 290
    bal["enemies"]["chaser"]["recovery_speed"] = 60
    bal["enemies"]["chaser"]["hover_y"] = 165
    bal["enemies"]["chaser"]["lunge_y"] = 254
    bal["enemies"]["chaser"]["telegraph_duration"] = 0.65
    bal["enemies"]["chaser"]["lunge_duration"] = 0.50
    bal["enemies"]["chaser"]["recovery_duration"] = 1.10

    with open(BALANCE_PATH, "w", encoding="utf-8") as f:
        json.dump(bal, f, indent=2)
    print("Updated data/game_balance.json")

def apply_all_patches():
    update_game_balance()

    with open(PROJECT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    title_screen = next(l for l in data["layouts"] if l["name"] == "Title_Screen")
    main_world = next(l for l in data["layouts"] if l["name"] == "Main_World")

    # =========================================================================
    # PERBAIKAN 1: Pre-place 24 Ground_Stick instances in Main_World
    # =========================================================================
    stick_specs = [
        # Tepi Hutan (7 sticks)
        (340, 1, 10, 0),
        (560, 1, 10, 0),
        (810, 2, 30, 1),
        (1080, 1, 10, 1),
        (1340, 2, 30, 2),
        (1580, 1, 10, 2),
        (1800, 2, 30, 2),
        # Hutan Rimba (9 sticks)
        (2120, 2, 30, 3),
        (2440, 1, 10, 3),
        (2720, 3, 85, 4),
        (3040, 2, 30, 4),
        (3320, 3, 85, 5),
        (3620, 2, 30, 5),
        (3900, 3, 85, 6),
        (4150, 2, 30, 6),
        (4340, 3, 85, 6),
        # Hutan Gelap (8 sticks)
        (4680, 3, 85, 7),
        (5080, 2, 30, 7),
        (5420, 3, 85, 8),
        (5820, 4, 250, 9),
        (6220, 3, 85, 9),
        (6620, 4, 250, 10),
        (7040, 3, 85, 11),
        (7480, 4, 250, 11),
    ]

    # Remove any existing Ground_Stick from instances
    main_world["instances"] = [inst for inst in main_world["instances"] if inst.get("name") != "Ground_Stick"]

    for x_pos, tier, val, chunk in stick_specs:
        inst = {
            "angle": 0,
            "customSize": false if "false" in dir() else False,
            "height": 16,
            "keepRatio": True,
            "layer": "",
            "locked": False,
            "name": "Ground_Stick",
            "persistentUuid": str(uuid.uuid4()),
            "width": 16,
            "x": x_pos,
            "y": 280,  # Resting right on top of Ground_Floor (Y = 296 - 16 = 280)
            "zOrder": 15,
            "numberProperties": [],
            "stringProperties": [],
            "initialVariables": [
                {"name": "tier", "type": "number", "value": tier},
                {"name": "base_value", "type": "number", "value": val},
                {"name": "chunk_id", "type": "number", "value": chunk}
            ]
        }
        main_world["instances"].append(inst)

    print(f"Pre-placed {len(stick_specs)} Ground_Stick instances in Main_World (Total instances: {len(main_world['instances'])})")

    # =========================================================================
    # PERBAIKAN 2A: Update Player Object Behavior (Responsive Speed & Physics)
    # =========================================================================
    player_obj = next(o for o in main_world["objects"] if o["name"] == "Player")
    for bh in player_obj.get("behaviors", []):
        if bh.get("type") == "PlatformBehavior::PlatformerObjectBehavior":
            bh["maxSpeed"] = 230
            bh["acceleration"] = 1800
            bh["deceleration"] = 1800
            bh["jumpSpeed"] = 440
            bh["gravity"] = 1150
    print("Updated Player PlatformerObjectBehavior physics.")

    # Ensure required variables exist in Main_World
    existing_var_names = {v["name"] for v in main_world["variables"]}
    new_vars = [
        ("chaser_phase_timer", 0),
        ("chaser_lock_x", 0),
        ("chaser_lock_y", 0),
        ("chaser_dir", 1),
        ("hazard_mult", 1.0)
    ]
    for vn, vval in new_vars:
        if vn not in existing_var_names:
            main_world["variables"].append({
                "name": vn,
                "type": "number",
                "value": vval
            })
    print("Ensured all required scene variables exist in Main_World.")

    # =========================================================================
    # PERBAIKAN 3: Responsive Title_Screen (Mouse Click & Keyboard)
    # =========================================================================
    title_screen["events"] = [
        # Event 0: Menu pulsing & background scroll
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
        # Event 1: Scene start (DepartScene) -> Load High Score
        make_event(
            conditions=[make_inst("DepartScene", [""])],
            actions=[
                make_inst("ModVarScene", ["transition_timer", "=", "0"]),
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
        # Event 2: Update High Score Text
        make_event(
            conditions=[],
            actions=[
                make_inst("TextObject::String", ["Txt_Title_High", "=", "\"Rekor: \" + ToString(Variable(high_score))"])
            ]
        ),
        # Event 3: Mouse Click OR Space OR Return to Start Game
        make_event(
            conditions=[
                make_inst("VarScene", ["transition_timer", "<=", "0"]),
                make_inst("BuiltinCommonInstructions::Once", []),
                make_inst("BuiltinCommonInstructions::Or", [], sub_instructions=[
                    make_inst("SourisBouton", ["", "Left"]),
                    make_inst("KeyPressed", ["", "Space"]),
                    make_inst("KeyPressed", ["", "Return"])
                ])
            ],
            actions=[
                make_inst("ModVarScene", ["transition_timer", "=", "0.20"]),
                make_inst("PlaySound", ["", "assets/audio/sfx_menu_select.wav", "no", "70", "1"])
            ]
        ),
        # Event 4: Transition Timer countdown -> Switch to Main_World
        make_event(
            conditions=[make_inst("VarScene", ["transition_timer", ">", "0"])],
            actions=[
                make_inst("ModVarScene", ["transition_timer", "=", "max(0, Variable(transition_timer) - TimeDelta())"])
            ],
            sub_events=[
                make_event(
                    conditions=[make_inst("VarScene", ["transition_timer", "<=", "0.01"])],
                    actions=[
                        make_inst("Scene", ["", "\"Main_World\"", "no"])
                    ]
                )
            ]
        )
    ]
    print("Updated Title_Screen events with SourisBouton + KeyPressed (Space/Return) and clean minimal design.")

    # =========================================================================
    # PERBAIKAN 4 & 2: Update Main_World Events Sheet
    # =========================================================================

    # In DepartScene (Event in Main_World):
    # Ensure Ground_Stick is set to proper animation based on tier, zOrder=15, Opacity=255, and Shown.
    for ev in main_world["events"]:
        for c in ev.get("conditions", []):
            if c.get("type", {}).get("value") == "DepartScene":
                ev["actions"].extend([
                    make_inst("ChangeAnimation", ["Ground_Stick", "=", "Ground_Stick.Variable(tier) - 1"]),
                    make_inst("SetZOrder", ["Ground_Stick", "=", "15"]),
                    make_inst("Opacity", ["Ground_Stick", "=", "255"]),
                    make_inst("Show", ["Ground_Stick", ""]),
                    make_inst("Hide", ["Txt_Warning_Banner"])
                ])
                break

    # Event 1: Bramble Hazard collision & reset per frame
    main_world["events"][1] = make_event(
        conditions=[],
        actions=[
            make_inst("ModVarScene", ["is_slowed", "=", "0"]),
            make_inst("ModVarScene", ["hazard_mult", "=", "1.0"])
        ],
        sub_events=[
            make_event(
                conditions=[
                    make_inst("CollisionNP", ["Player", "Hazard_Bramble", "", "", "no"])
                ],
                actions=[
                    make_inst("ModVarScene", ["is_slowed", "=", "1"]),
                    make_inst("ModVarScene", ["hazard_mult", "=", "0.65"])
                ]
            )
        ]
    )

    # Event 2: Player responsive speed scaling based on held_tier & is_slowed
    main_world["events"][2] = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Tier <= 1 (Empty or Tier 1): 230 px/s (slowed: 150)
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "<=", "1"])],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "0"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "230"])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "1"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "150"])]
                    )
                ]
            ),
            # Tier 2: 220 px/s (slowed: 143)
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "2"])],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "0"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "220"])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "1"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "143"])]
                    )
                ]
            ),
            # Tier 3: 208 px/s (slowed: 135)
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "3"])],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "0"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "208"])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "1"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "135"])]
                    )
                ]
            ),
            # Tier 4: 195 px/s (slowed: 127)
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "4"])],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "0"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "195"])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["is_slowed", "=", "1"])],
                        actions=[make_inst("PlatformBehavior::MaxSpeed", ["Player", "PlatformerObjectBehavior", "=", "127"])]
                    )
                ]
            )
        ]
    )

    # Event 4: Zone Banners & Tint Opacities (Clean minimalist names)
    main_world["events"][4] = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Zone change trigger
            make_event(
                conditions=[
                    make_inst("BuiltinCommonInstructions::CompareNumbers", ["Variable(current_zone)", "!=", "Variable(prev_zone)"])
                ],
                actions=[
                    make_inst("ModVarScene", ["prev_zone", "=", "Variable(current_zone)"]),
                    make_inst("ModVarScene", ["banner_timer", "=", "1.80"]),
                    make_inst("SetXY", ["Txt_Zone_Banner", "=", "270", "=", "36"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["current_zone", "=", "0"])],
                        actions=[make_inst("TextObject::String", ["Txt_Zone_Banner", "=", "\"Rumah\""])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["current_zone", "=", "1"])],
                        actions=[make_inst("TextObject::String", ["Txt_Zone_Banner", "=", "\"Tepi Hutan\""])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["current_zone", "=", "2"])],
                        actions=[make_inst("TextObject::String", ["Txt_Zone_Banner", "=", "\"Hutan Rimba\""])]
                    ),
                    make_event(
                        conditions=[make_inst("VarScene", ["current_zone", "=", "3"])],
                        actions=[make_inst("TextObject::String", ["Txt_Zone_Banner", "=", "\"Hutan Gelap\""])]
                    )
                ]
            ),
            # Banner Timer countdown & fade
            make_event(
                conditions=[make_inst("VarScene", ["banner_timer", ">", "0"])],
                actions=[
                    make_inst("ModVarScene", ["banner_timer", "=", "max(0, Variable(banner_timer) - TimeDelta())"]),
                    make_inst("TextObject::Opacity", ["Txt_Zone_Banner", "=", "clamp(Variable(banner_timer) / 0.4 * 255, 0, 255)"]),
                    make_inst("Show", ["Txt_Zone_Banner", ""])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["banner_timer", "<=", "0"])],
                actions=[make_inst("Hide", ["Txt_Zone_Banner"])]
            ),
            # Zone Tints (Clean fresh colors: Rumah & Tepi Hutan 0, Hutan Rimba 14, Hutan Gelap 24)
            make_event(
                conditions=[make_inst("VarScene", ["current_zone", "=", "0"])],
                actions=[make_inst("TiledSpriteObject::SetOpacity", ["Zone_Tint_Overlay", "=", "0"])]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["current_zone", "=", "1"])],
                actions=[make_inst("TiledSpriteObject::SetOpacity", ["Zone_Tint_Overlay", "=", "0"])]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["current_zone", "=", "2"])],
                actions=[
                    make_inst("TiledSpriteObject::SetColor", ["Zone_Tint_Overlay", "\"240;190;130\""]),
                    make_inst("TiledSpriteObject::SetOpacity", ["Zone_Tint_Overlay", "=", "14"])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["current_zone", "=", "3"])],
                actions=[
                    make_inst("TiledSpriteObject::SetColor", ["Zone_Tint_Overlay", "\"160;100;220\""]),
                    make_inst("TiledSpriteObject::SetOpacity", ["Zone_Tint_Overlay", "=", "24"])
                ]
            )
        ]
    )

    # Event 9: Emergency Drop [Q]
    main_world["events"][9] = make_event(
        conditions=[
            make_inst("KeyPressed", ["", "q"]),
            make_inst("BuiltinCommonInstructions::Once", []),
            make_inst("VarScene", ["held_tier", ">", "0"]),
            make_inst("VarScene", ["emergency_drop_cooldown", "<=", "0"])
        ],
        actions=[
            make_inst("Create", ["", "Ground_Stick", "Player.CenterX() - 8", "280", "\"\""]),
            make_inst("ModVarObjet", ["Ground_Stick", "tier", "=", "Variable(held_tier)"]),
            make_inst("ModVarObjet", ["Ground_Stick", "base_value", "=", "Variable(held_value)"]),
            make_inst("ModVarObjet", ["Ground_Stick", "chunk_id", "=", "floor(Player.CenterX() / 640)"]),
            make_inst("ChangeAnimation", ["Ground_Stick", "=", "Variable(held_tier) - 1"]),
            make_inst("SetZOrder", ["Ground_Stick", "=", "15"]),
            make_inst("Opacity", ["Ground_Stick", "=", "255"]),
            make_inst("Show", ["Ground_Stick", ""]),
            make_inst("ModVarScene", ["held_tier", "=", "0"]),
            make_inst("ModVarScene", ["held_value", "=", "0"]),
            make_inst("ModVarScene", ["emergency_drop_cooldown", "=", "0.30"]),
            make_inst("TextObject::String", ["Txt_Combat_Feedback", "=", "\"[Q] Lepas\""]),
            make_inst("SetXY", ["Txt_Combat_Feedback", "=", "Player.CenterX() - 30", "=", "Player.Y() - 24"]),
            make_inst("Show", ["Txt_Combat_Feedback", ""]),
            make_inst("ModVarScene", ["combat_feedback_timer", "=", "1.0"]),
            make_inst("PlaySound", ["", "assets/audio/sfx_drop.wav", "no", "70", "1"])
        ]
    )

    # Event 12: Thief AI Feedbacks & Recapture
    # Replace Thief texts with clean feedback
    for sub in main_world["events"][12].get("events", []):
        for act in sub.get("actions", []):
            if act.get("type", {}).get("value") == "TextObject::String":
                if "PENCURI MENGINCAR" in act["parameters"][2]:
                    act["parameters"][2] = "\"Pencuri!\""
                elif "KAYU DICURI" in act["parameters"][2]:
                    act["parameters"][2] = "\"Kayu Dicuri!\""
                elif "KAYU BERHASIL" in act["parameters"][2]:
                    act["parameters"][2] = "\"Kayu Kembali!\""
                elif "PENCURI KABUR" in act["parameters"][2]:
                    act["parameters"][2] = "\"Pencuri Kabur...\""
        for ssub in sub.get("events", []):
            for act in ssub.get("actions", []):
                if act.get("type", {}).get("value") == "TextObject::String":
                    if "PENCURI MENGINCAR" in act["parameters"][2]:
                        act["parameters"][2] = "\"Pencuri!\""
                    elif "KAYU DICURI" in act["parameters"][2]:
                        act["parameters"][2] = "\"Kayu Dicuri!\""
                    elif "KAYU BERHASIL" in act["parameters"][2]:
                        act["parameters"][2] = "\"Kayu Kembali!\""
                    elif "PENCURI KABUR" in act["parameters"][2]:
                        act["parameters"][2] = "\"Pencuri Kabur...\""
                elif act.get("type", {}).get("value") == "Create" and act["parameters"][1] == "Ground_Stick":
                    act["parameters"][3] = "280"
            for sssub in ssub.get("events", []):
                for act in sssub.get("actions", []):
                    if act.get("type", {}).get("value") == "TextObject::String":
                        if "PENCURI MENGINCAR" in act["parameters"][2]:
                            act["parameters"][2] = "\"Pencuri!\""
                        elif "KAYU DICURI" in act["parameters"][2]:
                            act["parameters"][2] = "\"Kayu Dicuri!\""
                        elif "KAYU BERHASIL" in act["parameters"][2]:
                            act["parameters"][2] = "\"Kayu Kembali!\""
                        elif "PENCURI KABUR" in act["parameters"][2]:
                            act["parameters"][2] = "\"Pencuri Kabur...\""

    # Event 13: Rework AI Musuh Bayangan (Enemy_Chaser) 4-Phase Machine
    # State 0: Inactive / Cooldown
    # State 1: Hover_Track (Y=165, speed 165 px/s)
    # State 2: Telegraph (0.65s, red flicker, sfx_alert.wav, locks target X, Y=254)
    # State 3: Lunge (0.50s, low sweep Y=254 at 290 px/s, counterplay jump)
    # State 4: Recovery (1.10s, floats back to Y=165 at 60 px/s)
    main_world["events"][13] = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Sub 0: Activation Check
            make_event(
                conditions=[
                    make_inst("VarScene", ["chaser_state", "=", "0"]),
                    make_inst("VarScene", ["chaser_cooldown", "<=", "0"]),
                    make_inst("BuiltinCommonInstructions::Or", [], sub_instructions=[
                        make_inst("BuiltinCommonInstructions::And", [], sub_instructions=[
                            make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">=", "2200"]),
                            make_inst("VarScene", ["held_tier", ">=", "3"])
                        ]),
                        make_inst("BuiltinCommonInstructions::And", [], sub_instructions=[
                            make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">=", "4600"]),
                            make_inst("VarScene", ["held_tier", ">=", "1"])
                        ])
                    ])
                ],
                actions=[
                    make_inst("ModVarScene", ["chaser_state", "=", "1"]),
                    make_inst("ModVarScene", ["chaser_phase_timer", "=", "1.50"]),
                    make_inst("SetXY", ["Enemy_Chaser", "=", "clamp(Player.CenterX() - 240, 200, 7800)", "=", "165"]),
                    make_inst("Show", ["Enemy_Chaser", ""]),
                    make_inst("ChangeColor", ["Enemy_Chaser", "\"255;255;255\""]),
                    make_inst("Opacity", ["Enemy_Chaser", "=", "255"]),
                    make_inst("ChangeAnimation", ["Enemy_Chaser", "=", "0"]),
                    make_inst("Hide", ["Txt_Warning_Banner"])
                ]
            ),
            # Sub 1: State 1 (Hover_Track — 1.5s)
            make_event(
                conditions=[make_inst("VarScene", ["chaser_state", "=", "1"])],
                actions=[
                    make_inst("ModVarScene", ["chaser_phase_timer", "=", "max(0, Variable(chaser_phase_timer) - TimeDelta())"]),
                    make_inst("SetY", ["Enemy_Chaser", "=", "165"])
                ],
                sub_events=[
                    # Track player X
                    make_event(
                        conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">", "Enemy_Chaser.CenterX()"])],
                        actions=[
                            make_inst("SetX", ["Enemy_Chaser", "+", "165 * TimeDelta()"]),
                            make_inst("FlipX", ["Enemy_Chaser", "no"])
                        ]
                    ),
                    make_event(
                        conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<", "Enemy_Chaser.CenterX()"])],
                        actions=[
                            make_inst("SetX", ["Enemy_Chaser", "-", "165 * TimeDelta()"]),
                            make_inst("FlipX", ["Enemy_Chaser", "yes"])
                        ]
                    ),
                    # Home base or wood dropped retreat
                    make_event(
                        conditions=[
                            make_inst("BuiltinCommonInstructions::Or", [], sub_instructions=[
                                make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<=", "180"]),
                                make_inst("BuiltinCommonInstructions::And", [], sub_instructions=[
                                    make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<", "4600"]),
                                    make_inst("VarScene", ["held_tier", "=", "0"])
                                ])
                            ])
                        ],
                        actions=[
                            make_inst("ModVarScene", ["chaser_state", "=", "0"]),
                            make_inst("ModVarScene", ["chaser_cooldown", "=", "10.0"]),
                            make_inst("SetXY", ["Enemy_Chaser", "=", "-1000", "=", "264"]),
                            make_inst("Hide", ["Enemy_Chaser"])
                        ]
                    ),
                    # Transition to State 2 (Telegraph)
                    make_event(
                        conditions=[
                            make_inst("VarScene", ["chaser_phase_timer", "<=", "0"]),
                            make_inst("BuiltinCommonInstructions::CompareNumbers", ["abs(Player.CenterX() - Enemy_Chaser.CenterX())", "<=", "220"])
                        ],
                        actions=[
                            make_inst("ModVarScene", ["chaser_state", "=", "2"]),
                            make_inst("ModVarScene", ["chaser_phase_timer", "=", "0.65"]),
                            make_inst("ModVarScene", ["chaser_lock_x", "=", "Player.CenterX()"]),
                            make_inst("ModVarScene", ["chaser_lock_y", "=", "254"]),
                            make_inst("ChangeColor", ["Enemy_Chaser", "\"255;80;80\""]),
                            make_inst("PlaySound", ["", "assets/audio/sfx_alert.wav", "no", "70", "1"])
                        ]
                    )
                ]
            ),
            # Sub 2: State 2 (Telegraph — 0.65s)
            make_event(
                conditions=[make_inst("VarScene", ["chaser_state", "=", "2"])],
                actions=[
                    make_inst("ModVarScene", ["chaser_phase_timer", "=", "max(0, Variable(chaser_phase_timer) - TimeDelta())"]),
                    make_inst("Opacity", ["Enemy_Chaser", "=", "150 + 105 * cos(Variable(chaser_phase_timer) * 40)"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["chaser_phase_timer", "<=", "0"])],
                        actions=[
                            make_inst("ModVarScene", ["chaser_state", "=", "3"]),
                            make_inst("ModVarScene", ["chaser_phase_timer", "=", "0.50"]),
                            make_inst("ChangeColor", ["Enemy_Chaser", "\"255;255;255\""]),
                            make_inst("Opacity", ["Enemy_Chaser", "=", "255"]),
                            make_inst("ChangeAnimation", ["Enemy_Chaser", "=", "1"]),
                            make_inst("SetY", ["Enemy_Chaser", "=", "254"])
                        ],
                        sub_events=[
                            make_event(
                                conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Variable(chaser_lock_x)", ">=", "Enemy_Chaser.CenterX()"])],
                                actions=[
                                    make_inst("ModVarScene", ["chaser_dir", "=", "1"]),
                                    make_inst("FlipX", ["Enemy_Chaser", "no"])
                                ]
                            ),
                            make_event(
                                conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Variable(chaser_lock_x)", "<", "Enemy_Chaser.CenterX()"])],
                                actions=[
                                    make_inst("ModVarScene", ["chaser_dir", "=", "-1"]),
                                    make_inst("FlipX", ["Enemy_Chaser", "yes"])
                                ]
                            )
                        ]
                    )
                ]
            ),
            # Sub 3: State 3 (Lunge — 0.50s)
            make_event(
                conditions=[make_inst("VarScene", ["chaser_state", "=", "3"])],
                actions=[
                    make_inst("ModVarScene", ["chaser_phase_timer", "=", "max(0, Variable(chaser_phase_timer) - TimeDelta())"]),
                    make_inst("SetX", ["Enemy_Chaser", "+", "Variable(chaser_dir) * 290 * TimeDelta()"]),
                    make_inst("SetY", ["Enemy_Chaser", "=", "254"])
                ],
                sub_events=[
                    # Fair Hit Detection: Player gets hit ONLY if close horizontally AND vertically
                    # (Jumping player has abs(CenterY diff) > 20, safely avoiding the hit!)
                    make_event(
                        conditions=[
                            make_inst("BuiltinCommonInstructions::CompareNumbers", ["abs(Player.CenterX() - Enemy_Chaser.CenterX())", "<=", "20"]),
                            make_inst("BuiltinCommonInstructions::CompareNumbers", ["abs(Player.CenterY() - Enemy_Chaser.CenterY())", "<=", "20"]),
                            make_inst("VarScene", ["invuln_timer", "<=", "0"])
                        ],
                        actions=[
                            make_inst("ModVarScene", ["stagger_timer", "=", "0.70"]),
                            make_inst("ModVarScene", ["invuln_timer", "=", "1.60"]),
                            make_inst("ModVarScene", ["shake_timer", "=", "0.50"]),
                            make_inst("PlaySound", ["", "assets/audio/sfx_hit.wav", "no", "70", "1"]),
                            make_inst("TextObject::String", ["Txt_Combat_Feedback", "=", "\"Kena Terjang!\""]),
                            make_inst("SetXY", ["Txt_Combat_Feedback", "=", "Player.CenterX() - 40", "=", "Player.Y() - 24"]),
                            make_inst("Show", ["Txt_Combat_Feedback", ""]),
                            make_inst("ModVarScene", ["combat_feedback_timer", "=", "1.2"])
                        ],
                        sub_events=[
                            # Drop wood on hit if carrying
                            make_event(
                                conditions=[make_inst("VarScene", ["held_tier", ">", "0"])],
                                actions=[
                                    make_inst("Create", ["", "Ground_Stick", "Player.CenterX() - 8", "280", "\"\""]),
                                    make_inst("ModVarObjet", ["Ground_Stick", "tier", "=", "Variable(held_tier)"]),
                                    make_inst("ModVarObjet", ["Ground_Stick", "base_value", "=", "Variable(held_value)"]),
                                    make_inst("ModVarObjet", ["Ground_Stick", "chunk_id", "=", "floor(Player.CenterX() / 640)"]),
                                    make_inst("ChangeAnimation", ["Ground_Stick", "=", "Variable(held_tier) - 1"]),
                                    make_inst("SetZOrder", ["Ground_Stick", "=", "15"]),
                                    make_inst("Show", ["Ground_Stick", ""]),
                                    make_inst("Opacity", ["Ground_Stick", "=", "255"]),
                                    make_inst("ModVarScene", ["held_tier", "=", "0"]),
                                    make_inst("ModVarScene", ["held_value", "=", "0"])
                                ]
                            )
                        ]
                    ),
                    # Barrier safety check
                    make_event(
                        conditions=[make_inst("BuiltinCommonInstructions::CompareNumbers", ["Enemy_Chaser.CenterX()", "<=", "180"])],
                        actions=[
                            make_inst("ModVarScene", ["barrier_flash_timer", "=", "0.8"]),
                            make_inst("ModVarScene", ["shake_timer", "=", "0.35"]),
                            make_inst("ModVarScene", ["chaser_state", "=", "0"]),
                            make_inst("ModVarScene", ["chaser_cooldown", "=", "10.0"]),
                            make_inst("SetXY", ["Enemy_Chaser", "=", "-1000", "=", "264"]),
                            make_inst("Hide", ["Enemy_Chaser"]),
                            make_inst("TextObject::String", ["Txt_Combat_Feedback", "=", "\"Barrier Aman\""]),
                            make_inst("SetXY", ["Txt_Combat_Feedback", "=", "180", "=", "240"]),
                            make_inst("Show", ["Txt_Combat_Feedback", ""]),
                            make_inst("ModVarScene", ["combat_feedback_timer", "=", "2.0"])
                        ]
                    ),
                    # Transition to State 4 (Recovery)
                    make_event(
                        conditions=[make_inst("VarScene", ["chaser_phase_timer", "<=", "0"])],
                        actions=[
                            make_inst("ModVarScene", ["chaser_state", "=", "4"]),
                            make_inst("ModVarScene", ["chaser_phase_timer", "=", "1.10"]),
                            make_inst("ChangeAnimation", ["Enemy_Chaser", "=", "0"])
                        ]
                    )
                ]
            ),
            # Sub 4: State 4 (Recovery — 1.10s)
            make_event(
                conditions=[make_inst("VarScene", ["chaser_state", "=", "4"])],
                actions=[
                    make_inst("ModVarScene", ["chaser_phase_timer", "=", "max(0, Variable(chaser_phase_timer) - TimeDelta())"]),
                    make_inst("SetY", ["Enemy_Chaser", "-", "60 * TimeDelta()"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["chaser_phase_timer", "<=", "0"])],
                        sub_events=[
                            # Check if player in home or abandoned wood
                            make_event(
                                conditions=[
                                    make_inst("BuiltinCommonInstructions::Or", [], sub_instructions=[
                                        make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<=", "180"]),
                                        make_inst("BuiltinCommonInstructions::And", [], sub_instructions=[
                                            make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<", "4600"]),
                                            make_inst("VarScene", ["held_tier", "=", "0"])
                                        ])
                                    ])
                                ],
                                actions=[
                                    make_inst("ModVarScene", ["chaser_state", "=", "0"]),
                                    make_inst("ModVarScene", ["chaser_cooldown", "=", "10.0"]),
                                    make_inst("SetXY", ["Enemy_Chaser", "=", "-1000", "=", "264"]),
                                    make_inst("Hide", ["Enemy_Chaser"])
                                ]
                            ),
                            # Otherwise loop back to State 1
                            make_event(
                                conditions=[
                                    make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">", "180"]),
                                    make_inst("BuiltinCommonInstructions::Or", [], sub_instructions=[
                                        make_inst("VarScene", ["held_tier", ">=", "3"]),
                                        make_inst("BuiltinCommonInstructions::And", [], sub_instructions=[
                                            make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", ">=", "4600"]),
                                            make_inst("VarScene", ["held_tier", ">=", "1"])
                                        ])
                                    ])
                                ],
                                actions=[
                                    make_inst("ModVarScene", ["chaser_state", "=", "1"]),
                                    make_inst("ModVarScene", ["chaser_phase_timer", "=", "1.50"]),
                                    make_inst("ChangeColor", ["Enemy_Chaser", "\"255;255;255\""]),
                                    make_inst("Opacity", ["Enemy_Chaser", "=", "255"])
                                ]
                            )
                        ]
                    )
                ]
            ),
            # Sub 5: Cooldown countdown when chaser_state == 0
            make_event(
                conditions=[make_inst("VarScene", ["chaser_state", "=", "0"])],
                actions=[
                    make_inst("ModVarScene", ["chaser_cooldown", "=", "max(0, Variable(chaser_cooldown) - TimeDelta())"])
                ]
            )
        ]
    )

    # Event 18: Prompt Interaksi Stick (Minimalist & Natural)
    main_world["events"][18] = make_event(
        conditions=[],
        actions=[make_inst("Hide", ["Txt_Interact"])],
        sub_events=[
            make_event(
                conditions=[make_inst("Distance", ["Player", "Ground_Stick", "28", ""])],
                actions=[
                    make_inst("PickNearest", ["Ground_Stick", "Player.CenterX()", "Player.CenterY()"]),
                    make_inst("Show", ["Txt_Interact", ""]),
                    make_inst("SetXY", ["Txt_Interact", "=", "Ground_Stick.CenterX() - 35", "=", "Ground_Stick.Y() - 20"])
                ],
                sub_events=[
                    # Empty hands: [E] Ambil
                    make_event(
                        conditions=[make_inst("VarScene", ["held_tier", "=", "0"])],
                        actions=[
                            make_inst("TextObject::String", ["Txt_Interact", "=", "\"[E] Ambil\""]),
                            make_inst("TextObject::ChangeColor", ["Txt_Interact", "\"245;242;235\""])
                        ]
                    ),
                    # Holding stick
                    make_event(
                        conditions=[make_inst("VarScene", ["held_tier", ">", "0"])],
                        actions=[
                            make_inst("ModVarScene", ["val_diff", "=", "Ground_Stick.Variable(base_value) - Variable(held_value)"])
                        ],
                        sub_events=[
                            # Upgrade (val_diff > 0): soft green
                            make_event(
                                conditions=[make_inst("VarScene", ["val_diff", ">", "0"])],
                                actions=[
                                    make_inst("TextObject::String", ["Txt_Interact", "=", "\"[E] Tukar (+)\""]),
                                    make_inst("TextObject::ChangeColor", ["Txt_Interact", "\"130;230;140\""])
                                ]
                            ),
                            # Equal (val_diff == 0): clean white
                            make_event(
                                conditions=[make_inst("VarScene", ["val_diff", "=", "0"])],
                                actions=[
                                    make_inst("TextObject::String", ["Txt_Interact", "=", "\"[E] Tukar\""]),
                                    make_inst("TextObject::ChangeColor", ["Txt_Interact", "\"245;242;235\""])
                                ]
                            ),
                            # Downgrade (val_diff < 0): soft coral
                            make_event(
                                conditions=[make_inst("VarScene", ["val_diff", "<", "0"])],
                                actions=[
                                    make_inst("TextObject::String", ["Txt_Interact", "=", "\"[E] Tukar (-)\""]),
                                    make_inst("TextObject::ChangeColor", ["Txt_Interact", "\"240;130;120\""])
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

    # Event 19: Swap Stick [E]
    main_world["events"][19] = make_event(
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
            # Empty hand pickup
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "0"])],
                actions=[
                    make_inst("ModVarScene", ["held_tier", "=", "Ground_Stick.Variable(tier)"]),
                    make_inst("ModVarScene", ["held_value", "=", "Ground_Stick.Variable(base_value)"]),
                    make_inst("Delete", ["Ground_Stick", ""]),
                    make_inst("ModVarScene", ["swap_cooldown", "=", "0.25"]),
                    make_inst("PlaySound", ["", "assets/audio/sfx_pickup.wav", "no", "70", "1"])
                ]
            ),
            # Swap with stick on ground
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", ">", "0"])],
                actions=[
                    make_inst("ModVarScene", ["temp_tier", "=", "Variable(held_tier)"]),
                    make_inst("ModVarScene", ["temp_val", "=", "Variable(held_value)"]),
                    make_inst("ModVarScene", ["drop_x", "=", "Ground_Stick.X()"]),
                    make_inst("ModVarScene", ["drop_y", "=", "280"]),
                    make_inst("ModVarScene", ["drop_chunk", "=", "Ground_Stick.Variable(chunk_id)"]),
                    make_inst("ModVarScene", ["held_tier", "=", "Ground_Stick.Variable(tier)"]),
                    make_inst("ModVarScene", ["held_value", "=", "Ground_Stick.Variable(base_value)"]),
                    make_inst("Delete", ["Ground_Stick", ""]),
                    make_inst("Create", ["", "Ground_Stick", "Variable(drop_x)", "Variable(drop_y)", "\"\""]),
                    make_inst("ModVarObjet", ["Ground_Stick", "tier", "=", "Variable(temp_tier)"]),
                    make_inst("ModVarObjet", ["Ground_Stick", "base_value", "=", "Variable(temp_val)"]),
                    make_inst("ModVarObjet", ["Ground_Stick", "chunk_id", "=", "Variable(drop_chunk)"]),
                    make_inst("ChangeAnimation", ["Ground_Stick", "=", "Variable(temp_tier) - 1"]),
                    make_inst("SetZOrder", ["Ground_Stick", "=", "15"]),
                    make_inst("Show", ["Ground_Stick", ""]),
                    make_inst("Opacity", ["Ground_Stick", "=", "255"]),
                    make_inst("ModVarScene", ["swap_cooldown", "=", "0.25"]),
                    make_inst("PlaySound", ["", "assets/audio/sfx_pickup.wav", "no", "70", "1"])
                ]
            )
        ]
    )

    # Event 20: Deposit Score at Home Base (Clean text)
    main_world["events"][20] = make_event(
        conditions=[
            make_inst("BuiltinCommonInstructions::CompareNumbers", ["Player.CenterX()", "<=", "180"]),
            make_inst("VarScene", ["held_tier", ">", "0"])
        ],
        actions=[
            make_inst("ModVarScene", ["earned", "=", "round(Variable(held_value) * (1 + Variable(current_chunk) * 0.15))"]),
            make_inst("ModVarScene", ["total_score", "+", "Variable(earned)"]),
            make_inst("TextObject::String", ["Txt_Floating_Gain", "=", "\"+\" + ToString(Variable(earned))"]),
            make_inst("SetXY", ["Txt_Floating_Gain", "=", "Player.CenterX() - 10", "=", "Player.Y() - 20"]),
            make_inst("Show", ["Txt_Floating_Gain", ""]),
            make_inst("ModVarScene", ["gain_timer", "=", "1.2"]),
            make_inst("ModVarScene", ["held_tier", "=", "0"]),
            make_inst("ModVarScene", ["held_value", "=", "0"]),
            make_inst("PlaySound", ["", "assets/audio/sfx_extraction.wav", "no", "70", "1"])
        ]
    )

    # Event 21: HUD & Slot Label (Minimalist)
    main_world["events"][21] = make_event(
        conditions=[],
        actions=[
            make_inst("TextObject::String", ["Txt_HUD", "=", "\"Kayu: \" + ToString(Variable(total_score))"])
        ],
        sub_events=[
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "0"])],
                actions=[
                    make_inst("ChangeAnimation", ["UI_Slot_Icon", "=", "0"]),
                    make_inst("TextObject::String", ["Txt_Slot_Label", "=", "\"\""])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "1"])],
                actions=[
                    make_inst("ChangeAnimation", ["UI_Slot_Icon", "=", "1"]),
                    make_inst("TextObject::String", ["Txt_Slot_Label", "=", "\"Ranting\""])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "2"])],
                actions=[
                    make_inst("ChangeAnimation", ["UI_Slot_Icon", "=", "2"]),
                    make_inst("TextObject::String", ["Txt_Slot_Label", "=", "\"Kayu Oak\""])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "3"])],
                actions=[
                    make_inst("ChangeAnimation", ["UI_Slot_Icon", "=", "3"]),
                    make_inst("TextObject::String", ["Txt_Slot_Label", "=", "\"Kayu Damar\""])
                ]
            ),
            make_event(
                conditions=[make_inst("VarScene", ["held_tier", "=", "4"])],
                actions=[
                    make_inst("ChangeAnimation", ["UI_Slot_Icon", "=", "4"]),
                    make_inst("TextObject::String", ["Txt_Slot_Label", "=", "\"Kayu Tua\""])
                ]
            )
        ]
    )

    # Event 30: Save Record Toast (Clean: "Rekor Baru!")
    for sub in main_world["events"][30].get("events", []):
        for ssub in sub.get("events", []):
            for act in ssub.get("actions", []):
                if act.get("type", {}).get("value") == "TextObject::String" and act["parameters"][0] == "Txt_Save_Toast":
                    act["parameters"][2] = "\"Rekor Baru!\""

    with open(PROJECT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("All patches successfully applied to StickScavenger.json!")

if __name__ == "__main__":
    apply_all_patches()
