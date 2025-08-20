from datetime import datetime, date
from uuid import uuid4
from mugennocore.model.manga import Manga
from .chapter_endpoints import parse_key_value_args
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.mangas import (
    get_manga_by_id,
    insert_manga,
    search_mangas_by_title,
    get_mangas_by_tag_name,
)

COMMANDS = {
    "get_manga": {
        "description": "Retrieve manga by ID",
        "args": ["manga_id:int"],
        "example": "get_manga manga_id=789",
    },
    "insert_manga": {
        "description": "Create test manga with optional title args",
        "args": ["--title_english:str?", "--title_native:str?", "--mal_id:int?"],
        "example": "insert_manga --title_english='Bleach' --mal_id=321",
    },
    "search_manga": {
        "description": "Search manga by title with pagination.",
        "args": ["title:str", "--limit:int?", "--offset:int?"],
        "example": "search_manga title=Hero --limit=5",
    },
    "filter_by_tag": {
        "description": "Filter manga by tag with pagination.",
        "args": ["tag:str", "--limit:int?", "--offset:int?"],
        "example": "filter_by_tag tag=Ação --limit=10",
    },
}


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

    if cmd == "get_manga":
        try:
            manga_id = int(args["manga_id"])
        except ValueError:
            print("manga_id must be an integer.")
            return

        manga = await get_manga_by_id(db, manga_id)
        print(manga or "Manga not found")

    elif cmd == "insert_manga":
        title_english = args.get("title_english", "Mugen Hero")
        title_native = args.get("title_native", "無限ヒーロー")

        try:
            mal_id = int(args.get("mal_id", 123456))
        except ValueError:
            print("mal_id must be an integer.")
            return

        manga = Manga(
            id=0,
            country_id=4,
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

    elif cmd == "search_manga":
        title = args.get("title")
        if not title:
            print("The 'title' argument is required.")
            return

        limit = int(args.get("limit", 10))
        offset = int(args.get("offset", 0))

        mangas = await search_mangas_by_title(db, title, limit, offset)
        if not mangas:
            print(f"No manga found with the title '{title}'.")
            return

        print(f"--- Search results for '{title}' ---")
        for m in mangas:
            print(f"  ID: {m.id} - {m.title_english}")

    elif cmd == "filter_by_tag":
        tag = args.get("tag")
        if not tag:
            print("The 'tag' argument is required.")
            return

        limit = int(args.get("limit", 10))
        offset = int(args.get("offset", 0))

        mangas = await get_mangas_by_tag_name(db, tag, limit, offset)
        if not mangas:
            print(f"No manga found with the tag '{tag}'.")
            return

        print(f"--- Mangas with the tag '{tag}' ---")
        for m in mangas:
            print(f"  ID: {m.id} - {m.title_english}")
