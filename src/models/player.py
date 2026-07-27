"""选手数据模型 — 精简版，只保留核心字段"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PlayerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    RETIRED = "retired"
    BANNED = "banned"


class PlayerRole(str, Enum):
    AWPER = "AWPer"
    IGL = "IGL"
    ENTRY = "Entry"
    SUPPORT = "Support"
    RIFLER = "Rifler"
    LURKER = "Lurker"
    COACH = "Coach"


class TeamMembershipStatus(str, Enum):
    STARTER = "starter"
    SUBSTITUTE = "substitute"
    STAND_IN = "stand-in"
    LOAN = "loan"


class CurrentTeam(BaseModel):
    team_id: str
    join_date: date
    contract_expiry: Optional[date] = None


class TeamHistoryEntry(BaseModel):
    team_id: str
    start_date: date
    end_date: Optional[date] = None
    status: TeamMembershipStatus = TeamMembershipStatus.STARTER


class MajorTitle(BaseModel):
    major_name: str
    date: date
    team_id: str
    placement: str = "1st"


class Player(BaseModel):
    """CS 职业选手核心资料"""
    id: str
    name: str
    country: str
    country_name: str
    birth_date: Optional[date] = None
    status: PlayerStatus
    roles: list[PlayerRole] = Field(default_factory=list)
    current_team: Optional[CurrentTeam] = None
    team_history: list[TeamHistoryEntry] = Field(default_factory=list)
    major_appearances: int = 0
    major_titles: list[MajorTitle] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.now)
    sources: list[str] = Field(default_factory=list)
    notes: Optional[str] = None