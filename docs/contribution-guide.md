# Contribution Guide

## Quick Start

```bash
# Add a new player
cp data/templates/player_template.json data/players/<team_id>/<player_id>.json
# Edit the JSON file, then:
bash scripts/validate.sh
bash scripts/build_index.sh

# Or scrape from Liquipedia
bash scripts/scrape.sh <player_id>
```

## Data Sources

| Source | Content | Method |
|--------|---------|--------|
| Liquipedia | Basic info, team history | `bash scripts/scrape.sh <id>` |
| HLTV | Statistics, achievements | Manual (see below) |

## Directory Rules

- Player files: `data/players/<current_team_id>/<player_id>.json`
- Retired players: `data/players/_retired/`
- Free agents: `data/players/_free_agents/`
- Team info: `data/players/<team_id>/_team.json`

## HLTV Manual Collection

For statistics (Rating, ADR, etc.) and detailed achievements (Major titles, MVP medals), visit:
- `https://www.hltv.org/player/<id>/<name>` -> Statistics tab
- `https://www.hltv.org/team/<id>/<name>` -> Roster info