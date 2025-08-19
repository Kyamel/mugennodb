from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class MangaReview:
   id: int
   review_id: int
   manga_id: int
   created_at: datetime
   updated_at: datetime