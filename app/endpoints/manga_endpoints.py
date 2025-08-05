from datetime import datetime, date
from uuid import uuid4
from mugennocore.model.manga import Manga
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.mangas import get_manga_by_id, insert_manga

COMMANDS = {
    "get_manga": {
        "description": "Retrieve manga by ID",
        "args": ["manga_id:int"],
        "example": "get_manga 789",
    },
    "insert_manga": {
        "description": "Create test manga with optional title args",
        "args": ["--title_english:str?", "--title_native:str?", "--mal_id:int?"],
        "example": "insert_manga --title_english='Bleach' --mal_id=321",
    },
}


def parse_optional_flags(parts: list[str]) -> dict[str, str]:
    """
    Converte partes como ["--title_english=Bleach", "--mal_id=321"]
    em {"title_english": "Bleach", "mal_id": "321"}
    """
    args = {}
    for part in parts:
        if part.startswith("--") and "=" in part:
            key, value = part[2:].split("=", 1)
            args[key] = value
    return args


async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
    if parts[0] == "get_manga":
        if len(parts) < 2:
            print("Usage: get_manga <manga_id>")
            return

        try:
            manga_id = int(parts[1])
        except ValueError:
            print("manga_id must be an integer.")
            return

        manga = await get_manga_by_id(db, manga_id)
        print(manga or "Manga not found")

    elif parts[0] == "insert_manga":
        args = parse_optional_flags(parts[1:])

        title_english = args.get("title_english", "Mugen Hero")
        title_native = args.get("title_native", "無限ヒーロー")

        try:
            mal_id = int(args.get("mal_id", 123456))
        except ValueError:
            print("mal_id must be an integer.")
            return

        manga = Manga(
            id=0,
            title_english=title_english,
            title_native=title_native,
            release_date=date(2023, 1, 1),
            finish_date=None,
            active_status="ongoing",
            comic_type="manga",
            cover=uuid4(),
            mal_id=mal_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mid = await insert_manga(db, manga)
        print(f"Manga inserted with ID {mid}")
