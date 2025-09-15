from dataclasses import field
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic.dataclasses import dataclass

from mugennocore.model.enums import EReadingStatus


@dataclass(slots=True)
class Reviews:
    user_id: UUID
    manga_id: UUID
    status: EReadingStatus = EReadingStatus.PLANNING
    score: Optional[int] = None
    review: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"Reviews({self.status.value} - Score: {self.score or 'N/A'})"

    def __repr__(self) -> str:
        return f"Reviews(user_id={self.user_id}, manga_id={self.manga_id}, status='{self.status.value}', score={self.score})"
