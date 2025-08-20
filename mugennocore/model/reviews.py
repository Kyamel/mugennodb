from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Review:
    """Represents a review written by a user."""

    review_id: int  # Primary Key
    users_id: int  # Foreign Key
    score: float
    content: str
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str:
        return f"Review {self.review_id} by User {self.users_id} - Score: {self.score}"

    def __repr__(self) -> str:
        return (
            f"Review(review_id={self.review_id}, user_id={self.users_id}, "
            f"score={self.score}, content={self.content!r}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )
