# Making the PDF

Every Beautiful Engine skill that produces a PDF uses the same pipeline: HTML styled with this skill's stylesheets, colors and fonts set by two scripts, rendered by headless Chrome, then checked. `<skill-dir>` means this skill's folder (the one holding SKILL.md).

## 1. Working folder

```bash
mkdir -p <project-slug> && cd <project-slug>
cp <skill-dir>/assets/base.css .            # documents
cp <skill-dir>/assets/deck.css .            # 16:9 decks only
cp <skill-dir>/assets/<template>.html doc.html
```

Keep a `notes.md` beside it with every fact, number and source as you find them; tool results get cleared from context in long sessions.

## 2. Fonts

```bash
python3 <skill-dir>/scripts/fonts.py "<Display Font>:400,600,700" "<Body Font>:400,600" "<Label Font>:400,500"
```

Paste the printed `<link>` lines at the FONT LINKS marker. Use Google Fonts names (Fontsource mirrors them). For a paid brand font, use the closest free stand-in (brand-extraction.md, section 2, when this skill has it) and say so where the type is described. If npm can't install anything, pick an installed family from `fc-list : family`.

## 3. Colors

```bash
python3 <skill-dir>/scripts/tokens.py --brand "#…" --accent "#…" \
  --font-display "<Display Font>" --font-body "<Body Font>" --font-label "<Label Font>" \
  --display-weight 600 --tracking -0.02em --radius 8px \
  --footer "<short footer text>" [--cover-stops "#…,#…,#…"] > tokens.html
```

Paste `tokens.html` at the TOKENS marker. Every line of the report it prints should say `ok`; a `WARNING` means pick different colors. `--brand` must be dark enough for headings (3:1 on white). For a light signature color, make the dark color `--brand` and the light one `--accent` or a cover stop. Without any brand to follow, use near-black `#16181d` with one confident accent.

## 4. Render and audit

```bash
node <skill-dir>/scripts/render.cjs doc.html "<Output-Name>.pdf" \
  || python3 <skill-dir>/scripts/render.py doc.html "<Output-Name>.pdf"
```

Fix every `FAIL` line (font didn't load, text under 4.5:1 contrast, a `{{placeholder}}` left behind) and render again. The Node renderer exits with code 2 when Playwright is missing, which hands off to the Python one; that tries Playwright, then a Chrome binary, then WeasyPrint. On someone's own computer, ask before installing a renderer.

## 5. Look at it

```bash
python3 <skill-dir>/scripts/contact_sheet.py "<Output-Name>.pdf" sheet.png
```

Open `sheet.png` and check: nothing clipped or overflowing, no near-empty pages, no heading stranded at the bottom of a page, tables fit, slides aren't crowded (if a slide is dense, split it). For a closer look at one page: `pdftoppm -r 110 -f N -l N -png "<Output-Name>.pdf" page`.

## Layout pieces

Documents (`base.css`): `.cover` (full-bleed first page), `.part-head`, section headings as `<h2 class="sec"><span class="num">01</span>Title</h2>` with `<h3 class="sub">` beneath them (keep heading levels in order: h1, then h2, then h3), `.callout` (`.big`, `.accent`, `.warn`), `.stats` > `.stat` (`.v`, `.k`, `.n`), `table.glance`, `table.data` (`td.num`, `tr.us`), `.cols` > `.card` (`.good`, `.bad`, `.plain`), `.timeline` > `.tl` (`.when`), `.swatches` > `.sw`, `.tag` (`.verified`, `.reported`, `.claim`, `.estimate`, `.unknown`), `ol.big` with `.why`, `ol.sources`, `.lede`, `.small`, `.muted`, `.credit`.

Decks (`deck.css`, after `base.css`): each `.slide` is one 16:9 page with an optional `.eyebrow`, `h2`, `.lede`, `.body` and `.foot` (left text; the slide number is added). `.slide.title-slide` is the brand cover, `.slide.section` a divider in the brand color. Layout: `.grid` with `.g2`, `.g3`, `.g4`, `.g-2-1`, `.g-1-2`; `.panel` (`.accent`, `.line`); `.kpi` (`.v`, `.k`, `.n`); `.steps` (numbered); `.plan` (wraps an SVG diagram); `.chip-row`; `.notes` (hidden).

## Writing rules for anything a client or employer will read

- Plain, specific and confident. Lead with the point, then the evidence. Short bullets and tables over long paragraphs.
- Every number has a source or is labeled as an estimate with its basis. Never invent results, prices, audience figures or experience.
- Avoid buzzwords ("revolutionary", "cutting-edge", "game-changing", "seamless", "synergy") and staged one-liners ("No X. Just Y."). Write full sentences.
- Never reproduce logos or brand artwork. Name the brands in text, describe marks in words, and link official assets.
