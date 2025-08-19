from typing import Optional
from mugennocore.interfaces.ichapter_review import IChapterReview
from mugennodb.database.mapping.chapter_review_map import record_to_chapter_review
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennocore.model.chapter_review import ChapterReview

async def insert_chapter_review(db: DatabaseProtocol, chapter_review: IChapterReview) -> bool:
    """
    Insere relacionamento entre capítulo e review.
    """
    record = await db.fetchrow(
        """
        INSERT INTO chapter_reviews (review_id, chapter_id)
        VALUES ($1, $2)
        RETURNING *
        """,
        chapter_review.review_id, chapter_review.chapter_id
    )
    return record is not None

async def get_chapter_review(db: DatabaseProtocol, review_id: int, chapter_id: int) -> Optional[ChapterReview]:
    """
    Busca relacionamento pelo par (review_id, chapter_id).
    """
    record = await db.fetchrow(
        """
        SELECT * FROM chapter_reviews
        WHERE review_id = $1 AND chapter_id = $2
        """,
        review_id, chapter_id
    )
    return record_to_chapter_review(record)
