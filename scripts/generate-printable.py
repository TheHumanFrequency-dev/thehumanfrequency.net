#!/usr/bin/env python3
"""
generate-printable.py — Build a single-page printable PDF for each wiki page.

Reads the same JSON content files used by the wiki HTML generator and outputs
a US Letter PDF with the wallet card centered and brand cues.

Layout:
  - US Letter portrait (8.5" x 11")
  - THF brand stripe at top (orange→magenta gradient)
  - Title + subtitle (page topic)
  - Wallet card centered: cream background, 5 protocol items
  - Source citation footer
  - Print instructions ("fold once for wallet, or laminate for fridge")

Usage:
    python3 generate-printable.py <content.json> <output.pdf>

Or via the build script:
    python3 build-printables.py  # batches all 28 pages
"""
import json
import sys
import re
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# THF brand colors
NAVY = HexColor("#0a0e1a")
NAVY3 = HexColor("#111827")
ORANGE = HexColor("#ff4500")
MAGENTA = HexColor("#e91e8c")
GOLD = HexColor("#c9a84c")
CREAM = HexColor("#f5f0e8")
DARK_TEXT = HexColor("#1a1a1a")
MUTED = HexColor("#555555")

# Use Helvetica families as approximations for Bebas/DM Sans
# (System fonts; the brand fonts would require shipping TTF files in the repo)
FONT_DISPLAY = "Helvetica-Bold"      # stand-in for Bebas Neue
FONT_BODY = "Helvetica"               # stand-in for DM Sans
FONT_BODY_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"


def strip_html(s: str) -> str:
    """Remove <em>, <strong>, etc. for plain-text rendering."""
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return s


def wrap_text(text: str, font: str, size: float, max_width: float, c: canvas.Canvas) -> list:
    """Wrap text to fit max_width. Returns a list of lines."""
    words = text.split()
    if not words:
        return []
    lines = []
    current = words[0]
    for w in words[1:]:
        test = current + " " + w
        if c.stringWidth(test, font, size) <= max_width:
            current = test
        else:
            lines.append(current)
            current = w
    lines.append(current)
    return lines


def render_brand_stripe(c, page_w):
    """Orange→magenta gradient stripe at top. ReportLab doesn't do gradients
    natively, so fake it with thin vertical bands."""
    stripe_h = 8
    n_bands = 60
    band_w = page_w / n_bands
    for i in range(n_bands):
        t = i / (n_bands - 1)
        # Lerp orange → magenta
        r = ORANGE.red + t * (MAGENTA.red - ORANGE.red)
        g = ORANGE.green + t * (MAGENTA.green - ORANGE.green)
        b = ORANGE.blue + t * (MAGENTA.blue - ORANGE.blue)
        c.setFillColor(Color(r, g, b))
        c.rect(i * band_w, LETTER[1] - stripe_h, band_w, stripe_h, fill=1, stroke=0)


