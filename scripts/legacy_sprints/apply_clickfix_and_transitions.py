import json

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

def apply_fixes():
    print("=" * 70)
    print("APPLYING ROBUST CLICK-FIX & FADE STATE-MACHINE")
    print("=" * 70)

    with open(PROJECT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    title_screen = next(l for l in data["layouts"] if l["name"] == "Title_Screen")
    main_world = next(l for l in data["layouts"] if l["name"] == "Main_World")

    # Clean variables in Title_Screen
    title_screen["variables"] = [
        {"name": "menu_pulse_time", "type": "number", "value": 0},
        {"name": "menu_scroll_x", "type": "number", "value": 0},
        {"name": "high_score", "type": "number", "value": 0},
        {"name": "fade_state", "type": "number", "value": 1},
        {"name": "fade_alpha", "type": "number", "value": 255}
    ]

    # Clean variables in Main_World
    mw_var_names = {v["name"] for v in main_world["variables"]}
    if "fade_state" not in mw_var_names:
        main_world["variables"].append({"name": "fade_state", "type": "number", "value": 1})
    if "fade_alpha" not in mw_var_names:
        main_world["variables"].append({"name": "fade_alpha", "type": "number", "value": 255})

    # =========================================================================
    # REBUILD Title_Screen Events (3 separate top-level input events, NO BuiltinCommonInstructions::Or)
    # =========================================================================
    title_screen["events"] = [
        # Event 0: Visual pulses & scroll
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
        # Event 1: DepartScene (Start of scene)
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
        # Event 2: High score text
        make_event(
            conditions=[],
            actions=[
                make_inst("TextObject::String", ["Txt_Title_High", "=", "\"Rekor: \" + ToString(Variable(high_score))"])
            ]
        ),
        # Event 3: Input 1 (Mouse Left Click)
        make_event(
            conditions=[
                make_inst("SourisBouton", ["", "Left"]),
                make_inst("VarScene", ["fade_state", "<=", "1"])
            ],
            actions=[
                make_inst("PlaySound", ["", "assets/audio/sfx_menu_select.wav", "no", "70", "1"]),
                make_inst("ModVarScene", ["fade_state", "=", "2"])
            ]
        ),
        # Event 4: Input 2 (Space Key)
        make_event(
            conditions=[
                make_inst("KeyPressed", ["", "Space"]),
                make_inst("VarScene", ["fade_state", "<=", "1"])
            ],
            actions=[
                make_inst("PlaySound", ["", "assets/audio/sfx_menu_select.wav", "no", "70", "1"]),
                make_inst("ModVarScene", ["fade_state", "=", "2"])
            ]
        ),
        # Event 5: Input 3 (Return Key)
        make_event(
            conditions=[
                make_inst("KeyPressed", ["", "Return"]),
                make_inst("VarScene", ["fade_state", "<=", "1"])
            ],
            actions=[
                make_inst("PlaySound", ["", "assets/audio/sfx_menu_select.wav", "no", "70", "1"]),
                make_inst("ModVarScene", ["fade_state", "=", "2"])
            ]
        ),
        # Event 6: Fade-In (fade_state == 1)
        make_event(
            conditions=[make_inst("VarScene", ["fade_state", "=", "1"])],
            actions=[
                make_inst("Show", ["Transition_Fade", ""]),
                make_inst("ModVarScene", ["fade_alpha", "-", "730 * max(0.016, TimeDelta())"]),
                make_inst("Opacity", ["Transition_Fade", "=", "max(0, Variable(fade_alpha))"])
            ],
            sub_events=[
                make_event(
                    conditions=[make_inst("VarScene", ["fade_alpha", "<=", "0"])],
                    actions=[
                        make_inst("ModVarScene", ["fade_state", "=", "0"]),
                        make_inst("ModVarScene", ["fade_alpha", "=", "0"]),
                        make_inst("Hide", ["Transition_Fade"])
                    ]
                )
            ]
        ),
        # Event 7: Fade-Out to Main_World (fade_state == 2)
        make_event(
            conditions=[make_inst("VarScene", ["fade_state", "=", "2"])],
            actions=[
                make_inst("Show", ["Transition_Fade", ""]),
                make_inst("ModVarScene", ["fade_alpha", "+", "850 * max(0.016, TimeDelta())"]),
                make_inst("Opacity", ["Transition_Fade", "=", "min(255, Variable(fade_alpha))"])
            ],
            sub_events=[
                make_event(
                    conditions=[make_inst("VarScene", ["fade_alpha", ">=", "255"])],
                    actions=[
                        make_inst("ModVarScene", ["fade_state", "=", "99"]),
                        make_inst("Scene", ["", "\"Main_World\"", "no"])
                    ]
                )
            ]
        )
    ]
    print(f"Title_Screen rebuilt with {len(title_screen['events'])} clean events.")

    # =========================================================================
    # UPDATE Main_World Fade Machine (fade_state = 1, 2, 3 with guard 99)
    # =========================================================================
    # Find mw_fade_event (the last event or by finding 'fade_alpha' and 'Scene' in subevents)
    # Replace the fade state machine in Main_World
    mw_fade_event = make_event(
        conditions=[],
        actions=[],
        sub_events=[
            # Sub 0: fade_state == 1 (Fade-In)
            make_event(
                conditions=[make_inst("VarScene", ["fade_state", "=", "1"])],
                actions=[
                    make_inst("Show", ["Transition_Fade", ""]),
                    make_inst("ModVarScene", ["fade_alpha", "-", "730 * max(0.016, TimeDelta())"]),
                    make_inst("Opacity", ["Transition_Fade", "=", "max(0, Variable(fade_alpha))"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["fade_alpha", "<=", "0"])],
                        actions=[
                            make_inst("ModVarScene", ["fade_state", "=", "0"]),
                            make_inst("ModVarScene", ["fade_alpha", "=", "0"]),
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
                    make_inst("ModVarScene", ["fade_alpha", "+", "850 * max(0.016, TimeDelta())"]),
                    make_inst("Opacity", ["Transition_Fade", "=", "min(255, Variable(fade_alpha))"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["fade_alpha", ">=", "255"])],
                        actions=[
                            make_inst("ModVarScene", ["fade_state", "=", "99"]),
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
                    make_inst("ModVarScene", ["fade_alpha", "+", "850 * max(0.016, TimeDelta())"]),
                    make_inst("Opacity", ["Transition_Fade", "=", "min(255, Variable(fade_alpha))"])
                ],
                sub_events=[
                    make_event(
                        conditions=[make_inst("VarScene", ["fade_alpha", ">=", "255"])],
                        actions=[
                            make_inst("ModVarScene", ["fade_state", "=", "99"]),
                            make_inst("Scene", ["", "\"Title_Screen\"", "no"])
                        ]
                    )
                ]
            )
        ]
    )

    # In Main_World events: replace the last event with mw_fade_event
    main_world["events"][-1] = mw_fade_event

    with open(PROJECT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("SUCCESS: StickScavenger.json patched cleanly!")

if __name__ == "__main__":
    apply_fixes()
