from datetime import datetime
from uuid import uuid4
from mugennocore.model.page import Page
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.pages import (
    get_page_by_chapter_and_number,
    insert_page,
)

COMMANDS = {
    "get_page": {
        "description": "Get specific page by chapter and number",
        "args": ["chapter_id:int", "pg_number:int"],
        "example": "get_page 10 2",
    },
    "insert_page": {
        "description": "Add test page with default values",
        "args": ["--chapter_id:int?", "--pg_number:int?"],
        "example": "insert_page --chapter_id=10 --pg_number=3",
    },
}


def parse_optional_flags(parts: list[str]) -> dict[str, str]:
    """
    Converte partes como ["--chapter_id=1", "--pg_number=2"] em {"chapter_id": "1", "pg_number": "2"}
    """
    args = {}
    for part in parts:
        if part.startswith("--") and "=" in part:
            key, value = part[2:].split("=", 1)
            args[key] = value
    return args


async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
    if parts[0] == "get_page":
        if len(parts) < 3:
            print("Usage: get_page <chapter_id> <pg_number>")
            return

        try:
            chapter_id = int(parts[1])
            pg_number = int(parts[2])
        except ValueError:
            print("chapter_id and pg_number must be integers.")
            return

        page = await get_page_by_chapter_and_number(db, chapter_id, pg_number)
        print(page or "Page not found")

    elif parts[0] == "insert_page":
        args = parse_optional_flags(parts[1:])

        try:
            chapter_id = int(args.get("chapter_id", "1"))
            pg_number = int(args.get("pg_number", "1"))
        except ValueError:
            print("chapter_id and pg_number must be integers.")
            return

        page = Page(
            id=0,
            chapter_id=chapter_id,
            pg_number=pg_number,
            source=uuid4(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        pid = await insert_page(db, page)
        print(f"Page inserted with ID {pid}")
