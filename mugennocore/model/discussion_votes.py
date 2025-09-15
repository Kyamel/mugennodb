from pydantic.dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class IDiscussionVote:
    discussion_id: UUID
    user_id: UUID
    vote: int
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"DiscussionVote({self.vote} on {self.discussion_id})"

    def __repr__(self) -> str:
        return f"IDiscussionVote(discussion_id={self.discussion_id}, user_id={self.user_id}, vote={self.vote}, created_at={self.created_at})"
