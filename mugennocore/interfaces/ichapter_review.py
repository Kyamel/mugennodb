from typing import Protocol, runtime_checkable


@runtime_checkable
class IChapterReview(Protocol):
    review_id: int
    chapter_id: int

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
