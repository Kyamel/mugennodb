# endpoints/user_endpoints.py
from datetime import datetime
from uuid import uuid4
from mugennocore.model.user import User
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.users import get_user_by_id, insert_user

COMMANDS = {"get_user": "Retrieve user by ID", "insert_dummy_user": "Create test user"}


async def handle_command(db: DatabaseProtocol, parts: list[str]):
    if parts[0] == "get_user":
        user_id = int(parts[1])
        user = await get_user_by_id(db, user_id)
        print(user or "User not found")

    elif parts[0] == "insert_dummy_user":
        user = User(
            id=0,
            user_name="admin",
            user_password="password123",
            user_role="admin",
            join_date=datetime.now(),
            email="admin@example.com",
            is_banned=False,
            nickname="admin",
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
