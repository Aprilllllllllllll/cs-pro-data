# Data Schema Reference

## Directory Structure

```
data/
├── players/                    # Player profiles, organized by current team folder
│   ├── <team_id>/              # Folder name = team_id
│   │   ├── _team.json          # Team metadata
│   │   ├── <player_id>.json    # Player profile
│   │   └── ...
│   ├── _retired/               # Retired players
│   └── _free_agents/           # Players without a team
├── index.json                  # Auto-generated global index (do not edit manually)
└── templates/                  # Templates for manual data entry
    ├── player_template.json
    └── team_template.json
```

## Player JSON Schema

### Top-level Fields

| Field | Type | Required | Description |
|-------|------|:---:|-------------|
| `id` | string | ✅ | Unique player ID, game alias in lowercase, e.g. `s1mple`, `zywoo` |
| `name` | string | ✅ | Real name (English), e.g. `Oleksandr Kostyliev` |
| `native_name` | string \| null | | Native language name |
| `country` | string | ✅ | ISO 3166-1 alpha-2 country code, e.g. `UA`, `FR` |
| `country_name` | string | ✅ | Country name in English, e.g. `Ukraine` |
| `birth_date` | string \| null | | Birth date, format `YYYY-MM-DD` |
| `status` | enum | ✅ | `active` / `inactive` / `retired` / `banned` |
| `roles` | enum[] | | `AWPer` / `IGL` / `Entry` / `Support` / `Rifler` / `Lurker` / `Coach` |
| `years_active` | string \| null | | Active years, e.g. `2013-present` |

### current_team

| Field | Type | Required | Description |
|-------|------|:---:|-------------|
| `team_id` | string | ✅ | Current team ID |
| `join_date` | string | ✅ | Join date, format `YYYY-MM-DD` |
| `contract_expiry` | string \| null | | Contract expiry date |

### team_history[]

| Field | Type | Required | Description |
|-------|------|:---:|-------------|
| `team_id` | string | ✅ | Historical team ID |
| `start_date` | string | ✅ | Join date |
| `end_date` | string \| null | | Leave date, `null` if still on the team |
| `status` | enum | | `starter` / `substitute` / `stand-in` / `loan` |

### major_titles[]

| Field | Type | Description |
|-------|------|-------------|
| `major_name` | string | Full Major tournament name |
| `date` | string | Championship date |
| `team_id` | string | Team at time of win |
| `placement` | string | Placement, `1st` for champion |

### hltv_top20_rankings[]

| Field | Type | Description |
|-------|------|-------------|
| `year` | int | Year of ranking |
| `rank` | int | Rank (1-20) |

### mvp_medals[]

| Field | Type | Description |
|-------|------|-------------|
| `tournament` | string | Tournament name |
| `date` | string | Date |
| `tier` | string | Tournament tier: `S-Tier` / `A-Tier` / `B-Tier` |

### statistics

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `hltv_rating` | float \| null | HLTV Rating 2.0 | HLTV |
| `total_maps` | int \| null | Total maps played | HLTV |
| `total_kills` | int \| null | Total kills | HLTV |
| `headshot_percentage` | float \| null | Headshot % | HLTV |
| `kills_per_round` | float \| null | Kills per round (KPR) | HLTV |
| `deaths_per_round` | float \| null | Deaths per round (DPR) | HLTV |
| `impact_rating` | float \| null | Impact rating | HLTV |
| `kast` | float \| null | KAST % | HLTV |
| `adr` | float \| null | Average damage per round | HLTV |

### social_links

| Field | Type | Description |
|-------|------|-------------|
| `twitter` | string \| null | Twitter/X profile URL |
| `twitch` | string \| null | Twitch channel URL |
| `instagram` | string \| null | Instagram profile URL |
| `youtube` | string \| null | YouTube channel URL |

### settings (Peripherals & Game Settings)

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `crosshair_code` | string \| null | Crosshair code (CS2 format) | ProSettings |
| `config_url` | string \| null | Config file download URL | ProSettings |
| `sensitivity` | float \| null | Mouse sensitivity | ProSettings |
| `edpi` | float \| null | Effective DPI | ProSettings |
| `zoom_sensitivity` | float \| null | Zoom sensitivity | ProSettings |
| `raw_input` | bool \| null | Raw input enabled | ProSettings |
| `resolution` | string \| null | e.g. `1280x960` | ProSettings |
| `aspect_ratio` | string \| null | e.g. `4:3` | ProSettings |
| `scaling_mode` | string \| null | `Stretched` / `Black Bars` / `Native` | ProSettings |
| `monitor` | string \| null | Monitor model | ProSettings |
| `mouse` | string \| null | Mouse model | ProSettings |
| `keyboard` | string \| null | Keyboard model | ProSettings |
| `headset` | string \| null | Headset model | ProSettings |
| `mousepad` | string \| null | Mousepad model | ProSettings |

