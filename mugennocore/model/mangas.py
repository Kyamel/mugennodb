
from dataclasses import field
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from uuid import UUID
from mugennocore.model.enums import EAgeRating, EComicType, EMangaStatus

@dataclass(slots=True, frozen=True)
class MangasRead:
    id: UUID
    country_id: int
    user_id: UUID
    title_english: str
    title_native: str
    release_date: date
    finish_date: Optional[date] = None
    age_rating: EAgeRating = EAgeRating.G
    status: EMangaStatus = EMangaStatus.ONGOING
    comic_type: str = EComicType.MANGA  # ou usar enum se você quiser criar
    mal_id: Optional[int] = None
    kitsu_id: Optional[int] = None
    cover_url: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None

@dataclass(slots=True, frozen=True)
class MangasCreate:
    country_id: int
    user_id: UUID
    title_english: str
    title_native: str
    release_date: date
    comic_type: EComicType  # 'MANGA', 'DOUJINSHI', etc.
    cover_url: str
    finish_date: Optional[date] = None
    age_rating: EAgeRating = EAgeRating.G
    status: EMangaStatus = EMangaStatus.ONGOING
    mal_id: Optional[int] = None
    kitsu_id: Optional[int] = None

@dataclass(slots=True, frozen=True)
class MangasUpdate:
    id: UUID
    country_id: Optional[int] = None
    title_english: Optional[str] = None
    title_native: Optional[str] = None
    release_date: Optional[date] = None
    finish_date: Optional[date] = None
    age_rating: Optional[EAgeRating] = None
    status: Optional[EMangaStatus] = None
    comic_type: Optional[EComicType] = None
    mal_id: Optional[int] = None
    kitsu_id: Optional[int] = None
    cover_url: Optional[str] = None
    updated_at: datetime = field(default_factory=datetime.now)
