---
name: sponsorship-pitch
description: Builds a sponsorship or brand partnership pitch deck as a designed 16:9 PDF with speaker notes, from a brand and a property (venue, event, team, league, festival, tour, creator, platform or media property). Researches both sides, shows why they fit, proposes activation ideas, packages partnership tiers, and lays out how results will be measured. Use when someone asks for a sponsorship deck, partnership proposal, sponsor pitch, rights package, or help pitching a brand on a sponsorship. Usage - /sponsorship-pitch followed by the brand and the property, for example "Oatly x Coachella".
---

# Sponsorship Pitch

Turn "brand + property" into a partnership pitch a sales team could walk into a meeting with: why this brand, why now, who the property reaches, three activation ideas, tiered packages, measurement, timeline, and next steps. The deck is a 16:9 PDF in the property's colors and type, with a speaker notes file and, on request, a two-page leave-behind.

## Usage

```
/sponsorship-pitch <brand> x <property> [budget or tier] [short] [leave-behind]
```

Plain requests work too:

- "Make a sponsorship deck pitching Oatly on our summer concert series." (attach a rate card or asset list if you have one)
- "Partnership pitch: Rivian x Outside Lands."
- "I'm a creator with 400K followers. Pitch Liquid Death on a sponsorship."
- "Package our venue's assets into three sponsor tiers for a bank."
- Add "short" for an 8-slide version, or "leave-behind" for a two-page summary PDF too.

**Direction.** By default the property is pitching the brand (a sales or partnerships team selling sponsorship). If the person is on the brand or agency side proposing to a property, flip the framing: the deck sells the idea to the property, and tiers become "what we'd want" rather than "what we offer". Say which direction you took.

**Files.** `<skill-dir>` means this skill's folder, the one holding this SKILL.md. Templates are in `assets/`, scripts in `scripts/`, and the shared PDF steps (fonts, colors, render, check) are in `references/rendering.md`.

## Hard rules

- **Never invent the property's numbers.** Attendance, audience, reach, demographics, past partner results and prices come from the person, the property's own published materials, or credible press, each with a source. If one is missing, write `[TBD: what's needed]` in the deck and list every TBD in your reply.
- **Never invent rights fees.** Use the person's rate card. Without one, show the tier structure with "Price on request", or benchmark ranges from sources tagged `Estimate` with what they're based on.
- **Check conflicts.** Search for the brand's current sponsorships and the property's current partners. If a competitor of the brand holds a category the pitch would need (category exclusivity), lead the reply with it and design around it.
- **Attribute the brand's priorities.** "What they're going after" must come from their own statements, campaigns, launches, earnings calls or credible press, with dates. Don't put words in the brand's mouth.
- **No logos.** Use a typographic lockup ("OATLY × COACHELLA") and describe marks in words. Never copy brand artwork or photography into the deck.
- **Keep it a pitch, not a report.** One idea per slide, big type, short lines. Detail goes in the notes.
- Keep `notes.md` as you research (fact | source | date); tool results get cleared from context.

## Workflow

Make a task list from these steps and tick them off.

1. **Pin down the two sides and the direction.** Confirm the exact brand (parent company, product line, market) and the property (which event, which year, which venue). Note any numbers, rate card, asset list or budget the person gave.
2. **Research the brand** (15–25 lookups): marketing priorities for the last 12–18 months (campaigns, launches, target audiences, leadership statements), sponsorships they hold now and their categories, recent activations and how they were received, competitors' sponsorships, values or commitments that would shape an activation. Use a browser for their newsroom and careers pages when one is available.
3. **Research the property** (10–20 lookups): what it is, dates and footprint, audience size and profile with sources, media and social reach, current and past partners, signature moments, assets available (naming, signage, digital, content, hospitality, sampling, data).
4. **Find the fit.** Write three sentences: what the brand needs, what the property uniquely has, and the bridge between them. That bridge is the deck's thesis and the title-slide line.
5. **Develop three activation ideas** of different scale: one signature on-site experience, one content or media idea that travels beyond the venue, and one always-on or value-add idea (loyalty, sampling, community, cause). Each gets a name, the idea in one sentence, how it works in 3–5 steps, the fan's experience, the brand's role, which assets it uses, and how it's measured.
6. **Package tiers.** Three tiers by default (for example Presenting, Official, Supporting), each listing rights, on-site assets, digital and content, hospitality, activation included, and price. Map each idea to the tier that unlocks it.
7. **Measurement.** For each brand objective: the KPI, how it's measured (ticket scans, QR, sampling counts, social, brand lift, sales lift via promo codes), who reports it, and when.
8. **Brand the deck** in the property's colors and type (extract them from its site per references/brand-extraction.md; if the person is the property and gave their own brand, use that). Add the sponsor as the accent only if it doesn't clash.
9. **Build** from `assets/pitch-template.html` following references/rendering.md (copy `base.css` and `deck.css`). Default 12–15 slides; "short" is 8: title, opportunity, fit, audience, one idea, tiers, measurement, next steps.
10. **Write the speaker notes** in `<Brand>-x-<Property>-Speaker-Notes.md`: for each slide, what to say in 2–4 sentences, plus likely objections (price, conflicts, proof of results, timing) with answers.
11. **Leave-behind** (only if asked): a two-page `base.css` document with the thesis, audience, the three ideas, tiers and contact.
12. **Render, audit, check** the contact sheet. Read every slide once as the brand's CMO would: is each claim sourced, is the ask clear, would they know what to do next?
13. **Deliver** the PDF, notes and any leave-behind. In the reply: the thesis in one line, the TBDs to fill, any conflicts found, and one suggested next step.

Output names: `<Brand>-x-<Property>-Partnership-Pitch-<YYYY-MM>.pdf`.

## Slide guide

| Slide | What goes on it |
|---|---|
| Title | Lockup, the thesis line, "Prepared for <brand team>", date, the property's name |
| The opportunity | The bridge in one sentence and three proof points with numbers |
| What <Brand> is going after | 3 priorities, each with evidence and date |
| Who we reach | 3–4 KPIs with sources, then who the shared audience is in plain words |
| The property | What it is, scale, signature moments, calendar |
| Ideas (divider) | |
| Idea 1–3 | Name, big idea, how it works, fan experience, assets used |
| Partnership tiers | Table: rights, assets, activation, media, hospitality, price |
| Measurement | Objective → KPI → method → reporting |
| Timeline | Signing → build → activation → recap, with dates |
| Track record | Past partner results, only if provided or published |
| Next steps | 2–3 concrete asks with dates, and the contact |
| Sources | Every number's source |
