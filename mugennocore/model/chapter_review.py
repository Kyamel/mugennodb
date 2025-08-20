from dataclasses import dataclass


@dataclass(slots=True)
class ChapterReview:
    review_id: int
    chapter_id: int
