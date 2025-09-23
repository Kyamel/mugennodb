from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass(slots=True, frozen=True)
class CountriesRead:
    id: int
    locale_code: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass(slots=True, frozen=True)
class CountriesCreate:
    locale_code: str

@dataclass(slots=True, frozen=True)
class CountriesUpdate:
    id: int
    locale_code: Optional[str] = None
    updated_at: datetime = field(default_factory=datetime.now)
