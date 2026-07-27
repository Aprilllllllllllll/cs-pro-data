"""战队数据模型"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# 枚举定义
# ============================================================

class TeamStatus(str, Enum):
    """战队状态"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISBANDED = "disbanded"


class Region(str, Enum):
    """赛区"""
    EU = "EU"
    NA = "NA"
    SA = "SA"
    CIS = "CIS"
    ASIA = "ASIA"
    OCE = "OCE"
    MEA = "MEA"


# ============================================================
# 嵌套模型
# ============================================================

class TeamAchievements(BaseModel):
    """战队成就"""
    major_titles: int = 0
    major_appearances: int = 0
    s_tier_titles: int = 0
    total_prize_money: Optional[float] = None
    hltv_ranking_best: Optional[int] = None
    hltv_ranking_best_date: Optional[str] = None


class TeamSocialLinks(BaseModel):
    """战队社交链接"""
    twitter: Optional[str] = None
    website: Optional[str] = None
    instagram: Optional[str] = None


# ============================================================
# 主模型
# ============================================================

class Team(BaseModel):
    """CS 战队完整资料"""
    # 身份标识
    id: str
    name: str
    short_name: Optional[str] = None
    country: str  # ISO 3166-1 alpha-2 或 "international"
    country_name: str
    region: Region

    # 组织信息
    organization: Optional[str] = None
    logo_url: Optional[str] = None

    # 时间线
    founded: Optional[str] = None
    disbanded: Optional[str] = None
    status: TeamStatus

    # 阵容
    current_roster: list[str] = Field(default_factory=list)
    coach: Optional[str] = None
    analyst: Optional[str] = None

    # 成就
    achievements: TeamAchievements = Field(default_factory=TeamAchievements)

    # 社交链接
    social_links: TeamSocialLinks = Field(default_factory=TeamSocialLinks)

    # 元数据
    last_updated: datetime = Field(default_factory=datetime.now)
    sources: list[str] = Field(default_factory=list)
    notes: Optional[str] = None