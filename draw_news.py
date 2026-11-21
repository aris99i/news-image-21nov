#!/usr/bin/env python3
"""Draw the front page of THE WORLD for Saturday, 21 November 2026.

One deterministic image: no timestamps, no randomness. Every story is a
verified fact from the 21 November 2026 news list supplied for this entry.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (163, 18, 18)
BLUE = (47, 111, 178)
GREEN = (58, 158, 79)
LIGHT_BLUE = (120, 170, 215)
GREY = (90, 86, 76)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

# (headline, body) for the 11 stories below the lead.
STORIES = [
    ("AI Sell-Off Wipes Out Nasdaq\u2019s 2026 Gains",
     "The S&P 500 fell 3.7% into correction; the Nasdaq slid 5.28%."),
    ("UK\u2013EU Sign Biggest Post-Brexit Deals",
     "Three pacts on food trade, carbon markets and youth mobility."),
    ("COP31 Runs Past Deadline in Antalya",
     "Climate talks deadlocked over fossil fuels as 200 nations failed to agree."),
    ("Houthi Missiles Target Riyadh Again",
     "The Saudi-led coalition intercepted three missiles for a third night."),
    ("FBI Database Reportedly Hacked",
     "FBI and Agriculture Department systems hit as US outages continue."),
    ("Quake Shakes Peru\u2019s Andes",
     "A magnitude 6.9 earthquake struck the Peruvian Andes."),
    ("Pill Beats Pancreatic Cancer in Trial",
     "Daraxonrasib made tumours undetectable in one in 12 patients."),
    ("Gen Z Protests Sweep Europe",
     "Demonstrations spread across 25 countries over wars, costs and climate."),
    ("Palisades Fire Arson Verdict",
     "A man was convicted of starting the deadly Los Angeles fire."),
    ("Trump Calls Putin \u2018My Friend\u2019",
     "Zelensky replied that Putin is a \u2018killer\u2019 as Trump defended his ties."),
    ("Bitcoin Slides Toward $62K",
     "Crypto liquidations topped $2 billion in 24 hours."),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to pixel width, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(draw, cx, cy, r):
    """Stylised globe: blue ocean, green land blobs, thin grid lines."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE, outline=INK, width=3)
    # Land blobs (abstract continents), clipped roughly inside the circle.
    blobs = [
        [(cx - 95, cy - 75), (cx - 30, cy - 95), (cx - 5, cy - 55),
         (cx - 55, cy - 30), (cx - 100, cy - 40)],
        [(cx + 15, cy - 70), (cx + 75, cy - 85), (cx + 95, cy - 35),
         (cx + 45, cy - 20), (cx + 10, cy - 35)],
        [(cx - 70, cy + 15), (cx - 10, cy + 5), (cx + 5, cy + 55),
         (cx - 45, cy + 80), (cx - 85, cy + 50)],
        [(cx + 35, cy + 25), (cx + 90, cy + 35), (cx + 80, cy + 85),
         (cx + 40, cy + 95), (cx + 25, cy + 55)],
    ]
    for blob in blobs:
        draw.polygon(blob, fill=GREEN)
    # Grid: meridians and parallels, clipped by the circle via short arcs.
    for k in (-0.55, 0.0, 0.55):
        x = cx + int(k * r)
        h = int(r * (1 - k * k) ** 0.5)
        draw.line([(x, cy - h), (x, cy + h)], fill=LIGHT_BLUE, width=2)
    for k in (-0.5, 0.0, 0.5):
        y = cy + int(k * r)
        wdt = int(r * (1 - k * k) ** 0.5)
        draw.line([(cx - wdt, y), (cx + wdt, y)], fill=LIGHT_BLUE, width=2)
    # Highlight arc top-left.
    draw.arc([cx - r + 12, cy - r + 12, cx + r - 40, cy + r - 40],
             start=150, end=250, fill=(255, 255, 255), width=6)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    f_mast = font(SERIF_BOLD, 96)
    d.text((W // 2, 24), "THE WORLD", font=f_mast, fill=INK, anchor="ma")
    f_date = font(SANS_BOLD, 21)
    d.text((36, 138), "SATURDAY, 21 NOVEMBER 2026", font=f_date, fill=INK)
    d.text((988, 138), "EDITION No. 21", font=f_date, fill=INK, anchor="ra")
    d.line([(36, 168), (988, 168)], fill=INK, width=3)
    d.line([(36, 173), (988, 173)], fill=INK, width=1)

    # ---- Lead story (left) ----
    f_kick = font(SANS_BOLD, 20)
    d.text((36, 192), "WAR IN UKRAINE", font=f_kick, fill=RED)
    f_lead_head = font(SERIF_BOLD, 40)
    head_lines = wrap(d, "Russia\u2019s Biggest Barrage Hits Kyiv \u2014 and Poland",
                      f_lead_head, 620)
    y = 222
    for line in head_lines:
        d.text((36, y), line, font=f_lead_head, fill=INK)
        y += 48
    f_lead_body = font(SERIF, 20)
    body_lines = wrap(
        d,
        "More than 400 drones and 110 missiles struck Ukraine overnight, "
        "killing at least eight in Kyiv; two missiles and a suspected drone "
        "came down in Poland, which Warsaw called a deliberate provocation.",
        f_lead_body, 620)
    y += 6
    for line in body_lines:
        d.text((36, y), line, font=f_lead_body, fill=INK)
        y += 27

    # ---- Globe (right) ----
    draw_globe(d, 834, 292, 132)
    f_cap = font(SANS_ITALIC, 15)
    cap = wrap(d, "Kyiv under fire as Russian missiles also land in Poland.",
               f_cap, 300)
    cy = 434
    for line in cap:
        d.text((834, cy), line, font=f_cap, fill=GREY, anchor="ma")
        cy += 19

    # ---- Rule above the story grid ----
    d.line([(36, 488), (988, 488)], fill=INK, width=2)

    # ---- Story grid: 3 columns, 4 / 4 / 3 stories ----
    cols = [STORIES[0:4], STORIES[4:8], STORIES[8:11]]
    x_starts = [36, 362, 688]
    col_w = 300
    f_story_head = font(SERIF_BOLD, 22)
    f_story_body = font(SANS, 16)
    y_top = 504
    max_y = y_top
    for x, stories in zip(x_starts, cols):
        y = y_top
        for headline, body in stories:
            lines = wrap(d, headline, f_story_head, col_w)
            for line in lines:
                d.text((x, y), line, font=f_story_head, fill=INK)
                y += 27
            y += 2
            blines = wrap(d, body, f_story_body, col_w)
            for line in blines:
                d.text((x, y), line, font=f_story_body, fill=INK)
                y += 20
            y += 12
        max_y = max(max_y, y)

    # ---- Footer ----
    d.line([(36, 988), (988, 988)], fill=INK, width=1)
    f_foot = font(SANS, 13)
    d.text((W // 2, 997),
           "All the news that fits on one page. Sources: One Turn, Horizon, "
           "BBC News, Al Jazeera, Guardian, Financial Times.",
           font=f_foot, fill=GREY, anchor="ma")

    print("grid bottom y =", max_y)
    img.save("entry.png")
    print("saved entry.png")


if __name__ == "__main__":
    main()
