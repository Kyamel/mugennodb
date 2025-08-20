from typing import Optional
from mugennodb.database.mapping.manga_review_map import record_to_mangaReview
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennocore.interfaces.imanga_review import IMangaReview

async def insert_manga_review(db: DatabaseProtocol, review: IMangaReview) -> int:
    record = await db.fetchrow(
        "INSERT INTO manga_reviews (review_id, manga_id) VALUES ($1, $2) RETURNING *",
        review.review_id, review.manga_id
    )
    return record["id"] if record else -1

async def get_review_by_id(db: DatabaseProtocol, id: int) -> Optional[IMangaReview]:
    record = await db.fetchrow("SELECT * FROM manga_reviews WHERE id = $1", id)
    return record_to_mangaReview(record) if record else None