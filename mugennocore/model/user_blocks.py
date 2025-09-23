from pydantic.dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class UserBlocks:
    blocker_id: UUID
    blocked_id: UUID
    created_at: datetime = field(default_factory=datetime.now)