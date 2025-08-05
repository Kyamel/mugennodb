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
        "example": "get_page chapter_id=10 pg_number=2",
    },
    "insert_page": {
        "description": "Add test page with default values",
        "args": ["--chapter_id:int?", "--pg_number:int?"],
        "example": "insert_page --chapter_id=10 --pg_number=3",
    },
}


def parse_key_value_args(parts: list[str]) -> dict[str, str]:
    """
    Converte partes como ["chapter_id=1", "--pg_number=2"] em {"chapter_id": "1", "pg_number": "2"}
    """
    args = {}
    for part in parts:
        if "=" in part:
            key, value = part.lstrip("-").split("=", 1)
            args[key] = value
    return args


async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
    if not parts:
        print("No command provided.")
        return

    cmd = parts[0]
    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}")
        return

    args_def = COMMANDS[cmd]["args"]
    required_keys = [arg.split(":")[0] for arg in args_def if not arg.startswith("--")]

    args = parse_key_value_args(parts[1:])

    # Validar argumentos obrigatórios
    for key in required_keys:
        if key not in args:
            print(f"Missing required argument: {key}")
            return

    if cmd == "get_page":
        try:
            chapter_id = int(args["chapter_id"])
            pg_number = int(args["pg_number"])
        except ValueError:
            print("chapter_id and pg_number must be integers.")
            return

        page = await get_page_by_chapter_and_number(db, chapter_id, pg_number)
        print(page or "Page not found")

    elif cmd == "insert_page":
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
