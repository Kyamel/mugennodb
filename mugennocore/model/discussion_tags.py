from dataclasses import field
from datetime import datetime
from uuid import UUID
from pydantic.dataclasses import dataclass


@dataclass(slots=True)
class DiscussionTags:
    discussion_id: UUID
    user_id: UUID
    tag_id: UUID
    created_at: datetime = field(default_factory=datetime.now)


    def __str__(self) -> str:
        return f"DiscussionTags(discussion={self.discussion_id}, tag={self.tag_id})"

    def __repr__(self) -> str:
        return f"DiscussionTags(discussion_id={self.discussion_id}, user_id={self.user_id}, tag_id={self.tag_id}, created_at={self.created_at})"
