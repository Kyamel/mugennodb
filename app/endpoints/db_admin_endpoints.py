from mugennodb.destroy import destroy_database_schema
from mugennodb.init import create_database_schema
from mugennodb.populate import populate_database_with_seed

COMMANDS = {
    "init_db": "Run SQL migrations to create or reset the database",
    "seed_db": "Seed the database with initial test data",
    "drop_all": "Delete all tables, views, functions, and sequences in the database",
}


async def handle_command(db, parts: list[str]):
    """Dispatches db admin commands from the REPL CLI."""
    if parts[0] == "init_db":
        await create_database_schema(db)
    elif parts[0] == "seed_db":
        await populate_database_with_seed(db)
    elif parts[0] == "drop_all":
        await destroy_database_schema(db)
