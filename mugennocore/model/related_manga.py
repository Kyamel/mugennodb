from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class RelatedManga:
    """Representa a relação entre dois mangás."""

    id: int
    source_manga_id: int
    related_manga_id: int
    relationship_type: str
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str:
        return (
            f"Mangá {self.source_manga_id} -> {self.relationship_type.upper()} "
            f"-> Mangá {self.related_manga_id}"
        )

    def __repr__(self) -> str:
        return (
            f"RelatedManga(id={self.id}, source_manga_id={self.source_manga_id}, "
            f"related_manga_id={self.related_manga_id}, "
            f"relationship_type={self.relationship_type!r}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )