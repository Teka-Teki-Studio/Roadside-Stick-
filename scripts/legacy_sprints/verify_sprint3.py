import json
import os
import sys

def verify_sprint3():
    # 1. Backup file check
    backup_path = "StickScavenger_sprint2_backup.json"
    if not os.path.exists(backup_path):
        print(f"FAIL: Backup file {backup_path} does not exist.")
        sys.exit(1)
    with open(backup_path, "r", encoding="utf-8") as f:
        json.load(f)
    print("PASS: StickScavenger_sprint2_backup.json exists and is valid JSON.")

    # 2. game_balance.json check
    balance_path = "data/game_balance.json"
    if not os.path.exists(balance_path):
        print(f"FAIL: {balance_path} does not exist.")
        sys.exit(1)
    with open(balance_path, "r", encoding="utf-8") as f:
        balance = json.load(f)

    # Sprint 2 keys
    assert balance.get("chunk_width") == 640
    assert balance.get("safe_zone_x") == 160
    assert "sticks" in balance and "zones" in balance
    # Sprint 3 keys
    assert "player_combat" in balance
    assert balance["player_combat"]["stagger_duration"] == 0.70
    assert balance["player_combat"]["invuln_duration"] == 1.60
    assert balance["player_combat"]["knockback_speed_x"] == -135
    assert balance["player_combat"]["emergency_drop_cooldown"] == 0.30
    assert "hazards" in balance
    assert balance["hazards"]["bramble_slow_multiplier"] in [0.55, 0.65]
    assert "enemies" in balance
    assert balance["enemies"]["safe_barrier_x"] == 180
    assert "thief" in balance["enemies"] and "chaser" in balance["enemies"]
    print("PASS: data/game_balance.json contains all Sprint 2 and Sprint 3 configurations.")

    # 3. StickScavenger.json validation
    project_path = "StickScavenger.json"
    if not os.path.exists(project_path):
        print(f"FAIL: {project_path} does not exist.")
        sys.exit(1)

    try:
        with open(project_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("PASS: StickScavenger.json is valid JSON.")
    except Exception as e:
        print(f"FAIL: JSON parse error: {e}")
        sys.exit(1)

    # Global properties
    props = data.get("properties", {})
    assert props.get("windowWidth") == 640
    assert props.get("windowHeight") == 360
    assert props.get("scaleMode") == "nearest"
    assert props.get("pixelsRounding") is True
    print("PASS: Global properties match (640x360, scaleMode='nearest', pixelsRounding=True).")

    # Resources check
    resources = data.get("resources", {}).get("resources", [])
    assert len(resources) >= 50, f"Expected at least 50 resources, found {len(resources)}"
    for r in resources:
        fpath = r.get("file", "")
        assert os.path.exists(fpath), f"Missing file: {fpath}"
        assert r.get("smoothed") is False, f"Resource {fpath} has smoothed: True"
    print(f"PASS: All {len(resources)} registered resources exist physically and have smoothed: false.")

    # Layout check
    layouts = data.get("layouts", [])
    assert len(layouts) >= 1
    main_world = next((l for l in layouts if l.get("name") == "Main_World"), None)
    assert main_world is not None
    print("PASS: Layout Main_World found.")

    # Layers check
    layers = [ly.get("name") for ly in main_world.get("layers", [])]
    expected_layers = [
        "Parallax_L0", "Parallax_L1", "Parallax_L2", "Parallax_L3",
        "", "Foreground_L5", "UI"
    ]
    for el in expected_layers:
        assert el in layers, f"Missing layer: {el}"
    assert len(layers) == 7, f"Expected exactly 7 layers, found {len(layers)}"
    print(f"PASS: Exactly 7 required layers present: {layers}")

    # Objects check (20 from Sprint 2 + 8 from Sprint 3 = 28 objects)
    sprint2_objects = [
        "Ground_Floor", "Wall_Left", "Home_Base", "Player", "Held_Stick", "Ground_Stick",
        "Bg_L0_Sky", "Bg_L1_Far", "Bg_L2_Mid", "Bg_L3_Near", "Fg_L5_Overlay",
        "Zone_Tint_Overlay", "UI_Slot_Frame", "UI_Slot_Icon", "Zone_Sign",
        "Txt_Interact", "Txt_HUD", "Txt_Slot_Label", "Txt_Zone_Banner", "Txt_Floating_Gain"
    ]
    sprint3_objects = [
        "Hazard_Bramble", "Safe_Barrier", "Enemy_Thief", "Enemy_Chaser",
        "UI_Alert_Indicator", "Alert_Vignette", "Txt_Warning_Banner", "Txt_Combat_Feedback"
    ]
    scene_objects = {obj.get("name"): obj for obj in main_world.get("objects", [])}
    for ro in sprint2_objects + sprint3_objects:
        assert ro in scene_objects, f"Missing object: {ro}"
    print(f"PASS: All {len(sprint2_objects)} Sprint 2 objects and {len(sprint3_objects)} Sprint 3 objects are present (Total: {len(scene_objects)}).")

    # TiledSprite schemas check
    tiled_objects = [
        "Bg_L0_Sky", "Bg_L1_Far", "Bg_L2_Mid", "Bg_L3_Near",
        "Fg_L5_Overlay", "Zone_Tint_Overlay", "Ground_Floor", "Wall_Left", "Alert_Vignette"
    ]
    for to in tiled_objects:
        obj = scene_objects[to]
        assert obj.get("type") == "TiledSpriteObject::TiledSprite", f"{to} is not TiledSprite"
        assert "animations" not in obj, f"{to} has invalid 'animations' array"
        assert "texture" in obj, f"{to} missing 'texture'"
        assert "width" in obj and "height" in obj, f"{to} missing width/height"
    print(f"PASS: All {len(tiled_objects)} TiledSprite objects have 100% valid schemas.")

    # Scene variables check
    vars_dict = {v["name"]: v for v in main_world.get("variables", [])}
    required_sprint3_vars = [
        "stagger_timer", "invuln_timer", "shake_timer", "thief_flee_timer",
        "thief_stun_timer", "chaser_telegraph_timer", "chaser_cooldown",
        "alert_pulse_time", "warning_timer", "barrier_flash_timer",
        "alert_level", "thief_state", "chaser_state", "stolen_tier",
        "stolen_value", "is_slowed", "emergency_drop_cooldown", "combat_feedback_timer"
    ]
    for rv in required_sprint3_vars:
        assert rv in vars_dict, f"Missing scene variable: {rv}"
        assert vars_dict[rv].get("type") == "number", f"Variable {rv} must be type 'number'"
        assert isinstance(vars_dict[rv].get("value"), (int, float)), f"Variable {rv} must have numeric initial value"
    print(f"PASS: All {len(required_sprint3_vars)} Sprint 3 state and timer variables are pure numbers.")

    # Events audit
    events = main_world.get("events", [])
    assert len(events) >= 15

    total_events = 0
    compare_timer_count = 0

    def check_event(ev):
        nonlocal total_events, compare_timer_count
        total_events += 1
        assert ev.get("type") == "BuiltinCommonInstructions::Standard"
        assert ev.get("disabled") is False
        assert ev.get("folded") is False
        assert isinstance(ev.get("conditions"), list)
        assert isinstance(ev.get("actions"), list)
        assert isinstance(ev.get("events"), list)

        for cond in ev["conditions"]:
            val = cond.get("type", {}).get("value", "")
            if val == "CompareTimer":
                compare_timer_count += 1
            if "subInstructions" in cond:
                for sub_c in cond["subInstructions"]:
                    if sub_c.get("type", {}).get("value", "") == "CompareTimer":
                        compare_timer_count += 1

        for sub_ev in ev["events"]:
            check_event(sub_ev)

    for ev in events:
        check_event(ev)

    assert compare_timer_count == 0, f"Found {compare_timer_count} CompareTimer conditions!"
    print(f"PASS: Audited {total_events} events and sub-events. 100% Standard structure, 0 CompareTimer conditions.")

    print("\nALL SPRINT 3 VERIFICATION CHECKS PASSED (100% OK)!")

if __name__ == "__main__":
    verify_sprint3()
