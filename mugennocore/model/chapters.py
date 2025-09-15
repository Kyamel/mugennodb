from pydantic.dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Chapters:
    id: UUID
    manga_id: UUID
    user_id: UUID
    country_id: int
    title: str
    cover_url: str
    ch_number: float
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"Chapters({self.title} - {self.ch_number})"

    def __repr__(self) -> str:
        return f"Chapters(id={self.id}, manga_id={self.manga_id}, title='{self.title}', ch_number={self.ch_number})"
