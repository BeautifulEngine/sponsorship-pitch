#!/usr/bin/env python3
"""Make one image of every page so you can check the layout at a glance.

Usage: python3 contact_sheet.py doc.pdf sheet.png [columns]
Then open sheet.png. For a close look at one page:
  pdftoppm -r 150 -f 3 -l 3 -png doc.pdf page
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image


def pages_as_images(pdf, tmp, dpi=45):
    if shutil.which("pdftoppm"):
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", pdf, os.path.join(tmp, "p")], check=True)
        return [Image.open(f) for f in sorted(glob.glob(os.path.join(tmp, "p-*.png")))]
    try:
        import pypdfium2 as pdfium  # pip install pypdfium2
    except ImportError:
        sys.exit("Need pdftoppm (poppler-utils) or pypdfium2 to preview pages.")
    doc = pdfium.PdfDocument(pdf)
    return [doc[i].render(scale=dpi / 72).to_pil() for i in range(len(doc))]


def main():
    pdf = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "sheet.png"
    cols = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    with tempfile.TemporaryDirectory() as tmp:
        ims = [im.convert("RGB") for im in pages_as_images(pdf, tmp)]
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + 8) + 8, rows * (h + 8) + 8), "#777777")
    for i, im in enumerate(ims):
        sheet.paste(im, (8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 8)))
    sheet.save(out)
    print(f"{len(ims)} pages -> {out}")


if __name__ == "__main__":
    main()
