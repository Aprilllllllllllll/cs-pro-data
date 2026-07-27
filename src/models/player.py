"""选手数据模型 — 包含所有枚举和嵌套模型定义"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# 枚举定义
# ============================================================

class PlayerStatus(str, Enum):
    """选手状态"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    RETIRED = "retired"
    BANNED = "banned"


class PlayerRole(str, Enum):
    """游戏内角色"""
    AWPER = "AWPer"
    IGL = "IGL"
    ENTRY = "Entry"
    SUPPORT = "Support"
    RIFLER = "Rifler"
    LURKER = "Lurker"
    COACH = "Coach"


class TeamMembershipStatus(str, Enum):
    """在队身份"""
    STARTER = "starter"
    SUBSTITUTE = "substitute"
    STAND_IN = "stand-in"
    LOAN = "loan"


# ============================================================
# 嵌套模型
# ============================================================

class CurrentTeam(BaseModel):
    """当前战队信息"""
    team_id: str
    join_date: date
    contract_expiry: Optional[date] = None


class TeamHistoryEntry(BaseModel):
    """历史战队记录"""
    team_id: str
    start_date: date
    end_date: Optional[date] = None
    status: TeamMembershipStatus = TeamMembershipStatus.STARTER


class MajorTitle(BaseModel):
    """Major 冠军记录"""
    major_name: str
    date: date
    team_id: str
    placement: str = "1st"


class HLTVTop20Ranking(BaseModel):
    """HLTV Top 20 年度排名"""
    year: int
    rank: int = Field(ge=1, le=20)


class MVPMedal(BaseModel):
    """MVP 奖章"""
    tournament: str
    date: date
    tier: str  # S-Tier, A-Tier, B-Tier


class PlayerStatistics(BaseModel):
    """选手统计数据"""
    hltv_rating: Optional[float] = None
    total_maps: Optional[int] = None
    total_kills: Optional[int] = None
    headshot_percentage: Optional[float] = None
    kills_per_round: Optional[float] = None
    deaths_per_round: Optional[float] = None
    impact_rating: Optional[float] = None
    kast: Optional[float] = None
    adr: Optional[float] = None


class SocialLinks(BaseModel):
    """社交链接"""
    twitter: Optional[str] = None
    twitch: Optional[str] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None


class PlayerSettings(BaseModel):
    """游戏设置与外设"""
    crosshair_code: Optional[str] = None
    config_url: Optional[str] = None
    sensitivity: Optional[float] = None
    edpi: Optional[float] = None
    zoom_sensitivity: Optional[float] = None
    raw_input: Optional[bool] = None
    resolution: Optional[str] = None
    aspect_ratio: Optional[str] = None
    scaling_mode: Optional[str] = None
    monitor: Optional[str] = None
    mouse: Optional[str] = None
    keyboard: Optional[str] = None
    headset: Optional[str] = None
    mousepad: Optional[str] = None


# ============================================================
# 主模型
# ============================================================

class Player(BaseModel):
    """CS 职业选手完整资料"""
    # 身份标识
    id: str
    name: str
    native_name: Optional[str] = None
    country: str  # ISO 3166-1 alpha-2
    country_name: str

    # 个人信息
    birth_date: Optional[date] = None
    status: PlayerStatus
    roles: list[PlayerRole] = Field(default_factory=list)
    years_active: Optional[str] = None

    # 当前战队
    current_team: Optional[CurrentTeam] = None

    # 战队历史
    team_history: list[TeamHistoryEntry] = Field(default_factory=list)

    # 成就
    major_appearances: int = 0
    major_titles: list[MajorTitle] = Field(default_factory=list)
    hltv_top20_rankings: list[HLTVTop20Ranking] = Field(default_factory=list)
    mvp_medals: list[MVPMedal] = Field(default_factory=list)

    # 统计数据
    statistics: PlayerStatistics = Field(default_factory=PlayerStatistics)

    # 社交链接
    social_links: SocialLinks = Field(default_factory=SocialLinks)

    # 游戏设置与外设
    settings: PlayerSettings = Field(default_factory=PlayerSettings)

    # 平台标识
    steam_id: Optional[str] = None
    steam_id64: Optional[str] = None
    faceit_profile: Optional[str] = None
    esea_profile: Optional[str] = None

    # 元数据
    last_updated: datetime = Field(default_factory=datetime.now)
    sources: list[str] = Field(default_factory=list)
    notes: Optional[str] = None