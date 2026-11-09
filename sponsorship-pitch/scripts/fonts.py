#!/usr/bin/env python3
"""Install free brand fonts from Fontsource (npm) into the working folder and
print the <link> tags for doc.html.

Usage (run from the working folder):
  python3 fonts.py "Inter Tight:400,500,600" "DM Mono:400,500"

Each argument is "Family Name:weights". Family names are Google Fonts names
(Fontsource mirrors them). For a proprietary brand font, pass the closest free
stand-in you chose (see references/brand-extraction.md).
"""
import json
import os
import re
import shutil
import subprocess
import sys


def slug(family):
    return re.sub(r"[^a-z0-9]+", "-", family.lower()).strip("-")


def main():
    specs = []
    for arg in sys.argv[1:]:
        fam, _, w = arg.partition(":")
        weights = [x.strip() for x in (w or "400,600").split(",") if x.strip()]
        specs.append((fam.strip(), slug(fam), weights))
    if not specs:
        sys.exit(__doc__)

    npm = shutil.which("npm")
    if npm:
        pkgs = [f"@fontsource/{s}" for _, s, _ in specs]
        # Save to a local package.json: "npm install --no-save" would delete fonts from earlier runs.
        if not os.path.exists("package.json"):
            with open("package.json", "w") as f:
                json.dump({"name": "beautiful-engine-fonts", "private": True}, f)
        cmd = [npm, "install", "--no-audit", "--no-fund", "--silent"]
        if subprocess.run(cmd + pkgs, capture_output=True, text=True).returncode:
            # one bad name fails the whole batch, so retry each package on its own
            for pkg in pkgs:
                r = subprocess.run(cmd + [pkg], capture_output=True, text=True)
                if r.returncode:
                    print(f"npm could not install {pkg}. {r.stderr.strip()[:200]}", file=sys.stderr)
    else:
        print("npm not found.", file=sys.stderr)

    ok = True
    for fam, s, weights in specs:
        base = os.path.join("node_modules", "@fontsource", s)
        if not os.path.isdir(base):
            ok = False
            print(f"MISSING {fam}: not on Fontsource or not installed. Check the exact Google Fonts name.", file=sys.stderr)
            continue
        have = sorted({m.group(1) for f in os.listdir(base) if (m := re.fullmatch(r"(\d{3})\.css", f))})
        for w in weights:
            if w in have:
                print(f'<link rel="stylesheet" href="node_modules/@fontsource/{s}/{w}.css">')
            else:
                print(f"note: {fam} has no {w} weight; available: {', '.join(have)}", file=sys.stderr)
        italic = [f"{w}-italic.css" for w in weights if os.path.exists(os.path.join(base, f"{w}-italic.css"))]
        if italic:
            print(f"note: italics available for {fam}: {', '.join(italic)}", file=sys.stderr)

    if not ok:
        fc = shutil.which("fc-list")
        if fc:
            fams = subprocess.run([fc, ":", "family"], capture_output=True, text=True).stdout.splitlines()
            fams = sorted({f.split(",")[0] for f in fams if f.strip()})
            print("Fonts installed on this machine you can fall back to: " + ", ".join(fams[:40]), file=sys.stderr)
        print("Fallback: use an installed family in tokens.py and say so in the Type section.", file=sys.stderr)


if __name__ == "__main__":
    main()
