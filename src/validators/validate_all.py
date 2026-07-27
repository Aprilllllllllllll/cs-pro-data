"""全量数据校验"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table

from src.models.player import Player

console = Console()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data" / "players"

VALID_COUNTRIES: set[str] = {
    "AF", "AL", "DZ", "AR", "AM", "AU", "AT", "AZ", "BH", "BD", "BY", "BE",
    "BO", "BA", "BR", "BG", "CA", "CL", "CN", "CO", "CR", "HR", "CU", "CY",
    "CZ", "DK", "DO", "EC", "EG", "SV", "EE", "ET", "FI", "FR", "GE", "DE",
    "GH", "GR", "GT", "HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IL",
    "IT", "JM", "JP", "JO", "KZ", "KE", "XK", "KW", "KG", "LV", "LB", "LT",
    "LU", "MK", "MY", "MT", "MX", "MD", "MN", "ME", "MA", "MM", "NP", "NL",
    "NZ", "NI", "NG", "NO", "PK", "PS", "PE", "PH", "PL", "PT", "QA", "RO",
    "RU", "SA", "RS", "SG", "SK", "SI", "ZA", "KR", "ES", "LK", "SE", "CH",
    "TW", "TH", "TR", "UA", "AE", "GB", "US", "UY", "UZ", "VE", "VN",
    "international",
}


class Issue:
    def __init__(self, level: str, file: str, message: str) -> None:
        self.level = level
        self.file = file
        self.message = message


issues: list[Issue] = []


def error(file: str, msg: str) -> None:
    issues.append(Issue("ERROR", file, msg))


def warning(file: str, msg: str) -> None:
    issues.append(Issue("WARNING", file, msg))


def main() -> int:
    console.print("\n[bold cyan]━━━ CS Pro Data Validation ━━━[/]\n")

    all_files = sorted(DATA_DIR.rglob("*.json"))
    if not all_files:
        console.print("[yellow]No JSON files found in data/players/[/]")
        return 0

    console.print(f"Found {len(all_files)} JSON files\n")

    # 解析 & 校验
    players: dict[str, Player] = {}
    for f in all_files:
        if f.name == "_team.json":
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            player = Player.model_validate(data)
            players[player.id] = player
        except Exception as e:
            error(str(f.relative_to(ROOT)), f"Invalid: {e}")

    console.print(f"Players: {len(players)} | Teams: {len([f for f in all_files if f.name == '_team.json'])}")

    # 交叉引用
    team_ids = set()
    for f in all_files:
        if f.name == "_team.json":
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                if "id" in data:
                    team_ids.add(data["id"])
            except Exception:
                pass

    for pid, p in players.items():
        if p.current_team and p.current_team.team_id not in team_ids:
            warning(f"player:{pid}", f"Team '{p.current_team.team_id}' not found in any _team.json")
        for h in p.team_history:
            if h.team_id not in team_ids:
                warning(f"player:{pid}", f"Historical team '{h.team_id}' not found")

    # 一致性
    for pid, p in players.items():
        for f in all_files:
            if f.name == f"{pid}.json":
                rel = str(f.relative_to(ROOT))
                if p.current_team:
                    parent_dir = f.parent.name
                    if parent_dir != p.current_team.team_id:
                        warning(rel, f"Folder '{parent_dir}' != current_team '{p.current_team.team_id}'")
                break

    # 输出
    if issues:
        table = Table(title="Validation Results")
        table.add_column("Level", style="bold", width=8)
        table.add_column("File", width=40)
        table.add_column("Message")
        for i in issues:
            color = {"ERROR": "red", "WARNING": "yellow"}[i.level]
            table.add_row(f"[{color}]{i.level}[/]", i.file, i.message)
        console.print(table)

    errs = sum(1 for i in issues if i.level == "ERROR")
    warns = sum(1 for i in issues if i.level == "WARNING")

    if errs == 0 and warns == 0:
        console.print("[bold green]All checks passed![/]")
    elif errs == 0:
        console.print(f"[bold yellow]{warns} warnings (no errors)[/]")
    else:
        console.print(f"[bold red]{errs} errors, {warns} warnings[/]")

    return 1 if errs > 0 else 0


if __name__ == "__main__":
    sys.exit(main())