### Platform Identifiers

| Field | Type | Description |
|-------|------|-------------|
| `steam_id` | string \| null | Steam ID (STEAM_1:0:xxx format) |
| `steam_id64` | string \| null | Steam 64-bit ID |
| `faceit_profile` | string \| null | Faceit profile URL |
| `esea_profile` | string \| null | ESEA profile URL |

### Metadata

| Field | Type | Description |
|-------|------|-------------|
| `last_updated` | string | ISO 8601 timestamp |
| `sources` | string[] | Data sources: `liquipedia` / `prosettings` / `hltv_manual` / `esl` / `blast` |
| `notes` | string \| null | Free-form notes |

---

## Team JSON Schema

| Field | Type | Required | Description |
|-------|------|:---:|-------------|
| `id` | string | ✅ | Unique team ID, lowercase |
| `name` | string | ✅ | Full team name |
| `short_name` | string \| null | | Abbreviation |
| `country` | string | ✅ | Country code or `international` |
| `country_name` | string | ✅ | Country name in English |
| `region` | enum | ✅ | `EU` / `NA` / `SA` / `CIS` / `ASIA` / `OCE` / `MEA` |
| `organization` | string \| null | | Parent organization name |
| `logo_url` | string \| null | | Logo image URL |
| `founded` | string \| null | | Year founded |
| `disbanded` | string \| null | | Year disbanded (if applicable) |
| `status` | enum | ✅ | `active` / `inactive` / `disbanded` |
| `current_roster` | string[] | | Current player IDs |
| `coach` | string \| null | | Coach player ID |
| `analyst` | string \| null | | Analyst player ID |
| `achievements.major_titles` | int | | Major championships won |
| `achievements.major_appearances` | int | | Major appearances |
| `achievements.s_tier_titles` | int | | S-Tier tournament wins |
| `achievements.total_prize_money` | float \| null | | Total prize money (USD) |
| `achievements.hltv_ranking_best` | int \| null | | Best HLTV world ranking |
| `achievements.hltv_ranking_best_date` | string \| null | | Date of best ranking |
| `social_links.twitter` | string \| null | | Twitter/X URL |
| `social_links.website` | string \| null | | Official website |
| `social_links.instagram` | string \| null | | Instagram URL |
| `last_updated` | string | | ISO 8601 timestamp |
| `sources` | string[] | | Data sources |
| `notes` | string \| null | | Free-form notes |

---

## Index File (`data/index.json`)

Auto-generated by `scripts/build_index.sh`. Provides:

- **Forward index**: `players.<id>` → file path + summary
- **Reverse indexes**:
  - `by_country` — grouped by country code
  - `by_role` — grouped by role
  - `by_status` — grouped by player status
- **Stats**: `player_count`, `team_count`

## Enum Values

### Player Status
| Value | Description |
|-------|-------------|
| `active` | Currently competing |
| `inactive` | On break or benched |
| `retired` | No longer competing |
| `banned` | Suspended / banned |

### Player Roles
| Value | Description |
|-------|-------------|
| `AWPer` | Primary sniper |
| `IGL` | In-game leader |
| `Entry` | Entry fragger |
| `Support` | Support player |
| `Rifler` | Rifle specialist |
| `Lurker` | Lurker / flanker |
| `Coach` | Team coach |

### Team Membership Status
| Value | Description |
|-------|-------------|
| `starter` | Starting roster |
| `substitute` | Official substitute |
| `stand-in` | Temporary stand-in |
| `loan` | On loan from another team |

### Region
| Value | Description |
|-------|-------------|
| `EU` | Europe |
| `NA` | North America |
| `SA` | South America |
| `CIS` | CIS / Eastern Europe |
| `ASIA` | Asia-Pacific |
| `OCE` | Oceania |
| `MEA` | Middle East & Africa |

### Team Status
| Value | Description |
|-------|-------------|
| `active` | Active roster |
| `inactive` | No active roster |
| `disbanded` | Organization dissolved |

## Country Codes

Use [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) two-letter codes. For multinational teams, use `international`.

## Validation Pipeline

Run `bash scripts/validate.sh` to execute 4 layers of checks:

1. **Structure** — JSON parsability + Pydantic model validation
2. **Semantics** — Enum values, date formats, country code validity
3. **Cross-reference** — Team ID references between players and `_team.json` files
4. **Consistency** — File name matches `id`, folder matches `current_team.team_id`