
from dataclasses import field
from pydantic.dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from uuid import UUID
from mugennocore.model.enums import EAgeRating, EMangaStatus
from pydantic_partial import create_partial_model
from pydantic import dataclasses as pdc


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
    

# 1. Para criação (não exige id nem timestamps)
MangasCreate = pdc.dataclass(
    create_partial_model(
        Mangas,
        exclude=("id", "created_at", "updated_at")
    )
)

# 2. Para update parcial (todos opcionais)
MangasUpdate = pdc.dataclass(create_partial_model(Mangas))

# 3. Para leitura (somente saída, imutável)
MangasRead = pdc.dataclass(Mangas, frozen=True)
