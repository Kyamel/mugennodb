from datetime import datetime
from typing import Protocol, runtime_checkable

@runtime_checkable
class IRelatedManga(Protocol):

    id: int
    source_manga_id: int
    related_manga_id: int
    relationship_type: str
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...