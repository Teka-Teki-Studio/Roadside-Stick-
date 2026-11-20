import os
from PIL import Image, ImageDraw

os.makedirs("assets/sprint3/enemies", exist_ok=True)
os.makedirs("assets/sprint3/hazards", exist_ok=True)
os.makedirs("assets/sprint3/ui", exist_ok=True)

# 1. Thief Animations (24x24 pixel art)
# Colors:
# Fur: #6b5b4d (body), #4a3e35 (dark fur/mask), #a8947f (belly/light fur)
# Mask: #1a1513, Eyes: #f9d71c (cunning amber)
# Clothing / Sack: #8b5a2b (burlap brown), #d4a373 (loot bag)
def create_thief_patrol(frame):
    img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Body
    draw.rectangle([8, 10, 16, 19], fill=(107, 91, 77, 255))
    draw.rectangle([10, 12, 14, 18], fill=(168, 148, 127, 255))
    # Head
    draw.rectangle([11, 4, 18, 11], fill=(107, 91, 77, 255))
    # Ears
    draw.point([(12, 3), (16, 3)], fill=(74, 62, 53, 255))
    # Mask & Snout
    draw.rectangle([14, 7, 18, 9], fill=(26, 21, 19, 255))
    draw.point([(16, 7)], fill=(249, 215, 28, 255)) # amber eye
    draw.point([(18, 9)], fill=(40, 30, 25, 255)) # snout tip
    # Tail
    draw.rectangle([4, 13, 8, 16], fill=(74, 62, 53, 255))
    draw.point([(3, 14), (3, 15)], fill=(107, 91, 77, 255))
    # Legs (walking cycle)
    if frame == 1:
        draw.rectangle([9, 20, 11, 23], fill=(50, 40, 35, 255))
        draw.rectangle([14, 19, 16, 22], fill=(50, 40, 35, 255))
    else:
        draw.rectangle([9, 19, 11, 22], fill=(50, 40, 35, 255))
        draw.rectangle([14, 20, 16, 23], fill=(50, 40, 35, 255))
    return img

def create_thief_stalk(frame):
    img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Low crouched predator stance
    draw.rectangle([6, 12, 16, 19], fill=(107, 91, 77, 255))
    draw.rectangle([8, 13, 14, 18], fill=(168, 148, 127, 255))
    # Low head
    draw.rectangle([14, 9, 21, 15], fill=(107, 91, 77, 255))
    # Mask
    draw.rectangle([16, 11, 21, 13], fill=(26, 21, 19, 255))
    draw.point([(18, 11)], fill=(255, 50, 50, 255)) # glowing red/amber focused eye
    draw.point([(21, 13)], fill=(30, 25, 20, 255))
    # Extended bushy tail
    draw.rectangle([2, 14, 6, 17], fill=(74, 62, 53, 255))
    # Sprinting paws
    if frame == 1:
        draw.rectangle([7, 19, 10, 22], fill=(50, 40, 35, 255))
        draw.rectangle([15, 20, 18, 23], fill=(50, 40, 35, 255))
    else:
        draw.rectangle([5, 20, 8, 23], fill=(50, 40, 35, 255))
        draw.rectangle([13, 19, 16, 22], fill=(50, 40, 35, 255))
    return img

