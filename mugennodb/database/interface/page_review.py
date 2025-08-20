from typing import Optional
from mugennodb.database.mapping.manga_review_map import record_to_mangaReview
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennocore.interfaces.ipage_review import IPageReview


async def insert_page_review(db: DatabaseProtocol, review: IPageReview) -> int:
    record = await db.fetchrow(
        "INSERT INTO page_reviews (review_id, page_id) VALUES ($1, $2) RETURNING *",
        review.review_id,
        review.page_id,
    )
    return record["id"] if record else -1


async def get_review_by_id(db: DatabaseProtocol, id: int) -> Optional[IPageReview]:
    record = await db.fetchrow("SELECT * FROM page_reviews WHERE id = $1", id)
    return record_to_pageReview(record) if record else None
