from dataclasses import field
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic.dataclasses import dataclass

from mugennocore.model.enums import EFlagStatus


@dataclass(slots=True)
class Flags:
    id: UUID
    target_type: str
    target_id: UUID
    user_id: UUID
    reason: str
    status: EFlagStatus = EFlagStatus.PENDING
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"Flags({self.status.value}: {self.reason[:30]}...)"

    def __repr__(self) -> str:
        return f"Flags(id={self.id}, target_type='{self.target_type}', target_id={self.target_id}, status='{self.status.value}', reason='{self.reason[:50]}...')"