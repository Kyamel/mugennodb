from dataclasses import field
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic.dataclasses import dataclass


@dataclass(slots=True)
class StaffProfiles:
    id: UUID
    user_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        name = self.name or (f"User#{self.user_id}" if self.user_id else "Anonymous")
        return f"StaffProfiles({name})"

    def __repr__(self) -> str:
        return f"StaffProfiles(id={self.id}, user_id={self.user_id}, name='{self.name}', description='{self.description}')"