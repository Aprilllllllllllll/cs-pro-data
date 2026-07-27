"""索引构建器 — 扫描 data/players/ 目录，生成 data/index.json"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console

from src.models.index import Index, PlayerIndexEntry, TeamIndexEntry
from src.models.player import Player, PlayerStatus
from src.models.team import Team, TeamStatus

console = Console()

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data" / "players"
INDEX_PATH = ROOT / "data" / "index.json"


def _find_json_files() -> list[Path]:
    return sorted(DATA_DIR.rglob("*.json"))


def _load_player(path: Path) -> Player | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return Player.model_validate(data)
    except Exception:
        return None


def _load_team(path: Path) -> Team | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return Team.model_validate(data)
    except Exception:
        return None


def build_index() -> Index:
    """扫描所有数据文件，构建索引"""
    files = _find_json_files()
    index = Index(last_built=datetime.now(timezone.utc))

    players: dict[str, Player] = {}
    teams: dict[str, Team] = {}

    for f in files:
        rel = str(f.relative_to(ROOT))
        if f.name == "_team.json":
            team = _load_team(f)
            if team:
                teams[team.id] = team
        else:
            player = _load_player(f)
            if player:
                players[player.id] = player

    # 构建选手索引
    for pid, p in players.items():
        current_team = p.current_team.team_id if p.current_team else None
        entry = PlayerIndexEntry(
            name=p.name,
            country=p.country,
            status=p.status.value,
            current_team=current_team,
            roles=[r.value for r in p.roles],
            major_titles=len(p.major_titles),
            file_path=str(_find_player_file(pid, files).relative_to(ROOT)),
        )
        index.players[pid] = entry

    # 构建战队索引
    for tid, t in teams.items():
        entry = TeamIndexEntry(
            name=t.name,
            country=t.country,
            region=t.region.value,
            status=t.status.value,
            player_count=len(t.current_roster),
            file_path=str(_find_team_file(tid, files).relative_to(ROOT)),
        )
        index.teams[tid] = entry

    index.player_count = len(players)
    index.team_count = len(teams)

    # 构建反向索引: 按国家
    by_country: dict[str, list[str]] = {}
    for pid, p in players.items():
        c = p.country.upper()
        by_country.setdefault(c, []).append(pid)
    index.by_country = {k: sorted(v) for k, v in sorted(by_country.items())}

    # 按角色
    by_role: dict[str, list[str]] = {}
    for pid, p in players.items():
        for role in p.roles:
            by_role.setdefault(role.value, []).append(pid)
    index.by_role = {k: sorted(v) for k, v in sorted(by_role.items())}

    # 按状态
    by_status: dict[str, list[str]] = {}
    for pid, p in players.items():
        s = p.status.value
        by_status.setdefault(s, []).append(pid)
    index.by_status = {k: sorted(v) for k, v in sorted(by_status.items())}

    return index


def _find_player_file(pid: str, files: list[Path]) -> Path:
    for f in files:
        if f.name == f"{pid}.json":
            return f
    raise FileNotFoundError(f"找不到选手文件: {pid}.json")


def _find_team_file(tid: str, files: list[Path]) -> Path:
    for f in files:
        if f.name == "_team.json":
            data = json.loads(f.read_text(encoding="utf-8"))
            if data.get("id") == tid:
                return f
    raise FileNotFoundError(f"找不到战队文件: {tid}/_team.json")


def main() -> int:
    console.print("\n[bold cyan]━━━ 构建索引 ━━━[/]\n")

    try:
        index = build_index()
    except Exception as e:
        console.print(f"[red]构建失败: {e}[/]")
        return 1

    # 写入文件
    index_json = index.model_dump(mode="json")
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(
        json.dumps(index_json, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    console.print(f"[green]✅ 索引已生成: data/index.json[/]")
    console.print(f"   选手总数: {index.player_count}")
    console.print(f"   战队总数: {index.team_count}")
    console.print(f"   国家分布: {len(index.by_country)} 个国家/地区")
    console.print(f"   角色分布: {len(index.by_role)} 种角色")
    console.print(f"   更新时间: {index.last_built.isoformat()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())