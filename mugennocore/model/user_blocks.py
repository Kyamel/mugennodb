from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

@dataclass(slots=True, frozen=True)
class UserBlocksRead:
    blocker_id: UUID
    blocked_id: UUID
    created_at: datetime = field(default_factory=datetime.now)

@dataclass(slots=True, frozen=True)
class UserBlocksCreate:
    blocker_id: UUID
    blocked_id: UUID

# Não precisa de update, pois PKs não mudam.
