from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Chapter:
    """Represents a Manga Chapter from the database."""

    id: int
    manga_id: int
    title: str
    cover: UUID
    ch_number: int
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str:
        return f"{self.ch_number} - {self.title}"

    def __repr__(self) -> str:
        return (
            f"Chapter(id={self.id}, manga_id={self.manga_id}, title={self.title!r}, "
            f"cover={self.cover}, ch_number={self.ch_number}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )
