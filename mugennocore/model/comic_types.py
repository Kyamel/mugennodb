
from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class ComicTypes:
    id: int
    name: str
    description: Optional[str] = None

    def __str__(self) -> str:
        return f"ComicTypes({self.name})"

    def __repr__(self) -> str:
        return f"ComicTypes(id={self.id}, name='{self.name}', description='{self.description}')"