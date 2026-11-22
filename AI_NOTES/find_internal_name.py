with open(r"C:\Program Files\GDevelop\resources\app.asar", "rb") as f:
    data = f.read()

import re
# Find where the instruction is defined
# In GDevelop libGD, it's: .SetInstruction("...", _("Change the width of a Sprite object."))
# Or obj.AddAction("...", _("Change the width of a Sprite object."))
for m in re.finditer(rb'([A-Za-z0-9_:]+)\x00[^\x00]*Change the width of a Sprite object\.', data):
    print("Match:", m.group(0)[:100])

for m in re.finditer(rb'Change the width of a Sprite object\.[^\x00]*\x00([A-Za-z0-9_:]+)', data):
    print("Match 2:", m.group(0)[:100])
