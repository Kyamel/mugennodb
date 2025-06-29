from mugennodb.init import create_database_schema
from mugennodb.populate import populate_database_with_seed

COMMANDS = {
    "init_db": "Run SQL migrations to create or reset the database",
    "seed_db": "Seed the database with initial test data",
}


async def handle_command(db, parts: list[str]):
    """Dispatches db admin commands from the REPL CLI."""
    if parts[0] == "init_db":
        await create_database_schema(db)
    elif parts[0] == "seed_db":
        await populate_database_with_seed(db)
