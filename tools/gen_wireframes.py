#!/usr/bin/env python3
"""
gen_wireframes.py

Generates 8 blueprint-style wireframe screens (SVG) for a 3D educational
game, per the URM visual canon:

- Background cream #fdfaf4, panel fill cream-2 #f7f2e7, ink #1a1a1a text,
  hairlines #e7e1d3, muted text #6b665c, single accent orange #e87722.
- No gradients, no shadows, no glassmorphism, no dark backgrounds.
- Fraunces/Georgia/serif for screen titles; Inter/system-ui/sans-serif for
  everything else.
- 1-1.5px stroked rectangles, rounded corners (rx=4), short real labels.

No external dependencies -- pure string templating of SVG markup.

Run:  python3 gen_wireframes.py
Output: /home/user/workspace/urm/wireframes/w1-entry.svg ... w8-guardian.svg
"""

import os
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------------------
# Canon constants
# ---------------------------------------------------------------------------

BG = "#fdfaf4"
PANEL = "#f7f2e7"
INK = "#1a1a1a"
HAIR = "#e7e1d3"
MUTED = "#6b665c"
ACCENT = "#e87722"

FONT_SERIF = "Fraunces, Georgia, serif"
FONT_SANS = "Inter, system-ui, sans-serif"

W, H = 1200, 760

OUT_DIR = "/home/user/workspace/urm/wireframes"

# ---------------------------------------------------------------------------
# Text-fit checker
# ---------------------------------------------------------------------------
# We cannot measure real glyph metrics (fonts may not be installed), so we
# use conservative average-advance-width estimates and hard-assert every
# text element fits within its declared container with >=12px padding on
# each side. This function raises on any failure so we can iterate the
# layout until the script runs clean.

_registered_texts = []  # for overlap checking: list of (x0,y0,x1,y1,label,screen)


def est_width(text, size, font="sans"):
    factor = 0.56 if font == "serif" else 0.58
    return factor * size * len(text)


def check_fit(label, text, size, font, box, pad=12, screen="?"):
    """box = (x, y, w, h) the container the text must sit inside, with pad
    on each side. Raises AssertionError with a clear message on failure."""
    x, y, w, h = box
    tw = est_width(text, size, font)
    avail = w - 2 * pad
    if tw > avail:
        raise AssertionError(
            f"[{screen}] TEXT OVERFLOW '{label}': text={text!r} size={size} "
            f"font={font} est_width={tw:.1f} > avail={avail:.1f} "
            f"(box w={w}, pad={pad})"
        )
    if size > h:
        # vertical sanity: font shouldn't be taller than the box allows
        raise AssertionError(
            f"[{screen}] TEXT TOO TALL '{label}': size={size} box_h={h}"
        )
    return tw


def register_text_bbox(screen, label, x_anchor, y_baseline, text, size, font,
                        anchor="start"):
    """Register an approximate bounding box for a rendered text element so
    we can later check for overlaps between any two text elements on the
    same screen."""
    tw = est_width(text, size, font)
    if anchor == "middle":
        x0 = x_anchor - tw / 2
    elif anchor == "end":
        x0 = x_anchor - tw
    else:
        x0 = x_anchor
    x1 = x0 + tw
    # baseline -> approximate top/bottom using standard cap-height/descender
    y0 = y_baseline - size * 0.8
    y1 = y_baseline + size * 0.25
    _registered_texts.append((screen, label, x0, y0, x1, y1))


def check_all_overlaps():
    """Check every pair of registered text bboxes *within the same screen*
    for overlap. Raises on first collision found."""
    by_screen = {}
    for rec in _registered_texts:
        by_screen.setdefault(rec[0], []).append(rec)
    for screen, items in by_screen.items():
        n = len(items)
        for i in range(n):
            for j in range(i + 1, n):
                _, li, x0i, y0i, x1i, y1i = items[i]
                _, lj, x0j, y0j, x1j, y1j = items[j]
                if x0i < x1j and x1i > x0j and y0i < y1j and y1i > y0j:
                    raise AssertionError(
                        f"[{screen}] TEXT OVERLAP between '{li}' and '{lj}': "
                        f"boxA=({x0i:.0f},{y0i:.0f},{x1i:.0f},{y1i:.0f}) "
                        f"boxB=({x0j:.0f},{y0j:.0f},{x1j:.0f},{y1j:.0f})"
                    )


# ---------------------------------------------------------------------------
# SVG primitive builders
# ---------------------------------------------------------------------------

def esc(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class Svg:
    def __init__(self, screen_id):
        self.screen = screen_id
        self.parts = []

    def raw(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=1.5, rx=4,
             dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
        )

    def line(self, x1, y1, x2, y2, stroke=HAIR, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>'
        )

    def circle(self, cx, cy, r, fill="none", stroke=INK, sw=1.5):
        self.parts.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def arc_path(self, d, stroke=INK, sw=1.5, fill="none"):
        self.parts.append(
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def text(self, x, y, s, size=14, font="sans", color=INK, weight="400",
              anchor="start", box=None, label=None, pad=12, letter_spacing=None):
        """Emit a <text> element AND run the fit/overlap bookkeeping.
        box: (x,y,w,h) container to validate against (required for safety,
        pass the visually intended container of this text)."""
        family = FONT_SERIF if font == "serif" else FONT_SANS
        lbl = label or s
        if box is not None:
            check_fit(lbl, s, size, font, box, pad=pad, screen=self.screen)
        register_text_bbox(self.screen, lbl, x, y, s, size, font, anchor=anchor)
        ls = f' letter-spacing="{letter_spacing}"' if letter_spacing else ""
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}" '
            f'text-anchor="{anchor}"{ls}>{esc(s)}</text>'
        )

    def image_placeholder(self, x, y, w, h, label, fill=PANEL, stroke=INK,
                            sw=1.5, size=13):
        """Rectangle with thin diagonal cross + centred label (the canon
        idiom for image/3D areas)."""
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw)
        self.line(x, y, x + w, y + h, stroke=HAIR, sw=1)
        self.line(x + w, y, x, y + h, stroke=HAIR, sw=1)
        # label on a small cream chip so the cross lines don't cross the glyphs
        tw = est_width(label, size, "sans")
        chip_pad = 10
        chip_w = tw + 4 * chip_pad
        chip_h = size + 14
        cx = x + w / 2
        cy = y + h / 2
        self.rect(cx - chip_w / 2, cy - chip_h / 2, chip_w, chip_h, fill=BG,
                   stroke=HAIR, sw=1, rx=3)
        self.text(cx, cy + size * 0.32, label, size=size, font="sans",
                   color=MUTED, anchor="middle",
                   box=(cx - chip_w / 2, cy - chip_h / 2, chip_w, chip_h),
                   label=f"imgph:{label}", pad=chip_pad)

    def chip(self, x, y, text_s, size=12, stroke=ACCENT, color=ACCENT,
              fill="none", pad_x=10, pad_y=6, anchor="start", label=None):
        """Small orange-outlined chip. Returns (w, h) used."""
        tw = est_width(text_s, size, "sans")
        w = tw + pad_x * 2
        h = size + pad_y * 2
        if anchor == "end":
            rx0 = x - w
        elif anchor == "middle":
            rx0 = x - w / 2
        else:
            rx0 = x
        self.rect(rx0, y, w, h, fill=fill, stroke=stroke, sw=1.5, rx=h / 2)
        self.text(rx0 + w / 2, y + h / 2 + size * 0.32, text_s, size=size,
                   font="sans", color=color, anchor="middle",
                   box=(rx0, y, w, h), label=label or f"chip:{text_s}",
                   pad=pad_x - 2)
        return w, h

    def pill_status(self, x, y, text_s, active, size=12, pad_x=10, pad_y=5,
                     label=None):
        stroke = ACCENT if active else HAIR
        color = ACCENT if active else INK
        tw = est_width(text_s, size, "sans")
        w = tw + pad_x * 2
        h = size + pad_y * 2
        self.rect(x, y, w, h, fill="none", stroke=stroke, sw=1.5, rx=h / 2)
        self.text(x + w / 2, y + h / 2 + size * 0.32, text_s, size=size,
                   font="sans", color=color, anchor="middle",
                   box=(x, y, w, h), label=label or f"pill:{text_s}",
                   pad=pad_x - 2)
        return w, h

    def stick_figure(self, x, y, w, h, label):
        """Small stick-figure placeholder box."""
        self.rect(x, y, w, h, fill=PANEL, stroke=INK, sw=1.5)
        cx = x + w / 2
        head_r = min(w, h) * 0.12
        top = y + h * 0.22
        self.circle(cx, top, head_r, fill="none", stroke=INK, sw=1.5)
        body_top = top + head_r
        body_bot = y + h * 0.68
        self.line(cx, body_top, cx, body_bot, stroke=INK, sw=1.5)
        armY = body_top + (body_bot - body_top) * 0.3
        self.line(cx - w * 0.16, armY + h * 0.06, cx + w * 0.16, armY - h * 0.02,
                   stroke=INK, sw=1.5)
        self.line(cx, body_bot, cx - w * 0.14, y + h * 0.86, stroke=INK, sw=1.5)
        self.line(cx, body_bot, cx + w * 0.14, y + h * 0.86, stroke=INK, sw=1.5)
        size = 11
        self.text(cx, y + h - 8, label, size=size, font="sans", color=MUTED,
                   anchor="middle", box=(x, y + h - 8 - size, w, size + 10),
                   label=f"stick:{label}")

    def padlock(self, x, y, s=16, stroke=MUTED):
        """Simple padlock glyph: rounded rect body + arc shackle."""
        body_h = s * 0.62
        body_y = y + s * 0.38
        self.rect(x, body_y, s, body_h, fill="none", stroke=stroke, sw=1.5, rx=2)
        r = s * 0.28
        cx = x + s / 2
        cy = body_y
        self.arc_path(
            f"M {cx - r:.1f} {cy:.1f} A {r:.1f} {r:.1f} 0 0 1 {cx + r:.1f} {cy:.1f}",
            stroke=stroke, sw=1.5,
        )

    def render(self):
        body = "\n  ".join(self.parts)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">\n'
            f'  <rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>\n'
            f'  {body}\n'
            f'</svg>\n'
        )


# ---------------------------------------------------------------------------
# Shared chrome: header (ID + title, section chip) and footer caption
# ---------------------------------------------------------------------------

MARGIN = 40
HEADER_H = 74
FOOTER_H = 44


def header(svg, screen_id, title, sections):
    # ID + title, top-left
    id_size = 13
    svg.text(MARGIN, 30, screen_id, size=id_size, font="sans", color=MUTED,
              weight="600", letter_spacing="0.5",
              box=(MARGIN, 12, 200, 22), label="header-id")
    title_size = 26
    svg.text(MARGIN, 60, title, size=title_size, font="serif", color=INK,
              weight="600", box=(MARGIN, 34, 640, 34), label="header-title")

    # section chip, top-right — width depends on text
    chip_label = "URM " + ", ".join(sections)
    tw = est_width(chip_label, 13, "sans")
    chip_pad_x = 14
    chip_w = tw + 2 * chip_pad_x
    chip_x = W - MARGIN - chip_w
    svg.chip(chip_x, 22, chip_label, size=13, pad_x=chip_pad_x, anchor="start",
              label="header-sections")

    svg.line(MARGIN, HEADER_H, W - MARGIN, HEADER_H, stroke=HAIR, sw=1.5)


def footer(svg, caption):
    y = H - 22
    svg.line(MARGIN, H - FOOTER_H, W - MARGIN, H - FOOTER_H, stroke=HAIR, sw=1.5)
    size = 13
    box = (MARGIN, y - size, W - 2 * MARGIN, size + 10)
    svg.text(MARGIN, y, caption, size=size, font="sans", color=MUTED,
              box=box, label="footer-caption")


