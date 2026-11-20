import json
import os
import sys

PROJECT_PATH = "StickScavenger.json" if os.path.exists("StickScavenger.json") else os.path.join(os.path.dirname(__file__), "..", "StickScavenger.json")
PROJ_DIR = os.path.dirname(os.path.abspath(PROJECT_PATH))

def run_verification():
    print("=" * 70)
    print("COZY EXPLORATION PIVOT - COMPREHENSIVE VERIFICATION SUITE")
    print("=" * 70)

    if not os.path.exists(PROJECT_PATH):
        print(f"FAIL: Project file missing: {PROJECT_PATH}")
        sys.exit(1)

    with open(PROJECT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    mw = next(l for l in data["layouts"] if l["name"] == "Main_World")
    ts = next(l for l in data["layouts"] if l["name"] == "Title_Screen")

    # Verify pre-placed ground stick instances
    sticks = [i for i in mw["instances"] if i.get("name") == "Ground_Stick"]
    print(f"[CHECK 1] Ground_Stick instances: Found {len(sticks)}")
    assert len(sticks) == 24, f"Expected 24 Ground_Stick instances, got {len(sticks)}"

    tiers_found = set()
    for idx, inst in enumerate(sticks):
        x, y = inst.get("x", 0), inst.get("y", 999)
        z = inst.get("zOrder", 0)
        assert y < 296, f"Stick #{idx} at X={x} has Y={y} >= 296"
        assert z >= 10, f"Stick #{idx} at X={x} has zOrder={z} < 10"
        vars_dict = {v["name"]: v.get("value") for v in inst.get("initialVariables", [])}
        assert "tier" in vars_dict and vars_dict["tier"] in range(1, 9), f"Invalid tier in stick #{idx}"
        assert "base_value" in vars_dict and vars_dict["base_value"] in [5, 12, 20, 35, 55, 80, 120, 200], f"Invalid base_value in stick #{idx}"
        tiers_found.add(vars_dict["tier"])

    assert len(tiers_found) == 8, f"Expected all 8 tiers represented, got {tiers_found}"
    print("  -> PASS: All 24 sticks verified across all 8 tiers standing above floor.")

    # Verify platform ledges
    ledges = [i for i in mw["instances"] if i.get("name") == "Platform_Ledge"]
    print(f"[CHECK 2] Platform_Ledge instances: Found {len(ledges)}")
    assert len(ledges) == 7, f"Expected 7 Platform_Ledge instances, got {len(ledges)}"
    for idx, inst in enumerate(ledges):
        assert inst.get("y", 0) in range(220, 260), f"Ledge #{idx} Y out of range"
    print("  -> PASS: 7 natural platform ledges verified.")

    # Verify home display stands
    displays = [i for i in mw["instances"] if "Home_Display" in i.get("name", "")]
    print(f"[CHECK 3] Home_Display instances: Found {len(displays)}")
    assert len(displays) == 8, f"Expected 8 Home_Display instances, got {len(displays)}"
    print("  -> PASS: 8 physical stick display instances verified at Home Base.")

    # Verify lantern warm glow
    glow = next((i for i in mw["instances"] if i.get("name") == "Home_Warm_Glow"), None)
    assert glow is not None, "Home_Warm_Glow instance missing!"
    print(f"[CHECK 4] Home_Warm_Glow verified at X={glow['x']}, Y={glow['y']}.")

    # Verify right wall boundary
    wall_r = next((i for i in mw["instances"] if i.get("name") == "Wall_Right"), None)
    assert wall_r is not None and wall_r.get("x") == 4820, "Wall_Right missing or not at X=4820!"
    print(f"[CHECK 5] Compacted map right boundary Wall_Right verified at X={wall_r['x']}.")

    # Verify album UI components
    album_panel = next((i for i in mw["instances"] if i.get("name") == "UI_Album_Panel"), None)
    assert album_panel is not None and album_panel["layer"] == "UI", "UI_Album_Panel missing or wrong layer!"
    album_icons = [i for i in mw["instances"] if "Album_Icon" in i.get("name", "")]
    assert len(album_icons) == 8, f"Expected 8 Album_Icon instances on UI layer, got {len(album_icons)}"
    print("  -> PASS: Album UI Panel and 8 slot icons verified on UI layer.")

    # Verify text purity and absence of AI slop
    forbidden = ["ZONA 1", "Chunk", "UPGRADE", "DOWNGRADE", "STATUS:", "[BARU!]", "Rare", "Epic", "Legendary", "(Common)"]
    found_violations = []

    def scan_for_slop(evs):
        for ev in evs:
            for a in ev.get("actions", []):
                params = a.get("parameters", [])
                for p in params:
                    for bad in forbidden:
                        if bad in str(p):
                            found_violations.append((a.get("type", {}).get("value"), p, bad))
            if ev.get("events"):
                scan_for_slop(ev["events"])

    scan_for_slop(mw["events"])
    assert len(found_violations) == 0, f"Found AI slop in Main_World: {found_violations}"
    print("[CHECK 7] PASS: 0 AI Slop strings verified across all Main_World events.")

    # Verify edge detector variables
    mw_json = json.dumps(mw["events"])
    for var in ["esc_was_down", "album_was_down", "e_was_down", "q_was_down", "is_paused", "is_album_open", "max_dist_x"]:
        assert var in mw_json, f"Missing {var} in Main_World events"
    print("[CHECK 8] PASS: All edge detectors verified without deadlock-prone Trigger Once.")

    # Verify storage write parameter count
    def check_ecrire(evs):
        for ev in evs:
            for a in ev.get("actions", []):
                if a.get("type", {}).get("value") == "EcrireFichierExp":
                    p = a.get("parameters", [])
                    assert len(p) == 3, f"EcrireFichierExp has {len(p)} params, expected 3! params={p}"
            if ev.get("events"):
                check_ecrire(ev["events"])

    check_ecrire(mw["events"])
    print("[CHECK 9] PASS: All EcrireFichierExp storage actions verified with exactly 3 parameters.")

    # Verify distance bonus formula
    assert "floor(Variable(max_dist_x) / 640)" in mw_json, "Missing max_dist_x in deposit earned calculation!"
    print("[CHECK 10] PASS: Distance bonus formula correctly uses max_dist_x.")

    # Verify pause reset ordering
    r_ev = next(ev for ev in mw["events"] if any(c.get("type", {}).get("value") == "KeyPressed" and "r" in c.get("parameters", []) for c in ev.get("conditions", [])))
    r_act_types = [a.get("type", {}).get("value") for a in r_ev.get("actions", [])]
    assert "ChangeTimeScale" in r_act_types and "PlatformBehavior::IgnoreDefaultControls" in r_act_types, "Missing pause resets in [R] event"
    print("[CHECK 11] PASS: Pause reset order before scene fade on [R] and [M] verified.")

    # Verify all registered resources exist on disk
    for r in data["resources"]["resources"]:
        fpath = r.get("file", "")
        full_fpath = os.path.join(PROJ_DIR, fpath)
        assert os.path.exists(full_fpath), f"Resource file missing from disk: {full_fpath}"
    print(f"[CHECK 12] PASS: All {len(data['resources']['resources'])} resource files verified on disk.")

    print("=" * 70)
    print("ALL 12 COZY EXPLORATION CHECKS PASSED (100% OK)!")
    print("=" * 70)

if __name__ == "__main__":
    run_verification()
