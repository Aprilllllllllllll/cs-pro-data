"""索引构建器 — 扫描 data/players/ 目录，生成 data/index.json"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console

from src.models.index import Index, PlayerIndexEntry, TeamIndexEntry
from src.models.player import Player
from src.models.team import Team

console = Console()

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data" / "players"
INDEX_PATH = ROOT / "data" / "index.json"


def main() -> int:
    console.print("\n[bold cyan]Building index[/]\n")

    files = sorted(DATA_DIR.rglob("*.json"))
    index = Index(last_built=datetime.now(timezone.utc))

    players: dict[str, Player] = {}
    teams: dict[str, Team] = {}

    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        if f.name == "_team.json":
            try:
                t = Team.model_validate(data)
                teams[t.id] = t
            except Exception:
                pass
        else:
            try:
                p = Player.model_validate(data)
                players[p.id] = p
            except Exception:
                pass

    for pid, p in players.items():
        index.players[pid] = PlayerIndexEntry(
            name=p.name,
            country=p.country,
            status=p.status.value,
            current_team=p.current_team.team_id if p.current_team else None,
            roles=[r.value for r in p.roles],
            major_titles=len(p.major_titles),
            file_path=str(next(f for f in files if f.name == f"{pid}.json").relative_to(ROOT)),
        )

    for tid, t in teams.items():
        index.teams[tid] = TeamIndexEntry(
            name=t.name,
            country=t.country,
            region=t.region.value,
            status=t.status.value,
            player_count=len(t.current_roster),
            file_path=str(next(f for f in files if f.name == "_team.json" and tid in f.read_text(encoding="utf-8")).relative_to(ROOT)),
        )

    index.player_count = len(players)
    index.team_count = len(teams)

    # 反向索引
    by_country: dict[str, list[str]] = {}
    by_role: dict[str, list[str]] = {}
    by_status: dict[str, list[str]] = {}
    for pid, p in players.items():
        c = p.country.upper()
        by_country.setdefault(c, []).append(pid)
        for r in p.roles:
            by_role.setdefault(r.value, []).append(pid)
        by_status.setdefault(p.status.value, []).append(pid)
    index.by_country = {k: sorted(v) for k, v in sorted(by_country.items())}
    index.by_role = {k: sorted(v) for k, v in sorted(by_role.items())}
    index.by_status = {k: sorted(v) for k, v in sorted(by_status.items())}

    INDEX_PATH.write_text(
        json.dumps(index.model_dump(mode="json"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    console.print(f"[green]Index written to data/index.json[/]")
    console.print(f"  Players: {index.player_count}")
    console.print(f"  Teams: {index.team_count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())