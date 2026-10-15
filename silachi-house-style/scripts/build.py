#!/usr/bin/env python3
"""Build a .docx in the Silachi Prestige Standard (SLF-HS-001).

Usage:
    python3 build.py content.json out.docx [--firm ../assets/firm.json]

The content file describes WHAT the document says. Every visual decision
comes from firm.json, so the style cannot drift between drafts.
See references/content-schema.md for the content format.
"""
import argparse
import copy
import json
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor

HERE = Path(__file__).resolve().parent
NUM_ID = 1001  # the one locked multilevel list
ABSTRACT_ID = 1001


# ---------- low-level helpers ----------

def set_fonts(rpr_owner, name):
    """Set ascii/hAnsi/cs/eastAsia fonts on a style or run."""
    rpr = rpr_owner.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)


def set_tracking(rpr_owner, pts):
    rpr = rpr_owner.get_or_add_rPr()
    sp = rpr.find(qn("w:spacing"))
    if sp is None:
        sp = OxmlElement("w:spacing")
        rpr.append(sp)
    sp.set(qn("w:val"), str(int(round(pts * 20))))


def rgb(hexstr):
    return RGBColor.from_string(hexstr)


def para_border(paragraph_or_style_ppr, side, size_pt, color, space_pt):
    ppr = paragraph_or_style_ppr
    bdr = ppr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = OxmlElement("w:pBdr")
        ppr.append(bdr)
    el = OxmlElement(f"w:{side}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(int(size_pt * 8)))
    el.set(qn("w:space"), str(int(space_pt)))
    el.set(qn("w:color"), color)
    bdr.append(el)


def add_field(paragraph, instr, style_font=None):
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), instr)
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    paragraph._p.append(fld)
    return fld


INLINE = re.compile(r"(\*\*.+?\*\*|\*.+?\*)")


def add_inline(paragraph, text):
    """Write text with **bold** and *italic* markup into a paragraph."""
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            paragraph.add_run(part[2:-2]).bold = True
        elif part.startswith("*") and part.endswith("*"):
            paragraph.add_run(part[1:-1]).italic = True
        else:
            paragraph.add_run(part)


# ---------- styles ----------

class Theme:
    def __init__(self, firm, court_safe):
        self.f = firm
        c = firm["colors"]
        black = "000000"
        self.ink = black if court_safe else c["ink"]
        self.ox = black if court_safe else c["oxblood"]
        self.gray = black if court_safe else c["graphite"]
        self.hair = black if court_safe else c["hairline"]
        self.serif = firm["fonts"]["serif"]
        self.sans = firm["fonts"]["sans"]


def make_style(doc, name, base=None, font=None, size=None, color=None,
               bold=None, italic=None, small_caps=None, caps=None, tracking=None,
               align=None, before=None, after=None, leading=None,
               left=None, hanging=None, first=None, keep_next=None):
    styles = doc.styles
    st = styles[name] if name in [s.name for s in styles] else styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    if base:
        st.base_style = styles[base]
    st.quick_style = True
    f = st.font
    if font:
        set_fonts(st.element, font)
    if size:
        f.size = Pt(size)
    if color:
        f.color.rgb = rgb(color)
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic
    if small_caps is not None:
        f.small_caps = small_caps
    if caps is not None:
        f.all_caps = caps
    if tracking:
        set_tracking(st.element, tracking)
    pf = st.paragraph_format
    if align:
        pf.alignment = align
    if before is not None:
        pf.space_before = Pt(before)
    if after is not None:
        pf.space_after = Pt(after)
    if leading:
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.line_spacing = Pt(leading)
    if left is not None:
        pf.left_indent = Inches(left)
    if hanging is not None:
        pf.first_line_indent = Inches(-hanging)
    if first is not None:
        pf.first_line_indent = Inches(first)
    if keep_next is not None:
        pf.keep_with_next = keep_next
    pf.widow_control = True
    return st


