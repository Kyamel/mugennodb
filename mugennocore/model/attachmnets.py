
from dataclasses import field
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic.dataclasses import dataclass


@dataclass(slots=True)
class Attachments:
    id: UUID
    target_type: str
    target_id: UUID
    file_name: str
    file_url: str
    type_id: int
    file_size: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"Attachments({self.file_name} for {self.target_type})"

    def __repr__(self) -> str:
        return f"Attachments(id={self.id}, target_type='{self.target_type}', target_id={self.target_id}, file_name='{self.file_name}')"
