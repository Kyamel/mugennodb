from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.manga_genres import (
    add_genre_to_manga,
    get_genres_for_manga,
)
from mugennodb.database.interface.mangas import get_manga_by_id
from mugennodb.database.interface.tags import insert_tag
from mugennocore.model.tag import Tag
from datetime import datetime
from .chapter_endpoints import parse_key_value_args


COMMANDS = {
    "add_genre": {
        "description": "Adds a genre (tag) to a manga.",
        "args": ["manga_id:int", "tag_id:int"],
        "example": "add_genre manga_id=1 tag_id=3",
    },
    "get_genres": {
        "description": "Lists the genres of a specific manga.",
        "args": ["manga_id:int"],
        "example": "get_genres manga_id=1",
    },
    "create_genre_tag": {
        "description": "Creates a new tag with the type 'GENRE'.",
        "args": ["name:str"],
        "example": "create_genre_tag name=Action",
    },
}


async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
    if not parts:
        print("No gender command provided.")
        return

    cmd = parts[0]
    if cmd not in COMMANDS:
        print(f"Command of unknown gender: {cmd}")
        return

    args = parse_key_value_args(parts[1:])

    required_keys = [arg.split(":")[0] for arg in COMMANDS[cmd].get("args", [])]
    for key in required_keys:
        if key not in args:
            print(f"Missing mandatory argument: {key}")
            print(f"Example: {COMMANDS[cmd]['example']}")
            return

    if cmd == "create_genre_tag":
        name = args["name"]
        genre_tag = Tag(
            id=0,
            name=name,
            type="GENRE",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        tag_id = await insert_tag(db, genre_tag)
        if tag_id != -1:
            print(f"✅ Gender Tag '{name}' created successfully! ID: {tag_id}")
        else:
            print(f"❌ Failed to create gender tag. Does it already exist?")

    elif cmd == "add_genre":
        try:
            manga_id = int(args["manga_id"])
            tag_id = int(args["tag_id"])
        except ValueError:
            print("Manga and tag IDs must be integers.")
            return

        rel_id = await add_genre_to_manga(db, manga_id, tag_id)
        if rel_id != -1:
            print(
                f"Gender (Tag ID: {tag_id}) added to Manga (ID: {manga_id}) successfully."
            )
        else:
            print("Couldn't add gender. Does the relationship already exist?")

    elif cmd == "get_genres":
        try:
            manga_id = int(args["manga_id"])
        except ValueError:
            print("Manga ID must be an integer.")
            return

        manga = await get_manga_by_id(db, manga_id)
        if not manga:
            print(f"Manga with ID {manga_id} not found.")
            return

        genres = await get_genres_for_manga(db, manga_id)

        print(f"--- Genres for '{manga.title_english}' ---")

        if not genres:
            print(f"No genre found for ID {manga_id} manga.")
            return

        genre_names = [genre.name for genre in genres]
        print(", ".join(genre_names))
        print("-----------------------------------")
