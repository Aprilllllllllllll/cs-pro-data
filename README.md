# CS Pro Data

A structured database of Counter-Strike professional players and teams — JSON storage, Pydantic validation, and a CLI toolchain for data integrity.

## Quick Start

```bash
bash scripts/setup.sh            # Set up environment
bash scripts/scrape.sh s1mple    # Scrape a player from Liquipedia
bash scripts/validate.sh         # Validate all data
bash scripts/build_index.sh      # Rebuild index
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
├── scripts/
│   ├── setup.sh
│   ├── validate.sh
│   ├── build_index.sh
│   └── scrape.sh
├── src/
│   ├── models/                     # Pydantic data models
│   └── scrapers/
│       └── liquipedia.py           # Liquipedia API scraper
├── docs/
│   ├── data-schema.md              # Field reference
│   └── contribution-guide.md       # Manual entry guide
└── pyproject.toml
```

## Sample Data

| Player | Team | Country | Role | Age | Major |
|--------|------|---------|------|:---:|:----:|
| **s1mple** | NAVI | 🇺🇦 Ukraine | AWPer, Rifler | 28 | 1× |
| **ZywOo** | Vitality | 🇫🇷 France | AWPer | 25 | 1× |
| **donk** | Spirit | 🇷🇺 Russia | Entry, Rifler | 19 | 1× |
| **NiKo** | Falcons | 🇧🇦 Bosnia | Rifler, IGL | 29 | 0× |
| **karrigan** | Falcons | 🇩🇰 Denmark | IGL, Entry | — | 0× |
| **dev1ce** | 100 Thieves | 🇩🇰 Denmark | AWPer | — | 4× |

## Adding a Player

```bash
cp data/templates/player_template.json data/players/<team_id>/<player_id>.json
# Edit JSON, then:
bash scripts/validate.sh
bash scripts/build_index.sh

# Or just scrape:
bash scripts/scrape.sh <player_id>
```

## Tech Stack

- **Python 3.11+** with **Pydantic v2**
- **uv** for package management
- JSON files as the sole data store