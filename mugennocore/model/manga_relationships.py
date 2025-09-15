from dataclasses import field
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic.dataclasses import dataclass


@dataclass(slots=True)
class MangaRelationships:
    id: UUID
    source_manga_id: UUID
    target_manga_id: UUID
    relationship_type_id: int
    user_id: UUID
    description: Optional[str] = None
    is_approved: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"MangaRelationships({self.source_manga_id} -> {self.target_manga_id})"

    def __repr__(self) -> str:
        return f"MangaRelationships(id={self.id}, source_manga_id={self.source_manga_id}, target_manga_id={self.target_manga_id}, type_id={self.relationship_type_id})"