def build_styles(doc, th):
    f = th.f
    b = f["body"]
    normal = doc.styles["Normal"]
    set_fonts(normal.element, th.serif)
    normal.font.size = Pt(b["size_pt"])
    normal.font.color.rgb = rgb(th.ink)

    make_style(doc, "SH Body", "Normal",
               align=WD_ALIGN_PARAGRAPH.LEFT if b.get("align") == "left" else WD_ALIGN_PARAGRAPH.JUSTIFY,
               before=0, after=b["after_pt"], leading=b["leading_exact_pt"])
    make_style(doc, "SH Eyebrow", "Normal", font=th.sans, size=f["eyebrow"]["size_pt"],
               color=th.ox, caps=True, tracking=f["eyebrow"]["tracking_pt"],
               before=0, after=4, keep_next=True)
    make_style(doc, "SH Title", "Normal", size=f["title"]["size_pt"], small_caps=True,
               tracking=f["title"]["tracking_pt"], before=0, after=4, leading=30, keep_next=True)
    make_style(doc, "SH Meta", "Normal", size=11, italic=True, color=th.gray,
               before=0, after=14, keep_next=True)
    a = f["article"]
    centered = a.get("align") == "center"
    caps = a.get("case") == "caps"
    art_font = th.sans if a.get("font") == "sans" else None
    art = make_style(doc, "SH Article", "Normal", font=art_font, size=a["size_pt"], small_caps=not caps, caps=caps,
                     bold=a.get("bold", False), tracking=a["tracking_pt"],
                     align=WD_ALIGN_PARAGRAPH.CENTER if centered else WD_ALIGN_PARAGRAPH.LEFT,
                     before=a["before_pt"], after=a["after_pt"],
                     left=0 if centered else 0.5, hanging=0 if centered else 0.5, keep_next=True)
    if a.get("underline"):
        art.font.underline = True
    if a.get("rule", True):
        para_border(art.element.get_or_add_pPr(), "top", a["rule_pt"], th.ox, 4)
    if a.get("double_rule"):
        para_border(art.element.get_or_add_pPr(), "bottom", 0.5, th.ox, 2)
    make_style(doc, "SH Section", "SH Body", left=0.5, hanging=0.5)
    make_style(doc, "SH Subsection", "SH Body", left=1.0, hanging=0.5)
    make_style(doc, "SH Bullet", "SH Body", left=0.75, hanging=0.25, after=4)
    make_style(doc, "SH Quote", "SH Body", size=12, leading=15, left=0.75)
    doc.styles["SH Quote"].paragraph_format.right_indent = Inches(0.75)
    make_style(doc, "SH Label", "Normal", font=th.sans, size=f["label"]["size_pt"],
               color=th.gray, caps=True, tracking=f["label"]["tracking_pt"], before=3, after=3)
    make_style(doc, "SH Value", "Normal", size=12, before=2, after=2, leading=15)
    make_style(doc, "SH Note", "Normal", size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER,
               before=18, after=0)
    make_style(doc, "SH Sig", "Normal", size=12, before=0, after=0, leading=15)
    make_style(doc, "SH Running", "Normal", font=th.sans, size=f["header_footer"]["size_pt"],
               color=th.gray, caps=True, tracking=f["header_footer"]["tracking_pt"], before=0, after=0)


# ---------- the locked multilevel list ----------

