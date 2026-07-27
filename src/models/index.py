"""索引数据模型"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PlayerIndexEntry(BaseModel):
    """索引中的选手摘要条目"""
    name: str
    country: str
    status: str
    current_team: Optional[str] = None
    roles: list[str] = Field(default_factory=list)
    major_titles: int = 0
    file_path: str


class TeamIndexEntry(BaseModel):
    """索引中的战队摘要条目"""
    name: str
    country: str
    region: str
    status: str
    player_count: int = 0
    file_path: str


class Index(BaseModel):
    """全局索引 — 由 build_index 脚本自动生成，禁止手动编辑"""
    last_built: datetime = Field(default_factory=datetime.now)
    player_count: int = 0
    team_count: int = 0

    players: dict[str, PlayerIndexEntry] = Field(default_factory=dict)
    teams: dict[str, TeamIndexEntry] = Field(default_factory=dict)

    by_country: dict[str, list[str]] = Field(default_factory=dict)
    by_role: dict[str, list[str]] = Field(default_factory=dict)
    by_status: dict[str, list[str]] = Field(default_factory=dict)