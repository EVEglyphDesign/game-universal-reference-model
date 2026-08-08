#!/usr/bin/env python3
"""EgD-POS-001 — The Additive Position. EVEglyphDesign canon PDF."""
import hashlib, datetime, re, sys
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, KeepTogether, Flowable, Table, TableStyle)

W, H = LETTER
CREAM = HexColor("#fdfaf4"); CREAM2 = HexColor("#f7f2e7")
INK = HexColor("#1a1a1a"); LINE = HexColor("#e7e1d3")
ORNG = HexColor("#e87722"); MUTE = HexColor("#6b665c")

F = "/home/user/workspace/fonts"
pdfmetrics.registerFont(TTFont("Fraunces", f"{F}/Fraunces-400.ttf"))
pdfmetrics.registerFont(TTFont("Fraunces-Bold", f"{F}/Fraunces-700.ttf"))
pdfmetrics.registerFont(TTFont("Inter", f"{F}/Inter-400.ttf"))
pdfmetrics.registerFont(TTFont("Inter-SB", f"{F}/Inter-600.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", f"{F}/Inter-700.ttf"))

SRC = "/home/user/workspace/gurm/model/EgD-URM-002-library-assessment.md"
OUT = "/home/user/workspace/gurm/docs/blueprint/EVEglyphDesign_GenAI_Library_Fit_Assessment.pdf"
TS = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
DOC_ID = "EgD-URM-002"; KEY_ID = "EgD-KEY-2026-07"
TITLE = "GenAI Library Fit Assessment"
SUB = ("An assessment of ten generative-AI Python libraries against the canon of EgD-URM-001, "
       "with the four admission gates and the findings that actually improve the repository.")
RAW = open(SRC, encoding="utf-8").read()
SHA = hashlib.sha256(RAW.encode("utf-8")).hexdigest()
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 0

MARGIN_L, MARGIN_R = 24*mm, 24*mm
TOP, BOT = 26*mm, 24*mm
FW = W - MARGIN_L - MARGIN_R


def S(name, **kw):
    b = dict(name=name, fontName="Inter", fontSize=10, leading=15.4,
             textColor=INK, alignment=TA_LEFT, spaceAfter=0)
    b.update(kw); return ParagraphStyle(**b)


st_h1 = S("h1", fontName="Fraunces-Bold", fontSize=15, leading=19, spaceAfter=3)
st_h2 = S("h2", fontName="Fraunces-Bold", fontSize=11.6, leading=15, spaceAfter=2)
st_body = S("b", spaceAfter=8)
st_bul = S("bu", spaceAfter=6, leftIndent=13, bulletIndent=2, firstLineIndent=0)
st_quote = S("q", fontName="Fraunces", fontSize=11.2, leading=17, spaceAfter=0)
st_cap = S("cap", fontSize=7.8, leading=11.6, textColor=MUTE, spaceAfter=6)


class Rule(Flowable):
    def __init__(self, w=FW, col=LINE, th=0.7, pad=0):
        Flowable.__init__(self); self.w = w; self.col = col; self.th = th; self.pad = pad
    def wrap(self, aw, ah): return (self.w, self.th + self.pad)
    def draw(self):
        self.canv.setStrokeColor(self.col); self.canv.setLineWidth(self.th)
        self.canv.line(0, self.pad, self.w, self.pad)


class Pull(Flowable):
    """Cream-2 panel with an orange left edge."""
    def __init__(self, text, style=st_quote, pad=9):
        Flowable.__init__(self); self.p = Paragraph(text, style); self.pad = pad
    def wrap(self, aw, ah):
        w = FW - 2*self.pad - 3
        _, h = self.p.wrap(w, ah)
        self.h = h + 2*self.pad; return (FW, self.h)
    def draw(self):
        c = self.canv
        c.setFillColor(CREAM2); c.setStrokeColor(LINE); c.setLineWidth(0.7)
        c.rect(0, 0, FW, self.h, stroke=1, fill=1)
        c.setFillColor(ORNG); c.rect(0, 0, 3, self.h, stroke=0, fill=1)
        self.p.drawOn(c, self.pad + 6, self.pad)