def build_numbering(doc, th):
    numbering = doc.part.numbering_part.element
    if th.f["article"].get("align") == "center":
        art_suffix, art_ppr = '<w:suff w:val="space"/>', '<w:ind w:left="0" w:firstLine="0"/>'
    else:
        art_suffix = ""
        art_ppr = '<w:tabs><w:tab w:val="num" w:pos="720"/></w:tabs><w:ind w:left="720" w:hanging="720"/>'
    abstract = parse_xml(f"""
<w:abstractNum {nsdecls('w')} w:abstractNumId="{ABSTRACT_ID}">
  <w:multiLevelType w:val="multilevel"/>
  <w:name w:val="SLF Prestige Outline"/>
  <w:lvl w:ilvl="0">
    <w:start w:val="1"/><w:numFmt w:val="upperRoman"/><w:pStyle w:val="SHArticle"/>
    <w:lvlText w:val="%1."/><w:lvlJc w:val="left"/>{art_suffix}
    <w:pPr>{art_ppr}</w:pPr>
    <w:rPr><w:color w:val="{th.ox}"/><w:smallCaps w:val="0"/></w:rPr>
  </w:lvl>
  <w:lvl w:ilvl="1">
    <w:start w:val="1"/><w:numFmt w:val="upperLetter"/><w:pStyle w:val="SHSection"/>
    <w:lvlText w:val="%2."/><w:lvlJc w:val="left"/><w:lvlRestart w:val="1"/>
    <w:pPr><w:tabs><w:tab w:val="num" w:pos="720"/></w:tabs><w:ind w:left="720" w:hanging="720"/></w:pPr>
    <w:rPr><w:b/></w:rPr>
  </w:lvl>
  <w:lvl w:ilvl="2">
    <w:start w:val="1"/><w:numFmt w:val="decimal"/><w:pStyle w:val="SHSubsection"/>
    <w:lvlText w:val="%3."/><w:lvlJc w:val="left"/><w:lvlRestart w:val="2"/>
    <w:pPr><w:tabs><w:tab w:val="num" w:pos="1440"/></w:tabs><w:ind w:left="1440" w:hanging="720"/></w:pPr>
  </w:lvl>
</w:abstractNum>""")
    bullets = parse_xml(f"""
<w:abstractNum {nsdecls('w')} w:abstractNumId="{ABSTRACT_ID + 1}">
  <w:multiLevelType w:val="singleLevel"/>
  <w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:pStyle w:val="SHBullet"/>
    <w:lvlText w:val="▪"/><w:lvlJc w:val="left"/>
    <w:pPr><w:ind w:left="1080" w:hanging="360"/></w:pPr>
    <w:rPr><w:color w:val="{th.ox}"/></w:rPr></w:lvl>
</w:abstractNum>""")
    # abstractNums must precede nums
    first_num = numbering.find(qn("w:num"))
    for node in (abstract, bullets):
        if first_num is not None:
            first_num.addprevious(node)
        else:
            numbering.append(node)
    numbering.append(parse_xml(
        f'<w:num {nsdecls("w")} w:numId="{NUM_ID}"><w:abstractNumId w:val="{ABSTRACT_ID}"/></w:num>'))
    numbering.append(parse_xml(
        f'<w:num {nsdecls("w")} w:numId="{NUM_ID + 1}"><w:abstractNumId w:val="{ABSTRACT_ID + 1}"/></w:num>'))

    # wire each heading style to its level so numbering follows the style
    for style_name, lvl, num in (("SH Article", 0, NUM_ID), ("SH Section", 1, NUM_ID),
                                 ("SH Subsection", 2, NUM_ID), ("SH Bullet", 0, NUM_ID + 1)):
        ppr = doc.styles[style_name].element.get_or_add_pPr()
        numpr = parse_xml(f'<w:numPr {nsdecls("w")}><w:ilvl w:val="{lvl}"/><w:numId w:val="{num}"/></w:numPr>')
        ppr.insert(0, numpr)


# ---------- page furniture ----------

