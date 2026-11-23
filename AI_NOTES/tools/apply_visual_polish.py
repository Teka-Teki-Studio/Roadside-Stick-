"""
apply_visual_polish.py  v3
Patch game.json untuk:
1. Boot: logo HD (884x198), camera shake saat logo muncul (parameter SetCameraX valid)
2. Loading: ganti bg -> DraftLoadingPXFix.png, tambah music bgm_loading.mp3
3. Lobby: Robi idle 10 frame 128x128, skala 384x384 di instance,
          music bgm_menu.mp3, VFX pulse + breathe effect (TimeFromStart())
"""
import json, os

PROJECT = r"c:\Users\DELL\Downloads\Proffesionalsss\TTS\Roadside-Stick-\game.json"

with open(PROJECT, 'r', encoding='utf-8') as f:
    g = json.load(f)

# ===========================================================
# RESOURCES - register new files
# ===========================================================
existing_res = {r['name'] for r in g['resources']['resources']}

def add_resource(name, file_path, kind='image'):
    if name not in existing_res:
        entry = {
            "alwaysLoaded": False,
            "file": file_path,
            "kind": kind,
            "metadata": "",
            "name": name,
            "userAdded": True
        }
        if kind == 'image':
            entry["smoothed"] = False
        g['resources']['resources'].append(entry)
        existing_res.add(name)
        print(f"  + Resource: {name}")

# Loading BG baru
add_resource("DraftLoadingPXFix.png", "ASSETS/BOOT/LOADING/DraftLoadingPXFix.png", "image")

# 10 idle frames (128x128 each)
for i in range(10):
    add_resource(f"robi_idle_{i:02d}.png",
                 f"ASSETS/CHARACTER/PLAYER/idle_frames/robi_idle_{i:02d}.png", "image")

# Audio
add_resource("bgm_loading.mp3", "ASSETS/AUDIO/bgm_loading.mp3", "audio")
add_resource("bgm_menu.mp3",    "ASSETS/AUDIO/bgm_menu.mp3",    "audio")

print(f"Resources total: {len(g['resources']['resources'])}")


# ===========================================================
# BOOT SCENE
# ===========================================================
for sc in g['layouts']:
    if sc['name'] != 'Boot':
        continue

    # 1. Scale-up logo instance: 884x198, centered 1024x576
    for inst in sc.get('instances', []):
        if inst.get('name') == 'Spr_BootLogo':
            inst['x'] = 70
            inst['y'] = 189
            inst['width']  = 884
            inst['height'] = 198
            inst['customSize'] = True
            print(f"Boot logo: positioned at ({inst['x']},{inst['y']}) size {inst['width']}x{inst['height']}")

    # 2. Camera shake events: oscillate camera X while BootTimer in [1.05 .. 1.25]
    boot_events = sc.get('events', [])
    for ev in boot_events:
        if ev.get('type') == 'BuiltinCommonInstructions::Group':
            # Remove any existing shake sub-events first to stay clean
            ev['events'] = [sub for sub in ev.get('events', []) 
                            if not any(a.get('type', {}).get('value') == 'SetCameraX' 
                                       for a in sub.get('actions', []))]
            
            subs = ev.get('events', [])
            shake_ev = {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {"type": {"value": "VarScene"}, "parameters": ["BootTimer", ">", "1.05"]},
                    {"type": {"value": "VarScene"}, "parameters": ["BootTimer", "<", "1.25"]}
                ],
                "actions": [
                    # SetCameraX: [currentScene="", operator="=", value, layer="\"\"", camera="0"]
                    {"type": {"value": "SetCameraX"},
                     "parameters": ["", "=", "512 + 4 * sin(Variable(BootTimer) * 60)", "\"\"", "0"]}
                ]
            }
            reset_cam = {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {"type": {"value": "VarScene"}, "parameters": ["BootTimer", ">=", "1.25"]}
                ],
                "actions": [
                    {"type": {"value": "SetCameraX"},
                     "parameters": ["", "=", "512", "\"\"", "0"]}
                ]
            }
            insert_at = max(0, len(subs) - 1)
            subs.insert(insert_at, shake_ev)
            subs.insert(insert_at + 1, reset_cam)
            print("Boot: camera shake events added")
            break

    sc['events'] = boot_events
    print("Boot scene patched!")


