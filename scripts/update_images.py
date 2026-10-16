import os
import glob
from PIL import Image, ImageDraw, ImageFont

art_dir = r"C:\Users\love sharma\.gemini\antigravity-ide\brain\726a9ff5-7482-4737-8fb8-706c253de17f"
emblem_path = glob.glob(os.path.join(art_dir, "campuspulse_emblem_*.jpg"))[0]
banner_path = glob.glob(os.path.join(art_dir, "campuspulse_banner_*.jpg"))[0]
notice_path = glob.glob(os.path.join(art_dir, "campus_notice_cover_*.jpg"))[0]
swarm_path = glob.glob(os.path.join(art_dir, "campus_swarm_cover_*.jpg"))[0]

print("Emblem:", emblem_path)
print("Banner:", banner_path)
print("Notice:", notice_path)
print("Swarm:", swarm_path)

# 1. Update frontend/public/icon.png
# We crop the emblem (shield) and make a 1024x1024 PNG with transparent or clean background
im_emblem = Image.open(emblem_path).convert("RGBA")
# Shield bbox is approx (180, 150, 844, 780)
shield_crop = im_emblem.crop((160, 140, 864, 780))
# Create 1024x1024 transparent canvas
icon = Image.new("RGBA", (1024, 1024), (255, 255, 255, 0))
# Resize shield maintaining aspect ratio to fit ~900x900
shield_crop.thumbnail((900, 900), Image.Resampling.LANCZOS)
# Make background transparent if near white
pix = shield_crop.load()
sw, sh = shield_crop.size
for y in range(sh):
    for x in range(sw):
        r, g, b, a = pix[x, y]
        if r > 245 and g > 245 and b > 245:
            # smooth fade for near-white
            diff = min(r, g, b) - 245
            alpha = max(0, 255 - int(diff * 25.5))
            pix[x, y] = (r, g, b, min(a, alpha))

paste_x = (1024 - shield_crop.width) // 2
paste_y = (1024 - shield_crop.height) // 2
icon.paste(shield_crop, (paste_x, paste_y), shield_crop)
icon.save("frontend/public/icon.png", format="PNG")
print("Saved frontend/public/icon.png")

# 2. Update frontend/src/assets/logo/MiroFish_logo_left.jpeg
# Original size: 3006 x 2084
hero_logo = Image.new("RGB", (3006, 2084), (255, 255, 255))
# Place full emblem (shield + text) centered
full_emblem = Image.open(emblem_path).convert("RGB")
# Scale full emblem to fit nicely
target_h = int(2084 * 0.92)
target_w = int(full_emblem.width * (target_h / full_emblem.height))
full_emblem_resized = full_emblem.resize((target_w, target_h), Image.Resampling.LANCZOS)
hero_logo.paste(full_emblem_resized, ((3006 - target_w) // 2, (2084 - target_h) // 2))
hero_logo.save("frontend/src/assets/logo/MiroFish_logo_left.jpeg", format="JPEG", quality=95)
print("Saved frontend/src/assets/logo/MiroFish_logo_left.jpeg")

# 3. Update Banners:
# frontend/src/assets/logo/MiroFish_logo_compressed.jpeg
# static/image/MiroFish_logo.jpeg
# static/image/MiroFish_logo_compressed.jpeg
banner_im = Image.open(banner_path).convert("RGB")
# Original banner size was 7616 x 2240 (ratio 3.4 : 1)
# Let's crop/pad banner_im (16:9) to standard high-res banner
bw, bh = banner_im.size
# Crop vertically to center if needed, or put on wide white background
wide_banner = Image.new("RGB", (7616, 2240), (255, 255, 255))
banner_scaled = banner_im.resize((int(2240 * (bw / bh)), 2240), Image.Resampling.LANCZOS)
# center it
wide_banner.paste(banner_scaled, ((7616 - banner_scaled.width) // 2, 0))
wide_banner.save("static/image/MiroFish_logo.jpeg", format="JPEG", quality=95)
wide_banner.save("static/image/MiroFish_logo_compressed.jpeg", format="JPEG", quality=90)
wide_banner.save("frontend/src/assets/logo/MiroFish_logo_compressed.jpeg", format="JPEG", quality=90)
print("Saved banner images")

# 4. Update video covers:
# static/image/wuhan-university-simulation-cover.png
notice_im = Image.open(notice_path).convert("RGB")
notice_resized = notice_im.resize((1920, 1080), Image.Resampling.LANCZOS)
notice_resized.save("static/image/wuhan-university-simulation-cover.png", format="PNG")
print("Saved wuhan-university-simulation-cover.png")

# static/image/red-chamber-simulation-cover.jpg
swarm_im = Image.open(swarm_path).convert("RGB")
swarm_resized = swarm_im.resize((2560, 1440), Image.Resampling.LANCZOS)
swarm_resized.save("static/image/red-chamber-simulation-cover.jpg", format="JPEG", quality=95)
print("Saved red-chamber-simulation-cover.jpg")

print("All base images updated successfully!")
