#!/usr/bin/env python3
"""Generate 1200x630 og-image.png for the WiiUE progress site.

Portable Pillow-only renderer — no machine-specific paths, no network.
Palette taken verbatim from index.html :root variables and assets/logo-light.svg.
Usage: python3 tools/make-og-image.py [out.png]
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "og-image.png"

W, H = 1200, 630

# Site palette (index.html :root + logo-light.svg)
BG = (238, 241, 244)          # --bg #eef1f4
STRIPE = (230, 234, 238)      # --stripe #e6eaee
SURFACE = (255, 255, 255)     # --surface #ffffff
LINE = (213, 219, 225)        # --line #d5dbe1
INK = (47, 58, 68)            # --ink #2f3a44
INK_SOFT = (107, 119, 130)    # --ink-soft #6b7782
ACCENT = (0, 166, 224)        # --accent #00a6e0
ACCENT_DEEP = (0, 132, 184)   # --accent-deep #0084b8
ACCENT_WASH = (223, 244, 252) # --accent-wash #dff4fc
DONE = (60, 179, 113)         # --done #3cb371
LOGO_GREY = (133, 133, 133)   # --logo-grey #858585
LOGO_BLUE = (5, 148, 207)     # --logo-blue #0594cf

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

def rounded(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Subtle horizontal stripes like the site background
for y in range(0, H, 6):
    d.rectangle([0, y, W, y + 2], fill=STRIPE)

# Top accent bar (Wii U blue)
d.rectangle([0, 0, W, 10], fill=ACCENT)

# ---- WiiUE wordmark (mimics logo-light.svg: grey "Wii" + blue "UE") ----
# Grey "Wii" drawn as text, blue "UE" as text, plus the two grey dots
# above the "i"s to echo the logo's circle accents.
f_word = font(150, bold=True)
# Measure to place grey + blue halves
grey_text = "Wii"
blue_text = "UE"
gw = d.textlength(grey_text, font=f_word)
bw = d.textlength(blue_text, font=f_word)
total = gw + bw
x0 = (W - total) / 2
y0 = 120
d.text((x0, y0), grey_text, font=f_word, fill=LOGO_GREY)
d.text((x0 + gw, y0), blue_text, font=f_word, fill=LOGO_BLUE)

# Two grey dots above the "i"s (echo the logo's circle accents)
# Approximate positions from text metrics: each "i" in DejaVu Bold ~0.28em wide
em = f_word.size
i_spacing = d.textlength("ii", font=f_word) / 2
dot_r = 16
dot_y = y0 - 46
for i in range(2):
    cx = x0 + gw * 0.28 + i * i_spacing
    d.ellipse([cx - dot_r, dot_y - dot_r, cx + dot_r, dot_y + dot_r], fill=LOGO_GREY)

# Wii U gamepad silhouette motif (rounded rect body + two sticks + dpad hint)
pad_w, pad_h = 300, 150
pad_x = (W - pad_w) / 2
pad_y = 300
rounded(d, [pad_x, pad_y, pad_x + pad_w, pad_y + pad_h], 34, SURFACE)
d.rectangle([pad_x, pad_y, pad_x + pad_w, pad_y + pad_h], outline=LINE, width=3)
# screen
rounded(d, [pad_x + 30, pad_y + 24, pad_x + 270, pad_y + 126], 18, ACCENT_WASH)
# left stick
d.ellipse([pad_x + 18, pad_y + 30, pad_x + 52, pad_y + 64], fill=ACCENT)
d.ellipse([pad_x + 24, pad_y + 36, pad_x + 46, pad_y + 58], fill=SURFACE)
# right stick (smaller, lower)
d.ellipse([pad_x + 248, pad_y + 86, pad_x + 282, pad_y + 120], fill=ACCENT_DEEP)
d.ellipse([pad_x + 254, pad_y + 92, pad_x + 276, pad_y + 114], fill=SURFACE)
# dpad hint
d.rectangle([pad_x + 18, pad_y + 96, pad_x + 52, pad_y + 124], fill=ACCENT_DEEP)
d.rectangle([pad_x + 24, pad_y + 102, pad_x + 46, pad_y + 118], fill=SURFACE)

# Tagline
f_tag = font(44, bold=True)
tag = "The Wii U emulator, but everything works."
tw = d.textlength(tag, font=f_tag)
d.text(((W - tw) / 2, 500), tag, font=f_tag, fill=INK)

# Sub-line: phase + tests badges
f_sub = font(30)
sub1 = "Phase 13: Real games"
sub2 = "90 tests passing"
s1w = d.textlength(sub1, font=f_sub)
s2w = d.textlength(sub2, font=f_sub)
gap = 28
total_w = s1w + gap + s2w
sx = (W - total_w) / 2
sy = 566
# badge 1 (accent wash pill)
d.rounded_rectangle([sx - 14, sy - 6, sx + s1w + 14, sy + 40], radius=20, fill=ACCENT_WASH)
d.text((sx, sy), sub1, font=f_sub, fill=ACCENT_DEEP)
# badge 2 (done wash pill)
x2 = sx + s1w + gap
d.rounded_rectangle([x2 - 14, sy - 6, x2 + s2w + 14, sy + 40], radius=20, fill=(227, 245, 234))
d.text((x2, sy), sub2, font=f_sub, fill=(46, 125, 84))

img.save(OUT, "PNG")
print(f"wrote {OUT} {img.size[0]}x{img.size[1]}")