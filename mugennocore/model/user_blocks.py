from pydantic.dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class UserBlocks:
    blocker_id: UUID
    blocked_id: UUID
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"UserBlocks({self.blocker_id} blocked {self.blocked_id})"

    def __repr__(self) -> str:
        return f"UserBlocks(blocker_id={self.blocker_id}, blocked_id={self.blocked_id}, created_at={self.created_at})"