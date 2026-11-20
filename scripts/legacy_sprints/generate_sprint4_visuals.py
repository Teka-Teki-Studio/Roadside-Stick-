"""Generate all Sprint 4 pixel art assets via PIL (NEAREST, no AI)."""
import os
from PIL import Image, ImageDraw

os.makedirs("assets/sprint4/title", exist_ok=True)
os.makedirs("assets/sprint4/ui", exist_ok=True)
os.makedirs("assets/sprint4/particles", exist_ok=True)

# 1. Title Background (640x360) — dark moody forest clearing with moonlight
def gen_title_bg():
    img = Image.new("RGBA", (640, 360), (8, 12, 24, 255))
    draw = ImageDraw.Draw(img)
    # Night sky gradient
    for y in range(180):
        c = int(8 + y * 0.08)
        draw.line([(0, y), (639, y)], fill=(c, c + 4, c + 16, 255))
    # Moon
    draw.ellipse([480, 30, 520, 70], fill=(240, 235, 210, 255))
    draw.ellipse([486, 28, 516, 58], fill=(8, 14, 30, 255))  # crescent shadow
    # Stars
    import random
    random.seed(42)
    for _ in range(60):
        sx, sy = random.randint(0, 639), random.randint(0, 160)
        brightness = random.randint(160, 255)
        draw.point([(sx, sy)], fill=(brightness, brightness, brightness - 20, 255))
    # Distant treeline silhouettes
    for x in range(0, 640, 3):
        h = 140 + int(30 * abs(((x * 7 + 50) % 200) / 100 - 1)) + random.randint(-8, 8)
        draw.rectangle([x, h, x + 2, 360], fill=(6, 10, 18, 255))
    # Closer tree silhouettes
    for x in range(0, 640, 5):
        h = 200 + int(40 * abs(((x * 3 + 100) % 160) / 80 - 1)) + random.randint(-12, 12)
        draw.rectangle([x, h, x + 4, 360], fill=(4, 8, 14, 255))
    # Ground
    draw.rectangle([0, 300, 639, 359], fill=(18, 25, 15, 255))
    draw.rectangle([0, 296, 639, 300], fill=(30, 45, 22, 255))
    # Atmospheric fog wisps
    for y in range(260, 310, 6):
        alpha = 30 - abs(y - 285)
        for x in range(0, 640, 20):
            w = random.randint(15, 40)
            draw.rectangle([x, y, x + w, y + 3], fill=(80, 90, 100, max(5, alpha)))
    img.save("assets/sprint4/title/title_bg.png")

