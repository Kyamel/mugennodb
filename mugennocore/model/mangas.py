
from dataclasses import field
from pydantic.dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from uuid import UUID
from mugennocore.model.enums import EAgeRating, EMangaStatus


@dataclass(slots=True)
class Mangas:
    id: UUID
    country_id: int
    user_id: UUID
    title_english: str
    title_native: str
    release_date: date
    comic_type_id: int
    finish_date: Optional[date] = None
    age_rating: EAgeRating = EAgeRating.G
    status: EMangaStatus = EMangaStatus.ONGOING
    mal_id: Optional[int] = None
    kitsu_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
  
    def __str__(self) -> str:
        return f"Mangas({self.title_english})"

    def __repr__(self) -> str:
        return f"Mangas(id={self.id}, title_english='{self.title_english}', status='{self.status.value}', comic_type_id={self.comic_type_id})"