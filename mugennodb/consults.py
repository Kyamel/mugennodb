import os
from mugennodb.conection.database_protocol import DatabaseProtocol

BASE_DIR = os.path.dirname(__file__)
CONSULTS_FILE = os.path.join(BASE_DIR, "database", "consults.sql")

async def execute_get_mangas_ongoing(db: DatabaseProtocol) -> None:
    with open(CONSULTS_FILE, encoding="utf-8") as f:
        sql = """
            SELECT
            title_english,
            release_date
            FROM mangas
            WHERE
            active_status = 'ongoing'
            ORDER BY
            release_date DESC;
        """
        resultados = await db.fetch(sql)
        print(f"[✓] Consulta executada. Encontrados {len(resultados)} resultados.")
        for manga in resultados:
            print(f"{manga['title_english']} - {manga['release_date']}")

async def execute_get_mangas_and_genres(db: DatabaseProtocol) -> None:
    with open(CONSULTS_FILE, encoding="utf-8") as f:
        sql = """
            SELECT
            m.title_english AS manga_title,
            t.tag_name AS genre
            FROM mangas AS m
            JOIN manga_genres AS mg
            ON m.id = mg.manga_id
            JOIN tags AS t
            ON mg.tag_id = t.id
            WHERE
            t.tag_type = 'genre'
            ORDER BY
            manga_title,
            genre;
        """
        resultados = await db.fetch(sql)
        print(f"[✓] Consulta executada. Encontrados {len(resultados)} resultados.")
        for manga in resultados:
            print(f" - {manga['manga_title']} ({manga['genre']})")

async def execute_get_users_without_reading(db: DatabaseProtocol) -> None:
    with open(CONSULTS_FILE, encoding="utf-8") as f:
        sql = """
            SELECT
            u.user_name,
            u.email
            FROM users AS u
            LEFT JOIN read AS r
            ON u.id = r.user_id
            WHERE
            r.user_id IS NULL;
        """
        resultados = await db.fetch(sql)
        print(f"[✓] Consulta executada. Encontrados {len(resultados)} resultados.")
        for user in resultados:
            print(f" - {user['user_name']} ({user['email']})")

async def execute_get_users_with_numReviews_and_averageScore(db: DatabaseProtocol) -> None:
    with open(CONSULTS_FILE, encoding="utf-8") as f:
        sql = """
            SELECT
            u.user_name,
            COUNT(r.users_id) AS number_of_reviews,
            AVG(r.score) AS average_score
            FROM users AS u
            JOIN review AS r
            ON u.id = r.users_id
            GROUP BY
            u.user_name
            HAVING
            COUNT(r.users_id) > 1;
        """
        resultados = await db.fetch(sql)
        print(f"[✓] Consulta executada. Encontrados {len(resultados)} resultados.")
        for user in resultados:
            print(f" - {user['user_name']} ({user['number_of_reviews']}) - Average Score: {user['average_score']:.2f}")

async def execute_get_mangas_same_genreOf_attackOnTitan(db: DatabaseProtocol) -> None:
    with open(CONSULTS_FILE, encoding="utf-8") as f:
        sql = """
            SELECT DISTINCT
            m.title_english
            FROM mangas m
            JOIN manga_genres mg
            ON m.id = mg.manga_id
            WHERE
            mg.tag_id IN (
                SELECT
                mg2.tag_id
                FROM mangas m2
                JOIN manga_genres mg2
                ON m2.id = mg2.manga_id
                WHERE
                m2.title_english = 'Attack on Titan'
            )
            AND m.title_english != 'Attack on Titan';
        """
        resultados = await db.fetch(sql)
        print(f"[✓] Consulta executada. Encontrados {len(resultados)} resultados.")
        for manga in resultados:
            print(f" - {manga['title_english']}")
