import json
import os

PROJECT_PATH = "StickScavenger.json"

def diagnose():
    print("=" * 70)
    print("DIAGNOSIS OF 6 CRITICAL RUNTIME BOTTLENECKS")
    print("=" * 70)

    with open(PROJECT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. firstLayout & layouts order
    first_layout = data.get("firstLayout")
    layout_names = [l["name"] for l in data.get("layouts", [])]
    print(f"[Point 1] firstLayout = '{first_layout}', Layouts in project = {layout_names}")
    if first_layout != "Title_Screen":
        print("  --> ISSUE: firstLayout is NOT 'Title_Screen'!")
    else:
        print("  --> OK: firstLayout is 'Title_Screen'.")

    # 2. Check all Scene actions
    print("\n[Point 2] Checking 'Scene' action parameters across all layouts:")
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

    for lname, path, params in scene_actions:
        print(f"  Layout '{lname}' at {path}: params = {params}")
        if len(params) > 1:
            p1 = params[1]
            if not (p1.startswith('"') and p1.endswith('"')):
                print(f"  --> ISSUE: Scene name parameter is raw '{p1}', NOT wrapped in expression quotes!")
            else:
                print(f"  --> OK: Scene param {p1} is properly quoted.")

    # 3. Check Title_Screen transition and events
    print("\n[Point 3] Checking Title_Screen transition & time scale logic:")
    ts = next(l for l in data["layouts"] if l["name"] == "Title_Screen")
    print(f"  Total events in Title_Screen: {len(ts['events'])}")
    for i, ev in enumerate(ts["events"]):
        cond_types = [c.get("type", {}).get("value") for c in ev.get("conditions", [])]
        act_types = [a.get("type", {}).get("value") for a in ev.get("actions", [])]
        print(f"  Event #{i}: Conds={cond_types}, Acts={act_types}, SubEvents={len(ev.get('events', []))}")
        # check if ChangeTimeScale is used
        for a in ev.get("actions", []):
            if a.get("type", {}).get("value") == "ChangeTimeScale":
                print(f"    WARNING: ChangeTimeScale in Title_Screen: {a.get('parameters')}")

    # 4. Check orphan instances
    print("\n[Point 4] Checking orphan instances in layouts:")
    for l in data["layouts"]:
        lname = l["name"]
        obj_names = {o["name"] for o in l["objects"]}
        inst_names = [i["name"] for i in l.get("instances", [])]
        orphans = [name for name in inst_names if name not in obj_names]
        print(f"  Layout '{lname}': {len(obj_names)} objects, {len(inst_names)} instances. Orphans: {len(orphans)}")
        if orphans:
            print(f"  --> ISSUE: Orphan instances in '{lname}': {set(orphans)}")
        else:
            print(f"  --> OK: 0 orphan instances in '{lname}'.")

    # 5. Check images & textures in resources and on disk
    print("\n[Point 5] Checking Sprite images & TiledSprite textures vs resources and disk:")
    registered_files = {r["file"]: r for r in data["resources"]["resources"]}
    missing_on_disk = []
    missing_in_res = []

    for l in data["layouts"]:
        for obj in l["objects"]:
            otype = obj.get("type", "")
            oname = obj.get("name", "")
            if otype == "Sprite":
                for a_idx, anim in enumerate(obj.get("animations", [])):
                    for d_idx, d in enumerate(anim.get("directions", [])):
                        for s_idx, sp in enumerate(d.get("sprites", [])):
                            img = sp.get("image", "")
                            if img:
                                if img not in registered_files:
                                    missing_in_res.append((oname, img))
                                if not os.path.exists(img):
                                    missing_on_disk.append((oname, img))
            elif "TiledSprite" in otype:
                tex = obj.get("texture", "")
                if tex:
                    if tex not in registered_files:
                        missing_in_res.append((oname, tex))
                    if not os.path.exists(tex):
                        missing_on_disk.append((oname, tex))

    print(f"  Missing in resources: {len(missing_in_res)}")
    for o, f in missing_in_res:
        print(f"    --> ISSUE: {o} uses '{f}' which is not in resources!")
    print(f"  Missing on disk: {len(missing_on_disk)}")
    for o, f in missing_on_disk:
        print(f"    --> ISSUE: {o} uses '{f}' which does not exist on disk!")
    if not missing_in_res and not missing_on_disk:
        print("  --> OK: All images and textures exist in resources and physically on disk.")

    # 6. Check animations of Ground_Stick, Held_Stick, UI_Slot_Icon, Zone_Sign
    print("\n[Point 6] Checking animation counts of key multi-state objects:")
    mw = next(l for l in data["layouts"] if l["name"] == "Main_World")
    key_objs = ["Ground_Stick", "Held_Stick", "UI_Slot_Icon", "Zone_Sign"]
    for kname in key_objs:
        obj = next((o for o in mw["objects"] if o["name"] == kname), None)
        if not obj:
            print(f"  --> ISSUE: Object '{kname}' NOT found in Main_World!")
            continue
        anims = obj.get("animations", [])
        print(f"  Object '{kname}': {len(anims)} animations defined:")
        for ai, anim in enumerate(anims):
            dirs = anim.get("directions", [])
            sprites = dirs[0].get("sprites", []) if dirs else []
            print(f"    Anim #{ai} ('{anim.get('name')}'): {len(sprites)} sprite(s) -> image: {sprites[0].get('image') if sprites else 'NONE'}")

    print("=" * 70)

if __name__ == "__main__":
    diagnose()
