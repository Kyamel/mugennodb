from dataclasses import field
from datetime import datetime
from typing import Optional
from pydantic.dataclasses import dataclass


@dataclass(slots=True)
class MangaRelationshipTypes:
    id: int
    name: str
    description: Optional[str] = None
    is_recursive: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"MangaRelationshipTypes({self.name})"

    def __repr__(self) -> str:
        return f"MangaRelationshipTypes (id={self.id}, name='{self.name}', is_recursive={self.is_recursive})"