CONTENT_TOP = HEADER_H + 26
CONTENT_BOTTOM = H - FOOTER_H - 20


# ---------------------------------------------------------------------------
# W1 — Entry: Three Doors
# ---------------------------------------------------------------------------

def build_w1():
    sid = "W1"
    svg = Svg(sid)
    header(svg, sid, "Entry — Three Doors", ["5.2", "5.3", "1.4"])

    hero = "We are here to protect you"
    hero_size = 22
    svg.text(W / 2, CONTENT_TOP + 14, hero, size=hero_size, font="serif",
              color=INK, anchor="middle",
              box=(MARGIN, CONTENT_TOP - 10, W - 2 * MARGIN, 40),
              label="hero-line")

    # Three large equal door cards
    row1_y = CONTENT_TOP + 50
    row1_h = 300
    gap = 24
    card_w = (W - 2 * MARGIN - 2 * gap) / 3
    doors = ["Mother", "Child", "Father"]
    for i, name in enumerate(doors):
        x = MARGIN + i * (card_w + gap)
        svg.rect(x, row1_y, card_w, row1_h, fill=PANEL, stroke=INK, sw=1.5)
        # door icon area
        icon_pad = 20
        icon_h = row1_h - 90
        svg.image_placeholder(x + icon_pad, row1_y + 20, card_w - 2 * icon_pad,
                                icon_h, "door art", size=13)
        label_y = row1_y + 20 + icon_h + 34
        svg.text(x + card_w / 2, label_y, name, size=20, font="serif",
                  color=INK, anchor="middle",
                  box=(x + 12, label_y - 24, card_w - 24, 30),
                  label=f"door-{name}")

    # Secondary thinner row of three small cards
    row2_y = row1_y + row1_h + 26
    row2_h = 90
    secs = ["Electric Utility", "Other Utility", "Enterprise"]
    for i, name in enumerate(secs):
        x = MARGIN + i * (card_w + gap)
        svg.rect(x, row2_y, card_w, row2_h, fill="none", stroke=HAIR, sw=1.5)
        svg.text(x + card_w / 2, row2_y + row2_h / 2 + 5, name, size=15,
                  font="sans", color=INK, anchor="middle",
                  box=(x + 12, row2_y + 10, card_w - 24, row2_h - 20),
                  label=f"sec-{name}")

    footer(svg, "First screen a visitor sees: three equal, login-free paths in, no account required to enter.")
    return svg


# ---------------------------------------------------------------------------
# W2 — Safety Notice and Consent Gate
# ---------------------------------------------------------------------------

def build_w2():
    sid = "W2"
    svg = Svg(sid)
    header(svg, sid, "Safety Notice and Consent Gate", ["2.1", "2.4", "2.6"])

    panel_x = MARGIN
    panel_y = CONTENT_TOP
    panel_w = W - 2 * MARGIN
    panel_h = 420
    svg.rect(panel_x, panel_y, panel_w, panel_h, fill=PANEL, stroke=INK, sw=1.5)

    ptitle = "This game does not have:"
    svg.text(panel_x + 24, panel_y + 34, ptitle, size=17, font="sans",
              color=INK, weight="600",
              box=(panel_x + 24, panel_y + 12, panel_w - 48, 28),
              label="panel-title")

    items = [
        "No chat", "No voice channels", "No friend requests", "No camera",
        "No microphone", "No uploads", "No ads or trackers", "No outbound links",
    ]
    cols = 2
    rows = 4
    grid_top = panel_y + 62
    cell_w = (panel_w - 48) / cols
    cell_h = (panel_h - 62 - 24) / rows
    box_s = 16
    for idx, item in enumerate(items):
        r = idx % rows
        c = idx // rows
        cx0 = panel_x + 24 + c * cell_w
        cy0 = grid_top + r * cell_h
        # checkbox glyph (empty box + faint diagonal to read as "absent/off")
        svg.rect(cx0, cy0 + cell_h / 2 - box_s / 2, box_s, box_s, fill=BG,
                  stroke=INK, sw=1.5, rx=3)
        tx = cx0 + box_s + 12
        ty = cy0 + cell_h / 2 + 5
        avail_w = cell_w - box_s - 12 - 12
        svg.text(tx, ty, item, size=14, font="sans", color=INK,
                  box=(tx - 12, cy0 + cell_h / 2 - 14, avail_w + 12, 28),
                  label=f"checklist-{item}")

    # Fictional imagery notice
    notice_y = panel_y + panel_h + 22
    notice_h = 46
    svg.rect(panel_x, notice_y, panel_w, notice_h, fill="none", stroke=HAIR, sw=1.5)
    notice_text = "Fictional imagery — all characters, places and events in this game are invented."
    svg.text(panel_x + 20, notice_y + notice_h / 2 + 5, notice_text, size=13,
              font="sans", color=MUTED,
              box=(panel_x + 20, notice_y + 8, panel_w - 40, notice_h - 16),
              label="fictional-imagery-notice")

    # Buttons
    btn_y = notice_y + notice_h + 26
    btn_h = 50
    btn1_w = 320
    btn2_w = 300
    svg.rect(panel_x, btn_y, btn1_w, btn_h, fill=ACCENT, stroke=ACCENT, sw=1.5)
    svg.text(panel_x + btn1_w / 2, btn_y + btn_h / 2 + 5, "I understand — continue",
              size=15, font="sans", color="#fdfaf4", anchor="middle",
              box=(panel_x + 16, btn_y + 8, btn1_w - 32, btn_h - 16),
              label="btn-continue")

    btn2_x = panel_x + btn1_w + 20
    svg.rect(btn2_x, btn_y, btn2_w, btn_h, fill="none", stroke=INK, sw=1.5)
    svg.text(btn2_x + btn2_w / 2, btn_y + btn_h / 2 + 5, "Skip the guided tour",
              size=15, font="sans", color=INK, anchor="middle",
              box=(btn2_x + 16, btn_y + 8, btn2_w - 32, btn_h - 16),
              label="btn-skip")

    footer(svg, "Consent gate stating plainly what is absent before any play begins, with an explicit continue action.")
    return svg


