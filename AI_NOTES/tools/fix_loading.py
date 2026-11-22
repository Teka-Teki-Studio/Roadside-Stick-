"""
fix_loading.py
Patch scene Loading di game.json:
1. Ganti SetWidth -> ChangeWidth (action valid GDevelop 5.6)
2. Update instance bar ke 1080x12, terpusat di viewport 1024x576
3. Pindahkan Spr_LoadingIndicator ke kanan loading bar
4. Update instance fill dan teks
"""
import json, copy

PROJECT = r"c:\Users\DELL\Downloads\Proffesionalsss\TTS\Roadside-Stick-\game.json"

# ---- Layout constants ----
# Bar file di disk: 1090x22 (saat ini). User minta gaya 1080x12.
# Kita akan set instance WIDTH ke 1024 (full viewport) supaya bar penuh layar.
# Height sesuai file: kalau file 1090x22 kita pakai H=12 (ramping) via custom size.
# Kalau nanti user ganti file ke 1080x12, hanya perlu reopen GDevelop -- instance size sudah benar.

VIEWPORT_W = 1024
VIEWPORT_H = 576

BAR_W = 1080          # Lebar bar (sedikit lebih lebar dari viewport, center)
BAR_H = 12            # Tinggi ramping sesuai permintaan user
BAR_X = (VIEWPORT_W - BAR_W) // 2   # = -28, bar sedikit melebihi kiri-kanan
BAR_Y = 540           # Dekat bawah layar

# Fill: mulai dari pixel dalam bar (tidak ada inner margin pada aset frame sederhana)
FILL_X = BAR_X
FILL_Y = BAR_Y
FILL_H = BAR_H
FILL_MAX_W = BAR_W    # fill penuh = selebar bar

# Spinner (indicator): kanan bar + 10px gap, vertikal center dengan bar
SPINNER_SIZE = 24
SPINNER_X = BAR_X + BAR_W + 10        # = -28 + 1080 + 10 = 1062
SPINNER_Y = BAR_Y + (BAR_H - SPINNER_SIZE) // 2  # center vertikal = 540 + (12-24)//2 = 534

# Teks label "Loading..." di atas bar, kiri
TXT_LOADING_X = 32
TXT_LOADING_Y = BAR_Y - 32
TXT_LOADING_W = 400
TXT_LOADING_H = 28

# Persen di atas bar, kanan (sebelum spinner)
TXT_PCT_W = 80
TXT_PCT_H = 28
TXT_PCT_X = SPINNER_X - TXT_PCT_W - 8   # = 1062 - 80 - 8 = 974
TXT_PCT_Y = BAR_Y - 32

print(f"BAR: X={BAR_X} Y={BAR_Y} W={BAR_W} H={BAR_H}")
print(f"FILL: X={FILL_X} Y={FILL_Y} W=1(init) H={FILL_H} MAX_W={FILL_MAX_W}")
print(f"SPINNER: X={SPINNER_X} Y={SPINNER_Y} SIZE={SPINNER_SIZE}")
print(f"TXT_LOADING: X={TXT_LOADING_X} Y={TXT_LOADING_Y}")
print(f"TXT_PCT: X={TXT_PCT_X} Y={TXT_PCT_Y}")

# ---- Load game.json ----
with open(PROJECT, 'r', encoding='utf-8') as f:
    g = json.load(f)

# ---- Find Loading scene ----
loading_scene = None
for sc in g['layouts']:
    if sc['name'] == 'Loading':
        loading_scene = sc
        break

if loading_scene is None:
    print("ERROR: Scene Loading tidak ditemukan!")
    exit(1)

# ---- Patch instances ----
for inst in loading_scene.get('instances', []):
    n = inst.get('name', '')
    if n == 'Spr_LoadingBarFrame':
        inst['x'] = BAR_X
        inst['y'] = BAR_Y
        inst['width'] = BAR_W
        inst['height'] = BAR_H
        inst['customSize'] = True
        print(f"  Patched {n}: x={inst['x']} y={inst['y']} w={inst['width']} h={inst['height']}")
    elif n == 'Spr_LoadingBarFill':
        inst['x'] = FILL_X
        inst['y'] = FILL_Y
        inst['width'] = 1
        inst['height'] = FILL_H
        inst['customSize'] = True
        print(f"  Patched {n}: x={inst['x']} y={inst['y']} w={inst['width']} h={inst['height']}")
    elif n == 'Spr_LoadingIndicator':
        inst['x'] = SPINNER_X
        inst['y'] = SPINNER_Y
        inst['width'] = SPINNER_SIZE
        inst['height'] = SPINNER_SIZE
        inst['customSize'] = True
        print(f"  Patched {n}: x={inst['x']} y={inst['y']} w={inst['width']} h={inst['height']}")
    elif n == 'Txt_Loading':
        inst['x'] = TXT_LOADING_X
        inst['y'] = TXT_LOADING_Y
        inst['width'] = TXT_LOADING_W
        inst['height'] = TXT_LOADING_H
        print(f"  Patched {n}: x={inst['x']} y={inst['y']}")
    elif n == 'Txt_LoadingPercent':
        inst['x'] = TXT_PCT_X
        inst['y'] = TXT_PCT_Y
        inst['width'] = TXT_PCT_W
        inst['height'] = TXT_PCT_H
        print(f"  Patched {n}: x={inst['x']} y={inst['y']}")

# ---- Patch events: ganti SetWidth -> ChangeWidth, update fill max width ----
def patch_events(events):
    for ev in events:
        # Patch actions
        actions = ev.get('actions', [])
        for i, action in enumerate(actions):
            t = action.get('type', {}).get('value', '')
            if t == 'SetWidth':
                params = action.get('parameters', [])
                # SetWidth: [object, operator, value]
                # ChangeWidth: same signature
                action['type'] = {'value': 'ChangeWidth'}
                # Update fill max width in the formula
                if len(params) >= 3 and 'LoadingProgress' in params[2]:
                    if 'Spr_LoadingBarFill' in params[0]:
                        # Update max width to FILL_MAX_W
                        params[2] = f'max(1, Variable(LoadingProgress) * {FILL_MAX_W})'
                        print(f"  Patched action SetWidth->ChangeWidth (fill): params={params}")
                    else:
                        print(f"  Patched action SetWidth->ChangeWidth: params={params}")
                else:
                    # Initial set to 1
                    if len(params) >= 1 and 'Spr_LoadingBarFill' in str(params):
                        params[2] = '1' if len(params) > 2 else params
                        print(f"  Patched action SetWidth->ChangeWidth (init): params={params}")
                    else:
                        print(f"  Patched action SetWidth->ChangeWidth: params={params}")
                action['parameters'] = params
        # Recurse into sub-events
        sub = ev.get('events', [])
        if sub:
            patch_events(sub)

events = loading_scene.get('events', [])
if isinstance(events, list):
    patch_events(events)
else:
    print("WARNING: events bukan list, skip patch events")

# ---- Write back ----
with open(PROJECT, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, separators=(',', ':'))

print("\nDone! game.json updated.")
