from dataclasses import field
from datetime import datetime
from typing import Optional
from uuid import UUID
from dataclasses import dataclass


@dataclass(slots=True)
class Notifications:
    id: UUID
    user_id: UUID
    target_type: str
    target_id: UUID
    type: str
    title: str
    content: Optional[str] = None
    is_read: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"Notifications({self.type}: {self.title})"

    def __repr__(self) -> str:
        return f"Notifications(id={self.id}, user_id={self.user_id}, type='{self.type}', title='{self.title}', is_read={self.is_read})"