# 2. Title Logo Banner (320x60) — "STICK SCAVENGER" pixel text banner
def gen_title_logo():
    img = Image.new("RGBA", (320, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Rustic wooden plank banner background
    draw.rounded_rectangle([4, 8, 316, 52], radius=4, fill=(90, 60, 35, 240), outline=(60, 40, 22, 255))
    draw.rounded_rectangle([8, 12, 312, 48], radius=3, fill=(120, 82, 48, 220))
    # Wood grain lines
    for y in range(14, 46, 4):
        draw.line([(10, y), (310, y)], fill=(100, 68, 38, 100))
    # Title text — simple pixel block letters "STICK SCAVENGER"
    # Using colored rectangle blocks to spell out (simplified large pixel text)
    tc = (255, 240, 180, 255)  # warm gold text
    # "S" at x=20
    letters_data = [
        # S
        [(20, 18, 30, 21), (18, 18, 21, 28), (20, 27, 30, 30), (28, 28, 31, 38), (18, 37, 30, 40)],
        # T
        [(34, 18, 48, 21), (38, 21, 42, 40)],
        # I
        [(52, 18, 56, 40)],
        # C
        [(60, 18, 72, 21), (58, 18, 61, 40), (60, 37, 72, 40)],
        # K
        [(76, 18, 80, 40), (80, 27, 84, 30), (84, 23, 88, 27), (88, 18, 92, 23), (84, 30, 88, 35), (88, 35, 92, 40)],
        # space
        [],
        # S
        [(106, 18, 116, 21), (104, 18, 107, 28), (106, 27, 116, 30), (114, 28, 117, 38), (104, 37, 116, 40)],
        # C
        [(122, 18, 134, 21), (120, 18, 123, 40), (122, 37, 134, 40)],
        # A
        [(140, 18, 152, 21), (138, 21, 141, 40), (150, 21, 153, 40), (140, 28, 152, 31)],
        # V
        [(156, 18, 160, 32), (160, 32, 164, 40), (164, 32, 168, 40), (168, 18, 172, 32)],
        # E
        [(176, 18, 188, 21), (176, 18, 179, 40), (178, 27, 186, 30), (176, 37, 188, 40)],
        # N
        [(192, 18, 196, 40), (196, 22, 200, 28), (200, 28, 204, 34), (204, 18, 208, 40)],
        # G
        [(214, 18, 226, 21), (212, 18, 215, 40), (214, 37, 226, 40), (224, 28, 227, 40), (220, 28, 227, 31)],
        # E
        [(232, 18, 244, 21), (232, 18, 235, 40), (234, 27, 242, 30), (232, 37, 244, 40)],
        # R
        [(248, 18, 260, 21), (248, 18, 251, 40), (258, 21, 261, 28), (250, 27, 260, 30), (254, 30, 258, 35), (258, 35, 262, 40)],
    ]
    for letter_rects in letters_data:
        for r in letter_rects:
            draw.rectangle(r, fill=tc)
    # Outline glow
    img.save("assets/sprint4/title/title_logo.png")

# 3. Menu Cursor / Selector Arrow (12x12)
def gen_menu_cursor():
    img = Image.new("RGBA", (12, 12), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon([(2, 1), (10, 6), (2, 11)], fill=(255, 220, 80, 255), outline=(180, 140, 40, 255))
    img.save("assets/sprint4/title/menu_cursor.png")

# 4. Mini-Radar Frame (100x20)
def gen_radar_frame():
    img = Image.new("RGBA", (100, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, 99, 19], radius=3, fill=(10, 15, 25, 200), outline=(60, 80, 100, 255))
    # Zone dividers
    draw.line([(33, 2), (33, 17)], fill=(50, 70, 90, 180))
    draw.line([(66, 2), (66, 17)], fill=(50, 70, 90, 180))
    # Zone colors
    draw.rectangle([2, 3, 32, 16], fill=(40, 120, 60, 80))   # Zone 1 green
    draw.rectangle([34, 3, 65, 16], fill=(180, 140, 60, 80))  # Zone 2 amber
    draw.rectangle([67, 3, 97, 16], fill=(140, 50, 100, 80))  # Zone 3 purple
    img.save("assets/sprint4/ui/radar_frame.png")

# 5. Radar Player Dot (4x4)
def gen_radar_dot():
    img = Image.new("RGBA", (4, 4), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 3, 3], fill=(255, 255, 100, 255), outline=(255, 200, 50, 255))
    img.save("assets/sprint4/ui/radar_dot.png")

# 6. Dust Particle (6x6) — 2 frames
def gen_dust():
    for frame in [1, 2]:
        img = Image.new("RGBA", (6, 6), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        if frame == 1:
            draw.ellipse([1, 1, 4, 4], fill=(160, 140, 110, 180))
            draw.point([(2, 2)], fill=(200, 180, 150, 220))
        else:
            draw.ellipse([0, 0, 5, 5], fill=(140, 120, 95, 120))
            draw.point([(2, 1), (3, 3)], fill=(180, 160, 130, 150))
        img.save(f"assets/sprint4/particles/dust_{frame}.png")

# 7. Glint / Sparkle (8x8) — 2 frames for high-tier stick glow
def gen_glint():
    for frame in [1, 2]:
        img = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        if frame == 1:
            draw.line([(4, 0), (4, 7)], fill=(255, 255, 200, 200))
            draw.line([(0, 4), (7, 4)], fill=(255, 255, 200, 200))
            draw.point([(4, 4)], fill=(255, 255, 255, 255))
        else:
            draw.line([(1, 1), (6, 6)], fill=(255, 240, 180, 160))
            draw.line([(6, 1), (1, 6)], fill=(255, 240, 180, 160))
            draw.point([(3, 3), (4, 4)], fill=(255, 255, 255, 220))
        img.save(f"assets/sprint4/particles/glint_{frame}.png")

# 8. Pause Overlay (640x360) — dark semi-transparent overlay
def gen_pause_overlay():
    img = Image.new("RGBA", (640, 360), (0, 0, 0, 160))
    img.save("assets/sprint4/ui/pause_overlay.png")

# 9. Save Toast Icon (16x16) — small floppy disk / checkmark icon
def gen_save_icon():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Floppy disk
    draw.rectangle([2, 2, 13, 14], fill=(60, 80, 140, 255), outline=(40, 55, 100, 255))
    draw.rectangle([4, 2, 11, 6], fill=(180, 180, 190, 255))
    draw.rectangle([5, 8, 10, 13], fill=(30, 45, 80, 255))
    draw.rectangle([6, 9, 9, 12], fill=(100, 130, 180, 255))
    # Green checkmark
    draw.line([(10, 10), (12, 13)], fill=(80, 255, 100, 255), width=2)
    draw.line([(12, 13), (15, 8)], fill=(80, 255, 100, 255), width=2)
    img.save("assets/sprint4/ui/save_icon.png")

gen_title_bg()
gen_title_logo()
gen_menu_cursor()
gen_radar_frame()
gen_radar_dot()
gen_dust()
gen_glint()
gen_pause_overlay()
gen_save_icon()

print("All Sprint 4 visual assets generated successfully!")
