#!/usr/bin/env python3
"""Render doc.html to PDF. Tries, in order:
1. Python Playwright with its bundled Chromium (full audit)
2. Python Playwright driving an installed Chrome/Chromium (full audit)
3. Headless Chrome/Chromium command line (no audit)
4. WeasyPrint (no audit; pip install weasyprint)

Usage: python3 render.py doc.html "Output-2026-11.pdf"
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def report(r):
    problems = 0
    for f in r["fonts"]:
        print(("ok   " if f["loaded"] else "FAIL ") + f"font {f['token']}: {f['family']}")
        problems += not f["loaded"]
    if r["lowContrast"]:
        for k, o in r["lowContrast"].items():
            print(f"FAIL contrast {o['ratio']}:1  {k}  e.g. \"{o['example']}\"")
            problems += 1
    else:
        print("ok   all text outside the cover is 4.5:1 or better")
    if r["placeholders"]:
        print("FAIL leftover placeholders: " + ", ".join(r["placeholders"]))
        problems += 1
    return problems


def with_playwright(src, out):
    from playwright.sync_api import sync_playwright
    url = "file://" + os.path.abspath(src)
    audit = open(os.path.join(HERE, "audit.js"), encoding="utf-8").read()
    with sync_playwright() as p:
        browser = None
        errors = []
        for kwargs in ({}, {"channel": "chrome"}, {"executable_path": shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome") or ""}):
            if kwargs.get("executable_path") == "":
                continue
            try:
                browser = p.chromium.launch(**kwargs)
                break
            except Exception as e:  # try the next browser
                errors.append(str(e).splitlines()[0])
        if browser is None:
            raise RuntimeError("; ".join(errors))
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        r = json.loads(page.evaluate(audit))
        page.pdf(path=out, prefer_css_page_size=True, print_background=True)
        browser.close()
    return report(r)


def with_chrome_cli(src, out):
    exe = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    if not exe:
        raise RuntimeError("no chrome binary")
    subprocess.run([exe, "--headless=new", "--no-sandbox", "--no-pdf-header-footer",
                    f"--print-to-pdf={os.path.abspath(out)}", "file://" + os.path.abspath(src)],
                   check=True, capture_output=True, timeout=120)
    print("note: rendered with headless Chrome CLI; fonts/contrast not audited")
    return 0


def with_weasyprint(src, out):
    import weasyprint
    weasyprint.HTML(filename=src, base_url=os.path.dirname(os.path.abspath(src))).write_pdf(out)
    print("note: rendered with WeasyPrint; fonts/contrast not audited. Check the preview closely.")
    return 0


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "doc.html"
    out = sys.argv[2] if len(sys.argv) > 2 else "doc.pdf"
    order = (("playwright", with_playwright), ("chrome-cli", with_chrome_cli), ("weasyprint", with_weasyprint))
    force = os.environ.get("BRIEF_RENDERER")  # e.g. BRIEF_RENDERER=weasyprint to test one renderer
    for name, fn in [o for o in order if not force or o[0] == force]:
        try:
            problems = fn(src, out)
            print(f"wrote {out} via {name}" + (f" with {problems} problem(s) to fix" if problems else ""))
            return
        except Exception as e:
            print(f"skip {name}: {str(e).splitlines()[0] if str(e) else type(e).__name__}", file=sys.stderr)
    sys.exit("No renderer worked. Install one: pip install playwright && python -m playwright install chromium, or pip install weasyprint")


if __name__ == "__main__":
    main()