# ===========================================================
# LOADING SCENE
# ===========================================================
for sc in g['layouts']:
    if sc['name'] != 'Loading':
        continue

    # 1. Update Spr_LoadingBg image -> DraftLoadingPXFix.png
    for obj in sc.get('objects', []):
        if obj.get('name') == 'Spr_LoadingBg':
            for anim in obj.get('animations', []):
                for d in anim.get('directions', []):
                    for spr in d.get('sprites', []):
                        spr['image'] = 'DraftLoadingPXFix.png'
                        print("Loading BG image -> DraftLoadingPXFix.png")

    # 2. Instance size 1024x576
    for inst in sc.get('instances', []):
        if inst.get('name') == 'Spr_LoadingBg':
            inst['width']  = 1024
            inst['height'] = 576
            inst['customSize'] = True

    # 3. Add PlayMusicOnChannel on scene start
    music_added = False
    for ev in sc.get('events', []):
        if ev.get('type') == 'BuiltinCommonInstructions::Group' and not music_added:
            for sub in ev.get('events', []):
                if sub.get('type') != 'BuiltinCommonInstructions::Standard':
                    continue
                conds = sub.get('conditions', [])
                if any(c.get('type', {}).get('value') == 'DepartScene' for c in conds):
                    # Clean previous music actions first
                    sub['actions'] = [a for a in sub.get('actions', [])
                                      if a.get('type', {}).get('value') != 'PlayMusicOnChannel']
                    sub['actions'].insert(0, {
                        "type": {"value": "PlayMusicOnChannel"},
                        "parameters": ["", "bgm_loading.mp3", "1", "yes", "60", "1"]
                    })
                    print("Loading: bgm_loading.mp3 PlayMusicOnChannel added")
                    music_added = True
                    break
            if music_added:
                break

    print("Loading scene patched!")


# ===========================================================
# LOBBY SCENE - Robi idle 10 frames + Music + VFX
# ===========================================================
for sc in g['layouts']:
    if sc['name'] != 'Lobby':
        continue

    # 1. Update Spr_PlayerLobby animation -> 10 frames 128x128
    for obj in sc.get('objects', []):
        if obj.get('name') == 'Spr_PlayerLobby':
            sprites = []
            for i in range(10):
                sprites.append({
                    "hasCustomCollisionMask": False,
                    "customCollisionMask": [],
                    "image": f"robi_idle_{i:02d}.png",
                    "points": [],
                    "originPoint": {"name": "origine", "x": 0, "y": 0},
                    "centerPoint": {"automatic": True, "name": "centre", "x": 64, "y": 64}
                })
            obj['animations'] = [{
                "name": "Idle",
                "useMultipleDirections": False,
                "directions": [{
                    "looping": True,
                    "timeBetweenFrames": 0.12,
                    "sprites": sprites
                }]
            }]
            print("Lobby: Spr_PlayerLobby 10 idle frames (128x128, 0.12s, looping)")

    # 2. Update instance: Robi portrait (waist-up) di kiri bawah layar
    for inst in sc.get('instances', []):
        if inst.get('name') == 'Spr_PlayerLobby':
            inst['x'] = 48
            inst['y'] = 190
            inst['width']  = 384
            inst['height'] = 384
            inst['customSize'] = True
            print(f"Lobby Robi instance: pos ({inst['x']},{inst['y']}) size {inst['width']}x{inst['height']}")

    # 3. Music on scene start
    music_added = False
    for ev in sc.get('events', []):
        if ev.get('type') == 'BuiltinCommonInstructions::Group' and not music_added:
            for sub in ev.get('events', []):
                if sub.get('type') != 'BuiltinCommonInstructions::Standard':
                    continue
                conds = sub.get('conditions', [])
                if any(c.get('type', {}).get('value') == 'DepartScene' for c in conds):
                    # Remove older audio actions
                    sub['actions'] = [a for a in sub.get('actions', [])
                                      if a.get('type', {}).get('value') not in ('StopMusicChannel', 'PlayMusicOnChannel')]
                    sub['actions'].insert(0, {
                        "type": {"value": "StopMusicChannel"},
                        "parameters": ["", "1"]
                    })
                    sub['actions'].insert(1, {
                        "type": {"value": "PlayMusicOnChannel"},
                        "parameters": ["", "bgm_menu.mp3", "1", "yes", "75", "1"]
                    })
                    print("Lobby: bgm_menu.mp3 on start added")
                    music_added = True
                    break
            if music_added:
                break

    # 4. VFX group - remove previous VFX group if present and re-add cleanly
    lobby_events = [ev for ev in sc.get('events', [])
                    if ev.get('title') != '[T3] Lobby — VFX & Efek Hidup']

    vfx_group = {
        "type": "BuiltinCommonInstructions::Group",
        "title": "[T3] Lobby — VFX & Efek Hidup",
        "parameters": [""],
        "events": [
            # Player breathe: subtle oscillation with TimeFromStart()
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [],
                "actions": [
                    {
                        "type": {"value": "SetX"},
                        "parameters": ["Spr_PlayerLobby", "=", "48 + 3 * sin(TimeFromStart() * 1.5)"]
                    },
                    {
                        "type": {"value": "SetY"},
                        "parameters": ["Spr_PlayerLobby", "=", "190 + 2 * sin(TimeFromStart() * 2.0)"]
                    }
                ]
            },
            # Play button subtle opacity pulse (220..255)
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [],
                "actions": [
                    {
                        "type": {"value": "ChangeOpacity"},
                        "parameters": ["Btn_Play", "=", "220 + 35 * sin(TimeFromStart() * 2.5)"]
                    }
                ]
            }
        ]
    }
    lobby_events.append(vfx_group)
    sc['events'] = lobby_events
    print("Lobby: VFX events updated cleanly (TimeFromStart)")
    print("Lobby scene patched!")


# ===========================================================
# WRITE BACK
# ===========================================================
with open(PROJECT, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print("\nAll patches applied cleanly to game.json!")
