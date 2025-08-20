from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class MangaGenre:

    id: int
    manga_id: int
    tag_id: int
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str:
        return f"Mangá ID {self.manga_id} <-> Gênero (Tag ID {self.tag_id})"

    def __repr__(self) -> str:
        return (
            f"MangaGenre(id={self.id}, manga_id={self.manga_id}, tag_id={self.tag_id}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )
