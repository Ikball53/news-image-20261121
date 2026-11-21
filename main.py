"""Dense one-day world news poster for Saturday 21 November 2026.

Draws a 1024x1024 newspaper-style image with PIL: masthead, a dotted
world map with red story markers, then seven regional briefings holding
34 short items that were each reported on the date above.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
PAPER = (255, 253, 244)
INK = (18, 18, 18)
RULE = (40, 40, 40)
RED = (196, 24, 24)
OCEAN = (214, 231, 242)
LAND = (240, 224, 178)
LAND_EDGE = (150, 128, 84)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_B = str(FONT_DIR / "DejaVuSerif-Bold.ttf")
SANS = str(FONT_DIR / "DejaVuSans.ttf")
SANS_B = str(FONT_DIR / "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# Each item: headline, short gloss, longitude, latitude, glyph kind.
REGIONS = [
    ("NORTH AMERICA", (30, 70, 140), [
        ("Anthropic debuts at $2 trillion", "Wall Street mega-IPO", -74.0, 40.7, "money"),
        ("FBI & USDA databases hacked", "Washington breach reported", -77.0, 38.9, "shield"),
        ("Palisades fire arsonist convicted", "Los Angeles deadly blaze", -118.2, 34.0, "flame"),
        ("AI sell-off: S&P in correction", "global stocks slide sharply", -87.6, 41.8, "chart"),
        ("GTA 6: $4.9B day-one sales", "record launch shatters marks", -122.4, 37.8, "star"),
    ]),
    ("LATIN AMERICA", (0, 128, 80), [
        ("Peru Andes hit by 6.9 quake", "no casualties reported yet", -75.0, -9.0, "quake"),
        ("Bolsonaro hospitalised, gut block", "Brasilia emergency admission", -47.9, -15.8, "cross"),
        ("Salvadoran troops lose 2 in Haiti", "gang fight, Port-au-Prince", -72.3, 18.5, "shield"),
        ("Chile-Philippines FTA signed", "APEC trans-Pacific corridor", -70.6, -33.4, "hand"),
    ]),
    ("EUROPE", (70, 90, 180), [
        ("Russia: 400 drones hit Kyiv", "missiles land in Poland", 30.5, 50.4, "burst"),
        ("UK-EU sign 3 post-Brexit deals", "Brussels reset summit", 4.3, 50.8, "hand"),
        ("Denmark expels Russian diplomat", "alleged rapper kill plot", 12.5, 55.6, "shield"),
        ("Cost-of-living protests spread", "Rome leads European marches", 12.5, 41.9, "flag"),
        ("Spain heads to Nov 29 vote", "banking tax extension planned", -3.7, 40.4, "vote"),
        ("Pancreatic pill erases tumours", "1 in 12 undetectable, London", -0.1, 51.5, "cross"),
        ("BepiColombo enters Mercury orbit", "ESA-JAXA mission arrives", 8.6, 50.1, "orbit"),
    ]),
    ("MIDDLE EAST", (180, 110, 20), [
        ("COP31 overtime: fossil row", "Antalya deal still blocked", 30.7, 36.8, "leaf"),
        ("Trump weighs new Iran strikes", "Israel presses for action", 51.4, 35.7, "burst"),
        ("Houthis strike Saudi Arabia", "missiles cross Red Sea", 45.0, 24.0, "burst"),
        ("Israeli fire kills in Gaza", "West Bank tensions rise", 34.3, 31.5, "flame"),
        ("Hormuz tankers hit; drone down", "US-Iran talks stalled", 56.5, 27.0, "wave"),
    ]),
    ("AFRICA", (150, 60, 30), [
        ("Congo Ebola: 11,613 cases", "WHO keeps global emergency", 23.0, -2.0, "cross"),
        ("Phumzile Mlambo-Ngcuka dies, 71", "first woman deputy president", 18.4, -33.9, "star"),
        ("700k displaced in S. Ethiopia", "conflict drives exodus", 38.0, 7.0, "flag"),
        ("Somalia expels UAE ambassador", "opposition rejects talks", 45.3, 2.0, "shield"),
        ("S. Africa holds rate at 7.25%", "split 4-3 bank vote", 28.0, -26.2, "chart"),
    ]),
    ("ASIA", (160, 30, 90), [
        ("Nikkei plunges 5.1% in sell-off", "Japan inflation 2.2%", 139.7, 35.7, "chart"),
        ("India tainted alcohol: 11 dead", "180+ hospitalised", 77.2, 28.6, "cross"),
        ("Kim inspects factories post-snub", "no Trump meeting in Asia", 125.7, 39.0, "flag"),
        ("India-Japan space & missile pact", "Tokyo 2+2 defence deal", 135.5, 34.6, "orbit"),
        ("China: Japan must fix attitude", "Xi-Takaichi APEC chill", 116.4, 39.9, "shield"),
    ]),
    ("OCEANIA / PACIFIC", (0, 130, 150), [
        ("N. Melbourne into 4th AFLW final", "beat Sydney at Princes Park", 144.9, -37.8, "ball"),
        ("Timor 6.8 quake felt in Darwin", "Banda Sea, no damage", 125.5, -10.5, "quake"),
        ("Cyclone Xavier fades near Samoa", "ex-Category 5 weakens", -171.7, -13.8, "wave"),
    ]),
]

# Rough continent outlines in (lon, lat) pairs for the locator map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-78, 58), (-76, 50), (-70, 44), (-70, 42), (-74, 39),
     (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-89, 30), (-94, 29),
     (-97, 26), (-97, 16), (-94, 17), (-90, 14), (-83, 9), (-79, 9),
     (-81, 13), (-84, 16), (-87, 21), (-90, 21), (-91, 19), (-97, 16),
     (-102, 18), (-105, 20), (-110, 23), (-114, 29), (-117, 33), (-122, 37),
     (-124, 46), (-123, 49), (-130, 56), (-140, 60), (-155, 60), (-165, 60)],
    [(-79, 9), (-75, 10), (-72, 12), (-68, 11), (-62, 10), (-55, 6),
     (-50, 0), (-44, -3), (-35, -8), (-39, -13), (-39, -18), (-41, -23),
     (-48, -26), (-52, -33), (-58, -35), (-62, -39), (-65, -41), (-65, -45),
     (-67, -50), (-69, -52), (-71, -54), (-74, -50), (-74, -44), (-73, -37),
     (-71, -30), (-70, -20), (-70, -18), (-75, -15), (-77, -12), (-81, -6),
     (-81, -1), (-80, 3), (-77, 7)],
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 49), (2, 51),
     (5, 53), (8, 55), (8, 57), (10, 59), (5, 58), (5, 60), (10, 63),
     (14, 67), (18, 69), (25, 71), (31, 70), (40, 67), (45, 68), (50, 69),
     (60, 69), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73),
     (130, 72), (140, 72), (150, 70), (160, 69), (170, 67), (178, 65),
     (170, 60), (162, 58), (158, 52), (150, 50), (142, 50), (140, 40),
     (135, 35), (129, 33), (122, 31), (120, 25), (110, 20), (108, 15),
     (106, 9), (103, 5), (100, 7), (98, 10), (97, 16), (92, 16), (91, 22),
     (88, 22), (86, 20), (80, 13), (77, 8), (72, 20), (66, 25), (61, 25),
     (57, 27), (52, 28), (50, 29), (48, 30), (43, 12), (38, 20), (35, 28),
     (36, 36), (30, 36), (27, 37), (23, 36), (19, 40), (12, 44), (7, 44),
     (3, 43), (3, 42), (0, 39), (-2, 37)],
    [(-17, 15), (-16, 20), (-15, 25), (-10, 29), (-6, 35), (0, 36), (10, 37),
     (11, 34), (20, 32), (30, 31), (32, 31), (34, 28), (35, 24), (37, 22),
     (39, 20), (40, 15), (43, 12), (48, 11), (51, 12), (51, 10), (48, 5),
     (42, 0), (40, -5), (40, -10), (36, -18), (36, -22), (33, -26),
     (28, -33), (20, -35), (17, -32), (12, -18), (13, -12), (9, -1),
     (9, 4), (4, 6), (-2, 5), (-8, 4), (-13, 8), (-17, 12)],
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (144, -38), (147, -38),
     (150, -37), (153, -27), (153, -22), (150, -22), (146, -19), (145, -15),
     (142, -11), (142, -14), (141, -17), (136, -15), (135, -12), (132, -11),
     (126, -14), (122, -17), (117, -20), (114, -22)],
    [(167, -45), (169, -43), (172, -41), (174, -39), (176, -38), (178, -37),
     (175, -36), (173, -35), (171, -41), (168, -46)],
]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    px = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    py = y0 + (78.0 - lat) / 138.0 * (y1 - y0)
    return px, py


def draw_glyph(draw, kind, cx, cy, colour):
    r = 5
    if kind == "cross":
        draw.line([(cx, cy - r), (cx, cy + r)], fill=colour, width=2)
        draw.line([(cx - r, cy), (cx + r, cy)], fill=colour, width=2)
    elif kind == "chart":
        draw.line([(cx - r, cy + 2), (cx - 1, cy - 1), (cx + 2, cy + 1),
                   (cx + r, cy - r)], fill=colour, width=2)
    elif kind == "quake":
        draw.line([(cx - r, cy), (cx - 2, cy - r), (cx + 1, cy + r),
                   (cx + r, cy)], fill=colour, width=2)
    elif kind == "burst":
        for dx, dy in [(0, -r), (r, 0), (0, r), (-r, 0), (4, -4), (-4, -4),
                       (4, 4), (-4, 4)]:
            draw.line([(cx, cy), (cx + dx, cy + dy)], fill=colour, width=1)
    elif kind == "wave":
        draw.arc([cx - r, cy - 3, cx, cy + 3], 180, 360, fill=colour, width=2)
        draw.arc([cx, cy - 3, cx + r, cy + 3], 180, 360, fill=colour, width=2)
    elif kind == "leaf":
        draw.ellipse([cx - 4, cy - r, cx + 4, cy + r], outline=colour, width=2)
        draw.line([(cx, cy - r), (cx, cy + r)], fill=colour, width=1)
    elif kind == "orbit":
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=colour)
        draw.ellipse([cx - r, cy - 2, cx + r, cy + 2], outline=colour, width=1)
    elif kind == "ball":
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=2)
        draw.line([(cx - r, cy), (cx + r, cy)], fill=colour, width=1)
    elif kind == "money":
        draw.text((cx - 3, cy - 6), "$", fill=colour, font=font(SANS_B, 11))
    elif kind == "flame":
        draw.polygon([(cx, cy - r), (cx + 4, cy + 3), (cx, cy + 1),
                      (cx - 4, cy + 3)], fill=colour)
    elif kind == "flag":
        draw.line([(cx - 3, cy - r), (cx - 3, cy + r)], fill=colour, width=2)
        draw.polygon([(cx - 3, cy - r), (cx + r, cy - 3), (cx - 3, cy)],
                     fill=colour)
    elif kind == "vote":
        draw.rectangle([cx - r, cy - 3, cx + r, cy + r], outline=colour, width=2)
        draw.line([(cx - 3, cy - r), (cx + 3, cy + 1)], fill=colour, width=2)
    elif kind == "hand":
        draw.ellipse([cx - r, cy - 3, cx + r, cy + 3], outline=colour, width=2)
    else:  # shield / star fallback: filled diamond
        draw.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
                     fill=colour)


def fit_text(draw, text, fnt, max_w):
    while text and draw.textlength(text, font=fnt) > max_w:
        text = text[:-1]
    return text


def build_poster():
    img = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    d = ImageDraw.Draw(img)
    total = sum(len(items) for _, _, items in REGIONS)

    # Masthead
    d.rectangle([0, 0, CANVAS, 10], fill=INK)
    d.text((CANVAS // 2, 34), "THE WORLD IN ONE DAY", fill=INK,
           font=font(SERIF_B, 34), anchor="mm")
    d.text((CANVAS // 2, 62),
           "Saturday 21 November 2026  •  %d dated stories  •  7 regions" % total,
           fill=INK, font=font(SANS_B, 16), anchor="mm")
    d.text((CANVAS // 2, 84),
           "COP31 overtime  •  Kyiv barrage hits Poland  •  Peru 6.9 quake",
           fill=RED, font=font(SANS_B, 15), anchor="mm")
    d.line([(14, 100), (CANVAS - 14, 100)], fill=RULE, width=2)

    # Locator map
    map_box = (14, 108, CANVAS - 14, 300)
    d.rectangle(map_box, fill=OCEAN, outline=RULE, width=1)
    for shape in CONTINENTS:
        pts = [project(lon, lat, map_box) for lon, lat in shape]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for _, colour, items in REGIONS:
        for _, _, lon, lat, _ in items:
            px, py = project(lon, lat, map_box)
            d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                      outline=(255, 255, 255), width=1)
    d.text((20, 306), "Red dots = story locations", fill=INK,
           font=font(SANS, 10))
    d.text((CANVAS - 20, 306), "All items reported 21 Nov 2026", fill=INK,
           font=font(SANS, 10), anchor="ra")

    # Regional briefings in two columns
    col_w = (CANVAS - 42) // 2
    columns = [(14, REGIONS[:3]), (14 + col_w + 14, REGIONS[3:])]
    head_f = font(SANS_B, 14)
    head_txt_f = font(SANS_B, 11)
    gloss_f = font(SANS, 9)
    row_h = 25
    for col_x, group in columns:
        y = 322
        for name, colour, items in group:
            d.rectangle([col_x, y, col_x + col_w, y + 22], fill=colour)
            for i, chip in enumerate([(255, 255, 255), (255, 210, 60), RED]):
                cx0 = col_x + col_w - 92 + i * 11
                d.rectangle([cx0, y + 6, cx0 + 9, y + 16], fill=chip)
            d.text((col_x + 8, y + 11), name, fill=(255, 255, 255),
                   font=head_f, anchor="lm")
            d.text((col_x + col_w - 8, y + 10), "%d stories" % len(items),
                   fill=(255, 255, 255), font=gloss_f, anchor="rm")
            y += 24
            for headline, gloss, _, _, kind in items:
                d.rectangle([col_x, y, col_x + col_w, y + row_h - 2],
                            fill=(255, 255, 255), outline=(225, 218, 198))
                draw_glyph(d, kind, col_x + 11, y + (row_h - 2) // 2, colour)
                tx = col_x + 24
                head = fit_text(d, headline, head_txt_f, col_w - 30)
                d.text((tx, y + 3), head, fill=INK, font=head_txt_f)
                sub = fit_text(d, gloss, gloss_f, col_w - 30)
                d.text((tx, y + 16), sub, fill=(85, 85, 85), font=gloss_f)
                y += row_h
            y += 8

    # Filler brief under the left column so the sheet reads full-bleed
    note_y = 852
    d.rectangle([14, note_y, 14 + col_w, note_y + 60], fill=(255, 248, 220),
                outline=RULE, width=1)
    d.text((24, note_y + 8), "THE DAY IN BRIEF", fill=RED, font=font(SANS_B, 12))
    d.text((24, note_y + 26), "War, markets and climate dominated Saturday:",
           fill=INK, font=font(SANS, 10))
    d.text((24, note_y + 40), "Kyiv barrage, AI sell-off, COP31 deadlock.",
           fill=INK, font=font(SANS, 10))

    # Bottom ticker band: three extra same-day briefs
    tick_y = CANVAS - 104
    d.rectangle([14, tick_y, CANVAS - 14, tick_y + 70], fill=(24, 24, 24))
    tickers = [
        ("MARKETS", "Nikkei -5.1%  •  S&P correction  •  XRP -10%  •  ASX worst week since Covid"),
        ("SCIENCE & SPORT", "BepiColombo at Mercury  •  Verstappen Vegas pole  •  Kane out months"),
    ]
    ty = tick_y + 8
    for label, line in tickers:
        d.text((26, ty), label, fill=(255, 210, 60), font=font(SANS_B, 11))
        d.text((26, ty + 14), line, fill=(255, 255, 255), font=font(SANS, 11))
        ty += 28
    d.text((CANVAS // 2, CANVAS - 18),
           "Sources: Reuters, AP, BBC, France 24 and regional wires, 21 Nov 2026",
           fill=(90, 90, 90), font=font(SANS, 10), anchor="mm")
    d.rectangle([0, CANVAS - 8, CANVAS, CANVAS], fill=INK)
    return img


def main():
    here = Path(__file__).resolve().parent
    poster = build_poster()
    poster.save(here / "entry.png", "PNG")
    out_dir = Path("/output")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        poster.save(out_dir / "entry.png", "PNG")
    except OSError:
        pass
    print("wrote entry.png", poster.size)


if __name__ == "__main__":
    main()
