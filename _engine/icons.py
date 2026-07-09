#!/usr/bin/env python3
"""icons.py -- fetch Lucide line icons, recolor to a brand hex, rasterize to PNG.

Lucide (https://lucide.dev, ISC license) icons are single-color line SVGs using
`currentColor`, so we swap that for the brand ink/accent and convert with
rsvg-convert. Cached by (name,color,size). Returns a PNG path, or None on failure
(caller falls back to a colored chip). No logos -- these are generic UI glyphs.
"""
import hashlib
import os
import re
import shutil
import subprocess
import urllib.request

LUCIDE = "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/{}.svg"
_SAFE = re.compile(r"^[a-z0-9-]+$")


def icon_png(name, hex_color, size_px, cache_dir, stroke=2.0):
    # icon name comes from (model-authored) spec content: allow only Lucide-style
    # slugs so it can't traverse the filesystem or the URL path.
    if not name or not _SAFE.match(name):
        return None
    os.makedirs(cache_dir, exist_ok=True)
    col = hex_color.lstrip("#")
    key = hashlib.md5(f"{name}-{col}-{size_px}-{stroke}".encode()).hexdigest()[:8]
    out = os.path.join(cache_dir, f"{name}-{key}.png")
    if os.path.exists(out):
        return out
    conv = shutil.which("rsvg-convert")
    if not conv:
        return None
    try:
        req = urllib.request.Request(LUCIDE.format(name),
                                     headers={"User-Agent": "kr-brand-decks"})
        svg = urllib.request.urlopen(req, timeout=12).read().decode("utf-8")
    except Exception:
        return None
    svg = svg.replace("currentColor", "#" + col)
    if 'stroke-width="2"' in svg:
        svg = svg.replace('stroke-width="2"', f'stroke-width="{stroke}"')
    tmp = out + ".svg"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(svg)
    try:
        subprocess.run([conv, "-w", str(size_px), "-h", str(size_px), tmp, "-o", out],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        return None
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return out if os.path.exists(out) else None


if __name__ == "__main__":
    import sys
    p = icon_png(sys.argv[1] if len(sys.argv) > 1 else "cpu",
                 sys.argv[2] if len(sys.argv) > 2 else "1428A0", 240, "/tmp/iconcache")
    print(p)