def create_thief_flee(frame):
    img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Carrying big bulging burlap sack on back
    draw.ellipse([4, 6, 13, 15], fill=(180, 130, 80, 255), outline=(120, 80, 40, 255))
    draw.point([(11, 7), (12, 6)], fill=(220, 170, 110, 255)) # tied knot
    # Stick sticking out of the bag!
    draw.line([(5, 6), (2, 2)], fill=(139, 69, 19, 255), width=2)
    # Body fleeing forward
    draw.rectangle([9, 11, 17, 19], fill=(107, 91, 77, 255))
    # Head looking back or panicked forward
    draw.rectangle([14, 7, 21, 13], fill=(107, 91, 77, 255))
    draw.rectangle([16, 8, 21, 11], fill=(26, 21, 19, 255))
    draw.point([(18, 9)], fill=(255, 255, 255, 255)) # wide panicked eye
    # Fast running legs
    if frame == 1:
        draw.rectangle([8, 19, 11, 23], fill=(50, 40, 35, 255))
        draw.rectangle([16, 18, 20, 21], fill=(50, 40, 35, 255))
    else:
        draw.rectangle([7, 18, 10, 21], fill=(50, 40, 35, 255))
        draw.rectangle([15, 19, 18, 23], fill=(50, 40, 35, 255))
    return img

def create_thief_stun(frame):
    img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Slumped on ground
    draw.rectangle([6, 15, 18, 21], fill=(107, 91, 77, 255))
    draw.rectangle([16, 14, 22, 19], fill=(74, 62, 53, 255))
    # X_X eyes
    draw.point([(18, 16), (20, 16)], fill=(255, 255, 255, 255))
    # Spinning dizzy stars above head
    if frame == 1:
        draw.point([(14, 8), (20, 7), (17, 11)], fill=(255, 215, 0, 255))
    else:
        draw.point([(17, 7), (14, 10), (21, 10)], fill=(255, 235, 50, 255))
    return img

# Save Thief
create_thief_patrol(1).save("assets/sprint3/enemies/thief_patrol_1.png")
create_thief_patrol(2).save("assets/sprint3/enemies/thief_patrol_2.png")
create_thief_stalk(1).save("assets/sprint3/enemies/thief_stalk_1.png")
create_thief_stalk(2).save("assets/sprint3/enemies/thief_stalk_2.png")
create_thief_flee(1).save("assets/sprint3/enemies/thief_flee_1.png")
create_thief_flee(2).save("assets/sprint3/enemies/thief_flee_2.png")
create_thief_stun(1).save("assets/sprint3/enemies/thief_stun_1.png")
create_thief_stun(2).save("assets/sprint3/enemies/thief_stun_2.png")

# 2. Chaser Animations (32x32 pixel art)
# Colors:
# Shadow smoke: #12091c (obsidian void), #2a133d (dark void purple), #4f1d6b (spectral purple)
# Eyes & Claws: #ff1a40 (burning blood-red), #ff7388 (fiery core)
def create_chaser_telegraph(frame):
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Menacing shadowy silhouette rising from mist
    draw.ellipse([8, 10, 24, 28], fill=(18, 9, 28, 220))
    draw.ellipse([10, 12, 22, 26], fill=(42, 19, 61, 230))
    # Eerie smoky tendrils
    if frame == 1:
        draw.line([(8, 12), (4, 8)], fill=(79, 29, 107, 180), width=2)
        draw.line([(24, 12), (28, 7)], fill=(79, 29, 107, 180), width=2)
        draw.line([(16, 8), (16, 3)], fill=(79, 29, 107, 180), width=2)
    else:
        draw.line([(8, 13), (3, 10)], fill=(79, 29, 107, 180), width=2)
        draw.line([(24, 13), (29, 9)], fill=(79, 29, 107, 180), width=2)
        draw.line([(16, 9), (15, 4)], fill=(79, 29, 107, 180), width=2)
    # Glowing piercing crimson eyes
    draw.rectangle([11, 16, 14, 18], fill=(255, 26, 64, 255))
    draw.rectangle([18, 16, 21, 18], fill=(255, 26, 64, 255))
    draw.point([(12, 17), (19, 17)], fill=(255, 200, 200, 255)) # hot center
    return img

