from dataclasses import field
from datetime import datetime
from uuid import UUID
from pydantic.dataclasses import dataclass


@dataclass(slots=True)
class UserFollows:
    follower_id: UUID
    following_id: UUID
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"UserFollows({self.follower_id} -> {self.following_id})"

    def __repr__(self) -> str:
        return f"UserFollows(follower_id={self.follower_id}, following_id={self.following_id}, created_at={self.created_at})"