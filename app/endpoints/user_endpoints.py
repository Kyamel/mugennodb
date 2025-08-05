from datetime import datetime
from uuid import uuid4
from mugennocore.model.user import User
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.users import get_user_by_id, insert_user

# Comandos disponíveis
COMMANDS = {
    "get_user": {
        "description": "Retrieve user by ID",
        "args": ["user_id:int"],
        "example": "get_user 101",
    },
    "insert_user": {
        "description": "Create test user with default values",
        "args": ["--role:str?", "--username:str?"],
        "example": "insert_user --role=admin --username=test",
    },
}


def parse_optional_flags(parts: list[str]) -> dict[str, str]:
    """
    Converte partes como ["--role=admin", "--username=test"] em {"role": "admin", "username": "test"}
    """
    args = {}
    for part in parts:
        if part.startswith("--") and "=" in part:
            key, value = part[2:].split("=", 1)
            args[key] = value
    return args


async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
    if parts[0] == "get_user":
        if len(parts) < 2:
            print("Usage: get_user <user_id>")
            return

        try:
            user_id = int(parts[1])
        except ValueError:
            print("user_id must be an integer.")
            return

        user = await get_user_by_id(db, user_id)
        print(user or "User not found")

    elif parts[0] == "insert_user":
        args = parse_optional_flags(parts[1:])

        role = args.get("role", "admin")
        username = args.get("username", "admin")

        user = User(
            id=0,
            user_name=username,
            user_password="password123",
            user_role=role,
            join_date=datetime.now(),
            email=f"{username}@example.com",
            is_banned=False,
            nickname=username,
            user_profile=uuid4(),
            user_banner=uuid4(),
            is_active=True,
            allow_nsfw=True,
            allow_dm=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        uid = await insert_user(db, user)
        print(f"User inserted with ID {uid}")
