#!/usr/bin/env python3
"""Generate the on-brand scan code + table card for the Ground Effect AR POC.
Edit URL below to your deployed HTTPS link, then: python3 make_qr.py
"""
import segno
from PIL import Image, ImageDraw, ImageFont
import os

# ---- EDIT THIS to your live HTTPS url once deployed ----
URL = "https://lotus-ground-effect.netlify.app"

BLACK  = (15, 15, 15)
YELLOW = (255, 242, 0)
WHITE  = (236, 236, 236)
HERE   = os.path.dirname(os.path.abspath(__file__))

# 1) raw QR: yellow modules on black, high error-correction (survives the styling)
qr = segno.make(URL, error='h')
qr.save(os.path.join(HERE, "qr_raw.png"), scale=20, border=2,
        dark="#FFF200", light="#0F0F0F")

# 2) branded A5-ish table card (portrait 1240x1748 ~ 150dpi A5)
CW, CH = 1240, 1748
card = Image.new("RGB", (CW, CH), BLACK)
d = ImageDraw.Draw(card)

def font(sz, bold=True):
    for p in [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Overpass-Bold.ttf",
        os.path.expanduser("~/Library/Fonts/Overpass-Bold.ttf" if bold else "~/Library/Fonts/Overpass-Regular.ttf"),
    ]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except: pass
    return ImageFont.load_default()

def ctext(y, s, f, fill, tracking=0):
    if tracking:
        # manual letter-spacing
        widths = [d.textlength(ch, font=f) for ch in s]
        total = sum(widths) + tracking*(len(s)-1)
        x = (CW-total)/2
        for ch,w in zip(s,widths):
            d.text((x,y), ch, font=f, fill=fill); x += w+tracking
    else:
        w = d.textlength(s, font=f)
        d.text(((CW-w)/2, y), s, font=f, fill=fill)

# corner ticks
def rect(x0,y0,x1,y1,fill):
    d.rectangle([min(x0,x1),min(y0,y1),max(x0,x1),max(y0,y1)], fill=fill)
T=70; TH=8
for (x,y,hx,hy) in [(70,70,1,1),(CW-70,70,-1,1),(70,CH-70,1,-1),(CW-70,CH-70,-1,-1)]:
    rect(x, y, x+hx*T, y+hy*TH, YELLOW)   # horizontal arm
    rect(x, y, x+hx*TH, y+hy*T, YELLOW)   # vertical arm

# eyebrow
ctext(150, "THE LAUNCH OF ELETRE X", font(30), WHITE, tracking=10)

# the straight line that bends (design DNA)
ly = 250
d.line([(360,ly),(720,ly)], fill=YELLOW, width=14)
d.line([(720,ly),(880,ly-120)], fill=YELLOW, width=14)

# headline
ctext(330, "GROUND", font(120), WHITE)
ctext(450, "EFFECT", font(120), YELLOW)

# QR, centered
q = Image.open(os.path.join(HERE,"qr_raw.png")).convert("RGB")
qs = 640
q = q.resize((qs,qs), Image.NEAREST)
card.paste(q, ((CW-qs)//2, 700))

# instruction (plain copy)
ctext(1440, "SCAN TO SEE THE FLOOR WORK", font(40), WHITE, tracking=6)
ctext(1510, "Point your phone here, then under the car", font(30, bold=False), (150,150,150))

# footer
ctext(CH-140, "LOTUS", font(30), YELLOW, tracking=14)

card.save(os.path.join(HERE,"scan_card.png"), "PNG")
print("Wrote qr_raw.png and scan_card.png  ->", URL)
