from datetime import datetime, date
from uuid import UUID, uuid4
from mugennocore.model.enums import EAgeRating, EComicType, EMangaStatus
from mugennocore.model.mangas import MangasCreate
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.repositories.mangas_repo import (
    get_manga_by_id,
    create_manga,
    search_mangas_by_title,
)

COMMANDS = {
    "get_manga": {
        "description": "Retrieve manga by ID",
        "args": ["manga_id:int"],
        "example": "get_manga manga_id=789",
    },
    "create_manga": {
        "description": "Create test manga with optional title args",
        "args": ["--title_english:str?", "--title_native:str?", "--mal_id:int?"],
        "example": "create_manga --title_english='Bleach' --mal_id=321",
    },
    "search_manga": {
        "description": "Search manga by title with pagination.",
        "args": ["title:str", "--limit:int?", "--offset:int?"],
        "example": "search_manga title=Hero --limit=5",
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

def parse_manga_id(manga_id_input) -> UUID:
    """Converte input para UUID, aceitando inteiros ou strings UUID"""
    try:
        # Tenta converter diretamente se for string UUID
        return UUID(manga_id_input)
    except (ValueError, TypeError):
        try:
            # Se for inteiro, converte para UUID "fácil"
            number = int(manga_id_input)
            hex_str = f"{number:032x}"
            return UUID(hex_str)
        except (ValueError, TypeError):
            raise ValueError("manga_id must be a valid UUID or integer")



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
            manga_id = parse_manga_id(args["manga_id"])
        except ValueError:
            print("manga_id must be an integer.")
            return

        manga = await get_manga_by_id(db, manga_id)
        print(manga or "Mangas not found")

    elif cmd == "create_manga":
        title_english = args.get("title_english", "Mugen Hero")
        title_native = args.get("title_native", "無限ヒーロー")

        try:
            mal_id = int(args.get("mal_id", 123456))
        except ValueError:
            print("mal_id must be an integer.")
            return

        manga_create = MangasCreate(
            country_id=1,
            user_id=UUID("00000000-0000-0000-0000-000000000001"),
            title_english=title_english,
            title_native=title_native,
            release_date=date(1999, 9, 21),
            finish_date=date(2014, 11, 10),
            age_rating=EAgeRating.PG12,
            status=EMangaStatus.COMPLETED,
            comic_type=EComicType.MANGA,
            cover_url="sla",
            mal_id=mal_id,
            kitsu_id=mal_id,
        )
        mid = await create_manga(db, manga_create)
        print(f"Mangas inserted with ID {mid}")

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