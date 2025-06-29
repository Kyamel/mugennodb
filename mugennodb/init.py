import os
from mugennodb.conection.database_protocol import DatabaseProtocol

BASE_DIR = os.path.dirname(__file__)
MIGRATION_DIR = os.path.join(BASE_DIR, "database", "migrations")


async def create_database_schema(db: DatabaseProtocol):
    for filename in sorted(os.listdir(MIGRATION_DIR)):
        if filename.endswith(".sql"):
            path = os.path.join(MIGRATION_DIR, filename)
            with open(path, encoding="utf-8") as f:
                sql = f.read()
                await db.execute_script(sql)
                print(f"[✓] Migration applied: {filename}")
