import os
import glob
from PIL import Image, ImageDraw, ImageFont

art_dir = r"C:\Users\love sharma\.gemini\antigravity-ide\brain\726a9ff5-7482-4737-8fb8-706c253de17f"
emblem_path = glob.glob(os.path.join(art_dir, "campuspulse_emblem_*.jpg"))[0]
emblem = Image.open(emblem_path).convert("RGB")

font_path = "C:/Windows/Fonts/segoeuib.ttf"
if not os.path.exists(font_path):
    font_path = "C:/Windows/Fonts/arialbd.ttf"

# Process screenshot-1.png
s1 = Image.open("static/image/Screenshot/screenshot-1.png").convert("RGB")
draw1 = ImageDraw.Draw(s1)

# 1. Clear old logo area: (1000, 100, 1480, 430) with white
draw1.rectangle([980, 95, 1490, 440], fill=(255, 255, 255))

# Paste new emblem scaled to fit height ~330
target_h = 330
target_w = int(emblem.width * (target_h / emblem.height))
emblem_resized = emblem.resize((target_w, target_h), Image.Resampling.LANCZOS)
# center in box
box_w = 1490 - 980
x_offset = 980 + (box_w - target_w) // 2
s1.paste(emblem_resized, (x_offset, 100))

# 2. Update navbar in screenshot-1
draw1.rectangle([30, 15, 180, 40], fill=(255, 255, 255))
font1 = ImageFont.truetype(font_path, 15)
draw1.text((36, 19), "CAMPUSPULSE AI", fill=(0, 0, 0), font=font1)

# Also check description text containing 'MiroFish' in screenshot-1
# Text bbox is roughly x: [175, 520], y: [330, 375]
# Let's inspect if needed or leave clean
s1.save("static/image/Screenshot/screenshot-1.png", format="PNG")
print("Updated screenshot-1.png")

# Process screenshot-2 through 6
screenshot_configs = [
    ("static/image/Screenshot/screenshot-2.png", (15, 15, 170, 40), (20, 20), 14),
    ("static/image/Screenshot/screenshot-3.png", (15, 15, 170, 40), (22, 19), 14),
    ("static/image/Screenshot/screenshot-4.png", (15, 15, 170, 40), (22, 19), 14),
    ("static/image/Screenshot/screenshot-5.png", (15, 12, 170, 38), (19, 16), 14),
    ("static/image/Screenshot/screenshot-6.png", (15, 8, 170, 32), (18, 10), 13),
]

for file_path, clear_rect, text_pos, font_size in screenshot_configs:
    im = Image.open(file_path).convert("RGB")
    draw = ImageDraw.Draw(im)
    draw.rectangle(list(clear_rect), fill=(255, 255, 255))
    font = ImageFont.truetype(font_path, font_size)
    draw.text(text_pos, "CAMPUSPULSE AI", fill=(0, 0, 0), font=font)
    im.save(file_path, format="PNG")
    print(f"Updated {file_path}")

print("All screenshots updated!")
