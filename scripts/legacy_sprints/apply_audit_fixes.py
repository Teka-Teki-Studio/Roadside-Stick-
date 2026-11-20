import json
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

def fix_instruction(inst, is_cond, lname):
    type_val = inst.get("type", {}).get("value", "")
    params = inst.get("parameters", [])

    if is_cond:
        # CollisionNP: must have 5 parameters [obj1, obj2, conditionInverted, currentScene, yesorno]
        if type_val == "CollisionNP" and len(params) == 4:
            inst["parameters"] = [params[0], params[1], params[2], "", params[3]]

        if "subInstructions" in inst:
            for sub in inst["subInstructions"]:
                fix_instruction(sub, True, lname)
    else:
        # SetColor -> ChangeColor (2 params: [object, color])
        if type_val == "SetColor":
            inst["type"]["value"] = "ChangeColor"
            # Ensure it has exactly 2 params: [object, color]
            if len(params) >= 2:
                inst["parameters"] = [params[0], params[1]]

        # SetOpacity -> Opacity (for Sprite) or TextObject::Opacity (for Text)
        elif type_val == "SetOpacity":
            obj_name = params[0] if len(params) > 0 else ""
            if obj_name.startswith("Txt_"):
                inst["type"]["value"] = "TextObject::Opacity"
            else:
                inst["type"]["value"] = "Opacity"

        # ChangeTimeScale: must have 2 parameters ["", scale]
        elif type_val == "ChangeTimeScale":
            if len(params) == 1:
                inst["parameters"] = ["", params[0]]

        # PlaySound: must have 5 parameters ["", soundfile, yesorno, volume, pitch]
        elif type_val == "PlaySound":
            # If param 0 is audio file (shifted)
            if len(params) == 6 and params[0].startswith("assets/audio"):
                sound_file = params[0]
                repeat = params[2] if params[2] in ["yes", "no"] else "no"
                vol = params[3]
                pitch = params[4]
                inst["parameters"] = ["", sound_file, repeat, str(vol), str(pitch)]
            elif len(params) == 5 and params[0].startswith("assets/audio"):
                sound_file = params[0]
                repeat = params[1] if params[1] in ["yes", "no"] else "no"
                vol = params[2]
                pitch = params[3]
                inst["parameters"] = ["", sound_file, repeat, str(vol), str(pitch)]

        # WriteNumberToJSONFile -> EcrireFichierExp (3 params: [storage, group, expression])
        elif type_val == "WriteNumberToJSONFile":
            inst["type"]["value"] = "EcrireFichierExp"
            # params was [val, storage, group, ""]
            # EcrireFichierExp expects [storage, group, expression]
            storage = params[1] if len(params) > 1 else '"StickScavengerSave"'
            group = params[2] if len(params) > 2 else '"high_score"'
            expr = params[0] if len(params) > 0 else 'Variable(high_score)'
            inst["parameters"] = [storage, group, expr]

        # ReadNumberFromJSONFile -> LireFichierExp (4 params: [storage, group, currentScene, scenevar])
        elif type_val == "ReadNumberFromJSONFile":
            inst["type"]["value"] = "LireFichierExp"
            # params was [storage, group, var_name, ""]
            # LireFichierExp expects [storage, group, "", var_name]
            storage = params[0] if len(params) > 0 else '"StickScavengerSave"'
            group = params[1] if len(params) > 1 else '"high_score"'
            var_name = params[2] if len(params) > 2 else 'high_score'
            inst["parameters"] = [storage, group, "", var_name]

def fix_events_list(events_list, lname):
    for ev in events_list:
        for c in ev.get("conditions", []):
            fix_instruction(c, True, lname)
        for a in ev.get("actions", []):
            fix_instruction(a, False, lname)
        if ev.get("events"):
            fix_events_list(ev["events"], lname)

