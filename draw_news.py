#!/usr/bin/env python3
"""Draw the front page of THE WORLD for Saturday, 21 November 2026.

A single 1024x1024 newspaper page: masthead, a small globe sketch,
one lead story and eleven more stories in a two-column grid.
Deterministic: no randomness, no timestamps, no network.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN

INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (110, 110, 110)
BLUE = (28, 68, 128)
LIGHT_BLUE = (198, 222, 240)
GREEN = (74, 140, 74)
PAPER = (252, 250, 244)


def load_font(bold, size):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def wrap(draw, text, font, max_width):
    """Split text into lines that fit max_width, word by word."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_globe(draw, cx, cy, r):
    """A small stylised globe: blue disc, meridians and land blobs."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=LIGHT_BLUE, outline=BLUE, width=3)
    # meridians
    for k in (0.45, 0.8):
        w = int(r * k)
        draw.ellipse([cx - w, cy - r, cx + w, cy + r], outline=BLUE, width=2)
    # parallels
    for dy in (-r // 2, r // 2):
        w = int((r * r - dy * dy) ** 0.5)
        draw.line([cx - w, cy + dy, cx + w, cy + dy], fill=BLUE, width=2)
    # rough land masses
    draw.ellipse([cx - r + 8, cy - r + 12, cx - 6, cy - 2], fill=GREEN)
    draw.ellipse([cx + 2, cy + 2, cx + r - 10, cy + r - 12], fill=GREEN)
    draw.ellipse([cx - 4, cy - r + 6, cx + 12, cy - r + 22], fill=GREEN)


LEAD_HEADLINE = "Russia's Biggest Barrage Yet Hits Ukraine"
LEAD_SUMMARY = (
    "More than 400 drones and 110 missiles struck cities overnight and "
    "eight people were killed in Kyiv. Two missiles and a drone came down "
    "inside Poland, raising fears the war is spilling across borders."
)

STORIES = [
    ("AI Stocks Drag Wall Street Down",
     "The S&P 500 slid 3.7% as investors dumped artificial-intelligence "
     "shares in the sharpest sell-off in months."),
    ("UK and EU Strike New Trade Deal",
     "London and Brussels reached a fresh trade agreement, easing border "
     "checks and cutting costs for exporters."),
    ("Climate Talks Stall in Antalya",
     "COP31 negotiations deadlocked in Turkey as countries split over "
     "fossil-fuel language in the draft text."),
    ("Houthi Missiles Strike Riyadh",
     "Missiles fired from Yemen hit the Saudi capital, damaging buildings "
     "and rattling markets across the region."),
    ("FBI Database Breached",
     "Hackers broke into a Federal Bureau of Investigation database, "
     "exposing sensitive records and triggering an urgent probe."),
    ("Magnitude 6.9 Quake Shakes Peru",
     "A powerful earthquake rattled southern Peru, sending residents into "
     "the streets as damage reports came in."),
    ("Pancreatic Cancer Pill Shows Promise",
     "An experimental pill delivered encouraging early results against one "
     "of the deadliest cancers, researchers said."),
    ("Gen Z Protests Sweep 25 European Nations",
     "Young demonstrators marched across 25 countries, demanding action "
     "on housing, jobs and the climate."),
    ("Palisades Arsonist Found Guilty",
     "A jury convicted the man accused of starting the Palisades wildfire, "
     "closing a case that gripped California."),
    ("Trump, Putin and Zelensky: Diplomacy in Motion",
     "Fresh signals from Washington, Moscow and Kyiv kept hopes of a "
     "negotiated end to the war flickering."),
    ("Bitcoin Drops to $62,000",
     "Bitcoin tumbled to $62,000 as more than $2 billion in leveraged "
     "positions were liquidated in a single day."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    masthead_font = load_font(True, 84)
    date_font = load_font(False, 20)
    kicker_font = load_font(True, 16)
    lead_head_font = load_font(True, 36)
    lead_body_font = load_font(False, 18)
    head_font = load_font(True, 19)
    body_font = load_font(False, 14)
    foot_font = load_font(False, 13)

    # --- masthead -------------------------------------------------------
    title = "THE WORLD"
    tw = draw.textlength(title, font=masthead_font)
    draw.text(((W - tw) / 2, 26), title, font=masthead_font, fill=INK)
    date_line = "Saturday, 21 November 2026"
    dw = draw.textlength(date_line, font=date_font)
    draw.text(((W - dw) / 2, 118), date_line, font=date_font, fill=GREY)
    draw_globe(draw, 918, 76, 44)
    draw.line([MARGIN, 152, W - MARGIN, 152], fill=INK, width=3)
    draw.line([MARGIN, 158, W - MARGIN, 158], fill=INK, width=1)

    # --- lead story ------------------------------------------------------
    y = 176
    draw.text((MARGIN, y), "LEAD STORY", font=kicker_font, fill=RED)
    y += 26
    for line in wrap(draw, LEAD_HEADLINE, lead_head_font, CONTENT_W):
        draw.text((MARGIN, y), line, font=lead_head_font, fill=INK)
        y += 44
    y += 4
    for line in wrap(draw, LEAD_SUMMARY, lead_body_font, CONTENT_W):
        draw.text((MARGIN, y), line, font=lead_body_font, fill=INK)
        y += 24
    draw.line([MARGIN, 322, W - MARGIN, 322], fill=INK, width=2)

    # --- two-column grid: 11 stories + one markets box ------------------
    grid_top = 338
    col_w = (CONTENT_W - 16) // 2
    row_h = 100
    row_gap = 6
    for idx, (headline, summary) in enumerate(STORIES):
        row = idx // 2
        col = idx % 2
        x = MARGIN + col * (col_w + 16)
        cy = grid_top + row * (row_h + row_gap)
        lines = wrap(draw, headline, head_font, col_w)
        hy = cy
        for line in lines[:2]:
            draw.text((x, hy), line, font=head_font, fill=INK)
            hy += 23
        for line in wrap(draw, summary, body_font, col_w)[:2]:
            draw.text((x, hy), line, font=body_font, fill=(60, 60, 60))
            hy += 18

    # markets box in the last grid cell (row 5, column 1)
    bx = MARGIN + (col_w + 16)
    by = grid_top + 5 * (row_h + row_gap)
    draw.rectangle([bx, by, bx + col_w, by + row_h],
                   outline=INK, width=2)
    draw.text((bx + 12, by + 8), "MARKETS", font=kicker_font, fill=RED)
    market_font = load_font(True, 14)
    draw.text((bx + 12, by + 32), "S&P 500  -3.7%   |   Bitcoin  $62,000",
              font=market_font, fill=INK)
    draw.text((bx + 12, by + 56), "AI sell-off rattles Wall Street as crypto",
              font=body_font, fill=(60, 60, 60))
    draw.text((bx + 12, by + 76), "liquidations pass $2 billion.",
              font=body_font, fill=(60, 60, 60))

    # --- footer ----------------------------------------------------------
    draw.line([MARGIN, 972, W - MARGIN, 972], fill=GREY, width=1)
    foot = "THE WORLD  |  Saturday, 21 November 2026  |  make.fun bounty entry"
    fw = draw.textlength(foot, font=foot_font)
    draw.text(((W - fw) / 2, 984), foot, font=foot_font, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()
