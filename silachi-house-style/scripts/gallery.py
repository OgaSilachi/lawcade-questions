#!/usr/bin/env python3
"""Render the same content in every style direction and lay page 1 side by side.

Usage:
    python3 gallery.py content.json out_dir [--directions ../assets/directions] [--firm ../assets/firm.json]

Writes one .docx and one page-1 PNG per direction, plus gallery.png (a
contact sheet). This is the gallery Claude does not have: the Partner picks
by looking, not by reading adjectives. Needs LibreOffice (soffice) and
pdftoppm for the PNGs; without them it still writes the .docx files.
"""
import argparse
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build import build  # noqa: E402


def merge(base, over):
    out = copy.deepcopy(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge(out[k], v)
        else:
            out[k] = v
    return out


def render_page1(docx, out_dir):
    if not (shutil.which("soffice") and shutil.which("pdftoppm")):
        return None
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(docx)],
                   check=True, capture_output=True)
    pdf = out_dir / (docx.stem + ".pdf")
    stem = out_dir / docx.stem
    subprocess.run(["pdftoppm", "-r", "70", "-png", "-f", "1", "-l", "1", "-singlefile", str(pdf), str(stem)], check=True)
    return Path(str(stem) + ".png")


def contact_sheet(items, out):
    from PIL import Image, ImageDraw, ImageFont
    imgs = [(label, Image.open(p)) for label, p in items if p]
    if not imgs:
        return None
    w, h = imgs[0][1].size
    cols, pad, cap = 3, 24, 34
    rows = (len(imgs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + pad) + pad, rows * (h + pad + cap) + pad), "#EDEBE8")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    for i, (label, im) in enumerate(imgs):
        x = pad + (i % cols) * (w + pad)
        y = pad + (i // cols) * (h + pad + cap)
        draw.text((x, y + 6), label, fill="#1A1A1A", font=font)
        sheet.paste(im, (x, y + cap))
    sheet.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("out_dir")
    ap.add_argument("--directions", default=str(HERE.parent / "assets" / "directions"))
    ap.add_argument("--firm", default=str(HERE.parent / "assets" / "firm.json"))
    a = ap.parse_args()
    out_dir = Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    base = json.loads(Path(a.firm).read_text())
    content = json.loads(Path(a.content).read_text())
    items = []
    for f in sorted(Path(a.directions).glob("*.json")):
        over = json.loads(f.read_text())
        label = over.pop("label", f.stem)
        docx = out_dir / f"{f.stem}.docx"
        build(content, merge(base, over), str(docx))
        items.append((label, render_page1(docx, out_dir)))
        print(f"Built {docx.name}")
    sheet = contact_sheet(items, out_dir / "gallery.png")
    print(f"Contact sheet: {sheet}" if sheet else "No renderer found; open the .docx files directly.")


if __name__ == "__main__":
    main()