# ---------------------------------------------------------------------------
# W3 — Chapter Select
# ---------------------------------------------------------------------------

def build_w3():
    sid = "W3"
    svg = Svg(sid)
    header(svg, sid, "Chapter Select", ["4.4", "3.4", "3.3"])

    # language selector, top right of content area
    lang_text = "EN / FR / ES"
    lsize = 13
    tw = est_width(lang_text, lsize, "sans")
    lang_w = tw + 24
    lang_h = 30
    lang_x = W - MARGIN - lang_w
    lang_y = CONTENT_TOP
    svg.rect(lang_x, lang_y, lang_w, lang_h, fill="none", stroke=HAIR, sw=1.5, rx=15)
    svg.text(lang_x + lang_w / 2, lang_y + lang_h / 2 + 4, lang_text, size=lsize,
              font="sans", color=INK, anchor="middle",
              box=(lang_x, lang_y, lang_w, lang_h), label="lang-selector")

    grid_top = CONTENT_TOP + lang_h + 18
    cols, rows = 3, 2
    gap = 20
    card_w = (W - 2 * MARGIN - (cols - 1) * gap) / cols
    card_h = (CONTENT_BOTTOM - grid_top - (rows - 1) * gap) / rows

    chapters = [
        ("Chapter 1", "Starter Twin", "Build your first digital twin together.", True),
        ("Chapter 2", "What We Kept", "Sort family memories worth saving.", True),
        ("Chapter 3", "Four Lost Days", "Piece together a missing week.", True),
        ("Chapter 4", "Locked chapter", "Unlocks after Chapter 3.", False),
        ("Chapter 5", "Locked chapter", "Unlocks after Chapter 4.", False),
        ("Chapter 6", "Locked chapter", "Unlocks after Chapter 5.", False),
    ]

    for idx, (num, title, desc, unlocked) in enumerate(chapters):
        r = idx // cols
        c = idx % cols
        x = MARGIN + c * (card_w + gap)
        y = grid_top + r * (card_h + gap)
        stroke = INK if unlocked else HAIR
        svg.rect(x, y, card_w, card_h, fill=PANEL if unlocked else "none",
                  stroke=stroke, sw=1.5)

        thumb_pad = 16
        thumb_h = card_h * 0.5
        svg.image_placeholder(x + thumb_pad, y + thumb_pad,
                                card_w - 2 * thumb_pad, thumb_h,
                                "thumbnail", size=12)

        # chapter number chip (top-left over card, small muted text since not
        # the single active element — reserve orange only for unlocked
        # active state per canon; keep numbers plain ink small caps)
        num_y = y + thumb_pad + thumb_h + 24
        svg.text(x + thumb_pad, num_y, num, size=12, font="sans", color=MUTED,
                  weight="600",
                  box=(x + thumb_pad, num_y - 14, card_w - 2 * thumb_pad, 18),
                  label=f"chnum-{num}")

        title_y = num_y + 22
        title_size = 16
        if not unlocked:
            # padlock glyph beside title
            lock_s = 16
            svg.padlock(x + card_w - thumb_pad - lock_s, title_y - lock_s + 2,
                         s=lock_s, stroke=MUTED)
            title_avail_w = card_w - 2 * thumb_pad - lock_s - 8
        else:
            title_avail_w = card_w - 2 * thumb_pad
        svg.text(x + thumb_pad, title_y, title, size=title_size, font="serif",
                  color=INK if unlocked else MUTED,
                  box=(x + thumb_pad, title_y - 18, title_avail_w, 22),
                  label=f"chtitle-{num}")

        desc_y = title_y + 22
        svg.text(x + thumb_pad, desc_y, desc, size=12, font="sans", color=MUTED,
                  box=(x + thumb_pad, desc_y - 14, card_w - 2 * thumb_pad, 18),
                  label=f"chdesc-{num}")

    footer(svg, "Chapter map showing progression and locks; language switch stays visible while browsing.")
    return svg


# ---------------------------------------------------------------------------
# W4 — Play Surface: 3D HUD
# ---------------------------------------------------------------------------