def render_pdf(content: dict, output_path: Path):
    """Render a single printable PDF for one wiki page."""
    page_w, page_h = LETTER
    c = canvas.Canvas(str(output_path), pagesize=LETTER)

    # Page background: subtle off-white (printable on any printer)
    c.setFillColor(white)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # Brand stripe top
    render_brand_stripe(c, page_w)

    # Header zone — THF identity
    y = page_h - 0.8 * inch
    c.setFillColor(NAVY)
    c.setFont(FONT_DISPLAY, 14)
    c.drawString(0.6 * inch, y, "THE HUMAN FREQUENCY")

    c.setFillColor(ORANGE)
    c.setFont(FONT_BODY_BOLD, 8)
    c.drawString(0.6 * inch, y - 14, "FIND COMMON GROUND")

    # Right-aligned: "thehumanfrequency.net/human-os/<slug>"
    c.setFillColor(MUTED)
    c.setFont(FONT_BODY, 8)
    url = f"thehumanfrequency.net/human-os/{content['slug']}"
    c.drawRightString(page_w - 0.6 * inch, y, url)

    c.setFillColor(MUTED)
    c.setFont(FONT_BODY, 7)
    pillar_label = f"HUMAN OS WIKI · PAGE {content['page_num']} · {content['pillar']}"
    c.drawRightString(page_w - 0.6 * inch, y - 14, pillar_label)

    # Divider line
    c.setStrokeColor(HexColor("#dddddd"))
    c.setLineWidth(0.5)
    c.line(0.6 * inch, y - 30, page_w - 0.6 * inch, y - 30)

    # Title
    y = y - 60
    c.setFillColor(NAVY)
    c.setFont(FONT_DISPLAY, 28)
    title = content["title"].upper()
    c.drawString(0.6 * inch, y, title)

    # Subtitle (source chapter)
    y -= 22
    c.setFillColor(MUTED)
    c.setFont(FONT_ITALIC, 11)
    subtitle = f"Sourced from {content['source_chapter']}"
    c.drawString(0.6 * inch, y, subtitle)

    # Card zone — the wallet card
    card_x = 0.6 * inch
    card_w = page_w - 1.2 * inch
    card_y_top = y - 20

    # We'll render content first to compute height, then draw the card background
    # Simpler approach: pre-compute height
    items = content["printable_card"]["items"]
    pc_title = content["printable_card"]["title"]
    pc_sub = content["printable_card"]["subtitle"]

    # Estimate card height
    inner_pad = 22
    item_v_space = 14  # space between items
    # Estimate per-item height: 1 line for num + 1 wrapped for text + 1-2 wrapped for help
    text_inner_w = card_w - 2 * inner_pad
    item_heights = []
    for item in items:
        text_lines = wrap_text(strip_html(item["text"]), FONT_BODY_BOLD, 10, text_inner_w, c)
        help_lines = wrap_text(strip_html(item["help"]), FONT_ITALIC, 9, text_inner_w, c)
        h = 12 + 2 + len(text_lines) * 12 + 2 + len(help_lines) * 11 + item_v_space
        item_heights.append(h)

    title_block_h = 16 + 4 + 12 + 14 + 8  # title + subtitle + rule + spacing
    foot_block_h = 8 + 14 + 4
    card_h = title_block_h + sum(item_heights) + foot_block_h + 2 * inner_pad

    card_y_bot = card_y_top - card_h

    # Draw card background
    c.setFillColor(CREAM)
    c.roundRect(card_x, card_y_bot, card_w, card_h, 12, fill=1, stroke=0)

    # Brand accent on top of card
    c.setFillColor(ORANGE)
    c.rect(card_x, card_y_top - 3, card_w, 3, fill=1, stroke=0)

    # Card content
    cy = card_y_top - inner_pad - 14
    c.setFillColor(DARK_TEXT)
    c.setFont(FONT_DISPLAY, 13)
    c.drawCentredString(page_w / 2, cy, pc_title)
    cy -= 14
    c.setFillColor(MUTED)
    c.setFont(FONT_BODY, 9)
    c.drawCentredString(page_w / 2, cy, pc_sub)
    cy -= 12
    # Rule
    c.setStrokeColor(HexColor("#888888"))
    c.setLineWidth(0.7)
    c.line(card_x + inner_pad, cy, card_x + card_w - inner_pad, cy)
    cy -= 18

    # Items
    for item in items:
        # Item number/label
        c.setFillColor(ORANGE)
        c.setFont(FONT_DISPLAY, 9)
        c.drawString(card_x + inner_pad, cy, strip_html(item["num"]))
        cy -= 13
        # Item text (bold)
        c.setFillColor(DARK_TEXT)
        c.setFont(FONT_BODY_BOLD, 10)
        text_lines = wrap_text(strip_html(item["text"]), FONT_BODY_BOLD, 10, text_inner_w, c)
        for line in text_lines:
            c.drawString(card_x + inner_pad, cy, line)
            cy -= 12
        # Item help (italic)
        c.setFillColor(MUTED)
        c.setFont(FONT_ITALIC, 9)
        help_lines = wrap_text(strip_html(item["help"]), FONT_ITALIC, 9, text_inner_w, c)
        for line in help_lines:
            c.drawString(card_x + inner_pad, cy, line)
            cy -= 11
        cy -= item_v_space - 4

    # Bottom rule + foot
    cy -= 4
    c.setStrokeColor(HexColor("#888888"))
    c.setLineWidth(0.7)
    c.line(card_x + inner_pad, cy, card_x + card_w - inner_pad, cy)
    cy -= 12
    c.setFillColor(MUTED)
    c.setFont(FONT_DISPLAY, 8)
    c.drawCentredString(page_w / 2, cy, "THE HUMAN FREQUENCY · FIND COMMON GROUND")

    # Footer zone — print instructions + URL
    foot_y = 0.6 * inch
    c.setFillColor(NAVY)
    c.setFont(FONT_BODY_BOLD, 9)
    c.drawString(0.6 * inch, foot_y + 28, "PRINT INSTRUCTIONS")
    c.setFont(FONT_BODY, 8.5)
    c.setFillColor(MUTED)
    c.drawString(0.6 * inch, foot_y + 14, "Fold this card in half along the horizontal center for a wallet-sized version,")
    c.drawString(0.6 * inch, foot_y, "or print on cardstock and laminate for the fridge or office wall.")

    # Right side: read full page link
    c.setFillColor(NAVY)
    c.setFont(FONT_BODY_BOLD, 9)
    c.drawRightString(page_w - 0.6 * inch, foot_y + 28, "READ THE FULL PAGE")
    c.setFillColor(ORANGE)
    c.setFont(FONT_BODY, 8.5)
    c.drawRightString(page_w - 0.6 * inch, foot_y + 14, f"thehumanfrequency.net/human-os/{content['slug']}")
    c.setFillColor(MUTED)
    c.setFont(FONT_BODY, 8.5)
    c.drawRightString(page_w - 0.6 * inch, foot_y, f"For the mechanism, the protocol, and citations.")

    # Page number / version stamp
    c.setFillColor(HexColor("#aaaaaa"))
    c.setFont(FONT_BODY, 7)
    c.drawCentredString(page_w / 2, 0.3 * inch, f"© 2026 The Human Frequency Inc. — v1 · {content['date_published']}")

    c.showPage()
    c.save()


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 generate-printable.py <content.json> <output.pdf>")
        sys.exit(1)
    content = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    render_pdf(content, out)
    print(f"  Wrote {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
