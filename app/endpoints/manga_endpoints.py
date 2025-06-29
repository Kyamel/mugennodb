# endpoints/manga_endpoints.py
from datetime import datetime, date
from uuid import uuid4
from mugennocore.model.manga import Manga
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.mangas import get_manga_by_id, insert_manga

COMMANDS = {
    "get_manga": "Retrieve manga by ID",
    "insert_dummy_manga": "Create test manga",
}


async def handle_command(db: DatabaseProtocol, parts: list[str]):
    if parts[0] == "get_manga":
        manga_id = int(parts[1])
        manga = await get_manga_by_id(db, manga_id)
        print(manga or "Manga not found")

    elif parts[0] == "insert_dummy_manga":
        manga = Manga(
            id=0,
            title_english="Mugen Hero",
            title_native="無限ヒーロー",
            release_date=date(2023, 1, 1),
            finish_date=None,
            active_status="ongoing",
            comic_type="manga",
            cover=uuid4(),
            mal_id=123456,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mid = await insert_manga(db, manga)
        print(f"Manga inserted with ID {mid}")
