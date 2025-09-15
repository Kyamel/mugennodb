from dataclasses import field
from datetime import datetime
from uuid import UUID
from pydantic.dataclasses import dataclass


@dataclass(slots=True)
class MangaStaff:
    id: UUID
    manga_id: UUID
    staff_profile_id: UUID
    staff_role_id: int
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"MangaStaff(manga={self.manga_id}, staff={self.staff_profile_id})"

    def __repr__(self) -> str:
        return f"MangaStaff(id={self.id}, manga_id={self.manga_id}, staff_profile_id={self.staff_profile_id}, staff_role_id={self.staff_role_id})"
