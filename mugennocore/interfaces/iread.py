from typing import Protocol, runtime_checkable
from datetime import datetime


@runtime_checkable
class IRead(Protocol):
    user_id: int
    manga_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
