# Data Contribution Guide

This guide explains how to manually add or edit CS player and team data.

## Quick Start

### 1. Copy the Template

```bash
# Add a new player
cp data/templates/player_template.json data/players/<team_id>/<player_id>.json

# Add a new team
cp data/templates/team_template.json data/players/<team_id>/_team.json
```

### 2. Fill in the Data

Edit the JSON file with the player's information. See [data-schema.md](data-schema.md) for detailed field descriptions.

### 3. Validate

```bash
bash scripts/validate.sh
```

Ensure there are no ERROR-level issues. WARNINGs are acceptable (e.g., historical team references that haven't been created yet).

### 4. Rebuild the Index

```bash
bash scripts/build_index.sh
```

## Data Sources

| Priority | Website | Content | Method |
|:---:|---------|---------|--------|
| 1 | [Liquipedia](https://liquipedia.net/counterstrike/) | Basic info, team history, achievements | Manual lookup |
| 2 | [ProSettings.net](https://prosettings.net/) | Peripherals, sensitivity, resolution | Manual lookup |
| 3 | [HLTV](https://www.hltv.org/) | Statistics (Rating, ADR, etc.) | Manual lookup |
| 4 | [Esports Earnings](https://www.esportsearnings.com/) | Prize money | Manual lookup |

## Manual Data Collection from HLTV

HLTV has strict anti-scraping measures. Please collect data manually by browsing:

### Player Page
1. Open `https://www.hltv.org/player/<id>/<name>`
2. **Top card** → Get: Rating 2.0, KPR, DPR, Impact, ADR, KAST
3. **"Statistics" tab** → Get: total maps, total kills, headshot %
4. **"Achievements" section** → Get: Major appearances, MVP medals
5. **"Team History" section** → Get: historical team timeline

### Team Page
1. Open `https://www.hltv.org/team/<id>/<name>`
2. **Top section** → Get: best HLTV ranking
3. **"Roster" section** → Get: current roster

## Field Conventions

### Player ID
- Game alias in lowercase, e.g. `s1mple`, `zywoo`, `donk`
- Preserve original spelling, including numbers and special characters
- For duplicate names, add a suffix: `niko-faze` vs `niko-og`

### Country Codes
Use [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) two-letter codes:
- Ukraine → `UA`
- France → `FR`
- Russia → `RU`
- Denmark → `DK`
- International roster → `international`

### Date Format
Always use `YYYY-MM-DD` format, e.g. `2021-11-07`.

### Tournament Tiers
- **S-Tier**: Majors, IEM Katowice, IEM Cologne, BLAST World Final, etc.
- **A-Tier**: ESL Pro League, BLAST Premier, other IEM events, etc.
- **B-Tier**: Regional leagues and secondary events

## Directory Conventions

- Player files go in `data/players/<current_team_id>/`
- File name must match the player `id`: `s1mple.json`
- Retired players go in `data/players/_retired/`
- Free agents go in `data/players/_free_agents/`
- Team info is always named `_team.json` inside the team's folder

## Examples

See the existing data in `data/players/` for complete examples:

- [s1mple](../data/players/navi/s1mple.json) — Full player profile
- [NAVI _team.json](../data/players/navi/_team.json) — Team profile
- [donk](../data/players/spirit/donk.json) — Rising star profile
- [Zywoo](../data/players/vitality/zywoo.json) — Current top player
- [NiKo](../data/players/falcons/niko.json) — Veteran with extensive team history