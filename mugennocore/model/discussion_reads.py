from dataclasses import field
from pydantic.dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class DiscussionReads:
    discussion_id: UUID
    user_id: UUID
    last_read_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"DiscussionReads(discussion={self.discussion_id}, user={self.user_id})"

    def __repr__(self) -> str:
        return f"DiscussionReads(discussion_id={self.discussion_id}, user_id={self.user_id}, last_read_at={self.last_read_at})"