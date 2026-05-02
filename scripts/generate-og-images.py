"""
Generate per-page OG images (1200x630 PNG) for all 28 Human OS Wiki pages
and update each page's og:image and twitter:image meta tags to point to
the new image.

THF brand identity:
  - Background: Midnight navy (#0a0e1a) with subtle orange/magenta radial glow
  - Top accent bar: orange-to-magenta gradient
  - Eyebrow: orange, all-caps, tight letter-spacing
  - Title: heavy display font, white
  - Footer: brand name + tagline

Run: python3 scripts/generate-og-images.py
Idempotent. Safe to re-run.
"""

import os
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# --- Paths ----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "human-os"
OUT_DIR = ROOT / "og-images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_DIR = Path("/sessions/magical-funny-fermat/mnt/.claude/skills/canvas-design/canvas-fonts")
FONT_DISPLAY = str(FONT_DIR / "BigShoulders-Bold.ttf")  # Bebas Neue stand-in
FONT_BODY    = str(FONT_DIR / "WorkSans-Bold.ttf")      # DM Sans stand-in
FONT_ITALIC  = str(FONT_DIR / "CrimsonPro-Italic.ttf")  # Playfair italic stand-in

# --- Brand palette --------------------------------------------------------
NAVY     = (10, 14, 26)
NAVY2    = (13, 20, 38)
ORANGE   = (255, 69, 0)
ORANGE2  = (255, 107, 53)
MAGENTA  = (233, 30, 140)
WHITE    = (255, 255, 255)
TEXT     = (232, 232, 232)
MUTED    = (136, 146, 164)

W, H = 1200, 630

# --- Helpers --------------------------------------------------------------

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient_bar(draw, x0, y0, x1, y1, c0, c1, vertical=False):
    """Paint a smooth gradient rectangle."""
    if vertical:
        for y in range(y0, y1):
            t = (y - y0) / max(1, (y1 - y0))
            draw.line([(x0, y), (x1, y)], fill=lerp(c0, c1, t))
    else:
        for x in range(x0, x1):
            t = (x - x0) / max(1, (x1 - x0))
            draw.line([(x, y0), (x, y1)], fill=lerp(c0, c1, t))


def radial_glow(size, center, color, max_radius, opacity=0.18):
    """Return an RGBA layer with a soft radial glow."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cx, cy = center
    steps = 60
    for i in range(steps, 0, -1):
        r = int(max_radius * (i / steps))
        a = int(255 * opacity * ((steps - i) / steps) ** 1.5)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, a))
    return layer.filter(ImageFilter.GaussianBlur(radius=12))


def wrap_text(text, font, max_width, draw):
    """Word-wrap title text to fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_title(text, max_width, max_height, line_height_ratio=0.95,
              start_size=128, min_size=60):
    """Pick the largest title size that fits in the box on <= 3 lines."""
    test_img = Image.new("RGB", (10, 10))
    test_draw = ImageDraw.Draw(test_img)
    for size in range(start_size, min_size - 1, -4):
        font = ImageFont.truetype(FONT_DISPLAY, size)
        lines = wrap_text(text, font, max_width, test_draw)
        if len(lines) > 3:
            continue
        line_h = size * line_height_ratio
        if line_h * len(lines) <= max_height:
            return font, lines
    # Fallback
    font = ImageFont.truetype(FONT_DISPLAY, min_size)
    return font, wrap_text(text, font, max_width, test_draw)


# --- Metadata extraction --------------------------------------------------

TITLE_RE   = re.compile(r"<title>([^<]+)</title>", re.IGNORECASE)
EYEBROW_RE = re.compile(r'class="hero-eyebrow"[^>]*>([^<]+)<', re.IGNORECASE)
H1_RE      = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).strip()


def extract_meta(html):
    title_match = TITLE_RE.search(html)
    raw_title = strip_tags(title_match.group(1)) if title_match else ""
    # "Fawn Response — The Human OS Wiki | The Human Frequency" → "Fawn Response"
    title = re.split(r"\s+[—|·]\s+", raw_title)[0].strip()

    eyebrow_match = EYEBROW_RE.search(html)
    eyebrow = strip_tags(eyebrow_match.group(1)) if eyebrow_match else "HUMAN OS WIKI"
    eyebrow = re.sub(r"\s+", " ", eyebrow).strip().upper()

    # Fall back to <h1> if title parse came up short
    if len(title) < 3:
        h1_match = H1_RE.search(html)
        if h1_match:
            title = strip_tags(h1_match.group(1)).strip()

    return title.upper(), eyebrow


# --- Image render ---------------------------------------------------------

