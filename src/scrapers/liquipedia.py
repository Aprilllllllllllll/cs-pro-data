"""Liquipedia 爬虫 — 精简版，只爬取核心字段"""

from __future__ import annotations

import json
import re
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional

import httpx
from rich.console import Console

from src.models.player import (
    CurrentTeam,
    MajorTitle,
    Player,
    PlayerRole,
    PlayerStatus,
    TeamHistoryEntry,
    TeamMembershipStatus,
)

console = Console()

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data" / "players"

API_URL = "https://liquipedia.net/counterstrike/api.php"
USER_AGENT = "cs-pro-data/0.1"

# 国家名 → 代码
COUNTRY_MAP: dict[str, str] = {
    "ukraine": "UA", "france": "FR", "russia": "RU", "denmark": "DK",
    "sweden": "SE", "germany": "DE", "united states": "US", "brazil": "BR",
    "canada": "CA", "finland": "FI", "norway": "NO", "poland": "PL",
    "spain": "ES", "united kingdom": "GB", "australia": "AU", "china": "CN",
    "south korea": "KR", "kazakhstan": "KZ", "turkey": "TR", "israel": "IL",
    "netherlands": "NL", "belgium": "BE", "estonia": "EE", "latvia": "LV",
    "lithuania": "LT", "bulgaria": "BG", "romania": "RO", "serbia": "RS",
    "bosnia and herzegovina": "BA", "croatia": "HR", "slovenia": "SI",
    "slovakia": "SK", "czech republic": "CZ", "hungary": "HU", "austria": "AT",
    "switzerland": "CH", "portugal": "PT", "mongolia": "MN", "vietnam": "VN",
    "india": "IN", "indonesia": "ID", "jordan": "JO", "saudi arabia": "SA",
    "south africa": "ZA", "argentina": "AR", "chile": "CL", "mexico": "MX",
    "kosovo": "XK", "north macedonia": "MK", "belarus": "BY",
}


def _country_code(name: str) -> str:
    return COUNTRY_MAP.get(name.strip().lower(), name)


def _role_map(raw: str) -> list[PlayerRole]:
    mapping = {
        "awp": PlayerRole.AWPER, "awper": PlayerRole.AWPER,
        "rifle": PlayerRole.RIFLER, "rifler": PlayerRole.RIFLER,
        "igl": PlayerRole.IGL,
        "entry": PlayerRole.ENTRY,
        "support": PlayerRole.SUPPORT,
        "lurker": PlayerRole.LURKER,
        "coach": PlayerRole.COACH,
    }
    roles: list[PlayerRole] = []
    for part in raw.lower().replace("/", ",").split(","):
        r = mapping.get(part.strip())
        if r and r not in roles:
            roles.append(r)
    return roles


def _status_map(raw: str) -> PlayerStatus:
    s = raw.strip().lower()
    if s == "active":
        return PlayerStatus.ACTIVE
    if s in ("inactive", "benched"):
        return PlayerStatus.INACTIVE
    if s == "retired":
        return PlayerStatus.RETIRED
    if s == "banned":
        return PlayerStatus.BANNED
    return PlayerStatus.ACTIVE


def _team_membership_status(raw: str) -> TeamMembershipStatus:
    s = raw.strip().lower()
    if s == "inactive":
        return TeamMembershipStatus.SUBSTITUTE
    if s == "loan":
        return TeamMembershipStatus.LOAN
    if s in ("stand-in", "standin"):
        return TeamMembershipStatus.STAND_IN
    return TeamMembershipStatus.STARTER


def _team_id(name: str) -> str:
    name = name.strip().lower()
    mapping = {
        "natus vincere": "navi", "team liquid": "liquid", "team vitality": "vitality",
        "team spirit": "spirit", "team falcons": "falcons", "faze clan": "faze",
        "g2 esports": "g2", "mousesports": "mouz", "hellraisers": "hellraisers",
        "flipsid3 tactics": "flipsid3", "courage gaming": "courage",
        "bc.game esports": "bcgame", "astralis": "astralis",
        "team solomid": "tsm", "team dignitas": "dignitas",
        "copenhagen wolves": "copenhagenwolves",
    }
    return mapping.get(name, re.sub(r'[^a-z0-9]', '', name))


# ── 爬取 ──────────────────────────────────────────────────

