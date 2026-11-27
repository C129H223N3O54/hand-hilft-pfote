import math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1080
S = 2                      # supersampling
w, h = W*S, H*S
rng = random.Random(2026)
np.random.seed(2026)

acc = np.zeros((h, w, 3), np.float32)

# ---- background: deep red glow bottom-left, fading to black at top
yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
nx, ny = xx / w, yy / h
d = np.sqrt(((nx - 0.32) * 1.25) ** 2 + ((ny - 1.12) * 1.0) ** 2)
t = np.clip(d / 1.05, 0, 1)
t = t ** 1.15
c0 = np.array([170, 8, 18], np.float32)   # bright crimson
c1 = np.array([95, 2, 10], np.float32)
c2 = np.array([4, 0, 1], np.float32)
bg = np.where(t[..., None] < 0.45,
              c0 + (c1 - c0) * (t[..., None] / 0.45),
              c1 + (c2 - c1) * ((t[..., None] - 0.45) / 0.55))
# darker vignette at very top
bg *= (0.55 + 0.45 * np.clip(ny * 1.6, 0, 1))[..., None]
acc += bg
del xx, yy, nx, ny, d, t, bg

def layer():
    return Image.new("RGB", (w, h), (0, 0, 0))

def add(img, gain=1.0, blur=0):
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur * S))
    acc[:] += np.asarray(img, np.float32) * gain

# ---- soft bokeh dots
L = layer(); dr = ImageDraw.Draw(L)
for _ in range(70):
    x, y = rng.uniform(0, w), rng.uniform(0, h)
    r = rng.uniform(6, 26) * S
    col = rng.choice([(255, 60, 60), (255, 120, 60), (255, 190, 90)])
    a = rng.uniform(0.15, 0.45)
    dr.ellipse([x-r, y-r, x+r, y+r], fill=tuple(int(c*a) for c in col))
add(L, 0.6, blur=6)

# ---- snow / glitter particles
def particles(n, rmin, rmax, cols, gain, blur):
    L = layer(); dr = ImageDraw.Draw(L)
    for _ in range(n):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        r = rng.uniform(rmin, rmax) * S
        a = rng.uniform(0.35, 1.0)
        col = rng.choice(cols)
        dr.ellipse([x-r, y-r, x+r, y+r], fill=tuple(int(c*a) for c in col))
    add(L, gain, blur)

white = [(255, 255, 255), (255, 240, 225)]
gold = [(255, 215, 140), (255, 190, 100)]
particles(900, 0.5, 1.3, white + gold, 0.9, 0)
particles(260, 1.2, 2.4, white, 0.8, 0.6)
particles(60, 2.0, 3.5, white + gold, 0.9, 1.5)

# a few 4-point twinkle stars
def twinkle(dr, x, y, size, col):
    for ang, ln in ((0, 1.0), (math.pi/2, 1.0), (math.pi/4, 0.45), (3*math.pi/4, 0.45)):
        dx, dy = math.cos(ang) * size * ln, math.sin(ang) * size * ln
        dr.line([x-dx, y-dy, x+dx, y+dy], fill=col, width=max(1, S))
L = layer(); dr = ImageDraw.Draw(L)
for _ in range(20):
    x, y = rng.uniform(0, w), rng.uniform(0, h * 0.95)
    twinkle(dr, x, y, rng.uniform(6, 16) * S, (255, 235, 200))
    r = 2 * S; dr.ellipse([x-r, y-r, x+r, y+r], fill=(255, 250, 235))
add(L, 0.8, 0)
add(L, 0.8, 2)

# ---- spiral light tree (right side)
cx = 0.765 * w
base_y = 0.86 * h
top_y = 0.21 * h
R0 = 0.115 * w
turns = 5.3
tilt = 0.20

pts = []
N = 2400
for i in range(N + 1):
    s = i / N
    r = R0 * (1 - s) ** 0.85 + 0.004 * w
    ang = s * turns * 2 * math.pi + 0.6
    x = cx + r * math.sin(ang)
    y = base_y - (base_y - top_y) * s + r * tilt * math.cos(ang)
    front = math.cos(ang)              # +1 front, -1 back
    pts.append((x, y, front, s))