def build_w4():
    sid = "W4"
    svg = Svg(sid)
    header(svg, sid, "Play Surface — 3D HUD", ["6.1", "7.2", "7.3", "9.4"])

    viewport_y = CONTENT_TOP
    viewport_h = CONTENT_BOTTOM - viewport_y
    svg.image_placeholder(MARGIN, viewport_y, W - 2 * MARGIN, viewport_h,
                            "3D viewport — WebGL 2.0 / glTF 2.0 scene", size=15)

    # top-left chapter title chip (over viewport)
    chap_text = "Chapter 3 — Four Lost Days"
    csize = 14
    tw = est_width(chap_text, csize, "sans")
    chip_w = tw + 28
    chip_h = 34
    cx = MARGIN + 16
    cy = viewport_y + 16
    svg.rect(cx, cy, chip_w, chip_h, fill=BG, stroke=HAIR, sw=1.5, rx=6)
    svg.text(cx + chip_w / 2, cy + chip_h / 2 + 5, chap_text, size=csize,
              font="sans", color=INK, anchor="middle",
              box=(cx, cy, chip_w, chip_h), label="hud-chapter-title")

    # top-right stand-up countdown pill
    pill_text = "Stand-Up in 7:42"
    psize = 14
    tw2 = est_width(pill_text, psize, "sans")
    pill_w = tw2 + 28
    pill_h = 34
    px = W - MARGIN - 16 - pill_w
    py = viewport_y + 16
    svg.rect(px, py, pill_w, pill_h, fill=BG, stroke=ACCENT, sw=1.5, rx=pill_h / 2)
    svg.text(px + pill_w / 2, py + pill_h / 2 + 5, pill_text, size=psize,
              font="sans", color=ACCENT, anchor="middle",
              box=(px, py, pill_w, pill_h), label="hud-standup-pill")

    # bottom-left control legend
    legend_w = 260
    legend_h = 96
    lx = MARGIN + 16
    ly = viewport_y + viewport_h - 16 - legend_h
    svg.rect(lx, ly, legend_w, legend_h, fill=BG, stroke=HAIR, sw=1.5, rx=6)
    controls = ["WASD  move", "Mouse  look", "Space  jump", "Esc  release mouse"]
    csize2 = 12
    for i, c in enumerate(controls):
        ty = ly + 22 + i * 19
        svg.text(lx + 14, ty, c, size=csize2, font="sans", color=MUTED,
                  box=(lx + 14, ty - 13, legend_w - 28, 17),
                  label=f"legend-{i}")

    # bottom-right camera rig diagram: nested boxes
    rig_w = 300
    rig_h = 150
    rx0 = W - MARGIN - 16 - rig_w
    ry0 = viewport_y + viewport_h - 16 - rig_h
    svg.rect(rx0, ry0, rig_w, rig_h, fill=BG, stroke=HAIR, sw=1.5, rx=6)

    outer_pad = 16
    outer_label = "CamYaw (yaw)"
    ox, oy = rx0 + outer_pad, ry0 + outer_pad
    ow, oh = rig_w - 2 * outer_pad, rig_h - 2 * outer_pad
    svg.rect(ox, oy, ow, oh, fill="none", stroke=INK, sw=1.5)
    svg.text(ox + 10, oy + 18, outer_label, size=12, font="sans", color=INK,
              box=(ox + 6, oy + 4, ow - 12, 18), label="rig-camyaw")

    mid_pad = 16
    mid_label = "SpringArm (pitch)"
    mx, my = ox + mid_pad, oy + 24 + 10
    mw, mh = ow - 2 * mid_pad, oh - 24 - 10 - mid_pad
    svg.rect(mx, my, mw, mh, fill="none", stroke=INK, sw=1.5)
    svg.text(mx + 10, my + 18, mid_label, size=11, font="sans", color=INK,
              box=(mx + 6, my + 4, mw - 12, 16), label="rig-springarm")

    inner_pad = 14
    inner_label = "Camera"
    ix, iy = mx + inner_pad, my + 24 + 8
    iw, ih = mw - 2 * inner_pad, mh - 24 - 8 - inner_pad
    svg.rect(ix, iy, iw, ih, fill=PANEL, stroke=INK, sw=1.5)
    svg.text(ix + iw / 2, iy + ih / 2 + 4, inner_label, size=11, font="sans",
              color=INK, anchor="middle",
              box=(ix + 6, iy, iw - 12, ih), label="rig-camera")

    footer(svg, "In-play HUD stays minimal: only chapter, well-being timer, controls and camera state are ever shown.")
    return svg


# ---------------------------------------------------------------------------
# W5 — Stand-Up Break Overlay
# ---------------------------------------------------------------------------

def build_w5():
    sid = "W5"
    svg = Svg(sid)
    header(svg, sid, "Stand-Up Break Overlay", ["2.3", "15.2"])

    # dimmed viewport behind modal — cream-2 fill with hairline, NOT dark
    viewport_y = CONTENT_TOP
    viewport_h = CONTENT_BOTTOM - viewport_y
    svg.rect(MARGIN, viewport_y, W - 2 * MARGIN, viewport_h, fill=PANEL,
              stroke=HAIR, sw=1.5)
    dim_label = "3D viewport — paused"
    dsize = 13
    tw = est_width(dim_label, dsize, "sans")
    svg.text(MARGIN + 24, viewport_y + 28, dim_label, size=dsize, font="sans",
              color=MUTED, box=(MARGIN + 24, viewport_y + 10, tw + 24, 24),
              label="dim-viewport-label")

    # centred modal panel
    modal_w = 620
    modal_h = 420
    mx = (W - modal_w) / 2
    my = viewport_y + (viewport_h - modal_h) / 2
    svg.rect(mx, my, modal_w, modal_h, fill=BG, stroke=INK, sw=1.5)

    # big countdown
    count_text = "66"
    csize = 72
    svg.text(mx + modal_w / 2, my + 90, count_text, size=csize, font="serif",
              color=ACCENT, anchor="middle",
              box=(mx + 40, my + 20, modal_w - 80, 90), label="countdown-66")

    # three prompts with stick-figure boxes
    prompts = ["Eyes", "Spine", "Reach"]
    pgap = 24
    pw = (modal_w - 48 - 2 * pgap) / 3
    ph = 130
    py = my + 130
    for i, p in enumerate(prompts):
        px = mx + 24 + i * (pw + pgap)
        svg.stick_figure(px, py, pw, ph - 26, p)
        label_y = py + ph - 4
        svg.text(px + pw / 2, label_y, p, size=14, font="sans", color=INK,
                  anchor="middle", weight="600",
                  box=(px, label_y - 16, pw, 20), label=f"prompt-{p}")

    # prominent line
    line_y = py + ph + 34
    svg.text(mx + modal_w / 2, line_y, "This cannot be skipped", size=17,
              font="sans", color=INK, weight="600", anchor="middle",
              box=(mx + 30, line_y - 20, modal_w - 60, 26),
              label="cannot-skip-line")

    # secondary outline button
    btn_w = 280
    btn_h = 44
    bx = mx + (modal_w - btn_w) / 2
    by = line_y + 24
    svg.rect(bx, by, btn_w, btn_h, fill="none", stroke=INK, sw=1.5)
    svg.text(bx + btn_w / 2, by + btn_h / 2 + 5, "I need the seated version",
              size=14, font="sans", color=INK, anchor="middle",
              box=(bx + 14, by + 8, btn_w - 28, btn_h - 16),
              label="btn-seated-version")

    footer(svg, "A full-screen, non-dismissible break that paces play with real movement prompts.")
    return svg


