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
        "example": "get_chapters manga_id=123 --limit=10",
    },
    "insert_chapter": {
        "description": "Add test chapter",
        "args": ["manga_id:int", "--ch_number:float?", "--title:str?"],
        "example": "insert_chapter manga_id=456 --ch_number=2.5 --title='Final Battle'",
    },
}


def parse_key_value_args(parts: list[str]) -> dict[str, str]:
    """
    Converte partes como ["manga_id=123", "--limit=10"] em {"manga_id": "123", "limit": "10"}
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

    for key in required_keys:
        if key not in args:
            print(f"Missing required argument: {key}")
            return

    if cmd == "get_chapters":
        try:
            manga_id = int(args["manga_id"])
            limit = int(args.get("limit", 0))
            offset = int(args.get("offset", 0))
        except ValueError:
            print("manga_id, limit and offset must be integers.")
            return

        chapters = await get_all_chapters_by_manga_id(db, manga_id)
        chapters = chapters[offset:]
        if limit:
            chapters = chapters[:limit]

        if chapters:
            for c in chapters:
                print(c)
        else:
            print("No chapters found")

    elif cmd == "insert_chapter":
        try:
            manga_id = int(args["manga_id"])
            ch_number = float(args.get("ch_number", 1))
        except ValueError:
            print("manga_id must be int and ch_number must be float.")
            return

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