def apply_fixes():
    with open(PROJECT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Apply generic instruction and parameter fixes to all layouts
    for layout in data["layouts"]:
        lname = layout["name"]
        fix_events_list(layout["events"], lname)

    # 2. Fix Title_Screen: Add GroupExists condition before LireFichierExp
    title_layout = next(l for l in data["layouts"] if l["name"] == "Title_Screen")
    # Event 1 in Title_Screen was DepartScene -> LireFichierExp
    # In GDevelop 5, reading a file should be guarded by GroupExists or read cleanly
    for ev in title_layout["events"]:
        for a in ev.get("actions", []):
            if a.get("type", {}).get("value") == "LireFichierExp":
                # Convert this event to sub-event under GroupExists
                ev["subInstructions"] = [] # clear any
                ev["actions"] = [
                    make_inst("ModVarScene", ["transition_timer", "=", "0"])
                ]
                ev["events"] = [
                    make_event(
                        conditions=[
                            make_inst("GroupExists", ['"StickScavengerSave"', '"high_score"'])
                        ],
                        actions=[
                            make_inst("LireFichierExp", ['"StickScavengerSave"', '"high_score"', "", "high_score"])
                        ]
                    )
                ]
                break

    # 3. Fix Main_World:
    main_world = next(l for l in data["layouts"] if l["name"] == "Main_World")

    # A. Fix Pause System: Replace with clean anti double-flip toggle (No PauseScene/UnpauseScene)
    # Find ev_pause_system (index 23 in root events or by searching for Pause_Overlay)
    pause_ev_idx = -1
    for idx, ev in enumerate(main_world["events"]):
        for a in ev.get("actions", []):
            if a.get("parameters", []) and a["parameters"][0] == "pause_cooldown":
                pause_ev_idx = idx
                break
        if pause_ev_idx >= 0:
            break

    if pause_ev_idx >= 0:
        main_world["events"][pause_ev_idx] = make_event(
            conditions=[
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

    # B. Fix Hitstop: real-time decrement (0.016 per frame) instead of TimeDelta()
    for ev in main_world["events"]:
        for sev in ev.get("events", []):
            for c in sev.get("conditions", []):
                if c.get("type", {}).get("value") == "VarScene" and len(c.get("parameters", [])) >= 2:
                    if c["parameters"][0] == "hitstop_timer" and c["parameters"][1] == ">":
                        # This is the hitstop active event
                        sev["actions"] = [
                            make_inst("ModVarScene", ["hitstop_timer", "=", "max(0, Variable(hitstop_timer) - 0.016)"]),
                            make_inst("ChangeTimeScale", ["", "0.05"])
                        ]

    # C. Fix Save/Load High Score in Main_World:
    # Find ev_save_load
    save_ev_idx = -1
    for idx, ev in enumerate(main_world["events"]):
        for sev in ev.get("events", []):
            for c in sev.get("conditions", []):
                if c.get("type", {}).get("value") == "VarScene" and len(c.get("parameters", [])) >= 1:
                    if c["parameters"][0] == "high_score":
                        save_ev_idx = idx
                        break
        if save_ev_idx >= 0:
            break

    if save_ev_idx >= 0:
        main_world["events"][save_ev_idx] = make_event(
            conditions=[],
            actions=[],
            sub_events=[
                # Load high score if storage exists
                make_event(
                    conditions=[
                        make_inst("VarScene", ["high_score", "=", "0"]),
                        make_inst("GroupExists", ['"StickScavengerSave"', '"high_score"'])
                    ],
                    actions=[
                        make_inst("LireFichierExp", ['"StickScavengerSave"', '"high_score"', "", "high_score"])
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

    # D. In Scene Start event (DepartScene): ensure high_score load has GroupExists
    for ev in main_world["events"]:
        for c in ev.get("conditions", []):
            if c.get("type", {}).get("value") == "DepartScene":
                # Ensure no old fake actions remain
                ev["actions"] = [
                    a for a in ev["actions"]
                    if a.get("type", {}).get("value") not in ["PauseScene", "UnpauseScene", "ReadNumberFromJSONFile", "WriteNumberToJSONFile"]
                ]
                break

    with open(PROJECT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("Audit fixes applied cleanly to StickScavenger.json!")

if __name__ == "__main__":
    apply_fixes()
