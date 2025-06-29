from datetime import datetime
from typing import Protocol, runtime_checkable
from uuid import UUID


@runtime_checkable
class IChapter(Protocol):
    id: int
    manga_id: int
    title: str
    cover: UUID
    ch_number: int
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
