from datetime import datetime
from typing import cast
from mugennocore.model.read import Read
from mugennodb.database.interface.read import (
    insert_read,
    get_read,
    update_read_status,
    delete_read,
)

COMMANDS = {
    "insert_read": {
        "description": "Inserts a user-manga relationship with status",
        "args": ["user_id:int", "manga_id:int", "--status:str?"],
        "example": "insert_read user_id=1 manga_id=10 --status=reading",
    },
    "get_read": {
        "description": "Search for a reading by user and manga",
        "args": ["user_id:int", "manga_id:int"],
        "example": "get_read user_id=1 manga_id=10",
    },
    "update_read_status": {
        "description": "Updates the reading status",
        "args": ["user_id:int", "manga_id:int", "status:str"],
        "example": "update_read_status user_id=1 manga_id=10 status=finished",
    },
    "delete_read": {
        "description": "Remove a reading",
        "args": ["user_id:int", "manga_id:int"],
        "example": "delete_read user_id=1 manga_id=10",
    },
}


def parse_args_key_value(parts: list[str]) -> dict[str, str]:
    """
    Converts parts ["user_id=101", "manga_id=5", "--status=reading"]
    into {"user_id": "101", "manga_id": "5", "status": "reading"}
    """
    args = {}
    for part in parts:
        if "=" in part:
            key, value = part.lstrip("-").split("=", 1)
            args[key] = value
    return args


async def handle_command(db, parts: list[str]) -> None:
    cmd = parts[0]
    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}")
        return

    args = parse_args_key_value(parts[1:])

    if cmd == "insert_read":
        read = Read(
            user_id=int(args["user_id"]),
            manga_id=int(args["manga_id"]),
            status=args.get("status", "reading"),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        success = await insert_read(db, read)
        print("Inserted!" if success else "Failed to insert")

    elif cmd == "get_read":
        read_result = await get_read(db, int(args["user_id"]), int(args["manga_id"]))
        if read_result is None:
            print("Not found")
        else:
            read =  cast(Read, read_result)
            print(read)


    elif cmd == "update_read_status":
        success = await update_read_status(
            db, int(args["user_id"]), int(args["manga_id"]), args["status"]
        )
        print("Updated!" if success else "Failed to update")

    elif cmd == "delete_read":
        success = await delete_read(db, int(args["user_id"]), int(args["manga_id"]))
        print("Deleted!" if success else "Failed to delete")
