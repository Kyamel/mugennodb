from datetime import date, datetime
from typing import Optional, Protocol, runtime_checkable
from uuid import UUID


@runtime_checkable
class IManga(Protocol):
    id: int
    title_english: str
    title_native: str
    release_date: date
    finish_date: Optional[date]
    active_status: str
    comic_type: str
    cover: UUID
    mal_id: int
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
