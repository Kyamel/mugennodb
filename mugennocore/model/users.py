from dataclasses import field
from typing import Optional
from pydantic.dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from mugennocore.model.enums import EUserRole


@dataclass(slots=True, frozen=True)
class UsersRead:
    id: UUID
    country_id: int
    username: str
    email: str
    password_hash: str
    role: EUserRole
    nickname: Optional[str] = None
    profile_bio: Optional[str] = None
    profile_banner: Optional[str] = None
    karma_score: int = 0
    is_active: bool = True
    is_banned: bool = False
    allow_nsfw: bool = False
    settings: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass(slots=True, frozen=True)
class UsersCreate:
    country_id: int
    username: str
    email: str
    password_hash: str
    role: EUserRole = EUserRole.USER
    nickname: Optional[str] = None
    profile_bio: Optional[str] = None
    profile_banner: Optional[str] = None
    allow_nsfw: bool = False
    settings: dict = field(default_factory=dict)

@dataclass(slots=True, frozen=True)
class UsersUpdate:
    id: UUID
    country_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[EUserRole] = None
    nickname: Optional[str] = None
    profile_bio: Optional[str] = None
    profile_banner: Optional[str] = None
    karma_score: Optional[int] = None
    is_active: Optional[bool] = None
    is_banned: Optional[bool] = None
    allow_nsfw: Optional[bool] = None
    settings: Optional[dict] = None
    updated_at: datetime = field(default_factory=datetime.now)
