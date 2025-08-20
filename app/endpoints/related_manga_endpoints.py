from datetime import datetime
from mugennocore.model.related_manga import RelatedManga
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.related_mangas import (
    add_relationship,
    get_related_mangas_by_source_id,
)
from .chapter_endpoints import parse_key_value_args


COMMANDS = {
    "add_relation": {
        "description": "Creates a relationship between two mangas.",
        "args": ["source_id:int", "related_id:int", "type:str"],
        "example": "add_relation source_id=1 related_id=2 type=SEQUEL",
    },
    "get_relations": {
        "description": "Lists all manga related to a source manga.",
        "args": ["source_id:int"],
        "example": "get_relations source_id=1",
    },
}


async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
    if not parts:
        print("No relation command provided.")
        return

    cmd = parts[0]
    if cmd not in COMMANDS:
        print(f"Unknown relation command: {cmd}")
        return

    args = parse_key_value_args(parts[1:])

    required_keys = [arg.split(":")[0] for arg in COMMANDS[cmd].get("args", [])]
    for key in required_keys:
        if key not in args:
            print(f"Missing mandatory argument: {key}")
            print(f"Example: {COMMANDS[cmd]['example']}")
            return

    if cmd == "add_relation":
        try:
            source_id = int(args["source_id"])
            related_id = int(args["related_id"])
        except ValueError:
            print("Manga IDs must be integers.")
            return

        rel_type = args["type"].upper()

        new_relation = RelatedManga(
            id=0,
            source_manga_id=source_id,
            related_manga_id=related_id,
            relationship_type=rel_type,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        rel_id = await add_relationship(db, new_relation)
        if rel_id != -1:
            print(f"✅ Relation of type '{rel_type}' created successfully! ID: {rel_id}")
        else:
            print("❌ Failed to create relationship. Check if manga IDs exist.")

    elif cmd == "get_relations":
        try:
            source_id = int(args["source_id"])
        except ValueError:
            print("Manga ID must be an integer.")
            return

        related_mangas = await get_related_mangas_by_source_id(db, source_id)

        if not related_mangas:
            print(f"No related manga found for ID manga {source_id}.")
            return

        print(f"--- Relations for Manga ID: {source_id} ---")
        for manga, rel_type in related_mangas:
            print(f"  [{rel_type}] -> {manga}")
        print("---------------------------------")