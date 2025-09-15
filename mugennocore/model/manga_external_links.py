from dataclasses import field
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic.dataclasses import dataclass

from mugennocore.model.enums import ELinkType


@dataclass(slots=True)
class MangaExternalLinks:
    id: UUID
    manga_id: UUID
    link_type: ELinkType
    url: str
    user_id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    is_approved: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"MangaExternalLinks({self.link_type.value}: {self.url})"

    def __repr__(self) -> str:
        return f"MangaExternalLinks(id={self.id}, manga_id={self.manga_id}, link_type='{self.link_type.value}', url='{self.url}', is_approved={self.is_approved})"
