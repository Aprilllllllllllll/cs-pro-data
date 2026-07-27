# CS Pro Data

A structured database of Counter-Strike professional players and teams — JSON storage, Pydantic validation, and a CLI toolchain for data integrity.

## Quick Start

```bash
# 1. Set up the environment
bash scripts/setup.sh

# 2. Validate all data
bash scripts/validate.sh

# 3. Rebuild the index
bash scripts/build_index.sh
```

## Project Structure

```
cs-pro-data/
├── data/
│   ├── players/                    # Player profiles, organized by current team
│   │   ├── <team_id>/              #   e.g. navi/, vitality/, spirit/
│   │   │   ├── _team.json          #   Team metadata
│   │   │   └── <player_id>.json    #   Player profile
│   │   ├── _retired/               # Retired players
│   │   └── _free_agents/           # Players without a team
│   ├── index.json                  # Auto-generated global index
│   └── templates/                  # Templates for manual data entry
│       ├── player_template.json
│       └── team_template.json
├── src/
│   ├── models/                     # Pydantic data models
│   │   ├── player.py               # Player model + enums
│   │   ├── team.py                 # Team model + enums
│   │   └── index.py                # Index model
│   ├── validators/
│   │   ├── validate_all.py         # 4-layer validation pipeline
│   │   └── build_index.py          # Index builder
│   └── scrapers/                   # Future: automated data collection
├── scripts/
│   ├── setup.sh
│   ├── validate.sh
│   └── build_index.sh
├── docs/
│   ├── data-schema.md              # Full schema reference
│   └── contribution-guide.md       # How to contribute data
├── tests/
├── logs/
└── pyproject.toml
```

## Sample Data

The repository includes 4 representative players across 4 teams:

| Player | Team | Country | Role | Major Titles | HLTV #1 |
|--------|------|---------|------|:---:|:---:|
| **s1mple** | NAVI | 🇺🇦 Ukraine | AWPer, Rifler | 1 | 3× |
| **ZywOo** | Vitality | 🇫🇷 France | AWPer | 1 | 4× |
| **donk** | Spirit | 🇷🇺 Russia | Entry, Rifler | 1 | 1× |
| **NiKo** | Falcons | 🇧🇦 Bosnia | Rifler, IGL | 0 | 0× |

## Adding a New Player

```bash
# 1. Copy the template
cp data/templates/player_template.json data/players/<team_id>/<player_id>.json

# 2. Edit the JSON file with player data

# 3. Validate
bash scripts/validate.sh

# 4. Rebuild the index
bash scripts/build_index.sh
```

## Adding a New Team

```bash
# 1. Create the team directory
mkdir -p data/players/<team_id>

# 2. Copy and fill in the team template
cp data/templates/team_template.json data/players/<team_id>/_team.json

# 3. Validate & rebuild
bash scripts/validate.sh && bash scripts/build_index.sh
```

## Data Sources

Data is collected from the following sources:

| Source | Content | Method |
|--------|---------|--------|
| [Liquipedia](https://liquipedia.net/counterstrike/) | Basic info, team history, achievements | Manual / API |
| [ProSettings.net](https://prosettings.net/) | Peripherals, sensitivity, settings | Manual |
| [HLTV](https://www.hltv.org/) | Statistics (Rating, ADR, etc.) | Manual (anti-scraping) |
| [Esports Earnings](https://www.esportsearnings.com/) | Prize money | Manual |

> **Note:** HLTV has strict anti-scraping measures. Statistics must be collected manually by browsing player pages.

## Validation Pipeline

The validator (`scripts/validate.sh`) runs 4 layers of checks:

1. **Structure** — JSON validity + Pydantic model validation
2. **Semantics** — Enum values, date formats, ISO country codes
3. **Cross-reference** — Player-team references (team_id, roster integrity)
4. **Consistency** — File name ↔ player ID, folder ↔ current_team

## Tech Stack

- **Python 3.11+** with **Pydantic v2** for data modeling
- **Rich** for terminal output
- **uv** for package management
- JSON files as the sole data store — Git-friendly, no database needed

## Documentation

- [Data Schema Reference](docs/data-schema.md) — Complete field definitions and types
- [Contribution Guide](docs/contribution-guide.md) — How to manually add or edit data

## License

Data sourced from Liquipedia is under [CC-BY-SA](https://creativecommons.org/licenses/by-sa/3.0/).