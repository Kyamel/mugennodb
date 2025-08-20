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
        "example": "get_user user_id=101",
    },
    "insert_user": {
        "description": "Create test user with default values",
        "args": ["--role:str?", "--username:str?"],
        "example": "insert_user --role=admin --username=test",
    },
}


def parse_args_key_value(parts: list[str]) -> dict[str, str]:
    """
    Converts parts ["user_id=101", "--role=admin"] in {"user_id": "101", "role": "admin"}
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

    args = parse_args_key_value(parts[1:])

    # Check required args
    for key in required_keys:
        if key not in args:
            print(f"Missing required argument: {key}")
            return

    if cmd == "get_user":
        try:
            user_id = int(args["user_id"])
        except ValueError:
            print("user_id must be an integer.")
            return

        user = await get_user_by_id(db, user_id)
        print(user or "User not found")

    elif cmd == "insert_user":
        role = args.get("role", "admin")
        username = args.get("username", "admin")

        user = User(
            id=0,
            country_id=4,
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
