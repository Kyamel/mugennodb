from dataclasses import field
from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(slots=True)
class Comments:
    id: UUID
    discussion_id: UUID
    user_id: UUID
    content: str
    reply_to: Optional[UUID] = None
    karma_score: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"Comments({preview})"

    def __repr__(self) -> str:
        return f"Comments(id={self.id}, discussion_id={self.discussion_id}, user_id={self.user_id}, karma_score={self.karma_score})"

