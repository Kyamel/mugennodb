from datetime import datetime
from typing import Protocol, runtime_checkable
from uuid import UUID

@runtime_checkable
class ICountry(Protocol):
    """Define a interface (contrato) para um objeto Country."""

    id: int
    lang: str
    locale_code: str
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...