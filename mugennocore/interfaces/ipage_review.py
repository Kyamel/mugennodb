from typing import Protocol, runtime_checkable
from datetime import datetime

@runtime_checkable
class IPageReview(Protocol):
   id: int
   review_id: int
   page_id: int
   created_at: datetime
   updated_at: datetime

   def __str__(self) -> str: ...
   def __repr__(self) -> str: ...