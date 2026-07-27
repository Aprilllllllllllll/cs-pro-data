"""全量数据校验编排器

四层校验：
  1. 结构验证 — JSON 可解析 + Pydantic 模型校验
  2. 语义验证 — 枚举值、日期格式、国家代码合法性
  3. 交叉引用 — 选手与战队之间的 team_id / roster 引用完整性
  4. 一致性验证 — 文件名与 id 匹配、文件夹与 current_team 匹配
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

# 修复 Windows 终端中文编码问题
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from rich.console import Console
from rich.table import Table

from src.models.player import Player, PlayerStatus
from src.models.team import Team, TeamStatus

console = Console()

# 项目根目录
ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data" / "players"

# ISO 3166-1 alpha-2 国家代码白名单
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


# ============================================================
# 日志收集
# ============================================================

class Issue:
    """一条校验问题"""

    def __init__(self, level: str, file: str, message: str) -> None:
        self.level = level  # ERROR | WARNING | INFO
        self.file = file
        self.message = message


issues: list[Issue] = []


def error(file: str, msg: str) -> None:
    issues.append(Issue("ERROR", file, msg))


def warning(file: str, msg: str) -> None:
    issues.append(Issue("WARNING", file, msg))


def info(file: str, msg: str) -> None:
    issues.append(Issue("INFO", file, msg))


# ============================================================
# 辅助函数
# ============================================================

def _find_json_files(base: Path) -> list[Path]:
    """递归收集所有 .json 文件"""
    return sorted(base.rglob("*.json"))


def _load_json(path: Path) -> Optional[dict]:
    """加载 JSON 文件，失败返回 None"""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        error(str(path), f"JSON 解析失败: {e}")
        return None


def _validate_player(data: dict, path: Path) -> Optional[Player]:
    """Pydantic 模型校验"""
    try:
        return Player.model_validate(data)
    except Exception as e:
        error(str(path), f"模型校验失败: {e}")
        return None


def _validate_team(data: dict, path: Path) -> Optional[Team]:
    """Pydantic 模型校验"""
    try:
        return Team.model_validate(data)
    except Exception as e:
        error(str(path), f"模型校验失败: {e}")
        return None


# ============================================================
# 第 1 层：结构验证
# ============================================================

def validate_structure(files: list[Path]) -> tuple[dict[str, Player], dict[str, Team]]:
    """解析 JSON 并校验 Pydantic 模型"""
    players: dict[str, Player] = {}
    teams: dict[str, Team] = {}

    for f in files:
        rel = str(f.relative_to(ROOT))
        data = _load_json(f)
        if data is None:
            continue

        if f.name == "_team.json":
            team = _validate_team(data, f)
            if team:
                teams[team.id] = team
        else:
            player = _validate_player(data, f)
            if player:
                if player.id in players:
                    error(rel, f"选手 ID 重复: {player.id}")
                players[player.id] = player

    return players, teams


# ============================================================
# 第 2 层：语义验证
# ============================================================

def validate_semantics(players: dict[str, Player], teams: dict[str, Team]) -> None:
    """校验枚举值、日期格式、国家代码等"""
    for pid, p in players.items():
        # 国家代码
        if p.country.upper() not in VALID_COUNTRIES:
            warning(f"player:{pid}", f"国家代码 '{p.country}' 不在 ISO 3166-1 列表中")

        # 日期合理性
        if p.birth_date and p.birth_date.year < 1970:
            warning(f"player:{pid}", f"出生年份 {p.birth_date.year} 异常")
        if p.birth_date and p.birth_date.year > 2015:
            warning(f"player:{pid}", f"出生年份 {p.birth_date.year} 异常（选手年龄太小）")

    for tid, t in teams.items():
        if t.country.upper() not in VALID_COUNTRIES:
            warning(f"team:{tid}", f"国家代码 '{t.country}' 不在 ISO 3166-1 列表中")


# ============================================================
# 第 3 层：交叉引用
# ============================================================

def validate_cross_references(
    players: dict[str, Player],
    teams: dict[str, Team],
    files: list[Path],
) -> None:
    """校验选手与战队之间的引用完整性"""
    all_team_ids = set(teams.keys())
    # 也收集所有在 _team.json 中出现的 team_id
    for f in files:
        if f.name == "_team.json":
            data = _load_json(f)
            if data and "id" in data:
                all_team_ids.add(data["id"])

    for pid, p in players.items():
        # 当前战队引用
        if p.current_team and p.current_team.team_id not in all_team_ids:
            error(
                f"player:{pid}",
                f"current_team.team_id '{p.current_team.team_id}' 不存在于任何 _team.json",
            )
        # 历史战队引用
        for h in p.team_history:
            if h.team_id not in all_team_ids:
                warning(
                    f"player:{pid}",
                    f"team_history 中的 team_id '{h.team_id}' 不存在于任何 _team.json",
                )
        # Major 冠军中的战队引用
        for m in p.major_titles:
            if m.team_id not in all_team_ids:
                warning(
                    f"player:{pid}",
                    f"major_titles 中的 team_id '{m.team_id}' 不存在于任何 _team.json",
                )

    # 检查 _team.json 的 roster 中引用的选手是否存在
    all_player_ids = set(players.keys())
    for tid, t in teams.items():
        for pid in t.current_roster:
            if pid not in all_player_ids:
                warning(
                    f"team:{tid}",
                    f"current_roster 中的选手 '{pid}' 不存在于 data/players/",
                )
        if t.coach and t.coach not in all_player_ids:
            warning(
                f"team:{tid}",
                f"coach '{t.coach}' 不存在于 data/players/",
            )


# ============================================================
# 第 4 层：一致性
# ============================================================

def validate_consistency(players: dict[str, Player], files: list[Path]) -> None:
    """校验文件名与 id 一致、文件夹与 current_team 一致"""
    # 构建 id -> file_path 的映射
    id_to_path: dict[str, Path] = {}
    for f in files:
        if f.name == "_team.json":
            continue
        data = _load_json(f)
        if data and "id" in data:
            pid = data["id"]
            if pid in id_to_path:
                warning(
                    str(f.relative_to(ROOT)),
                    f"选手 ID '{pid}' 也存在于 {id_to_path[pid].relative_to(ROOT)}",
                )
            id_to_path[pid] = f

    for pid, p in players.items():
        file_path = id_to_path.get(pid)
        if not file_path:
            continue
        rel = str(file_path.relative_to(ROOT))

        # 文件名应与 id 一致
        expected_name = f"{pid}.json"
        if file_path.name != expected_name:
            error(rel, f"文件名应为 '{expected_name}'，实际为 '{file_path.name}'")

        # 文件夹应与 current_team 一致
        if p.current_team:
            parent_dir = file_path.parent.name
            if parent_dir != p.current_team.team_id:
                error(
                    rel,
                    f"文件所在文件夹 '{parent_dir}' 与 current_team.team_id "
                    f"'{p.current_team.team_id}' 不一致",
                )
        elif p.status == PlayerStatus.RETIRED:
            parent_dir = file_path.parent.name
            if parent_dir != "_retired":
                warning(rel, f"退役选手应放在 _retired/ 目录，当前在 '{parent_dir}/'")
        elif p.status in (PlayerStatus.INACTIVE, PlayerStatus.BANNED):
            parent_dir = file_path.parent.name
            if parent_dir not in ("_retired", "_free_agents"):
                info(rel, f"非现役选手放在 '{parent_dir}/'，建议移至 _free_agents/ 或 _retired/")


# ============================================================
# 主流程
# ============================================================

def main() -> int:
    console.print("\n[bold cyan]━━━ CS 职业选手资料库 数据校验 ━━━[/]\n")

    # 收集文件
    all_files = _find_json_files(DATA_DIR)
    if not all_files:
        console.print("[yellow]⚠ data/players/ 目录下没有找到 JSON 文件[/]")
        return 0

    console.print(f"找到 {len(all_files)} 个 JSON 文件\n")

    # 第 1 层：结构验证
    console.print("[bold]第 1 层：结构验证[/]")
    players, teams = validate_structure(all_files)
    console.print(f"  选手: {len(players)} | 战队: {len(teams)}")

    if not players and not teams:
        console.print("[yellow]  没有成功解析的数据文件，跳过后续校验[/]\n")
        _print_summary()
        return 0 if not _has_errors() else 1

    # 第 2 层：语义验证
    console.print("[bold]第 2 层：语义验证[/]")
    validate_semantics(players, teams)

    # 第 3 层：交叉引用
    console.print("[bold]第 3 层：交叉引用[/]")
    validate_cross_references(players, teams, all_files)

    # 第 4 层：一致性
    console.print("[bold]第 4 层：一致性[/]")
    validate_consistency(players, all_files)

    # 输出报告
    console.print()
    _print_summary()

    return 0 if not _has_errors() else 1


def _has_errors() -> bool:
    return any(i.level == "ERROR" for i in issues)


def _print_summary() -> None:
    """打印彩色汇总表格"""
    error_count = sum(1 for i in issues if i.level == "ERROR")
    warn_count = sum(1 for i in issues if i.level == "WARNING")
    info_count = sum(1 for i in issues if i.level == "INFO")

    if issues:
        table = Table(title="校验结果")
        table.add_column("级别", style="bold", width=8)
        table.add_column("文件", width=40)
        table.add_column("描述")

        for i in issues:
            color = {"ERROR": "red", "WARNING": "yellow", "INFO": "dim"}[i.level]
            table.add_row(f"[{color}]{i.level}[/]", i.file, i.message)

        console.print(table)

    total = len(issues)
    if total == 0:
        console.print("[bold green]✅ 全部校验通过！[/]")
    else:
        console.print(
            f"\n[bold]总计:[/] "
            f"[red]{error_count} 错误[/] | "
            f"[yellow]{warn_count} 警告[/] | "
            f"[dim]{info_count} 提示[/]"
        )
        if error_count > 0:
            console.print("[bold red]❌ 存在错误，请修复后重新校验[/]")
        else:
            console.print("[bold yellow]⚠ 没有错误，但存在警告[/]")


if __name__ == "__main__":
    sys.exit(main())