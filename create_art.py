from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

# ==========================================
# CREATE ADDON ICON (512x512)
# ==========================================
size = 512
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Background circle with gradient
for r in range(size//2, 0, -1):
    ratio = r / (size//2)
    color = (230 - int(60 * ratio), 100 - int(40 * ratio), 20)
    draw.ellipse([size//2 - r, size//2 - r, size//2 + r, size//2 + r], fill=color)

# Outer glow
glow = img.copy()
glow = glow.filter(ImageFilter.GaussianBlur(20))
img = Image.alpha_composite(glow, img)
draw = ImageDraw.Draw(img)

# Play triangle
cx, cy = size // 2, size // 2
triangle_size = 120
points = [
    (cx - triangle_size * 0.6, cy - triangle_size),
    (cx - triangle_size * 0.6, cy + triangle_size),
    (cx + triangle_size * 1.2, cy)
]
draw.polygon(points, fill=(255, 255, 255, 240))

# Film strip lines on left side
for i in range(6):
    y = 80 + i * 70
    draw.rounded_rectangle([30, y, 55, y + 45], radius=8, fill=(0, 0, 0, 150))
    draw.ellipse([35, y + 10, 50, y + 35], fill=(100, 100, 100, 100))

# "OCP" text at bottom
try:
    font = ImageFont.truetype("arial.ttf", 60)
except:
    font = ImageFont.load_default()

draw.text((size//2 - 60, size - 90), "OCP", fill=(255, 255, 255, 200), font=font)

# Save icon
img.convert('RGB').save('C:/Users/user/Workspace/kodi_all_in_one_app/custom_build/addons/plugin.video.opencodeplayer/icon.png', 'PNG')
print('Created icon.png')

# ==========================================
# CREATE FANART (1920x1080)
# ==========================================
w, h = 1920, 1080
bg = Image.new('RGB', (w, h), (15, 15, 20))
draw = ImageDraw.Draw(bg)

# Animated-looking gradient background
for y in range(h):
    ratio = y / h
    # Dark blue to dark orange gradient
    r = int(15 + 40 * ratio)
    g = int(15 + 10 * ratio)
    b = int(20 - 10 * ratio)
    draw.line([(0, y), (w, y)], fill=(r, g, b))

# Subtle film grain noise
for _ in range(5000):
    x = random.randint(0, w - 1)
    y = random.randint(0, h - 1)
    alpha = random.randint(0, 30)
    draw.point((x, y), fill=(255, 255, 255, alpha))

# Horizontal film strip accents
for i in range(3):
    y_start = 100 + i * 400
    for x in range(0, w, 120):
        draw.rounded_rectangle([x + 10, y_start, x + 50, y_start + 40], radius=8, fill=(40, 40, 50, 150))
        draw.ellipse([x + 18, y_start + 8, x + 42, y_start + 32], fill=(80, 80, 90, 100))

# Large centered play button
cx, cy = w // 2, h // 2
play_r = 200

# Outer circle
for r in range(play_r, 0, -1):
    ratio = r / play_r
    color = (int(230 * ratio), int(100 * ratio), int(20 * ratio))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

# Inner circle
draw.ellipse([cx - 120, cy - 120, cx + 120, cy + 120], fill=(30, 30, 35))

# Play triangle
tri_size = 60
tri_points = [
    (cx - tri_size * 0.5, cy - tri_size),
    (cx - tri_size * 0.5, cy + tri_size),
    (cx + tri_size * 1.0, cy)
]
draw.polygon(tri_points, fill=(255, 200, 100))

# Title text
try:
    title_font = ImageFont.truetype("arial.ttf", 80)
    sub_font = ImageFont.truetype("arial.ttf", 40)
except:
    title_font = ImageFont.load_default()
    sub_font = ImageFont.load_default()

# Shadow
draw.text((cx - 252, cy + 252), "OPEN CODE PLAYER", fill=(0, 0, 0, 150), font=title_font)
# Main text
draw.text((cx - 250, cy + 250), "OPEN CODE PLAYER", fill=(255, 180, 80), font=title_font)

# Subtitle
draw.text((cx - 120, cy + 340), "Stream Movies & TV Shows", fill=(180, 180, 200), font=sub_font)

# Save fanart
bg.save('C:/Users/user/Workspace/kodi_all_in_one_app/custom_build/addons/plugin.video.opencodeplayer/fanart.jpg', 'JPEG', quality=95)
print('Created fanart.jpg')

print('Done!')
