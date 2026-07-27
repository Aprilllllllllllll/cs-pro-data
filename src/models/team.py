"""战队数据模型 — 精简版"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TeamStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISBANDED = "disbanded"


class Region(str, Enum):
    EU = "EU"
    NA = "NA"
    SA = "SA"
    CIS = "CIS"
    ASIA = "ASIA"
    OCE = "OCE"
    MEA = "MEA"


class Team(BaseModel):
    id: str
    name: str
    short_name: Optional[str] = None
    country: str
    country_name: str
    region: Region
    founded: Optional[str] = None
    status: TeamStatus
    current_roster: list[str] = Field(default_factory=list)
    coach: Optional[str] = None
    major_titles: int = 0
    last_updated: datetime = Field(default_factory=datetime.now)
    sources: list[str] = Field(default_factory=list)
    notes: Optional[str] = None