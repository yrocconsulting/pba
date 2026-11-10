#!/usr/bin/env python3
"""Generate assets/img/contours.svg: a sonar-chart style depth-contour pattern.

Needs numpy and scikit-image. Deterministic (fixed seed), so re-running gives the same art.
"""
import pathlib
import numpy as np
from skimage import measure

W, H, S = 1600, 1000, 4          # svg size, grid step
rng = np.random.default_rng(723)
y, x = np.mgrid[0:H:S, 0:W:S].astype(float)
z = np.zeros_like(x)
for _ in range(14):              # humps and holes on the lake bottom
    cx, cy = rng.uniform(-100, W + 100), rng.uniform(-100, H + 100)
    r = rng.uniform(120, 420)
    z += rng.uniform(-1, 1) * np.exp(-(((x - cx) ** 2 + (y - cy) ** 2) / (2 * r * r)))
z += 0.25 * np.sin(x / 260 + 1.3) * np.cos(y / 210)   # a channel-like ripple
z += 0.08 * np.sin(x / 70) * np.sin(y / 90)

levels = np.linspace(z.min(), z.max(), 46)[1:-1]
paths = []
for i, lv in enumerate(levels):
    major = i % 5 == 0
    for c in measure.find_contours(z, lv):
        if len(c) < 12:
            continue
        c = measure.approximate_polygon(c, tolerance=0.6)
        pts = " ".join(f"{p[1] * S:.0f},{p[0] * S:.0f}" for p in c)
        paths.append(f'<polyline class="{"M" if major else "m"}" points="{pts}"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">'
       '<style>polyline{fill:none;stroke:#d4af37;stroke-linejoin:round}'
       '.m{stroke-width:1;stroke-opacity:.55}.M{stroke-width:1.6;stroke-opacity:1}</style>'
       + "".join(paths) + "</svg>")
out = pathlib.Path(__file__).resolve().parent.parent / "assets/img/contours.svg"
out.write_text(svg)
print(out, len(svg) // 1024, "KB,", len(paths), "lines")
