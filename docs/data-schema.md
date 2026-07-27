# Data Schema Reference

## Player JSON (simplified)

| Field | Type | Required | Description |
|-------|------|:---:|-------------|
| `id` | string | ✅ | Unique player ID, lowercase alias, e.g. `s1mple` |
| `name` | string | ✅ | Real name, e.g. `Oleksandr Kostyliev` |
| `country` | string | ✅ | ISO 3166-1 alpha-2 code, e.g. `UA`, `FR` |
| `country_name` | string | ✅ | Country name, e.g. `Ukraine` |
| `birth_date` | string \| null | | Birth date `YYYY-MM-DD` |
| `status` | enum | ✅ | `active` / `inactive` / `retired` / `banned` |
| `roles` | enum[] | | `AWPer` / `IGL` / `Entry` / `Support` / `Rifler` / `Lurker` / `Coach` |
| `current_team` | object \| null | | `{team_id, join_date, contract_expiry?}` |
| `team_history` | array | | `[{team_id, start_date, end_date?, status?}]` |
| `major_appearances` | int | | Major tournament count |
| `major_titles` | array | | `[{major_name, date, team_id, placement}]` |
| `last_updated` | string | | ISO 8601 timestamp |
| `sources` | string[] | | Data sources: `liquipedia`, `hltv_manual`, etc. |
| `notes` | string \| null | | Free-form notes |

## Team JSON (simplified)

| Field | Type | Required | Description |
|-------|------|:---:|-------------|
| `id` | string | ✅ | Team ID, lowercase |
| `name` | string | ✅ | Full team name |
| `country` | string | ✅ | Country code or `international` |
| `region` | enum | ✅ | `EU` / `NA` / `SA` / `CIS` / `ASIA` / `OCE` / `MEA` |
| `status` | enum | ✅ | `active` / `inactive` / `disbanded` |
| `current_roster` | string[] | | Player IDs |
| `coach` | string \| null | | Coach ID |
| `major_titles` | int | | Major championships won |
| `last_updated` | string | | ISO 8601 timestamp |

## Commands

```bash
bash scripts/setup.sh                  # Initialize environment
bash scripts/validate.sh               # Validate all data
bash scripts/build_index.sh            # Rebuild index
bash scripts/scrape.sh s1mple zywoo   # Scrape from Liquipedia
```