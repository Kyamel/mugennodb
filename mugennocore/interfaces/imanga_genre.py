from datetime import datetime
from typing import Protocol, runtime_checkable

@runtime_checkable
class IMangaGenre(Protocol):

    id: int
    manga_id: int
    tag_id: int
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...