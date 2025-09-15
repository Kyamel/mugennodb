from dataclasses import field
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic.dataclasses import dataclass

from mugennocore.model.enums import EReadingStatus


@dataclass(slots=True)
class ReadingProgress:
    user_id: UUID
    chapter_id: UUID
    status: EReadingStatus = EReadingStatus.PLANNING
    score: Optional[int] = None
    review: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"ReadingProgress({self.status.value} - Score: {self.score or 'N/A'})"

    def __repr__(self) -> str:
        return f"ReadingProgress(user_id={self.user_id}, chapter_id={self.chapter_id}, status='{self.status.value}', score={self.score})"