class Code(Flowable):
    """Monospaced block on cream-2 with an orange left edge. Splits across pages."""
    FS = 7.9; LEAD = 10.2; PAD = 7

    def __init__(self, lines):
        Flowable.__init__(self); self.lines = lines

    def wrap(self, aw, ah):
        self.h = len(self.lines) * self.LEAD + 2 * self.PAD
        return (FW, self.h)

    def split(self, aw, ah):
        fit = int((ah - 2 * self.PAD) // self.LEAD)
        if fit < 2 or fit >= len(self.lines):
            return [] if fit < 2 else [self]
        return [Code(self.lines[:fit]), Code(self.lines[fit:])]

    def draw(self):
        c = self.canv
        c.setFillColor(CREAM2); c.setStrokeColor(LINE); c.setLineWidth(0.7)
        c.rect(0, 0, FW, self.h, stroke=1, fill=1)
        c.setFillColor(ORNG); c.rect(0, 0, 2.4, self.h, stroke=0, fill=1)
        y = self.h - self.PAD - self.FS
        for ln in self.lines:
            txt = ln.replace("\t", "    ")
            stripped = txt.lstrip()
            if stripped.startswith("#"):
                c.setFillColor(MUTE)
            else:
                c.setFillColor(INK)
            c.setFont("Courier", self.FS)
            c.drawString(self.PAD + 6, y, txt)
            y -= self.LEAD


# Header-aware column widths. Keyed by the tuple of header cells, so a table's
# proportions follow its actual content rather than its column count alone.
WIDTH_OVERRIDES = {
    ("#", "Finding", "Class", "Why it matters"): [0.05, 0.26, 0.155, 0.535],
    ("Gate", "Derived from", "The test"): [0.15, 0.43, 0.42],
    ("#", "Library", "A", "B", "C", "D", "Verdict"):
        [0.045, 0.175, 0.072, 0.072, 0.072, 0.114, 0.45],
    ("Claim in the list", "Correction"): [0.20, 0.80],
}


def mk_table(rows):
    """Markdown pipe table -> canon-styled platypus Table. rows[0] is the header."""
    head, body = rows[0], rows[1:]
    n = len(head)
    override = WIDTH_OVERRIDES.get(tuple(head))
    st_th = S("th", fontName="Inter-SB", fontSize=7.3, leading=9.2, textColor=MUTE)
    st_td = S("td", fontName="Inter", fontSize=8.0, leading=10.4, textColor=INK)
    st_id = S("tdid", fontName="Inter-SB", fontSize=8.0, leading=10.4, textColor=INK)
    data = [[Paragraph(esc(c.upper()), st_th) for c in head]]
    for r in body:
        data.append([Paragraph(esc(c), st_id if j == 0 else st_td)
                     for j, c in enumerate(r)])
    # Column widths: first column narrow (an ID), last columns narrow, prose gets the rest.
    if n == 2:
        widths = [0.16, 0.84]
    elif n == 3:
        widths = [0.18, 0.57, 0.25]
    elif n == 4:
        widths = [0.11, 0.28, 0.45, 0.16]
    elif n == 5:
        widths = [0.10, 0.24, 0.40, 0.14, 0.12]
    else:
        widths = [1.0 / n] * n
    if override:
        widths = override
    t = Table(data, colWidths=[w * FW for w in widths], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, ORNG),
        ("LINEBELOW", (0, 1), (-1, -2), 0.4, LINE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.7, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CREAM, CREAM2]),
    ]))
    return t


def esc(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r'<font name="Inter-Bold">\1</font>', s)
    s = re.sub(r"`([^`]+?)`", r'<font name="Courier" size="8.6">\1</font>', s)
    s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", s)
    s = re.sub(r"\[([^\]]+?)\]\((https?://[^)\s]+)\)",
               lambda m: '<link href="%s" color="#c25e10"><u>%s</u></link>'
                         % (m.group(2).replace("&amp;", "&"), m.group(1)), s)
    return s


def parse(md):
    """Markdown subset -> flowables. Skips the H1 block; it is the cover."""
    out = []
    lines = md.split("\n")
    i = 0
    seen_h1 = False
    para = []

    def flush():
        nonlocal para
        if para:
            out.append(Paragraph(esc(" ".join(para)), st_body)); para = []

    while i < len(lines):
        ln = lines[i].rstrip()
        if ln.startswith("# "):
            flush(); seen_h1 = True; i += 1; continue
        if not seen_h1:
            i += 1; continue
        if ln.startswith("```"):
            flush()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i].rstrip("\n")); i += 1
            i += 1
            out.append(Spacer(1, 4)); out.append(Code(buf)); out.append(Spacer(1, 10))
            continue
        if ln.startswith("> "):
            flush()
            q = [ln[2:]]
            while i + 1 < len(lines) and lines[i+1].startswith("> "):
                i += 1; q.append(lines[i][2:])
            out.append(Spacer(1, 3)); out.append(Pull(esc(" ".join(q))))
            out.append(Spacer(1, 11)); i += 1; continue
        if ln.startswith("### "):
            flush(); out.append(Spacer(1, 6))
            out.append(KeepTogether([Paragraph(esc(ln[4:]), st_h2), Spacer(1, 3)]))
            i += 1; continue
        if ln.startswith("## "):
            flush(); out.append(Spacer(1, 12))
            out.append(KeepTogether([Rule(col=ORNG, th=1.6), Spacer(1, 6),
                                     Paragraph(esc(ln[3:]), st_h1), Spacer(1, 5)]))
            i += 1; continue
        if ln.strip() == "---":
            flush(); i += 1; continue
        if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i+1].strip()):
            flush()
            def cells(s):
                return [c.strip() for c in s.strip().strip("|").split("|")]
            rows = [cells(ln)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i])); i += 1
            width = len(rows[0])
            rows = [r + [""] * (width - len(r)) if len(r) < width else r[:width] for r in rows]
            out.append(Spacer(1, 4)); out.append(mk_table(rows)); out.append(Spacer(1, 11))
            continue
        m = re.match(r"^(\d+)\. (.*)", ln)
        if ln.startswith("- ") or m:
            flush()
            txt = m.group(2) if m else ln[2:]
            mark = f"{m.group(1)}." if m else "\u2014"
            while i + 1 < len(lines) and lines[i+1].startswith("  ") and lines[i+1].strip():
                i += 1; txt += " " + lines[i].strip()
            out.append(Paragraph(esc(txt), st_bul, bulletText=mark))
            i += 1; continue
        if not ln.strip():
            flush(); i += 1; continue
        if ln.startswith("**Document ID**") or ln.startswith("©") or ln.startswith("*Pour"):
            i += 1; continue
        para.append(ln.strip()); i += 1
    flush()
    return out


