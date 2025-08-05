from datetime import datetime
from uuid import uuid4
from mugennocore.model.chapter import Chapter
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.chapters import (
    get_all_chapters_by_manga_id,
    insert_chapter,
)

COMMANDS = {
    "get_chapters": {
        "description": "List chapters for manga",
        "args": ["manga_id:int", "--limit:int?", "--offset:int?"],
        "example": "get_chapters 123 --limit=10",
    },
    "insert_chapter": {
        "description": "Add test chapter",
        "args": ["manga_id:int", "--ch_number:float?", "--title:str?"],
        "example": "insert_chapter 456 --ch_number=2.5 --title='Final Battle'",
    },
}


def parse_optional_flags(parts: list[str]) -> dict[str, str]:
    args = {}
    for part in parts:
        if part.startswith("--") and "=" in part:
            key, value = part[2:].split("=", 1)
            args[key] = value
    return args


async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
    if parts[0] == "get_chapters":
        if len(parts) < 2:
            print("Usage: get_chapters <manga_id> [--limit=10] [--offset=0]")
            return

        try:
            manga_id = int(parts[1])
        except ValueError:
            print("manga_id must be an integer.")
            return

        args = parse_optional_flags(parts[2:])
        limit = int(args.get("limit", 0))
        offset = int(args.get("offset", 0))

        chapters = await get_all_chapters_by_manga_id(db, manga_id)

        if chapters:
            for c in chapters:
                print(c)
        else:
            print("No chapters found")

    elif parts[0] == "insert_chapter":
        if len(parts) < 2:
            print(
                "Usage: insert_chapter <manga_id> [--ch_number=1.0] [--title='Chapter Name']"
            )
            return

        try:
            manga_id = int(parts[1])
        except ValueError:
            print("manga_id must be an integer.")
            return

        args = parse_optional_flags(parts[2:])
        ch_number = int(args.get("ch_number", 1))
        title = args.get("title", "Chapter One")

        chapter = Chapter(
            id=0,
            manga_id=manga_id,
            title=title,
            cover=uuid4(),
            ch_number=ch_number,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        cid = await insert_chapter(db, chapter)
        print(f"Chapter inserted with ID {cid}")
