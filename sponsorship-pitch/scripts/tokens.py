#!/usr/bin/env python3
"""Turn a few brand colors into the full token block for doc.html.

Example:
  python3 tokens.py --brand "#141213" --accent "#2EA281" \
      --font-display "Inter Tight" --font-label "DM Mono" \
      --footer "Acme · Company Brief · Nov 2026" \
      --cover-stops "#F4BE5C,#E4C187,#9EB7B3" --brand-soft "#E3FCEE" > tokens.html

Paste the printed <style> block into doc.html after base.css.
It also prints a contrast report to stderr and fixes what it safely can:
- darkens --accent until small links/labels reach 4.5:1 on paper
- picks white or ink for text on the brand color
- checks cover text against every cover gradient stop
"""
import argparse
import sys


def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(c))) for c in rgb)


def lum(h):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex_to_rgb(h)
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    l1, l2 = sorted((lum(a), lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def mix(a, b, t):
    """t of color a over color b (t=0.1 -> 10% a)."""
    ra, rb = hex_to_rgb(a), hex_to_rgb(b)
    return rgb_to_hex(tuple(ra[i] * t + rb[i] * (1 - t) for i in range(3)))


def darken_until(color, bg, target, step=0.04):
    c = color
    for _ in range(40):
        if contrast(c, bg) >= target:
            return c
        c = mix("#000000", c, step)
    return c


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--brand", required=True, help="primary brand color (headings, rules, default cover)")
    p.add_argument("--accent", required=True, help="secondary brand color (links, markers, meters)")
    p.add_argument("--ink", default="#16181d")
    p.add_argument("--paper", default="#ffffff")
    p.add_argument("--muted", default=None)
    p.add_argument("--brand-soft", default=None, help="callout tint; default is a light mix of brand (or accent if brand is near-black)")
    p.add_argument("--accent-soft", default=None)
    p.add_argument("--font-display", default="DM Sans")
    p.add_argument("--font-body", default=None)
    p.add_argument("--font-label", default=None, help="small labels/eyebrows; use the brand's mono if it has one")
    p.add_argument("--display-weight", default="600")
    p.add_argument("--tracking", default="-0.02em")
    p.add_argument("--radius", default="8px")
    p.add_argument("--footer", default="")
    p.add_argument("--cover-stops", default=None, help="comma list of hex stops for a gradient cover (top-left to bottom-right)")
    p.add_argument("--cover-ink", default=None)
    argv = sys.argv[1:]
    for i, x in enumerate(argv[:-1]):  # let "--tracking -0.03em" work (argparse reads -0.03em as a flag)
        if x == "--tracking" and argv[i + 1].startswith("-"):
            argv[i:i + 2] = [f"--tracking={argv[i + 1]}"]
            break
    a = p.parse_args(argv)

    notes = []
    paper, ink, brand = a.paper, a.ink, a.brand
    body = a.font_body or a.font_display
    label = a.font_label or body
    muted = a.muted or mix(ink, paper, 0.66)
    if contrast(muted, paper) < 4.5:
        muted = darken_until(muted, paper, 4.6)
        notes.append(f"muted darkened to {muted}")

    accent = a.accent
    if contrast(accent, paper) < 4.5:
        fixed = darken_until(accent, paper, 4.6)
        notes.append(f"accent {accent} -> {fixed} so small links/labels reach 4.5:1 (keep {accent} for big shapes)")
        accent_shape = accent
        accent = fixed
    else:
        accent_shape = accent

    brand_ink = "#ffffff" if contrast("#ffffff", brand) >= contrast(ink, brand) else ink
    if contrast(brand, paper) < 3:
        notes.append(f"WARNING brand {brand} is too light for headings ({contrast(brand, paper):.2f}:1); pass the brand's dark color as --brand and the light one as --accent or a cover stop")

    near_black = lum(brand) < 0.03
    brand_soft = a.brand_soft or (mix(accent_shape, paper, 0.12) if near_black else mix(brand, paper, 0.09))
    accent_soft = a.accent_soft or mix(accent_shape, paper, 0.12)
    accent_deep = darken_until(mix(accent, ink, 0.75), accent_soft, 4.6)
    rule = mix(ink, paper, 0.14)

    if a.cover_stops:
        stops = [s.strip() for s in a.cover_stops.split(",") if s.strip()]
        cover_ink = a.cover_ink or (ink if min(contrast(ink, s) for s in stops) >= min(contrast("#ffffff", s) for s in stops) else "#ffffff")
        worst = min(contrast(cover_ink, s) for s in stops)
        if worst < 4.5:
            notes.append(f"WARNING cover text {cover_ink} only reaches {worst:.2f}:1 on the lightest/darkest stop; adjust stops")
        n = len(stops)
        lin = ", ".join(f"{s} {round(i * 100 / max(1, n - 1))}%" for i, s in enumerate(stops))
        cover_bg = (f"radial-gradient(70% 55% at 100% 100%, {stops[-1]}f2 0%, {stops[-1]}00 70%), "
                    f"linear-gradient(170deg, {lin})")
        cover_solid = stops[0]
    else:
        cover_ink = a.cover_ink or brand_ink
        cover_bg = brand
        cover_solid = brand
    cover_rule = "rgba(255,255,255,.32)" if cover_ink.lower() in ("#fff", "#ffffff") else "rgba(0,0,0,.28)"

    good, bad = "#1f6f43", "#a3322b"
    css = f"""<style>
:root {{
  --brand: {brand}; --brand-ink: {brand_ink}; --accent: {accent}; --accent-shape: {accent_shape}; --accent-deep: {accent_deep};
  --ink: {ink}; --muted: {muted}; --paper: {paper}; --rule: {rule};
  --brand-soft: {brand_soft}; --accent-soft: {accent_soft}; --muted-soft: {mix(muted, paper, 0.14)};
  --good-soft: {mix(good, paper, 0.11)}; --bad-soft: {mix(bad, paper, 0.09)};
  --cover-bg: {cover_bg}; --cover-ink: {cover_ink}; --cover-rule: {cover_rule}; --cover-bg-solid: {cover_solid};
  --font-display: "{a.font_display}", system-ui, sans-serif; --font-body: "{body}", system-ui, sans-serif; --font-label: "{label}", ui-monospace, monospace;
  --display-weight: {a.display_weight}; --display-tracking: {a.tracking}; --radius: {a.radius};
}}
@page {{ background: {paper};
  @bottom-left {{ content: "{a.footer}"; font-family: "{body}", sans-serif; font-size: 7.5pt; color: {muted}; }}
  @bottom-right {{ content: counter(page); font-family: "{body}", sans-serif; font-size: 7.5pt; color: {muted}; }} }}
@page cover {{ margin: 0; @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}
.meter i.on {{ background: {accent_shape}; }}
li::marker {{ color: {accent_shape}; }}
</style>"""
    print(css)

    report = [
        ("ink on paper", contrast(ink, paper), 7),
        ("muted on paper", contrast(muted, paper), 4.5),
        ("accent (links) on paper", contrast(accent, paper), 4.5),
        ("brand on paper", contrast(brand, paper), 3),
        ("brand-ink on brand", contrast(brand_ink, brand), 4.5),
        ("ink on brand-soft", contrast(ink, brand_soft), 4.5),
        ("accent-deep on accent-soft", contrast(accent_deep, accent_soft), 4.5),
        ("cover text on cover (worst stop)", min(contrast(cover_ink, s) for s in (stops if a.cover_stops else [brand])), 4.5),
    ]
    for name, r, m in report:
        print(f"{'ok  ' if r >= m else 'FAIL'} {name}: {r:.2f} (min {m})", file=sys.stderr)
    for n in notes:
        print("note: " + n, file=sys.stderr)


if __name__ == "__main__":
    main()