def paint(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM); canvas.rect(0, 0, W, H, stroke=0, fill=1)
    canvas.saveState()
    canvas.translate(W/2, H/2); canvas.rotate(38)
    canvas.setFont("Fraunces-Bold", 60); canvas.setFillColor(HexColor("#f5f0e6"))
    canvas.drawCentredString(0, -18, "EVEglyphDesign")
    canvas.setFont("Inter", 12.5)
    canvas.drawCentredString(0, -44, "C A N O N   \u00b7   C O N T R O L L E D   C O P Y")
    canvas.restoreState()
    canvas.setFont("Inter-SB", 7); canvas.setFillColor(MUTE)
    canvas.drawString(MARGIN_L, H - 15*mm,
                      "EVEglyphDesign  \u00b7  GenAI Library Fit Assessment  \u00b7  " + DOC_ID)
    canvas.drawRightString(W - MARGIN_R, H - 15*mm, KEY_ID)
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.7)
    canvas.line(MARGIN_L, H - 17*mm, W - MARGIN_R, H - 17*mm)
    canvas.line(MARGIN_L, 17*mm, W - MARGIN_R, 17*mm)
    canvas.setFont("Inter", 6.6); canvas.setFillColor(MUTE)
    canvas.drawString(MARGIN_L, 13.4*mm,
                      "\u00a9 2026 EVEglyphDesign. All rights reserved. Controlled copy.  \u00b7  "
                      + TS + "  \u00b7  SHA-256 " + SHA[:20] + "\u2026")
    canvas.drawString(MARGIN_L, 10.6*mm, "Pour le bien-\u00eatre du peuple.")
    tot = f" of {PAGES}" if PAGES else ""
    canvas.setFont("Inter-SB", 7.4)
    canvas.drawRightString(W - MARGIN_R, 13.4*mm, f"Page {canvas.getPageNumber()}{tot}")
    canvas.restoreState()


def cover(canvas, doc):
    paint(canvas, doc)
    canvas.saveState()
    y = H - 72*mm
    canvas.setFillColor(ORNG); canvas.setFont("Inter-SB", 8)
    canvas.drawString(MARGIN_L, y + 34*mm, "E V E G L Y P H D E S I G N   \u00b7   A S S E S S M E N T   \u00b7   E g D - U R M - 0 0 2")
    canvas.setFillColor(INK); canvas.setFont("Fraunces-Bold", 29)
    canvas.drawString(MARGIN_L, y + 20*mm, TITLE)
    canvas.setFillColor(ORNG); canvas.rect(MARGIN_L, y + 15*mm, 42*mm, 2.4, stroke=0, fill=1)
    canvas.restoreState()


def build():
    frame = Frame(MARGIN_L, BOT, FW, H - TOP - BOT, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    frame1 = Frame(MARGIN_L, BOT, FW, H - 66*mm - BOT, id="f1",
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = BaseDocTemplate(OUT, pagesize=LETTER, title=f"{TITLE} — {DOC_ID}",
                          author="EVEglyphDesign", subject=SUB,
                          leftMargin=MARGIN_L, rightMargin=MARGIN_R,
                          topMargin=TOP, bottomMargin=BOT)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame1], onPage=cover),
        PageTemplate(id="body", frames=[frame], onPage=paint),
    ])
    story = [
        Rule(), Spacer(1, 9),
        Paragraph(
            f'<font name="Inter-SB">Document ID</font>  {DOC_ID}'
            f'&nbsp;&nbsp;\u00b7&nbsp;&nbsp;<font name="Inter-SB">Key ID</font>  {KEY_ID}'
            f'&nbsp;&nbsp;\u00b7&nbsp;&nbsp;<font name="Inter-SB">Status</font>  v1.0 \u2014 FOR REVIEW AND APPROVAL'
            f'&nbsp;&nbsp;\u00b7&nbsp;&nbsp;<font name="Inter-SB">Issued</font>  {TS}',
            st_cap),
        Paragraph(f'<font name="Inter-SB">SHA-256 of source</font>  '
                  f'<font name="Courier" size="7">{SHA}</font>', st_cap),
        Spacer(1, 4),
    ] + parse(RAW)
    # switch to the full-height body frame after the cover page
    from reportlab.platypus import NextPageTemplate, PageBreak
    story.insert(0, NextPageTemplate("body"))
    doc.build(story)
    from pypdf import PdfReader
    return len(PdfReader(OUT).pages)


if __name__ == "__main__":
    n = build()
    print("pages", n, "stamped", PAGES, "sha", SHA[:16])