# ---------------------------------------------------------------------------
# W6 — Twin Quest: Connect Tools
# ---------------------------------------------------------------------------

def build_w6():
    sid = "W6"
    svg = Svg(sid)
    header(svg, sid, "Twin Quest — Connect Tools", ["5.1", "5.5", "12.2"])

    # 4-step progress rail
    steps = ["Request", "Authenticate", "Fork twin", "Connect tools"]
    rail_y = CONTENT_TOP + 10
    rail_h = 64
    gap = 20
    step_w = (W - 2 * MARGIN - 3 * gap) / 4
    active_idx = 3
    for i, s in enumerate(steps):
        x = MARGIN + i * (step_w + gap)
        active = i == active_idx
        stroke = ACCENT if active else HAIR
        fill = "none"
        svg.rect(x, rail_y, step_w, rail_h, fill=fill, stroke=stroke, sw=1.5)
        num_chip_d = 24
        chip_x = x + 14
        chip_y = rail_y + rail_h / 2 - num_chip_d / 2
        if active:
            svg.rect(chip_x, chip_y, num_chip_d, num_chip_d, fill=ACCENT,
                      stroke=ACCENT, sw=1.5, rx=num_chip_d / 2)
            num_color = "#fdfaf4"
        else:
            svg.rect(chip_x, chip_y, num_chip_d, num_chip_d, fill="none",
                      stroke=HAIR, sw=1.5, rx=num_chip_d / 2)
            num_color = MUTED
        svg.text(chip_x + num_chip_d / 2, chip_y + num_chip_d / 2 + 5,
                  str(i + 1), size=13, font="sans", color=num_color,
                  anchor="middle", box=(chip_x, chip_y, num_chip_d, num_chip_d),
                  label=f"step-num-{i}", pad=4)
        label_x = chip_x + num_chip_d + 10
        label_size = 14
        svg.text(label_x, rail_y + rail_h / 2 + 5, s, size=label_size,
                  font="sans", color=ACCENT if active else INK,
                  weight="600" if active else "400",
                  box=(label_x, rail_y + rail_h / 2 - 12,
                       x + step_w - label_x - 10, 22),
                  label=f"step-label-{s}")
        if i < len(steps) - 1:
            ax = x + step_w + gap / 2
            svg.line(ax - 6, rail_y + rail_h / 2, ax + 6, rail_y + rail_h / 2,
                      stroke=HAIR, sw=1.5)

    # 6-card connect grid
    grid_top = rail_y + rail_h + 26
    cols, rows = 3, 2
    ggap = 20
    card_w = (W - 2 * MARGIN - (cols - 1) * ggap) / cols
    card_h = 118
    tools = ["WhatsApp", "iPhone", "Android", "AI Glasses", "Calendar", "Files"]
    for idx, tool in enumerate(tools):
        r = idx // cols
        c = idx % cols
        x = MARGIN + c * (card_w + ggap)
        y = grid_top + r * (card_h + ggap)
        svg.rect(x, y, card_w, card_h, fill=PANEL, stroke=INK, sw=1.5)

        icon_s = 40
        icon_x = x + 18
        icon_y = y + (card_h - icon_s) / 2
        svg.rect(icon_x, icon_y, icon_s, icon_s, fill=BG, stroke=INK, sw=1.5)
        svg.line(icon_x, icon_y, icon_x + icon_s, icon_y + icon_s, stroke=HAIR, sw=1)
        svg.line(icon_x + icon_s, icon_y, icon_x, icon_y + icon_s, stroke=HAIR, sw=1)

        name_x = icon_x + icon_s + 16
        name_y = y + card_h / 2 - 6
        avail_w = card_w - (name_x - x) - 16
        svg.text(name_x, name_y, tool, size=15, font="sans", color=INK,
                  weight="600", box=(name_x, name_y - 18, avail_w, 22),
                  label=f"tool-name-{tool}")

        btn_w = 100
        btn_h = 30
        btn_x = name_x
        btn_y = name_y + 14
        svg.rect(btn_x, btn_y, btn_w, btn_h, fill="none", stroke=INK, sw=1.5)
        svg.text(btn_x + btn_w / 2, btn_y + btn_h / 2 + 5, "Connect", size=13,
                  font="sans", color=INK, anchor="middle",
                  box=(btn_x, btn_y, btn_w, btn_h), label=f"tool-btn-{tool}")

    # footer line above the caption
    fl_y = grid_top + rows * card_h + (rows - 1) * ggap + 30
    fl_text = "Your twin's data stays yours. Export it any time."
    svg.text(W / 2, fl_y, fl_text, size=14, font="sans", color=MUTED,
              anchor="middle", weight="600",
              box=(MARGIN, fl_y - 18, W - 2 * MARGIN, 24),
              label="footer-line-data-yours")

    footer(svg, "Guided flow for linking real-world tools to a sandboxed twin, ending on an explicit ownership promise.")
    return svg


# ---------------------------------------------------------------------------
# W7 — The Village
# ---------------------------------------------------------------------------

