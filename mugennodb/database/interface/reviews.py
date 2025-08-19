from typing import Optional
from mugennocore.interfaces.ireview import IReview
from mugennodb.database.mapping.review_map import record_to_review
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennocore.model.reviews import Review


async def insert_review(db: DatabaseProtocol, review: IReview) -> int:
    record = await db.fetchrow(
        """
        INSERT INTO review (users_id, score, content, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING review_id
        """,
        review.users_id,
        review.score,
        review.content,
        review.created_at,
        review.updated_at
    )
    return record["review_id"] if record else -1


async def get_review_by_id(db: DatabaseProtocol, review_id: int) -> Optional[Review]:
    record = await db.fetchrow(
        "SELECT * FROM review WHERE review_id = $1",
        review_id
    )
    return record_to_review(record)


async def list_reviews(db: DatabaseProtocol) -> list[Review]:
    records = await db.fetch("SELECT * FROM review")
    return [record_to_review(r) for r in records if r is not None]
