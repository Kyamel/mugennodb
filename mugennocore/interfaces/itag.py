from datetime import datetime
from typing import Protocol, runtime_checkable
from uuid import UUID

@runtime_checkable
class ITag(Protocol):

    id: int
    name: str
    type: str
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...