def draw_spiral(width_front, width_back, col, back_dim, only_front=None):
    L = layer(); dr = ImageDraw.Draw(L)
    for (x0, y0, f0, s0), (x1, y1, f1, s1) in zip(pts, pts[1:]):
        f = (f0 + f1) / 2
        k = (f + 1) / 2                  # 0 back .. 1 front
        bright = back_dim + (1 - back_dim) * k
        # fade in at the very bottom so the ribbon emerges from light
        bright *= min(1.0, 0.25 + s0 * 6)
        wd = (width_back + (width_front - width_back) * k) * (1 - 0.45 * s0) * S
        c = tuple(int(v * bright) for v in col)
        dr.line([x0, y0, x1, y1], fill=c, width=max(1, int(round(wd))))
    return L

add(draw_spiral(34, 18, (255, 120, 20), 0.25), 0.55, blur=22)   # wide amber haze
add(draw_spiral(14, 7, (255, 170, 50), 0.30), 0.9, blur=7)       # gold glow
add(draw_spiral(5, 2.5, (255, 225, 140), 0.30), 1.0, blur=1.5)   # bright ribbon
add(draw_spiral(1.6, 0.8, (255, 252, 230), 0.20), 1.0, blur=0)   # hot core

# fairy-light sparkles scattered along and around the spiral
L = layer(); dr = ImageDraw.Draw(L)
for _ in range(650):
    x, y, f, s = pts[rng.randrange(len(pts))]
    if f < -0.3 and rng.random() < 0.6:
        continue
    jitter = (1 - s) * 0.02 * w + 4 * S
    x += rng.gauss(0, jitter); y += rng.gauss(0, jitter * 0.8)
    r = rng.uniform(0.6, 2.2) * S
    a = rng.uniform(0.4, 1.0)
    col = rng.choice([(255, 230, 160), (255, 200, 110), (255, 255, 240)])
    dr.ellipse([x-r, y-r, x+r, y+r], fill=tuple(int(c*a) for c in col))
add(L, 1.0, 0)
add(L, 1.2, 3)

# glittering light dust drifting down below the tree
L = layer(); dr = ImageDraw.Draw(L)
for _ in range(420):
    x = cx + rng.gauss(0, 0.075 * w)
    y = base_y + abs(rng.gauss(0, 0.05 * h)) - 0.03 * h
    r = rng.uniform(0.5, 1.8) * S
    a = rng.uniform(0.3, 1.0)
    dr.ellipse([x-r, y-r, x+r, y+r], fill=(int(255*a), int(205*a), int(120*a)))
add(L, 1.0, 0)
add(L, 0.9, 2.5)

# ---- star on top
sx, sy = cx + 0.002 * w, top_y - 0.058 * h
R_out, R_in = 0.042 * h, 0.018 * h
star = []
for k in range(10):
    ang = -math.pi / 2 + k * math.pi / 5
    rr = R_out if k % 2 == 0 else R_in
    star.append((sx + rr * math.cos(ang) * S, sy + rr * math.sin(ang) * S))
star.append(star[0])

# halo
L = layer(); dr = ImageDraw.Draw(L)
for rr, a in ((0.07 * h, 0.22), (0.045 * h, 0.35), (0.025 * h, 0.5)):
    rr *= S
    dr.ellipse([sx-rr, sy-rr, sx+rr, sy+rr], fill=(int(255*a), int(150*a), int(40*a)))
add(L, 1.0, blur=14)

for wd, col, gain, bl in ((18, (255, 150, 30), 0.8, 10),
                          (8, (255, 200, 80), 1.0, 3),
                          (3.5, (255, 240, 170), 1.0, 0.8),
                          (1.4, (255, 255, 245), 1.0, 0)):
    L = layer(); dr = ImageDraw.Draw(L)
    dr.line(star, fill=col, width=int(wd * S), joint="curve")
    add(L, gain, bl)

# star rays
L = layer(); dr = ImageDraw.Draw(L)
twinkle(dr, sx, sy, 0.05 * h * S, (255, 230, 170))
add(L, 0.7, 1.5)

# ---- finish
img = np.clip(acc, 0, 255)
# fine grain against banding
img += np.random.normal(0, 1.2, img.shape).astype(np.float32)
img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")
img = img.resize((W, H), Image.LANCZOS)
out = sys.argv[1]
img.save(out, optimize=True)
print("saved", out)
