from dataclasses import field
from datetime import datetime
from uuid import UUID
from pydantic.dataclasses import dataclass


@dataclass(slots=True)
class MangaTags:
    manga_id: UUID
    user_id: UUID
    tag_id: UUID
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"MangaTags(manga={self.manga_id}, tag={self.tag_id})"

    def __repr__(self) -> str:
        return f"MangaTags(manga_id={self.manga_id}, user_id={self.user_id}, tag_id={self.tag_id}, created_at={self.created_at})"
