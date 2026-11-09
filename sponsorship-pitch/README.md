# Sponsorship Pitch

Builds a sponsorship or brand partnership pitch deck as a designed 16:9 PDF with speaker notes, from a brand and a property (venue, event, team, league, festival, tour, creator, platform or media property). Researches both sides, shows why they fit, proposes activation ideas, packages partnership tiers, and lays out how results will be measured.

## Install

**Claude app (web, desktop):** turn on Settings > Capabilities > "Code execution and file creation". Then go to Customize > Skills, click "+", then "+ Create skill" > "Upload a skill", and upload `sponsorship-pitch.zip` as is (don't unzip it).

**Claude Code:** install the whole Beautiful Engine collection:

```bash
claude plugin marketplace add BeautifulEngine/skills
claude plugin install beautiful-engine@beautiful-engine
```

Then use `/beautiful-engine:sponsorship-pitch`, or ask in plain words.

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

## Made by Beautiful Engine

Made by [Beautiful Engine](https://www.beautifulengine.com), a creative studio in Los Angeles. Questions, ideas, or something broke? [Open an issue](https://github.com/BeautifulEngine/skills/issues/new). More skills: [github.com/BeautifulEngine/skills](https://github.com/BeautifulEngine/skills).

