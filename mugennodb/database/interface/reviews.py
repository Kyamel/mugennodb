from typing import Optional
from mugennocore.interfaces.ireview import IReview
from mugennodb.database.mapping.review_map import record_to_review
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennocore.model.reviews import Review


async def insert_manga_review(
    db: DatabaseProtocol, review: IReview, manga_id: int
) -> int:
    async with db.transaction() as conn:
        # 1Inserir review
        record = await conn.fetchrow(
            """
            INSERT INTO review (users_id, score, content, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING review_id
            """,
            review.users_id,
            review.score,
            review.content,
            review.created_at,
            review.updated_at,
        )
        if not record:
            return -1

        review_id = record["review_id"]

        # Relacionar review com o mangá
        await conn.execute(
            """
            INSERT INTO manga_reviews (review_id, manga_id)
            VALUES ($1, $2)
            """,
            review_id,
            manga_id,
        )

    # Se chegou aqui, a transação foi commitada
    return review_id


async def list_manga_reviews(db: DatabaseProtocol, manga_id: int) -> list[Review]:
    try:
        # Primeiro verifica se o mangá existe
        manga_check = await db.fetchval("SELECT id FROM mangas WHERE id = $1", manga_id)
        if not manga_check:
            print(f"Error: Manga with ID {manga_id} does not exist")
            return []

        # Busca as reviews associadas a esse mangá
        query = """
        SELECT r.*
        FROM review r
        JOIN manga_reviews mr ON mr.review_id = r.review_id
        WHERE mr.manga_id = $1
        ORDER BY r.created_at DESC
        """
        records = await db.fetch(query, manga_id)

        if not records:
            print(f"No reviews found for manga_id {manga_id}")
            return []

        return [
            review for row in records if (review := record_to_review(row)) is not None
        ]

    except Exception as e:
        print(f"Error in list_manga_reviews: {e}")
        return []
