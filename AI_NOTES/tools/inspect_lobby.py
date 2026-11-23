import json

with open(r'c:\Users\DELL\Downloads\Proffesionalsss\TTS\Roadside-Stick-\game.json', 'r', encoding='utf-8') as f:
    g = json.load(f)

for sc in g['layouts']:
    if sc['name'] == 'Lobby':
        print('INSTANCES:')
        for inst in sc['instances']:
            n = inst.get('name', '?')
            print(f"  {n}: x={inst.get('x')} y={inst.get('y')} w={inst.get('width')} h={inst.get('height')} customSize={inst.get('customSize')}")
        print()
        print('OBJECTS:')
        for obj in sc['objects']:
            print(f"  {obj['name']} ({obj.get('type', '?')})")
        print()
        print('EVENTS:')
        for ev in sc.get('events', []):
            print(f"  Group: {ev.get('title','')} ({len(ev.get('events',[]))} subs)")
        break
