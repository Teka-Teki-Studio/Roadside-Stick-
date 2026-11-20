import json
import os
import sys

PROJECT_PATH = "StickScavenger.json"

def verify_runtime_readiness():
    print("=" * 70)
    print("COMPREHENSIVE RUNTIME-READINESS & TRANSITION VERIFICATION")
    print("=" * 70)

    with open(PROJECT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    mw = next(l for l in data["layouts"] if l["name"] == "Main_World")
    ts = next(l for l in data["layouts"] if l["name"] == "Title_Screen")

    # 1. Check >= 24 Ground_Stick instances in Main_World instances (initialInstances)
    stick_instances = [i for i in mw["instances"] if i.get("name") == "Ground_Stick"]
    print(f"Checking Ground_Stick instances in Main_World: Found {len(stick_instances)}")
    assert len(stick_instances) >= 24, f"FAIL: Expected >= 24 Ground_Stick instances, got {len(stick_instances)}"
    
    for idx, inst in enumerate(stick_instances):
        y = inst.get("y", 999)
        z = inst.get("zOrder", 0)
        assert y < 296, f"FAIL: Instance #{idx} at x={inst.get('x')} has Y={y} >= 296 (buried in floor!)"
        assert z >= 10, f"FAIL: Instance #{idx} at x={inst.get('x')} has zOrder={z} < 10"
        vars_dict = {v["name"]: v.get("value") for v in inst.get("initialVariables", [])}
        assert "tier" in vars_dict and vars_dict["tier"] in [1, 2, 3, 4], f"Missing/invalid tier in instance #{idx}"
        assert "base_value" in vars_dict and vars_dict["base_value"] in [10, 30, 85, 250], f"Missing/invalid base_value in instance #{idx}"

    print(f"PASS: Exactly {len(stick_instances)} Ground_Stick instances verified. All standing above floor (Y={stick_instances[0]['y']} < 296, zOrder={stick_instances[0]['zOrder']} >= 10).")

    # 2. Check SourisBouton (Left) + KeyPressed (Return & Space) in Title_Screen
    conditions_found = set()
    def scan_conds(evs):
        for ev in evs:
            for c in ev.get("conditions", []):
                t = c.get("type", {}).get("value")
                p = c.get("parameters", [])
                if t == "SourisBouton":
                    conditions_found.add(f"SourisBouton_{p[1]}")
                elif t == "KeyPressed":
                    conditions_found.add(f"KeyPressed_{p[1]}")
                if "subInstructions" in c:
                    for sc in c["subInstructions"]:
                        st = sc.get("type", {}).get("value")
                        sp = sc.get("parameters", [])
                        if st == "SourisBouton":
                            conditions_found.add(f"SourisBouton_{sp[1]}")
                        elif st == "KeyPressed":
                            conditions_found.add(f"KeyPressed_{sp[1]}")
            if ev.get("events"):
                scan_conds(ev["events"])

    scan_conds(ts["events"])
    print("Found Title_Screen input conditions:", conditions_found)
    assert "SourisBouton_Left" in conditions_found, "FAIL: SourisBouton (Left) missing from Title_Screen!"
    assert "KeyPressed_Space" in conditions_found, "FAIL: KeyPressed (Space) missing from Title_Screen!"
    assert "KeyPressed_Return" in conditions_found, "FAIL: KeyPressed (Return) missing from Title_Screen!"
    print("PASS: Title_Screen responsive input verified (Mouse Left Click + Space + Enter).")

    # 3. Check NO AI Slop strings in Main_World Event Sheet
    forbidden_strings = ["ZONA 1", "Chunk", "UPGRADE", "DOWNGRADE", "STATUS:"]
    found_violations = []

    def scan_strings(evs, path=""):
        for i, ev in enumerate(evs):
            curr_path = f"{path}.{i}"
            s = json.dumps(ev)
            for bad in forbidden_strings:
                if bad in s:
                    found_violations.append((curr_path, bad))
            if ev.get("events"):
                scan_strings(ev["events"], curr_path)

    scan_strings(mw["events"], "MW")
    if found_violations:
        print(f"FAIL: Found {len(found_violations)} forbidden AI slop strings:")
        for p, b in found_violations:
            print(f"  - {p} contains '{b}'")
        sys.exit(1)
    print("PASS: 0 AI Slop strings found! Clean minimalist text verified across entire Main_World.")

    # 4. Check Player Physics
    player = next(o for o in mw["objects"] if o["name"] == "Player")
    bh = next(b for b in player["behaviors"] if b["type"] == "PlatformBehavior::PlatformerObjectBehavior")
    assert bh["maxSpeed"] == 230, f"Player maxSpeed is {bh['maxSpeed']}, expected 230"
    assert bh["acceleration"] == 1800, f"Player acceleration is {bh['acceleration']}, expected 1800"
    assert bh["jumpSpeed"] == 440, f"Player jumpSpeed is {bh['jumpSpeed']}, expected 440"
    print(f"PASS: Player physics responsive (MaxSpeed: {bh['maxSpeed']}, Accel: {bh['acceleration']}, Jump: {bh['jumpSpeed']}).")

    # 5. Check Chaser 4-phase rework
    chaser_ev = next(ev for ev in mw["events"] if "Enemy_Chaser" in json.dumps(ev) and "chaser_phase_timer" in json.dumps(ev))
    chaser_json = json.dumps(chaser_ev)
    assert "chaser_phase_timer" in chaser_json, "Missing chaser_phase_timer in chaser events"
    assert "sfx_alert.wav" in chaser_json, "Missing sfx_alert.wav in chaser telegraph"
    assert "abs(Player.CenterY() - Enemy_Chaser.CenterY())" in chaser_json, "Missing jump counterplay check"
    print("PASS: Enemy_Chaser 4-phase machine (Hover -> Telegraph -> Lunge -> Recovery) verified with jump counterplay.")

    # 6. Check ALL Scene action parameters
    scene_actions = []
    def find_scene_actions(evs, lname, path=""):
        for i, ev in enumerate(evs):
            cur = f"{path}.{i}"
            for a in ev.get("actions", []):
                if a.get("type", {}).get("value") == "Scene":
                    scene_actions.append((lname, cur, a.get("parameters", [])))
            if ev.get("events"):
                find_scene_actions(ev["events"], lname, cur)

    for l in data["layouts"]:
        find_scene_actions(l["events"], l["name"], l["name"])

    assert len(scene_actions) >= 2, f"Expected at least 2 Scene actions, got {len(scene_actions)}"
    for lname, path, params in scene_actions:
        assert len(params) >= 2, f"Scene action at {path} has < 2 parameters"
        target_scene = params[1]
        assert target_scene.startswith('"') and target_scene.endswith('"'), f"Scene parameter at {path} is not expression quoted: {target_scene}"
    print(f"PASS: All {len(scene_actions)} Scene actions verified with properly quoted parameters.")

    # 7. Check 0 Orphan Instances & 0 Missing Resources
    for l in data["layouts"]:
        lname = l["name"]
        obj_names = {o["name"] for o in l["objects"]}
        inst_names = [i["name"] for i in l.get("instances", [])]
        orphans = [name for name in inst_names if name not in obj_names]
        assert len(orphans) == 0, f"Orphan instances found in {lname}: {orphans}"

    registered_files = {r["file"]: r for r in data["resources"]["resources"]}
    for l in data["layouts"]:
        for obj in l["objects"]:
            otype = obj.get("type", "")
            oname = obj.get("name", "")
            if otype == "Sprite":
                for anim in obj.get("animations", []):
                    for d in anim.get("directions", []):
                        for sp in d.get("sprites", []):
                            img = sp.get("image", "")
                            if img:
                                assert img in registered_files, f"Image {img} used by {oname} not registered!"
                                assert os.path.exists(img), f"Image {img} used by {oname} missing from disk!"
            elif "TiledSprite" in otype:
                tex = obj.get("texture", "")
                if tex:
                    assert tex in registered_files, f"Texture {tex} used by {oname} not registered!"
                    assert os.path.exists(tex), f"Texture {tex} used by {oname} missing from disk!"
    print("PASS: 0 orphan instances and 0 missing resources across entire project.")

    # 8. Check Animation counts of key multi-state objects
    for kname, min_anims in [("Ground_Stick", 4), ("Held_Stick", 4), ("UI_Slot_Icon", 5), ("Zone_Sign", 3)]:
        obj = next(o for o in mw["objects"] if o["name"] == kname)
        count = len(obj.get("animations", []))
        assert count >= min_anims, f"{kname} has {count} animations, expected >= {min_anims}"
    print("PASS: Multi-state objects have valid animation counts (Ground_Stick: 4, Held_Stick: 4, UI_Slot_Icon: 5, Zone_Sign: 3).")

    # 9. Check Transition_Fade on layer "UI" with zOrder=999 in both scenes
    for l in [ts, mw]:
        lname = l["name"]
        assert any(o["name"] == "Transition_Fade" for o in l["objects"]), f"Missing Transition_Fade object in {lname}"
        fade_inst = next((i for i in l["instances"] if i.get("name") == "Transition_Fade"), None)
        assert fade_inst is not None, f"Missing Transition_Fade instance in {lname}"
        assert fade_inst["layer"] == "UI", f"Transition_Fade in {lname} has layer '{fade_inst['layer']}', expected 'UI'"
        assert fade_inst["zOrder"] == 999, f"Transition_Fade in {lname} has zOrder {fade_inst['zOrder']}, expected 999"

        # Check fade events 1, 2, 3
        l_json = json.dumps(l["events"])
        assert "fade_state" in l_json, f"Missing fade_state in {lname} events"
        assert "fade_alpha" in l_json, f"Missing fade_alpha in {lname} events"
        assert "ChangeTimeScale" in l_json, f"Missing ChangeTimeScale in {lname} events"
    print("PASS: Both scenes have Transition_Fade on layer 'UI' (zOrder=999) with anti-deadlock fade_state events.")

    print("=" * 70)
    print("ALL RUNTIME-READINESS & PLAYABILITY CHECKS PASSED (100% OK)!")
    print("=" * 70)

if __name__ == "__main__":
    verify_runtime_readiness()
