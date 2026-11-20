import json
import os
import re
import sys

PROJECT_PATH = "StickScavenger.json" if os.path.exists("StickScavenger.json") else os.path.join(os.path.dirname(__file__), "..", "StickScavenger.json")
PROJ_DIR = os.path.dirname(os.path.abspath(PROJECT_PATH))

VALID_CONDITIONS = {
    "AnimationEnded": 1,
    "BuiltinCommonInstructions::And": 0,
    "BuiltinCommonInstructions::CompareNumbers": 3,
    "BuiltinCommonInstructions::Once": 0,
    "BuiltinCommonInstructions::Or": 0,
    "CollisionNP": 5,
    "DepartScene": 1,
    "Distance": 4,
    "KeyPressed": 2,
    "PlatformBehavior::IsMoving": 2,
    "PlatformBehavior::IsOnFloor": 2,
    "VarScene": 3,
    "GroupExists": 2,
    "SourisBouton": 2,
}

VALID_ACTIONS = {
    "ChangeAnimation": 3,
    "ChangeColor": 2,
    "ChangeTimeScale": 2,
    "Create": 5,
    "Delete": 2,
    "EcrireFichierExp": 3,
    "EcrireFichierTxt": 3,
    "FlipX": 2,
    "Hide": 1,
    "LireFichierExp": 4,
    "LireFichierTxt": 4,
    "ModVarObjet": 4,
    "ModVarScene": 3,
    "Opacity": 3,
    "PickNearest": 3,
    "PlatformBehavior::IgnoreDefaultControls": 3,
    "PlatformBehavior::MaxSpeed": 4,
    "PlatformBehavior::SimulateJumpKey": 2,
    "PlatformBehavior::SimulateLeftKey": 2,
    "PlatformBehavior::SimulateRightKey": 2,
    "PlaySound": 5,
    "PlaySoundCanal": 6,
    "Scene": 3,
    "SetCameraCenterX": 5,
    "SetCameraCenterY": 5,
    "SetX": 3,
    "SetXY": 5,
    "SetY": 3,
    "SetZOrder": 3,
    "Show": 2,
    "StopSoundCanal": 2,
    "TextObject::ChangeColor": 2,
    "TextObject::Opacity": 3,
    "TextObject::String": 3,
    "TiledSpriteObject::SetColor": 2,
    "TiledSpriteObject::SetOpacity": 3,
    "ZoomCamera": 4,
}

