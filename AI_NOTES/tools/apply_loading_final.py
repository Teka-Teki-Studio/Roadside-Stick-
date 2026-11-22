import json

PROJECT = r"c:\Users\DELL\Downloads\Proffesionalsss\TTS\Roadside-Stick-\game.json"

with open(PROJECT, 'r', encoding='utf-8') as f:
    g = json.load(f)

# Find Loading layout
loading = None
for sc in g['layouts']:
    if sc['name'] == 'Loading':
        loading = sc
        break

if not loading:
    print("Loading scene not found!")
    exit(1)

# Layout constants for 1024x576
BAR_X = 32
BAR_Y = 520
BAR_W = 920
BAR_H = 12

SPINNER_X = 968
SPINNER_Y = 514
SPINNER_SIZE = 24

TXT_Y = 490

# 1. Update Instances
for inst in loading.get('instances', []):
    name = inst.get('name')
    if name == 'Spr_LoadingBarFrame':
        inst['x'] = BAR_X
        inst['y'] = BAR_Y
        inst['width'] = BAR_W
        inst['height'] = BAR_H
        inst['customSize'] = True
        inst['zOrder'] = 10
        inst['layer'] = 'UI'
    elif name == 'Spr_LoadingBarFill':
        inst['x'] = BAR_X
        inst['y'] = BAR_Y
        inst['width'] = 1
        inst['height'] = BAR_H
        inst['customSize'] = True
        inst['zOrder'] = 11
        inst['layer'] = 'UI'
    elif name == 'Spr_LoadingIndicator':
        inst['x'] = SPINNER_X
        inst['y'] = SPINNER_Y
        inst['width'] = SPINNER_SIZE
        inst['height'] = SPINNER_SIZE
        inst['customSize'] = True
        inst['zOrder'] = 12
        inst['layer'] = 'UI'
    elif name == 'Txt_Loading':
        inst['x'] = BAR_X
        inst['y'] = TXT_Y
        inst['width'] = 300
        inst['height'] = 28
        inst['zOrder'] = 12
        inst['layer'] = 'UI'
    elif name == 'Txt_LoadingPercent':
        inst['x'] = 900
        inst['y'] = TXT_Y
        inst['width'] = 52
        inst['height'] = 28
        inst['zOrder'] = 12
        inst['layer'] = 'UI'

# 2. Update Text Object formatting (pure white, vcr.ttf, no outline)
for obj in loading.get('objects', []):
    if obj.get('name') in ['Txt_Loading', 'Txt_LoadingPercent']:
        obj['color'] = '255;255;255'
        obj['fontResourceName'] = 'vcr.ttf'
        obj['isOutlineEnabled'] = False
        obj['outlineThickness'] = 0

# 3. Clean and rebuild Loading Events
new_events = [
    {
        "type": "BuiltinCommonInstructions::Group",
        "title": "[T2] Loading — Progres & Load Save",
        "parameters": [""],
        "events": [
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {
                        "type": {"value": "DepartScene"},
                        "parameters": [""]
                    }
                ],
                "actions": [
                    {
                        "type": {"value": "ModVarScene"},
                        "parameters": ["LoadingTimer", "=", "0"]
                    },
                    {
                        "type": {"value": "ModVarScene"},
                        "parameters": ["LoadingProgress", "=", "0"]
                    },
                    {
                        "type": {"value": "ChangeWidth"},
                        "parameters": ["Spr_LoadingBarFill", "=", "1"]
                    },
                    {
                        "type": {"value": "PlayAnimation"},
                        "parameters": ["Spr_LoadingIndicator"]
                    },
                    {
                        "type": {"value": "TextObject::String"},
                        "parameters": ["Txt_LoadingPercent", "=", '"0%"']
                    },
                    {
                        "type": {"value": "LireFichierExp"},
                        "parameters": ['"roadsidestick_save_v1"', '"level"', "1", "Save.level"]
                    },
                    {
                        "type": {"value": "LireFichierExp"},
                        "parameters": ['"roadsidestick_save_v1"', '"money"', "0", "Save.money"]
                    },
                    {
                        "type": {"value": "LireFichierExp"},
                        "parameters": ['"roadsidestick_save_v1"', '"soundOn"', "1", "Save.soundOn"]
                    },
                    {
                        "type": {"value": "LireFichierExp"},
                        "parameters": ['"roadsidestick_save_v1"', '"bagTier"', "0", "Save.bagTier"]
                    },
                    {
                        "type": {"value": "LireFichierExp"},
                        "parameters": ['"roadsidestick_save_v1"', '"drinkQty"', "0", "Save.drinkQty"]
                    }
                ]
            },
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [],
                "actions": [
                    {
                        "type": {"value": "ModVarScene"},
                        "parameters": ["LoadingTimer", "+", "TimeDelta()"]
                    },
                    {
                        "type": {"value": "ModVarScene"},
                        "parameters": ["LoadingProgress", "=", "min(1, Variable(LoadingTimer) / 3.8)"]
                    },
                    {
                        "type": {"value": "ChangeWidth"},
                        "parameters": ["Spr_LoadingBarFill", "=", "max(1, Variable(LoadingProgress) * 920)"]
                    },
                    {
                        "type": {"value": "TextObject::String"},
                        "parameters": ["Txt_LoadingPercent", "=", 'ToString(round(Variable(LoadingProgress) * 100)) + "%"']
                    }
                ]
            },
            {
                "type": "BuiltinCommonInstructions::Standard",
                "conditions": [
                    {
                        "type": {"value": "VarScene"},
                        "parameters": ["LoadingTimer", ">=", "4.0"]
                    }
                ],
                "actions": [
                    {
                        "type": {"value": "Scene"},
                        "parameters": ["", '"Lobby"', "no"]
                    }
                ]
            }
        ]
    }
]

loading['events'] = new_events

with open(PROJECT, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print("Successfully updated game.json with clean Loading scene configuration!")
