from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.destroy import destroy_database_schema
from mugennodb.init import create_database_schema
from mugennodb.populate import populate_database_with_seed
from mugennodb.consults import execute_get_mangas_ongoing
from mugennodb.consults import execute_get_mangas_and_genres
from mugennodb.consults import execute_get_users_without_reading
from mugennodb.consults import execute_get_users_with_numReviews_and_averageScore
from mugennodb.consults import execute_get_mangas_same_genreOf_attackOnTitan


COMMANDS = {
    "init_db": {
        "description": "Run SQL migrations to create or reset the database",
        "args": [],
        "example": "init_db",
    },
    "seed_db": {
        "description": "Seed the database with initial test data",
        "args": [],
        "example": "seed_db",
    },
    "drop_all": {
        "description": "Delete all tables, views, functions, and sequences in the database",
        "args": [],
        "example": "drop_all",
    },
    "get_users_with_reviews": {
        "description": "Get users who have written more than one review",
        "args": [],
        "example": "get_users_with_reviews",
    },
    "get_mangas_ongoing": {
        "description": "Get all ongoing mangas",
        "args": [],
        "example": "get_mangas_ongoing",
    },
    "get_mangas_and_genres": {
        "description": "Get all mangas and their genres",
        "args": [],
        "example": "get_mangas_and_genres",
    },
    "get_users_without_reading": {
        "description": "Get users who have not read any manga",
        "args": [],
        "example": "get_users_without_reading",
    },
    "get_mangas_same_genreOf_attackOnTitan": {
        "description": "Get all mangas that share the same genre as 'Attack on Titan'",
        "args": [],
        "example": "get_mangas_same_genreOf_attackOnTitan",
    },
}


async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
    """Dispatches db admin commands from the REPL CLI."""
    if parts[0] == "init_db":
        await create_database_schema(db)
    elif parts[0] == "seed_db":
        await populate_database_with_seed(db)
    elif parts[0] == "drop_all":
        await destroy_database_schema(db)
    elif parts[0] == "get_users_with_reviews":
        await execute_get_users_with_reviews(db)
    elif parts[0] == "get_mangas_ongoing":
        await execute_get_mangas_ongoing(db)
    elif parts[0] == "get_mangas_and_genres":
        await execute_get_mangas_and_genres(db)
    elif parts[0] == "get_users_without_reading":
        await execute_get_users_without_reading(db)
    elif parts[0] == "get_mangas_same_genreOf_attackOnTitan":
        await execute_get_mangas_same_genreOf_attackOnTitan(db)
