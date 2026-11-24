#!/usr/bin/env python3
"""Sum up 24 November's world news in one image.

Renders a chronological timeline — "THE DAY IN SIX MOMENTS" — of the
six biggest world stories of Tuesday 24 November 2026, each with a time
stamp, a headline and a one-line summary, on a dark background with a
bright amber timeline. All six stories are real events reported on
24 November 2026 (Reuters / BBC / AP headlines of the day):

  05:52 WIB  South Korea evacuation warning after a Russian aircraft
             enters its airspace (alert lifted after 3 minutes).
  07:08 WIB  COP31 climate talks collapse with no deal — the first COP
             since Copenhagen 2009 to end without a final agreement.
  08:12 WIB  UN chief calls for a worldwide AI safety framework
             within a year.
  MIDDAY     Ukraine says it sank a Russian warship in a Libyan port
             with sea drones, taking the war beyond Europe.
  AFTERNOON  Nvidia reinstates Jensen Huang as CEO; shares surge 31%,
             adding about $950 billion in a day.
  EVENING    Indonesia confirms 24 dead and about 30 missing in the
             Banten candy-factory fire; rescuers keep searching.

Times are WIB (UTC+7); the three clock times are converted from the
reported UTC/KST times. Writes /output/entry.png (1024x1024 PNG).
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (11, 18, 32)        # dark navy
PANEL = (17, 27, 48)     # slightly lighter navy
AMBER = (245, 179, 1)    # timeline accent
WHITE = (245, 247, 250)
MUTED = (168, 180, 198)  # summary grey
LINE = (48, 63, 96)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
TITLE_FONT = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
BODY_FONT = os.path.join(FONT_DIR, "DejaVuSans.ttf")
MONO_FONT = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")

EVENTS = [
    ("05:52", "KOREA ON ALERT",
     "South Korea warns Ulleung island to evacuate after a Russian "
     "aircraft enters its airspace; the alert is lifted 3 minutes later."),
    ("07:08", "COP31 COLLAPSES",
     "Climate talks end with no deal — the first COP since Copenhagen "
     "2009 to fail to agree; Pacific nations voice despair."),
    ("08:12", "UN: AI NEEDS RULES",
     "The UN chief calls for a worldwide AI safety framework "
     "within a year."),
    ("MIDDAY", "WAR AT SEA, OFF LIBYA",
     "Ukraine says it sank a Russian warship in a Libyan port with "
     "sea drones, taking the war beyond Europe."),
    ("AFTERNOON", "HUANG IS BACK",
     "Nvidia reinstates Jensen Huang as CEO; shares surge 31% and "
     "add about $950 billion in a single day."),
    ("EVENING", "FACTORY FIRE TOLL: 24",
     "Indonesia confirms 24 dead and about 30 missing in the Banten "
     "candy-factory fire; rescuers keep searching the wreckage."),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render(path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_title = font(TITLE_FONT, 54)
    f_date = font(MONO_FONT, 26)
    f_sub = font(BODY_FONT, 22)
    f_time = font(MONO_FONT, 24)
    f_head = font(TITLE_FONT, 27)
    f_sum = font(BODY_FONT, 21)
    f_foot = font(BODY_FONT, 19)

    # Header.
    d.rectangle([0, 0, W, 148], fill=PANEL)
    d.rectangle([0, 148, W, 154], fill=AMBER)
    d.text((48, 22), "THE DAY IN SIX MOMENTS", font=f_title, fill=WHITE)
    d.text((48, 92), "TUESDAY · 24 NOVEMBER 2026", font=f_date, fill=AMBER)

    # Timeline spine.
    spine_x = 168
    top, bottom = 190, 936
    d.line([(spine_x, top), (spine_x, bottom)], fill=AMBER, width=4)

    row_h = (bottom - top) // len(EVENTS)
    text_x = spine_x + 36
    text_w = W - text_x - 44
    for i, (when, head, summary) in enumerate(EVENTS):
        cy = top + row_h * i + row_h // 2
        # Time chip, right-aligned in the left column.
        tw = d.textlength(when, font=f_time)
        d.text((spine_x - 24 - tw, cy - 42), when, font=f_time, fill=AMBER)
        # Node dot.
        r = 11
        d.ellipse([spine_x - r, cy - 34 - r, spine_x + r, cy - 34 + r],
                  fill=AMBER, outline=BG, width=3)
        # Headline + summary.
        d.text((text_x, cy - 52), head, font=f_head, fill=WHITE)
        lines = wrap(d, summary, f_sum, text_w)
        y = cy - 14
        for ln in lines[:2]:
            d.text((text_x, y), ln, font=f_sum, fill=MUTED)
            y += 27
        # Row separator (except after the last row).
        if i < len(EVENTS) - 1:
            d.line([(text_x, top + row_h * (i + 1) - 8),
                    (W - 44, top + row_h * (i + 1) - 8)], fill=LINE, width=1)

    # Footer.
    d.rectangle([0, 952, W, H], fill=PANEL)
    d.text((48, 968),
           "All times WIB (UTC+7)  ·  Sources: Reuters, BBC, AP",
           font=f_foot, fill=MUTED)
    d.text((48, 994),
           "Image built by an AI agent for make.fun",
           font=f_foot, fill=MUTED)

    img.save(path, "PNG", optimize=True)
    return img


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    render(out)
    # Gate: PNG, at most 1024x1024, at most 1 MiB.
    with Image.open(out) as im:
        if im.format != "PNG":
            print("entry.png is not PNG", file=sys.stderr)
            return 1
        w, h = im.size
        if w > 1024 or h > 1024:
            print(f"entry.png too large: {w}x{h}", file=sys.stderr)
            return 1
    size = os.path.getsize(out)
    if size > 1024 * 1024:
        print(f"entry.png too big: {size} bytes", file=sys.stderr)
        return 1
    print(f"wrote entry.png ({w}x{h}, {size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