def run_healthcheck():
    print("=" * 70)
    print("DEEP HEALTHCHECK & AUDIT: GDevelop 5 Project (StickScavenger.json)")
    print("=" * 70)

    if not os.path.exists(PROJECT_PATH):
        print(f"FATAL: {PROJECT_PATH} does not exist.")
        sys.exit(1)

    with open(PROJECT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    findings = []
    
    # Check registered resources exist on disk
    resources = data.get("resources", {}).get("resources", [])
    for r in resources:
        fpath = r.get("file", "")
        full_fpath = os.path.join(PROJ_DIR, fpath)
        if not os.path.exists(full_fpath):
            findings.append({
                "category": "MISSING_RESOURCE",
                "scene": "GLOBAL",
                "detail": f"Resource file '{fpath}' does not exist on disk."
            })
        if r.get("kind") == "image" and r.get("smoothed") is not False:
            findings.append({
                "category": "SMOOTHED_IMAGE",
                "scene": "GLOBAL",
                "detail": f"Resource image '{fpath}' has smoothed: true (must be false)."
            })

    # Collect layout objects and verify instance ownership
    layouts = data.get("layouts", [])
    all_registered_files = {r.get("file") for r in resources}

    for layout in layouts:
        lname = layout.get("name", "Unknown")
        objs = layout.get("objects", [])
        obj_names = set()
        
        for obj in objs:
            oname = obj.get("name", "")
            otype = obj.get("type", "")
            obj_names.add(oname)

            # Check sprite animation files
            if otype == "Sprite":
                for anim in obj.get("animations", []):
                    for d in anim.get("directions", []):
                        for sp in d.get("sprites", []):
                            img = sp.get("image", "")
                            if img and img not in all_registered_files:
                                findings.append({
                                    "category": "UNREGISTERED_SPRITE_IMAGE",
                                    "scene": lname,
                                    "detail": f"Object '{oname}' uses image '{img}' not registered in project resources."
                                })
            elif "TiledSprite" in otype:
                tex = obj.get("texture", "")
                if tex and tex not in all_registered_files:
                    findings.append({
                        "category": "UNREGISTERED_TILED_TEXTURE",
                        "scene": lname,
                        "detail": f"Object '{oname}' uses texture '{tex}' not registered in project resources."
                    })

        # Check instance references
        instances = layout.get("instances", [])
        for inst in instances:
            iname = inst.get("name", "")
            if iname not in obj_names:
                findings.append({
                    "category": "ORPHAN_INSTANCE",
                    "scene": lname,
                    "detail": f"Instance '{iname}' at ({inst.get('x')}, {inst.get('y')}) references object not defined in layout."
                })

        # Audit events in scene
        events = layout.get("events", [])
        audit_events(events, lname, findings)

    # Print summary
    print("\nAUDIT SUMMARY:")
    print(f"Total Layouts audited: {len(layouts)}")
    total_events_count = sum(count_events(l.get("events", [])) for l in layouts)
    print(f"Total Events audited: {total_events_count}")
    print(f"Unique Condition types ({len(VALID_CONDITIONS)}): {sorted(list(VALID_CONDITIONS.keys()))}")
    print(f"Unique Action types ({len(VALID_ACTIONS)}): {sorted(list(VALID_ACTIONS.keys()))}")
    print(f"TOTAL FINDINGS / VIOLATIONS: {len(findings)}")
    print("-" * 70)

    if findings:
        for f in findings:
            print(f"[{f['category']}] Scene: {f['scene']} -> {f['detail']}")
        print("\n" + "=" * 70)
        print("RESULT: FAILED WITH VIOLATIONS!")
        print("=" * 70)
        sys.exit(1)
    else:
        print("\n" + "=" * 70)
        print("RESULT: 100% HEALTHCHECK PASS! NO ERRORS FOUND.")
        print("=" * 70)

def count_events(evs):
    c = len(evs)
    for ev in evs:
        if ev.get("events"):
            c += count_events(ev["events"])
    return c

def audit_events(evs, lname, findings, path=""):
    for idx, ev in enumerate(evs):
        cur_path = f"{path}[{idx}]" if path else f"{lname}[{idx}]"
        
        # Audit conditions
        for cidx, c in enumerate(ev.get("conditions", [])):
            ctype = c.get("type", {}).get("value", "")
            params = c.get("parameters", [])
            
            if ctype not in VALID_CONDITIONS:
                findings.append({
                    "category": "UNKNOWN_INSTRUCTION",
                    "scene": lname,
                    "detail": f"Condition #{cidx} at {cur_path} has unknown type '{ctype}'"
                })
            else:
                expected_p = VALID_CONDITIONS[ctype]
                if len(params) != expected_p:
                    findings.append({
                        "category": "PARAM_COUNT_MISMATCH",
                        "scene": lname,
                        "detail": f"Condition #{cidx} ('{ctype}') at {cur_path} has {len(params)} params, expected {expected_p}"
                    })

            # Check single equals relational operator
            if ctype in ["VarScene", "BuiltinCommonInstructions::CompareNumbers"]:
                if len(params) >= 2 and params[1] in ["==", "==="]:
                    findings.append({
                        "category": "INVALID_OPERATOR",
                        "scene": lname,
                        "detail": f"Condition '{ctype}' at {cur_path} uses operator '{params[1]}', must be '='"
                    })

            # Recurse sub-instructions
            if "subInstructions" in c:
                for sidx, sc in enumerate(c["subInstructions"]):
                    sctype = sc.get("type", {}).get("value", "")
                    sparams = sc.get("parameters", [])
                    if sctype not in VALID_CONDITIONS:
                        findings.append({
                            "category": "UNKNOWN_INSTRUCTION",
                            "scene": lname,
                            "detail": f"Sub-condition #{sidx} at {cur_path} has unknown type '{sctype}'"
                        })

        # Audit actions
        for aidx, a in enumerate(ev.get("actions", [])):
            atype = a.get("type", {}).get("value", "")
            params = a.get("parameters", [])

            if atype not in VALID_ACTIONS:
                findings.append({
                    "category": "UNKNOWN_INSTRUCTION",
                    "scene": lname,
                    "detail": f"Action #{aidx} at {cur_path} has unknown type '{atype}' (params={params})"
                })
            else:
                expected_p = VALID_ACTIONS[atype]
                if len(params) != expected_p:
                    findings.append({
                        "category": "PARAM_COUNT_MISMATCH",
                        "scene": lname,
                        "detail": f"Action #{aidx} ('{atype}') at {cur_path} has {len(params)} params, expected {expected_p} (params={params})"
                    })

            # Check expression quotes for Scene actions
            if atype == "Scene" and len(params) >= 2:
                scene_arg = params[1]
                if not (scene_arg.startswith('"') and scene_arg.endswith('"')):
                    findings.append({
                        "category": "UNQUOTED_SCENE_PARAM",
                        "scene": lname,
                        "detail": f"Action 'Scene' at {cur_path} has unquoted scene parameter: {scene_arg}"
                    })

            # Check single equals for ModVar
            if atype in ["ModVarScene", "ModVarObjet"]:
                if len(params) >= 2 and params[1] in ["==", "==="]:
                    findings.append({
                        "category": "INVALID_OPERATOR",
                        "scene": lname,
                        "detail": f"Action '{atype}' at {cur_path} uses operator '{params[1]}', must be '='"
                    })

        # Recurse sub-events
        if ev.get("events"):
            audit_events(ev["events"], lname, findings, cur_path)

if __name__ == "__main__":
    run_healthcheck()
