from dataclasses import field
from typing import Optional
from pydantic.dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from mugennocore.model.enums import EUserRole


@dataclass(slots=True)
class Users:
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
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"Users({self.username})"

    def __repr__(self) -> str:
        return f"Users(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role.value}', karma_score={self.karma_score})"
