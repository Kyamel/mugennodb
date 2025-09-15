from dataclasses import field
from datetime import datetime
from uuid import UUID
from pydantic.dataclasses import dataclass


@dataclass(slots=True)
class IGroupMember:
    group_id: UUID
    user_id: UUID
    is_moderator: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        role = "Moderator" if self.is_moderator else "Member"
        return f"GroupMember(user={self.user_id}, {role})"

    def __repr__(self) -> str:
        return f"IGroupMember(group_id={self.group_id}, user_id={self.user_id}, is_moderator={self.is_moderator}, created_at={self.created_at})"
