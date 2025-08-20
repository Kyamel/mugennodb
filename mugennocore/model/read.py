from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Read:
    user_id: int
    manga_id: int
    status: str
    created_at: datetime
    updated_at: datetime
