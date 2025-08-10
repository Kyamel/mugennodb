from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class Tag:
    """Represents a Tag from the database."""

    id: int
    name: str
    type: str
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str:
        return f"{self.name} ({self.type})"

    def __repr__(self) -> str:
        return (
            f"Tag(id={self.id}, name={self.name!r}, type={self.type!r}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )