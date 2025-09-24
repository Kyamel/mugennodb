from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

@dataclass(slots=True, frozen=True)
class UserFollowsRead:
    follower_id: UUID
    following_id: UUID
    created_at: datetime = field(default_factory=datetime.now)

@dataclass(slots=True, frozen=True)
class UserFollowsCreate:
    follower_id: UUID
    following_id: UUID

# Como o PK é composto, normalmente não atualizamos o follow, então não precisa de update.