def create_chaser_chase(frame):
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Aggressive lunge beast shape
    draw.ellipse([6, 12, 26, 26], fill=(18, 9, 28, 255))
    draw.ellipse([10, 10, 28, 22], fill=(42, 19, 61, 255))
    # Horns / spikes
    draw.polygon([(18, 9), (22, 3), (23, 9)], fill=(18, 9, 28, 255))
    draw.polygon([(12, 10), (14, 5), (16, 10)], fill=(18, 9, 28, 255))
    # Slashing claws
    draw.line([(24, 18), (30, 23)], fill=(255, 50, 70, 255), width=2)
    draw.line([(26, 20), (31, 26)], fill=(255, 50, 70, 255), width=2)
    # Burning crimson eyes
    draw.rectangle([20, 13, 24, 15], fill=(255, 26, 64, 255))
    draw.point([(22, 14)], fill=(255, 230, 230, 255))
    # Legs / shadowy stride
    if frame == 1:
        draw.line([(8, 24), (5, 30)], fill=(30, 15, 45, 255), width=3)
        draw.line([(20, 24), (25, 31)], fill=(30, 15, 45, 255), width=3)
    else:
        draw.line([(10, 24), (13, 31)], fill=(30, 15, 45, 255), width=3)
        draw.line([(18, 24), (15, 30)], fill=(30, 15, 45, 255), width=3)
    return img

def create_chaser_retreat():
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Fading smoke cloud dissolving into shadows
    draw.ellipse([8, 14, 24, 26], fill=(42, 19, 61, 140))
    draw.ellipse([11, 16, 21, 24], fill=(79, 29, 107, 100))
    draw.point([(13, 18), (19, 18)], fill=(255, 26, 64, 120))
    return img

create_chaser_telegraph(1).save("assets/sprint3/enemies/chaser_telegraph_1.png")
create_chaser_telegraph(2).save("assets/sprint3/enemies/chaser_telegraph_2.png")
create_chaser_chase(1).save("assets/sprint3/enemies/chaser_chase_1.png")
create_chaser_chase(2).save("assets/sprint3/enemies/chaser_chase_2.png")
create_chaser_retreat().save("assets/sprint3/enemies/chaser_retreat_1.png")