def fetch_wikitext(player_id: str) -> Optional[str]:
    params = {
        "action": "parse", "page": player_id,
        "prop": "wikitext", "format": "json", "redirects": "1",
    }
    try:
        resp = httpx.get(API_URL, params=params, headers={
            "User-Agent": USER_AGENT, "Accept-Encoding": "gzip",
        }, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            return None
        return data["parse"]["wikitext"]["*"]
    except Exception:
        return None


def parse_infobox(text: str) -> dict:
    m = re.search(r'\{\{Infobox player\n(.*?)\}\}', text, re.DOTALL)
    if not m:
        return {}
    result = {}
    for line in m.group(1).split("\n"):
        kv = re.match(r'\|(\w+)=(.+)', line)
        if kv:
            result[kv.group(1).strip()] = kv.group(2).strip()
    return result


def parse_team_history(text: str) -> list[dict]:
    entries = []
    for m in re.finditer(r'\{\{TH\|([^}]+?)\}\}', text):
        parts = m.group(1).strip().split("|")
        if len(parts) < 2:
            continue
        date_range = parts[0].strip()
        team_name = parts[1].strip()
        status = parts[2].strip() if len(parts) > 2 else ""

        if "link=" in team_name.lower():
            continue

        # 分割日期范围
        dates = re.split(r'\s*[—–]\s*|\s+-\s+', date_range)
        if len(dates) < 2:
            continue
        start = dates[0].replace("??", "01")
        end = dates[1].replace("??", "01")
        if "Present" in end:
            end = ""

        if "????" in start or "????" in end:
            continue

        entries.append({
            "team_name": team_name,
            "start_date": start,
            "end_date": end,
            "status": status,
        })
    return entries


def scrape_player(player_id: str) -> Optional[Player]:
    console.print(f"  [cyan]Scraping {player_id}...[/]")

    text = fetch_wikitext(player_id)
    if not text:
        console.print(f"  [red]Failed to fetch {player_id}[/]")
        return None

    info = parse_infobox(text)
    if not info:
        console.print(f"  [red]No infobox found for {player_id}[/]")
        return None

    pid = info.get("id", player_id).lower()
    name = info.get("romanized_name", info.get("name", pid))
    country_raw = info.get("country", "")
    country = _country_code(country_raw)
    birth_raw = info.get("birth_date", "")
    birth = date.fromisoformat(birth_raw) if birth_raw and len(birth_raw) == 10 else None
    status = _status_map(info.get("status", "Active"))
    roles = _role_map(info.get("roles", ""))

    # 当前战队
    current_team_id = info.get("team", "").strip()
    current_team = None
    if current_team_id:
        current_team = CurrentTeam(team_id=_team_id(current_team_id), join_date=date.today())

    # 战队历史
    team_history: list[TeamHistoryEntry] = []
    for h in parse_team_history(text):
        try:
            sd = date.fromisoformat(h["start_date"])
            ed = date.fromisoformat(h["end_date"]) if h["end_date"] else None
            team_history.append(TeamHistoryEntry(
                team_id=_team_id(h["team_name"]),
                start_date=sd,
                end_date=ed,
                status=_team_membership_status(h["status"]),
            ))
        except ValueError:
            continue

    # HLTV Top 20
    hltv_rankings = []
    for m in re.finditer(
        r'ranked the (\d+)(?:st|nd|rd|th) best player of (\d{4}) by (?:\[\[)?HLTV(?:\]\])?',
        text, re.IGNORECASE,
    ):
        year = int(m.group(2))
        if year >= 2013:
            hltv_rankings.append({"year": year, "rank": int(m.group(1))})

    # 按年份去重
    seen = set()
    rankings = []
    for r in sorted(hltv_rankings, key=lambda x: x["year"], reverse=True):
        key = (r["year"], r["rank"])
        if key not in seen:
            seen.add(key)
            rankings.append(r)

    return Player(
        id=pid,
        name=name,
        country=country,
        country_name=country_raw,
        birth_date=birth,
        status=status,
        roles=roles,
        current_team=current_team if current_team_id else None,
        team_history=team_history,
        major_appearances=0,
        major_titles=[],
        last_updated=datetime.now(timezone.utc),
        sources=["liquipedia"],
        notes=f"HLTV Top 20: {len(rankings)} entries" if rankings else None,
    )


def save_player(player: Player) -> Path:
    if player.current_team:
        team_dir = player.current_team.team_id
    elif player.status == PlayerStatus.RETIRED:
        team_dir = "_retired"
    else:
        team_dir = "_free_agents"

    out_dir = DATA_DIR / team_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{player.id}.json"

    out_path.write_text(player.model_dump_json(indent=2, exclude_none=False), encoding="utf-8")
    return out_path


def main() -> int:
    args = sys.argv[1:]
    if not args:
        console.print("[red]Usage: python -m src.scrapers.liquipedia <player_id> [player_id ...][/]")
        return 1

    console.print(f"\n[bold cyan]Scraping {len(args)} players[/]\n")

    success = 0
    for pid in args:
        player = scrape_player(pid)
        if player:
            path = save_player(player)
            console.print(f"  [green]{pid} -> {path.relative_to(ROOT)}[/]")
            success += 1
        time.sleep(2)

    console.print(f"\n[bold]{success}/{len(args)} succeeded[/]")
    return 0 if success > 0 else 1


if __name__ == "__main__":
    sys.exit(main())