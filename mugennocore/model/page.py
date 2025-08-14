from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(slots=True)
class Page:
    id: int
    chapter_id: int
    pg_number: int
    source: UUID
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str:
        return (
            f"Page {self.pg_number} (Chapter {self.chapter_id}) - Source: {self.source}"
        )

    def __repr__(self) -> str:
        return (
            f"Page(id={self.id}, chapter_id={self.chapter_id}, pg_number={self.pg_number}, "
            f"source={self.source}, created_at={self.created_at.isoformat()}, updated_at={self.updated_at.isoformat()})"
        )
