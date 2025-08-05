from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.destroy import destroy_database_schema
from mugennodb.init import create_database_schema
from mugennodb.populate import populate_database_with_seed

COMMANDS = {
    "init_db": {
        "description": "Run SQL migrations to create or reset the database",
        "args": ["--confirm"],
        "example": "init_db --confirm",
    },
    "seed_db": {
        "description": "Seed the database with initial test data",
        "args": ["--sample-size:int?"],
        "example": "seed_db --sample-size=50",
    },
    "drop_all": {
        "description": "Delete all tables, views, functions, and sequences in the database",
        "args": ["--confirm"],
        "example": "drop_all --confirm",
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
