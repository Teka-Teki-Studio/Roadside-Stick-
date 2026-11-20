import json
import os
import sys

import json
import os
import sys

def verify():
    backup_path = "StickScavenger_sprint1_backup.json"
    if not os.path.exists(backup_path):
        print(f"FAIL: Backup file {backup_path} does not exist.")
        sys.exit(1)
    with open(backup_path, "r", encoding="utf-8") as f:
        json.load(f)
    print("PASS: StickScavenger_sprint1_backup.json exists and is valid.")

    balance_path = "data/game_balance.json"
    if not os.path.exists(balance_path):
        print(f"FAIL: {balance_path} does not exist.")
        sys.exit(1)
    with open(balance_path, "r", encoding="utf-8") as f:
        balance = json.load(f)
    assert balance.get("chunk_width") == 640
    assert balance.get("safe_zone_x") == 160
    assert "sticks" in balance and "zones" in balance
    print("PASS: data/game_balance.json exists and conforms to spec.")

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

    props = data.get("properties", {})
    assert props.get("windowWidth") == 640
    assert props.get("windowHeight") == 360
    assert props.get("scaleMode") == "nearest"
    assert props.get("pixelsRounding") is True
    print("PASS: Global properties match (640x360, scaleMode='nearest', pixelsRounding=True).")

    resources = data.get("resources", {}).get("resources", [])
    assert len(resources) >= 30, f"Expected at least 30 resources, found {len(resources)}"
    for r in resources:
        fpath = r.get("file", "")
        assert os.path.exists(fpath), f"Missing file: {fpath}"
        assert r.get("smoothed") is False, f"Resource {fpath} is smoothed: true"
    print(f"PASS: All {len(resources)} registered resources exist physically and have smoothed: false.")

    layouts = data.get("layouts", [])
    assert len(layouts) >= 1
    main_world = next((l for l in layouts if l.get("name") == "Main_World"), None)
    assert main_world is not None
    print("PASS: Layout Main_World found.")

    layers = [ly.get("name") for ly in main_world.get("layers", [])]
    expected_layers = [
        "Parallax_L0", "Parallax_L1", "Parallax_L2", "Parallax_L3",
        "", "Foreground_L5", "UI"
    ]
    for el in expected_layers:
        assert el in layers, f"Missing layer: {el}"
    print(f"PASS: All 7 required layers present: {layers}")

    required_objects = [
        "Ground_Floor", "Wall_Left", "Home_Base", "Player", "Held_Stick", "Ground_Stick",
        "Bg_L0_Sky", "Bg_L1_Far", "Bg_L2_Mid", "Bg_L3_Near", "Fg_L5_Overlay",
        "Zone_Tint_Overlay", "UI_Slot_Frame", "UI_Slot_Icon", "Zone_Sign",
        "Txt_Interact", "Txt_HUD", "Txt_Slot_Label", "Txt_Zone_Banner", "Txt_Floating_Gain"
    ]
    scene_objects = {obj.get("name"): obj for obj in main_world.get("objects", [])}
    for ro in required_objects:
        assert ro in scene_objects, f"Missing object: {ro}"

    tiled_objects = [
        "Bg_L0_Sky", "Bg_L1_Far", "Bg_L2_Mid", "Bg_L3_Near",
        "Fg_L5_Overlay", "Zone_Tint_Overlay", "Ground_Floor", "Wall_Left"
    ]
    for to in tiled_objects:
        obj = scene_objects[to]
        assert obj.get("type") == "TiledSpriteObject::TiledSprite", f"{to} is not TiledSprite"
        assert "animations" not in obj, f"{to} has invalid 'animations' array"
        assert "texture" in obj, f"{to} missing 'texture'"
        assert "width" in obj and "height" in obj, f"{to} missing width/height"
    print(f"PASS: All {len(required_objects)} required objects are defined with valid TiledSprite schemas.")

    events = main_world.get("events", [])
    assert len(events) > 0

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
    print(f"PASS: Audited {total_events} events and sub-events. 100% Standard, 0 CompareTimer conditions.")

    print("\nALL SPRINT 2 VERIFICATION CHECKS PASSED (100% OK)!")

if __name__ == "__main__":
    verify()
