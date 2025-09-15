from pydantic.dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(slots=True)
class IDiscussion:
    id: UUID
    user_id: UUID
    country_id: int
    title: str
    content: str
    manga_id: Optional[UUID] = None
    chapter_id: Optional[UUID] = None
    group_id: Optional[UUID] = None
    is_read_only: bool = False
    is_mod_only: bool = False
    is_deleted: bool = False
    karma_score: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"Discussion({self.title})"

    def __repr__(self) -> str:
        return f"IDiscussion(id={self.id}, title='{self.title}', user_id={self.user_id}, karma_score={self.karma_score})"

