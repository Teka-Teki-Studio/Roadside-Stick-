"""Sprint 4 comprehensive verification script."""
import json
import os
import sys

def verify_sprint4():
    # 1. Backup check
    for bp in ["StickScavenger_sprint1_backup.json",
               "StickScavenger_sprint2_backup.json",
               "StickScavenger_sprint3_backup.json"]:
        assert os.path.exists(bp), f"FAIL: Missing backup {bp}"
        with open(bp, "r", encoding="utf-8") as f:
            json.load(f)
    print("PASS: All 3 sprint backup files exist and are valid JSON.")

    # 2. game_balance.json
    with open("data/game_balance.json", "r", encoding="utf-8") as f:
        balance = json.load(f)
    for k in ["chunk_width", "sticks", "zones", "player_combat", "hazards", "enemies", "juice", "audio"]:
        assert k in balance, f"Missing key: {k}"
    assert balance["juice"]["hitstop_rare_swap"] == 0.05
    assert balance["juice"]["foot_dust_lifetime"] == 0.24
    assert balance["audio"]["master_sfx_volume"] == 70
    assert balance["audio"]["step_sfx_interval"] == 0.24
    print("PASS: game_balance.json contains ALL Sprint 2/3/4 config blocks.")

    # 3. Project JSON validity
    with open("StickScavenger.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print("PASS: StickScavenger.json is valid JSON.")

    # 4. Global properties
    props = data["properties"]
    assert props["windowWidth"] == 640
    assert props["windowHeight"] == 360
    assert props["scaleMode"] == "nearest"
    assert props["pixelsRounding"] is True
    print("PASS: Global properties (640x360, nearest, pixelsRounding).")

    # 5. Resources — all files exist, all images smoothed=false
    resources = data["resources"]["resources"]
    img_res = [r for r in resources if r["kind"] == "image"]
    aud_res = [r for r in resources if r["kind"] == "audio"]
    assert len(img_res) >= 55, f"Expected >=55 image resources, got {len(img_res)}"
    assert len(aud_res) >= 10, f"Expected >=10 audio resources, got {len(aud_res)}"
    for r in resources:
        fp = r["file"]
        assert os.path.exists(fp), f"Missing resource file: {fp}"
        if r["kind"] == "image":
            assert r["smoothed"] is False, f"Image {fp} has smoothed:true"
    print(f"PASS: {len(img_res)} images (smoothed=false) + {len(aud_res)} audio files all exist.")

    # 6. Audio WAV validation
    expected_audio = [
        "sfx_pickup.wav", "sfx_drop.wav", "sfx_step.wav", "sfx_extraction.wav",
        "sfx_hit.wav", "sfx_alert.wav", "sfx_menu_select.wav", "sfx_pause.wav",
        "sfx_steal.wav", "sfx_recapture.wav"
    ]
    for aud in expected_audio:
        fp = f"assets/audio/{aud}"
        assert os.path.exists(fp), f"Missing audio: {fp}"
        assert os.path.getsize(fp) > 100, f"Audio file too small: {fp}"
    print(f"PASS: All {len(expected_audio)} chiptune SFX WAV files verified.")

    # 7. Layouts
    layout_names = [l["name"] for l in data["layouts"]]
    assert "Title_Screen" in layout_names, "Missing Title_Screen layout"
    assert "Main_World" in layout_names, "Missing Main_World layout"
    assert data["firstLayout"] == "Title_Screen"
    print(f"PASS: Layouts {layout_names}, firstLayout=Title_Screen.")

    # 8. Title_Screen validation
    ts = next(l for l in data["layouts"] if l["name"] == "Title_Screen")
    ts_obj_names = {o["name"] for o in ts["objects"]}
    for required in ["Title_Bg", "Title_Logo", "Menu_Cursor",
                     "Txt_Title_Start", "Txt_Title_High", "Txt_Title_Hint"]:
        assert required in ts_obj_names, f"Title_Screen missing object: {required}"
    # Verify Title_Bg is TiledSprite with no animations
    title_bg = next(o for o in ts["objects"] if o["name"] == "Title_Bg")
    assert title_bg["type"] == "TiledSpriteObject::TiledSprite"
    assert "animations" not in title_bg
    assert "texture" in title_bg
    print(f"PASS: Title_Screen has {len(ts_obj_names)} objects including all required.")

    # 9. Main_World — Sprint 1-3 preservation
    mw = next(l for l in data["layouts"] if l["name"] == "Main_World")
    layers = [ly["name"] for ly in mw["layers"]]
    expected_layers = ["Parallax_L0", "Parallax_L1", "Parallax_L2", "Parallax_L3",
                       "", "Foreground_L5", "UI"]
    assert layers == expected_layers, f"Layer mismatch: {layers}"
    print(f"PASS: Main_World has exactly 7 layers: {layers}")

    # Sprint 2 objects
    sprint2_objs = [
        "Ground_Floor", "Wall_Left", "Home_Base", "Player", "Held_Stick", "Ground_Stick",
        "Bg_L0_Sky", "Bg_L1_Far", "Bg_L2_Mid", "Bg_L3_Near", "Fg_L5_Overlay",
        "Zone_Tint_Overlay", "UI_Slot_Frame", "UI_Slot_Icon", "Zone_Sign",
        "Txt_Interact", "Txt_HUD", "Txt_Slot_Label", "Txt_Zone_Banner", "Txt_Floating_Gain"
    ]
    # Sprint 3 objects
    sprint3_objs = [
        "Hazard_Bramble", "Safe_Barrier", "Enemy_Thief", "Enemy_Chaser",
        "UI_Alert_Indicator", "Alert_Vignette", "Txt_Warning_Banner", "Txt_Combat_Feedback"
    ]
    # Sprint 4 objects
    sprint4_objs = [
        "Dust_Particle", "Glint_Sparkle", "Radar_Frame", "Radar_Dot",
        "Pause_Overlay", "Save_Icon", "Txt_Pause", "Txt_Pause_Sub", "Txt_Save_Toast"
    ]

    mw_obj_names = {o["name"] for o in mw["objects"]}
    for obj_list, label in [(sprint2_objs, "Sprint 2"), (sprint3_objs, "Sprint 3"),
                            (sprint4_objs, "Sprint 4")]:
        for name in obj_list:
            assert name in mw_obj_names, f"Missing {label} object: {name}"

    print(f"PASS: All {len(sprint2_objs)} S2 + {len(sprint3_objs)} S3 + {len(sprint4_objs)} S4 objects present (Total: {len(mw_obj_names)}).")

    # 10. TiledSprite schema validation
    tiled_names = ["Bg_L0_Sky", "Bg_L1_Far", "Bg_L2_Mid", "Bg_L3_Near",
                   "Fg_L5_Overlay", "Zone_Tint_Overlay", "Ground_Floor",
                   "Wall_Left", "Alert_Vignette", "Pause_Overlay"]
    for tn in tiled_names:
        obj = next(o for o in mw["objects"] if o["name"] == tn)
        assert obj["type"] == "TiledSpriteObject::TiledSprite", f"{tn} wrong type"
        assert "animations" not in obj, f"{tn} has illegal 'animations' key"
        assert "texture" in obj, f"{tn} missing 'texture'"
    print(f"PASS: All {len(tiled_names)} TiledSprite objects have valid schemas.")

    # 11. Sprint 4 variables
    var_dict = {v["name"]: v for v in mw["variables"]}
    sprint4_vars = [
        "is_paused", "pause_cooldown", "hitstop_timer", "dust_spawn_timer",
        "step_sfx_timer", "glint_pulse_time", "save_toast_timer",
        "menu_pulse_time", "high_score", "radar_player_px"
    ]
    for vn in sprint4_vars:
        assert vn in var_dict, f"Missing Sprint 4 variable: {vn}"
        assert var_dict[vn]["type"] == "number", f"{vn} not number type"
    print(f"PASS: All {len(sprint4_vars)} Sprint 4 variables are pure numbers.")

    # 12. Event audit — BOTH layouts
    total_events = 0
    compare_timer_count = 0

    def check_event(ev):
        nonlocal total_events, compare_timer_count
        total_events += 1
        assert ev.get("type") == "BuiltinCommonInstructions::Standard", \
            f"Event type is {ev.get('type')}"
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

    for layout in data["layouts"]:
        for ev in layout.get("events", []):
            check_event(ev)

    assert compare_timer_count == 0, f"Found {compare_timer_count} CompareTimer conditions!"
    print(f"PASS: Audited {total_events} total events across all layouts. "
          f"100% Standard structure, 0 CompareTimer.")

    # 13. Camera shake integration preserved
    camera_found = False
    def find_camera_shake(ev):
        nonlocal camera_found
        for act in ev.get("actions", []):
            params = act.get("parameters", [])
            for p in params:
                if isinstance(p, str) and "Variable(shake_x)" in p:
                    camera_found = True
                    return
        for sub in ev.get("events", []):
            find_camera_shake(sub)
    for ev in mw["events"]:
        find_camera_shake(ev)
    assert camera_found, "Camera shake integration (shake_x) not found!"
    print("PASS: Camera shake integration (shake_x/shake_y offset) preserved.")

    # 14. Audio resource registration
    audio_res_files = {r["file"] for r in resources if r["kind"] == "audio"}
    for aud in expected_audio:
        fp = f"assets/audio/{aud}"
        assert fp in audio_res_files, f"Audio {fp} not registered in resources"
    print(f"PASS: All {len(expected_audio)} audio files registered with kind='audio'.")

    print(f"\n{'='*60}")
    print("ALL SPRINT 4 VERIFICATION CHECKS PASSED (100% OK)!")
    print(f"{'='*60}")

if __name__ == "__main__":
    verify_sprint4()
