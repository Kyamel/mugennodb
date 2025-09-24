from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import Optional

@dataclass(slots=True, frozen=True)
class ChaptersRead:
    id: UUID
    manga_id: UUID
    user_id: UUID
    country_id: int
    title: str
    cover_url: str
    ch_number: str 
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass(slots=True, frozen=True)
class ChaptersCreate:
    manga_id: UUID
    user_id: UUID
    country_id: int
    title: str
    cover_url: str
    ch_number: str 

@dataclass(slots=True, frozen=True)
class ChaptersUpdate:
    id: UUID
    manga_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    country_id: Optional[int] = None
    title: Optional[str] = None
    cover_url: Optional[str] = None
    ch_number: Optional[str] = None  
    updated_at: datetime = field(default_factory=datetime.now)