def setup_page(doc, th, content):
    p = th.f["page"]
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.top_margin, sec.bottom_margin = Inches(p["margin_top_in"]), Inches(p["margin_bottom_in"])
    sec.left_margin = sec.right_margin = Inches(p["margin_side_in"])
    sec.header_distance, sec.footer_distance = Inches(p["header_in"]), Inches(p["footer_in"])
    sec.different_first_page_header_footer = True
    text_w = 8.5 - 2 * p["margin_side_in"]

    # first page: centered wordmark
    fh = sec.first_page_header
    h1 = fh.paragraphs[0]
    h1.style = doc.styles["SH Running"]
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h1.add_run(th.f["firm"]["name"])
    set_tracking(r._r, 3)
    r.font.color.rgb = rgb(th.ink)
    r.font.size = Pt(9.5)
    h2 = fh.add_paragraph(th.f["firm"]["address_line"], style="SH Running")
    h2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h2.runs[0].font.all_caps = False

    # running header
    hp = sec.header.paragraphs[0]
    hp.style = doc.styles["SH Running"]
    hp.paragraph_format.tab_stops.add_tab_stop(Inches(text_w), WD_TAB_ALIGNMENT.RIGHT)
    hp.add_run(th.f["firm"]["name"] + "\t" + content.get("short_title", content["title"]))
    para_border(hp._p.get_or_add_pPr(), "bottom", 0.5, th.hair, 4)

    # footers (first page and running), live Page X of Y
    for footer in (sec.footer, sec.first_page_footer):
        fp = footer.paragraphs[0]
        fp.style = doc.styles["SH Running"]
        fp.paragraph_format.tab_stops.add_tab_stop(Inches(text_w), WD_TAB_ALIGNMENT.RIGHT)
        fp.add_run((("Matter " + content["matter_no"]) if content.get("matter_no") else "") + "\tPage ")
        add_field(fp, "PAGE")
        fp.add_run(" of ")
        add_field(fp, "NUMPAGES")
    return text_w


def hairline_table(table, th, inside=True):
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{side}")
        if side in ("top", "bottom") or (side == "insideH" and inside):
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), "4")
            el.set(qn("w:color"), th.hair)
        else:
            el.set(qn("w:val"), "nil")
        borders.append(el)
    tbl_pr.append(borders)


def no_split(table):
    for row in table.rows:
        trpr = row._tr.get_or_add_trPr()
        trpr.append(OxmlElement("w:cantSplit"))


def set_col_widths(table, widths_in):
    """Fix widths in the grid and every cell so Word and LibreOffice agree."""
    table.autofit = False
    grid = table._tbl.tblGrid
    for col, w in zip(grid.findall(qn("w:gridCol")), widths_in):
        col.set(qn("w:w"), str(int(w * 1440)))
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    table._tbl.tblPr.append(layout)
    for row in table.rows:
        for cell, w in zip(row.cells, widths_in):
            cell.width = Inches(w)


# ---------- content ----------

