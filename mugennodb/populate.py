import os
from mugennodb.conection.database_protocol import DatabaseProtocol

BASE_DIR = os.path.dirname(__file__)
SEED_FILE = os.path.join(BASE_DIR, "database", "seeds.sql")


async def populate_database_with_seed(db: DatabaseProtocol) -> None:
    with open(SEED_FILE, encoding="utf-8") as f:
        sql = f.read()
        await db.execute_script(sql)
        print(f"[✓] Seed applied: {SEED_FILE.split(os.sep)[-1]}")
