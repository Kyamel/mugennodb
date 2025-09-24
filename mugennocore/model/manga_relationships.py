from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from mugennocore.model.enums import EMangaRelationshipType

@dataclass(slots=True, frozen=True)
class MangaRelationshipsRead:
    id: UUID
    source_manga_id: UUID
    target_manga_id: UUID
    user_id: UUID
    relationship_type: EMangaRelationshipType  # 'SEQUEL','PREQUEL','SPINOFF','PARODY','FANMADE'
    description: Optional[str] = None
    is_approved: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass(slots=True, frozen=True)
class MangaRelationshipsCreate:
    source_manga_id: UUID
    target_manga_id: UUID
    user_id: UUID
    relationship_type: EMangaRelationshipType  
    description: Optional[str] = None
    is_approved: bool = False

@dataclass(slots=True, frozen=True)
class MangaRelationshipsUpdate:
    id: UUID
    source_manga_id: Optional[UUID] = None
    target_manga_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    relationship_type: Optional[EMangaRelationshipType] = None
    description: Optional[str] = None
    is_approved: Optional[bool] = None
    updated_at: datetime = field(default_factory=datetime.now)
