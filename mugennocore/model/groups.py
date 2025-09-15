from pydantic.dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(slots=True)
class IGroup:
    id: UUID
    owner_id: UUID
    name: str
    description: Optional[str] = None
    is_open: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"Groups({self.name})"

    def __repr__(self) -> str:
        return f"Groups(id={self.id}, name='{self.name}', owner_id={self.owner_id}, is_open={self.is_open})"
