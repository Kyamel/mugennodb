from mugennocore.interfaces.runtime_checkable import IUser
from mugennodb.database.mapping.manga_riview_map import record_to_mangaReview
from mugennodb.conection.database_protocol import DatabaseProtocol

async def insert_review(db: DatabaseProtocol, review: IMangaReview) -> int:
    record = await db.fetchrow(
        "INSERT INTO manga_reviews (review_id, manga_id) VALUES ($1, $2) RETURNING *",
        review.reviewId, review.mangaId
    )
    return record["id"] if record else -1

async def get_review_by_id(db: DatabaseProtocol, review_id: int) -> Optional[IMangaReview]:
    record = await db.fetchrow("SELECT * FROM manga_reviews WHERE id = $1", review_id)
    return record_to_mangaReview(record) if record else None