def build_w7():
    sid = "W7"
    svg = Svg(sid)
    header(svg, sid, "The Village", ["6.4", "4.5", "7.5"])

    sidebar_w = 300
    gap = 24
    map_w = W - 2 * MARGIN - sidebar_w - gap
    map_h = CONTENT_BOTTOM - CONTENT_TOP
    map_x = MARGIN
    map_y = CONTENT_TOP

    svg.rect(map_x, map_y, map_w, map_h, fill=PANEL, stroke=INK, sw=1.5)
    map_label = "Top-down village map"
    svg.text(map_x + 18, map_y + 26, map_label, size=13, font="sans",
              color=MUTED, box=(map_x + 18, map_y + 8, map_w - 36, 20),
              label="map-label")

    # placeholder buildings
    buildings = [
        (map_x + 60, map_y + 70, 120, 90, "Hall"),
        (map_x + 260, map_y + 60, 100, 70, "Library"),
        (map_x + 420, map_y + 100, 130, 100, "Garden"),
        (map_x + 90, map_y + 220, 110, 80, "Workshop"),
        (map_x + 300, map_y + 230, 120, 90, "Market"),
    ]
    for bx, by, bw, bh, bname in buildings:
        if by + bh > map_y + map_h - 20:
            bh = map_y + map_h - 20 - by
        svg.rect(bx, by, bw, bh, fill=BG, stroke=INK, sw=1.5)
        svg.text(bx + bw / 2, by + bh / 2 + 4, bname, size=11, font="sans",
                  color=MUTED, anchor="middle",
                  box=(bx + 6, by, bw - 12, bh), label=f"bldg-{bname}")

    # dashed paths connecting buildings -- routed through the open gaps
    # between rectangles (never through a building's interior/label area)
    # Hall (bottom, x mid=120) down to y=190, across to Workshop top (x=145)
    svg.line(map_x + 120, map_y + 160, map_x + 120, map_y + 190, stroke=MUTED,
              sw=1.5, dash="4,4")
    svg.line(map_x + 120, map_y + 190, map_x + 145, map_y + 190, stroke=MUTED,
              sw=1.5, dash="4,4")
    svg.line(map_x + 145, map_y + 190, map_x + 145, map_y + 220, stroke=MUTED,
              sw=1.5, dash="4,4")
    # Hall (right edge, y=115) across the gap to Library (left edge, y=115)
    svg.line(map_x + 180, map_y + 115, map_x + 260, map_y + 115, stroke=MUTED,
              sw=1.5, dash="4,4")
    # Library (right edge, y=95) across the gap to Garden (left edge, y=140)
    svg.line(map_x + 360, map_y + 95, map_x + 420, map_y + 95, stroke=MUTED,
              sw=1.5, dash="4,4")
    svg.line(map_x + 420, map_y + 95, map_x + 420, map_y + 140, stroke=MUTED,
              sw=1.5, dash="4,4")
    # Workshop (right edge, y=260) across the gap to Market (left edge, y=275)
    svg.line(map_x + 200, map_y + 260, map_x + 300, map_y + 260, stroke=MUTED,
              sw=1.5, dash="4,4")
    svg.line(map_x + 300, map_y + 260, map_x + 300, map_y + 275, stroke=MUTED,
              sw=1.5, dash="4,4")

    # voice indicator pill on the map
    voice_text = "Voice: off"
    vsize = 12
    tw = est_width(voice_text, vsize, "sans")
    vw = tw + 24
    vh = 28
    vx = map_x + map_w - vw - 16
    vy = map_y + map_h - vh - 16
    svg.rect(vx, vy, vw, vh, fill=BG, stroke=HAIR, sw=1.5, rx=vh / 2)
    svg.text(vx + vw / 2, vy + vh / 2 + 4, voice_text, size=vsize, font="sans",
              color=MUTED, anchor="middle", box=(vx, vy, vw, vh),
              label="voice-indicator")

    # right sidebar
    sb_x = map_x + map_w + gap
    sb_y = map_y
    sb_h_header = 34
    svg.text(sb_x, sb_y + 22, "Your cohort", size=17, font="serif", color=INK,
              weight="600", box=(sb_x, sb_y + 2, sidebar_w, 26),
              label="cohort-title")

    names = ["Amara", "Theo", "Priya", "Lucas", "Nadia"]
    badges = ["Helper", "New", "Guide", "Helper", "New"]
    row_h = 52
    list_top = sb_y + sb_h_header + 12
    for i, (nm, bd) in enumerate(zip(names, badges)):
        ry = list_top + i * row_h
        svg.line(sb_x, ry + row_h - 8, sb_x + sidebar_w, ry + row_h - 8,
                  stroke=HAIR, sw=1)
        avatar_s = 30
        svg.circle(sb_x + avatar_s / 2, ry + 14, avatar_s / 2, fill=BG,
                    stroke=INK, sw=1.5)
        name_x = sb_x + avatar_s + 14
        svg.text(name_x, ry + 10, nm, size=14, font="sans", color=INK,
                  weight="600", box=(name_x, ry - 6, 130, 20),
                  label=f"cohort-name-{nm}")
        badge_text = bd
        bsize = 11
        btw = est_width(badge_text, bsize, "sans")
        badge_w = btw + 24
        badge_h = 22
        badge_x = sb_x + sidebar_w - badge_w
        badge_y = ry
        stroke = ACCENT if bd == "Helper" else HAIR
        color = ACCENT if bd == "Helper" else MUTED
        svg.rect(badge_x, badge_y, badge_w, badge_h, fill="none", stroke=stroke,
                  sw=1.5, rx=badge_h / 2)
        svg.text(badge_x + badge_w / 2, badge_y + badge_h / 2 + 4, badge_text,
                  size=bsize, font="sans", color=color, anchor="middle",
                  box=(badge_x, badge_y, badge_w, badge_h),
                  label=f"cohort-badge-{nm}")

    # callout box at bottom of sidebar
    callout_y = list_top + len(names) * row_h + 10
    callout_h = map_y + map_h - callout_y
    if callout_h < 70:
        callout_h = 70
    svg.rect(sb_x, callout_y, sidebar_w, callout_h, fill=PANEL, stroke=HAIR, sw=1.5)
    callout_lines = ["Standing comes from evidenced", "help to others. No followers,", "no streaks."]
    for i, ln in enumerate(callout_lines):
        ly = callout_y + 24 + i * 18
        svg.text(sb_x + 14, ly, ln, size=12, font="sans", color=MUTED,
                  box=(sb_x + 14, ly - 14, sidebar_w - 28, 18),
                  label=f"callout-line-{i}")

    footer(svg, "Shared social hub where standing reflects verified help given, not attention metrics.")
    return svg


# ---------------------------------------------------------------------------
# W8 — Guardian and Review Panel
# ---------------------------------------------------------------------------

def build_w8():
    sid = "W8"
    svg = Svg(sid)
    header(svg, sid, "Guardian and Review Panel", ["1.2", "2.7", "14.2"])

    table_x = MARGIN
    table_y = CONTENT_TOP
    table_w = W - 2 * MARGIN

    col_widths_ratio = [0.40, 0.18, 0.18, 0.24]
    col_widths = [table_w * r for r in col_widths_ratio]
    col_x = [table_x]
    for cw in col_widths:
        col_x.append(col_x[-1] + cw)

    header_h = 40
    row_h = 42
    headers = ["Item", "Reviewer", "Status", "Date"]

    svg.rect(table_x, table_y, table_w, header_h, fill=PANEL, stroke=INK, sw=1.5)
    for i, h in enumerate(headers):
        hx = col_x[i] + 14
        svg.text(hx, table_y + header_h / 2 + 5, h, size=13, font="sans",
                  color=INK, weight="600",
                  box=(hx, table_y, col_widths[i] - 24, header_h),
                  label=f"th-{h}")

    rows = [
        ("Chapter 3 catechetical text", "Church review", "Approved", "12 Jul 2026"),
        ("Narrator script v4", "Church review", "In review", "28 Jul 2026"),
        ("Safety walls audit", "Safeguarding", "Approved", "05 Jul 2026"),
        ("Accessibility check", "Accessibility", "Open", "01 Aug 2026"),
        ("Asset licence register", "Legal", "Approved", "18 Jun 2026"),
        ("Public URL fetch", "Release", "Approved", "22 Jul 2026"),
    ]

    table_h = header_h + row_h * len(rows)
    svg.rect(table_x, table_y, table_w, table_h, fill="none", stroke=INK, sw=1.5)
    for i in range(len(col_x)):
        svg.line(col_x[i], table_y, col_x[i], table_y + table_h, stroke=HAIR, sw=1.5)

    for r_idx, (item, reviewer, status, date) in enumerate(rows):
        ry = table_y + header_h + r_idx * row_h
        if r_idx > 0:
            svg.line(table_x, ry, table_x + table_w, ry, stroke=HAIR, sw=1.5)

        item_x = col_x[0] + 14
        svg.text(item_x, ry + row_h / 2 + 5, item, size=13, font="sans",
                  color=INK, box=(item_x, ry, col_widths[0] - 24, row_h),
                  label=f"row{r_idx}-item")

        rev_x = col_x[1] + 14
        svg.text(rev_x, ry + row_h / 2 + 5, reviewer, size=13, font="sans",
                  color=INK, box=(rev_x, ry, col_widths[1] - 24, row_h),
                  label=f"row{r_idx}-reviewer")

        active = status in ("In review", "Open")
        pill_x = col_x[2] + 14
        svg.pill_status(pill_x, ry + row_h / 2 - 12, status, active, size=12,
                          label=f"row{r_idx}-status")

        date_x = col_x[3] + 14
        svg.text(date_x, ry + row_h / 2 + 5, date, size=13, font="sans",
                  color=MUTED, box=(date_x, ry, col_widths[3] - 24, row_h),
                  label=f"row{r_idx}-date")

    # "What the child saw" summary panel
    summary_y = table_y + table_h + 26
    summary_h = 130
    svg.rect(table_x, summary_y, table_w, summary_h, fill=PANEL, stroke=INK, sw=1.5)
    svg.text(table_x + 20, summary_y + 28, "What the child saw", size=16,
              font="serif", color=INK, weight="600",
              box=(table_x + 20, summary_y + 8, table_w - 40, 24),
              label="summary-title")

    summary_lines = [
        "Chapter 3, session of 28 Jul 2026 — 22 minutes played.",
        "Two Stand-Up breaks completed, none skipped.",
        "No chat, uploads or outbound links were available at any point.",
    ]
    for i, ln in enumerate(summary_lines):
        ly = summary_y + 54 + i * 22
        svg.text(table_x + 20, ly, ln, size=13, font="sans", color=INK,
                  box=(table_x + 20, ly - 15, table_w - 40, 20),
                  label=f"summary-line-{i}")

    note_y = summary_y + summary_h + 24
    svg.text(table_x, note_y, "Visibility, not surveillance.", size=13,
              font="sans", color=MUTED, weight="600",
              box=(table_x, note_y - 15, table_w, 20),
              label="visibility-note")

    footer(svg, "Guardian-facing audit trail pairing review status with a plain summary of what the child experienced.")
    return svg


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

BUILDERS = [
    ("w1-entry.svg", build_w1),
    ("w2-safety.svg", build_w2),
    ("w3-chapters.svg", build_w3),
    ("w4-hud.svg", build_w4),
    ("w5-standup.svg", build_w5),
    ("w6-twinquest.svg", build_w6),
    ("w7-village.svg", build_w7),
    ("w8-guardian.svg", build_w8),
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    results = []
    for filename, builder in BUILDERS:
        _registered_texts.clear()
        svg = builder()
        check_all_overlaps()
        content = svg.render()
        path = os.path.join(OUT_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        results.append((filename, path))

    # Verification pass
    print(f"{'file':<20}{'bytes':>10}{'text-elems':>14}{'well-formed':>14}")
    all_ok = True
    for filename, path in results:
        size = os.path.getsize(path)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        try:
            root = ET.fromstring(content)
            well_formed = True
        except ET.ParseError as e:
            well_formed = False
            print(f"  XML PARSE ERROR in {filename}: {e}")
        text_count = content.count("<text ")
        ok_size = size > 2048
        if not (well_formed and ok_size):
            all_ok = False
        print(f"{filename:<20}{size:>10}{text_count:>14}{str(well_formed):>14}"
              f"{'  (SIZE<2KB!)' if not ok_size else ''}")

    print()
    if all_ok:
        print("All files well-formed XML and > 2KB. Overflow/overlap assertions passed for all 8 screens.")
    else:
        print("ISSUES DETECTED — see above.")


if __name__ == "__main__":
    main()