def front_matter(doc, th, c, text_w):
    doc.add_paragraph(c["doc_type"], style="SH Eyebrow")
    doc.add_paragraph(c["title"], style="SH Title")
    if c.get("meta"):
        meta = doc.add_paragraph(c["meta"], style="SH Meta")
        para_border(meta._p.get_or_add_pPr(), "bottom", th.f["article"]["rule_pt"], th.ox, 10)
    rows = (c.get("at_a_glance") or []) if th.f.get("panel", True) else []
    if rows:
        doc.add_paragraph("At a Glance", style="SH Eyebrow").paragraph_format.space_before = Pt(6)
        t = doc.add_table(rows=len(rows), cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        hairline_table(t, th)
        for (label, value), row in zip(rows, t.rows):
            row.cells[0].paragraphs[0].style = doc.styles["SH Label"]
            row.cells[0].paragraphs[0].add_run(label)
            row.cells[1].paragraphs[0].style = doc.styles["SH Value"]
            add_inline(row.cells[1].paragraphs[0], value)
        set_col_widths(t, [1.9, text_w - 1.9])
        no_split(t)
        doc.add_paragraph("", style="SH Body").paragraph_format.space_after = Pt(2)


def body(doc, th, blocks):
    for blk in blocks:
        if "article" in blk:
            doc.add_paragraph(blk["article"], style="SH Article")
        elif "section" in blk:
            p = doc.add_paragraph(style="SH Section")
            lead = p.add_run(blk["section"].rstrip(".") + ".")
            lead.bold = True
            lead.font.small_caps = True
            p.add_run("  ")
            add_inline(p, blk.get("text", ""))
        elif "sub" in blk:
            add_inline(doc.add_paragraph(style="SH Subsection"), blk["sub"])
        elif "p" in blk:
            add_inline(doc.add_paragraph(style="SH Body"), blk["p"])
        elif "quote" in blk:
            add_inline(doc.add_paragraph(style="SH Quote"), blk["quote"])
        elif "bullets" in blk:
            for item in blk["bullets"]:
                add_inline(doc.add_paragraph(style="SH Bullet"), item)
        else:
            raise ValueError(f"Unknown block: {blk}")


def signature_page(doc, th, sig, text_w):
    doc.add_paragraph("[Signature page follows.]", style="SH Note")
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    doc.add_paragraph("Signature Page", style="SH Eyebrow")
    add_inline(doc.add_paragraph(style="SH Body"),
               sig.get("attestation", "The parties sign this Agreement to be effective on the Effective Date."))
    parties = list(sig.get("parties", []))
    if sig.get("firm", True):
        parties.append({"firm": True})
    cols = 2
    nrows = (len(parties) + cols - 1) // cols
    t = doc.add_table(rows=nrows, cols=cols)
    hairline_table(t, th, inside=False)
    # remove the top/bottom rules too: signature tables are borderless
    for el in t._tbl.tblPr.find(qn("w:tblBorders")):
        el.set(qn("w:val"), "nil")
    for i, party in enumerate(parties):
        cell = t.rows[i // cols].cells[i % cols]
        first = cell.paragraphs[0]
        first.style = doc.styles["SH Sig"]
        if party.get("firm"):
            lines = [(th.f["firm"]["signature_name"], True), ("", False),
                     ("_" * 30, False), ("By: " + th.f["firm"]["attorney"], False),
                     (th.f["firm"]["bar_no"], False), ("Date: ______________________", False)]
        else:
            lines = [(party["name"], True), ("", False), ("_" * 30, False)]
            for fld in party.get("fields", ["Name", "Title", "Date"]):
                lines.append((f"{fld}: ______________________", False))
        for j, (txt, is_name) in enumerate(lines):
            p = first if j == 0 else cell.add_paragraph(style="SH Sig")
            if txt == "":
                p.paragraph_format.space_after = Pt(24)
                continue
            r = p.add_run(txt)
            if is_name:
                r.bold = True
                r.font.small_caps = True
            p.paragraph_format.keep_with_next = True
        cell.add_paragraph(style="SH Sig").paragraph_format.space_after = Pt(18)
    set_col_widths(t, [text_w / 2] * 2)
    no_split(t)


def build(content, firm, out):
    th = Theme(firm, content.get("court_safe", False))
    doc = Document()
    build_styles(doc, th)
    build_numbering(doc, th)
    text_w = setup_page(doc, th, content)
    # python-docx starts with one empty paragraph; reuse nothing, just remove it
    for p in list(doc.paragraphs):
        p._p.getparent().remove(p._p)
    front_matter(doc, th, content, text_w)
    body(doc, th, content.get("body", []))
    if content.get("signature"):
        signature_page(doc, th, content["signature"], text_w)
    core = doc.core_properties
    core.title = content["title"]
    core.author = firm["firm"]["name"]
    core.comments = f"{firm['standard']} v{firm['version']}"
    doc.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("out")
    ap.add_argument("--firm", default=str(HERE.parent / "assets" / "firm.json"))
    a = ap.parse_args()
    content = json.loads(Path(a.content).read_text())
    firm = json.loads(Path(a.firm).read_text())
    build(content, firm, a.out)
    print(f"Built {a.out} ({firm['standard']} v{firm['version']})")


if __name__ == "__main__":
    sys.exit(main())