def render_og(title, eyebrow, out_path):
    img = Image.new("RGB", (W, H), NAVY)

    # Subtle vertical navy gradient
    grad = Image.new("RGB", (W, H), NAVY)
    gd = ImageDraw.Draw(grad)
    gradient_bar(gd, 0, 0, W, H, NAVY, NAVY2, vertical=True)
    img = Image.blend(img, grad, 0.5)

    # Soft orange glow + softer magenta glow
    glow1 = radial_glow((W, H), (W // 2 + 80, int(H * 0.55)), ORANGE, 720, opacity=0.22)
    glow2 = radial_glow((W, H), (int(W * 0.85), int(H * 0.18)), MAGENTA, 520, opacity=0.14)
    img = Image.alpha_composite(img.convert("RGBA"), glow1)
    img = Image.alpha_composite(img, glow2).convert("RGB")

    draw = ImageDraw.Draw(img)

    # Top accent bar — orange to magenta gradient (4px tall)
    gradient_bar(draw, 0, 0, W, 4, ORANGE, MAGENTA)

    # Layout box
    pad_x = 80
    inner_w = W - 2 * pad_x

    # Eyebrow (orange, small caps)
    eb_font = ImageFont.truetype(FONT_BODY, 24)
    eb_y = 110
    # Eyebrow accent line
    draw.line([(pad_x, eb_y + 14), (pad_x + 40, eb_y + 14)], fill=ORANGE, width=2)
    draw.text((pad_x + 56, eb_y), eyebrow, font=eb_font, fill=ORANGE)

    # Title — fit and wrap
    title_top = eb_y + 70
    title_max_h = 360
    title_font, lines = fit_title(title, inner_w, title_max_h)
    line_h = int(title_font.size * 0.95)
    y = title_top
    for line in lines:
        draw.text((pad_x, y), line, font=title_font, fill=WHITE)
        y += line_h

    # Footer brand row
    foot_y = H - 80
    # Frequency wave glyph (left of brand)
    wave_x, wave_y = pad_x, foot_y + 6
    wave_pts = []
    for i in range(0, 80, 2):
        t = i / 80
        # Simple sine-like wave path
        import math
        wy = wave_y + 14 + int(math.sin(t * math.pi * 4) * 10)
        wave_pts.append((wave_x + i, wy))
    draw.line(wave_pts, fill=ORANGE, width=2)

    brand_font = ImageFont.truetype(FONT_BODY, 22)
    brand_x = pad_x + 100
    draw.text((brand_x, foot_y), "THE HUMAN ", font=brand_font, fill=WHITE)
    th_w = draw.textlength("THE HUMAN ", font=brand_font)
    draw.text((brand_x + th_w, foot_y), "FREQUENCY", font=brand_font, fill=ORANGE)

    tag_font = ImageFont.truetype(FONT_BODY, 14)
    draw.text((brand_x, foot_y + 32), "FIND COMMON GROUND", font=tag_font, fill=MUTED)

    # Right-side small label
    label_font = ImageFont.truetype(FONT_BODY, 16)
    label = "THE HUMAN OS WIKI"
    lw = draw.textlength(label, font=label_font)
    draw.text((W - pad_x - lw, foot_y + 8), label, font=label_font, fill=MUTED)

    img.save(out_path, "PNG", optimize=True)


# --- HTML meta-tag rewrite ------------------------------------------------

OG_IMG_RE  = re.compile(r'(<meta\s+property="og:image"\s+content=")[^"]+("\s*/?>)', re.IGNORECASE)
TW_IMG_RE  = re.compile(r'(<meta\s+property="twitter:image"\s+content=")[^"]+("\s*/?>)', re.IGNORECASE)
LD_IMG_RE  = re.compile(r'("image"\s*:\s*")https://thehumanfrequency\.net/og-image\.png(")')


def update_html(path, slug):
    html = path.read_text(encoding="utf-8")
    new_url = f"https://thehumanfrequency.net/og-images/wiki-{slug}.png"

    new_html, n1 = OG_IMG_RE.subn(rf'\g<1>{new_url}\g<2>', html)
    new_html, n2 = TW_IMG_RE.subn(rf'\g<1>{new_url}\g<2>', new_html)
    new_html, n3 = LD_IMG_RE.subn(rf'\g<1>{new_url}\g<2>', new_html)

    if new_html != html:
        path.write_text(new_html, encoding="utf-8")
    return n1, n2, n3


# --- Main -----------------------------------------------------------------

def main():
    pages = sorted([p for p in WIKI_DIR.glob("*.html") if p.name != "index.html"])
    print(f"Found {len(pages)} wiki pages")

    for path in pages:
        slug = path.stem
        html = path.read_text(encoding="utf-8")
        title, eyebrow = extract_meta(html)
        out_path = OUT_DIR / f"wiki-{slug}.png"
        render_og(title, eyebrow, out_path)
        n_og, n_tw, n_ld = update_html(path, slug)
        size_kb = out_path.stat().st_size // 1024
        print(f"  {slug:35s}  {size_kb:>4d} KB  meta(og={n_og},tw={n_tw},ld={n_ld})  {title!r}")

    print(f"\nWrote {len(pages)} images to {OUT_DIR}")


if __name__ == "__main__":
    main()
