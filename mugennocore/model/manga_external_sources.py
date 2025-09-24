from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid
from mugennocore.model.enums import ESourceType


@dataclass(slots=True, frozen=True)
class MangaExternalSourcesCreate:
    manga_id: uuid.UUID
    user_id: uuid.UUID
    external_id: str
    source_type: ESourceType = ESourceType.INDEXER
    description: Optional[str] = None


@dataclass(slots=True, frozen=True)
class MangaExternalSourcesUpdate:
    id: uuid.UUID
    description: Optional[str] = None
    is_approved: Optional[bool] = None
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass(slots=True, frozen=True)
class MangaExternalSourcesRead:
    id: uuid.UUID
    manga_id: uuid.UUID
    user_id: uuid.UUID
    source_type: ESourceType
    external_id: str
    description: Optional[str]
    is_approved: bool
    created_at: datetime
    updated_at: datetime
