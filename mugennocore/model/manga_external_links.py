from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from mugennocore.model.enums import ELinkType

@dataclass(slots=True, frozen=True)
class MangaExternalLinksRead:
    id: UUID
    manga_id: UUID
    url: str
    user_id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    is_approved: bool = False
    link_type: ELinkType = ELinkType.COMMUNITY  # 'PURCHASE', 'OFFICIAL', 'COMMUNITY', 'INFORMATION'
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass(slots=True, frozen=True)
class MangaExternalLinksCreate:
    manga_id: UUID
    link_type: ELinkType
    url: str
    user_id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    is_approved: bool = False

@dataclass(slots=True, frozen=True)
class MangaExternalLinksUpdate:
    id: UUID
    manga_id: Optional[UUID] = None
    link_type: Optional[ELinkType] = None
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[UUID] = None
    is_approved: Optional[bool] = None
    updated_at: datetime = field(default_factory=datetime.now)