# 3. Hazard Brambles (32x20 pixel art)
# Sharp barbed briars, dark thorny stems, poisonous thorns
def create_hazard_bramble():
    img = Image.new("RGBA", (32, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Dark tangled stems
    stems = [
        [(2, 19), (6, 12), (12, 16), (18, 8), (24, 14), (30, 19)],
        [(4, 19), (10, 9), (16, 14), (22, 10), (28, 18)],
        [(8, 19), (14, 6), (20, 12), (26, 19)]
    ]
    for stem in stems:
        draw.line(stem, fill=(45, 30, 20, 255), width=2)
    # Sharp thorns (crossings)
    thorns = [
        (6, 10), (10, 8), (14, 5), (18, 7), (22, 9), (26, 12),
        (5, 14), (12, 13), (17, 11), (23, 13), (27, 15)
    ]
    for tx, ty in thorns:
        draw.point([(tx, ty)], fill=(90, 65, 40, 255))
        draw.point([(tx+1, ty-1)], fill=(180, 160, 130, 255)) # needle barb
    # Toxic reddish-purple thorns/berries
    berries = [(9, 11), (15, 8), (21, 12), (13, 15), (25, 14)]
    for bx, by in berries:
        draw.point([(bx, by)], fill=(160, 30, 50, 255))
        draw.point([(bx, by+1)], fill=(100, 15, 30, 255))
    return img

create_hazard_bramble().save("assets/sprint3/hazards/hazard_bramble.png")

# 4. Safe Barrier (20x48 pixel art)
# Wooden sanctum totem ward with glowing magical cyan / gold runes at X=180
def create_safe_barrier():
    img = Image.new("RGBA", (20, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Wooden Totem Posts
    draw.rectangle([5, 8, 14, 47], fill=(80, 55, 35, 255), outline=(50, 35, 20, 255))
    draw.rectangle([7, 10, 12, 45], fill=(110, 75, 50, 255))
    # Carved Head / Totem Top
    draw.polygon([(4, 8), (10, 2), (15, 8)], fill=(90, 60, 40, 255))
    # Sacred Ward Rope wrap
    draw.line([(5, 16), (14, 18)], fill=(200, 180, 140, 255), width=2)
    draw.line([(5, 32), (14, 34)], fill=(200, 180, 140, 255), width=2)
    # Glowing Cyan Runes (Ward Magic)
    runes = [
        (9, 12), (10, 12), (9, 13),
        (8, 23), (11, 23), (9, 24), (10, 25), (9, 26), (11, 26), # Ankh/Rune
        (9, 39), (10, 39), (10, 40), (9, 41), (10, 41)
    ]
    for rx, ry in runes:
        draw.point([(rx, ry)], fill=(80, 240, 255, 255))
    # Subtle barrier shield aura beam on the left/right
    for y in range(4, 48, 4):
        draw.point([(2, y), (17, y)], fill=(80, 240, 255, 120))
    return img

create_safe_barrier().save("assets/sprint3/hazards/safe_barrier.png")

# 5. UI Alert Indicator (20x20 pixel art)
# 4 states: 0=Safe, 1=Caution, 2=Danger, 3=Panic
def create_ui_alert(state):
    img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Outer dark circular frame
    draw.ellipse([1, 1, 18, 18], fill=(20, 20, 25, 230), outline=(60, 60, 70, 255))
    if state == 0:
        # Safe - Green Sacred Shield
        draw.polygon([(10, 4), (15, 7), (15, 12), (10, 16), (5, 12), (5, 7)], fill=(40, 180, 80, 255), outline=(100, 255, 140, 255))
        draw.line([(10, 6), (10, 14)], fill=(160, 255, 180, 255), width=1)
    elif state == 1:
        # Caution - Yellow Vigilant Eye
        draw.ellipse([4, 6, 16, 14], fill=(230, 190, 30, 255), outline=(255, 230, 80, 255))
        draw.ellipse([8, 7, 12, 13], fill=(30, 25, 10, 255))
        draw.point([(9, 8)], fill=(255, 255, 255, 255)) # reflection
    elif state == 2:
        # Danger - Orange Warning Diamond
        draw.polygon([(10, 3), (17, 10), (10, 17), (3, 10)], fill=(240, 110, 20, 255), outline=(255, 170, 60, 255))
        draw.line([(10, 6), (10, 11)], fill=(255, 255, 255, 255), width=2)
        draw.point([(10, 14)], fill=(255, 255, 255, 255))
    elif state == 3:
        # Panic / High Alert - Crimson Skull / Beast
        draw.ellipse([5, 4, 15, 14], fill=(220, 30, 40, 255), outline=(255, 90, 100, 255))
        draw.rectangle([7, 13, 13, 16], fill=(220, 30, 40, 255))
        draw.point([(7, 8), (12, 8)], fill=(15, 0, 5, 255)) # dark eye sockets
        draw.line([(8, 15), (12, 15)], fill=(15, 0, 5, 255), width=1) # teeth
    return img

create_ui_alert(0).save("assets/sprint3/ui/ui_alert_safe.png")
create_ui_alert(1).save("assets/sprint3/ui/ui_alert_caution.png")
create_ui_alert(2).save("assets/sprint3/ui/ui_alert_danger.png")
create_ui_alert(3).save("assets/sprint3/ui/ui_alert_panic.png")

# 6. Alert Vignette (640x360 pixel art border gradient)
def create_alert_vignette():
    img = Image.new("RGBA", (640, 360), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Red danger vignette around borders
    for i in range(24):
        alpha = int(120 * (1 - i / 24))
        draw.rectangle([i, i, 639 - i, 359 - i], outline=(220, 20, 30, alpha))
    return img

create_alert_vignette().save("assets/sprint3/ui/alert_vignette.png")

print("All Sprint 3 pixel art assets generated successfully!")
