from datetime import datetime
from uuid import uuid4
from mugennocore.model.page_review import PageReview
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.page_review import insert_page_review


COMMANDS = {
    "insert_page_review": {
        "description": "Create test page review with default values",
        "args": ["--page_id:str?", "--review_id:int?"],
        "example": "insert_page_review --page_id=1 --review_id=1",
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

async def handle_command(db, parts: list[str]) -> None:
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

    if cmd == "insert_page_review":
        page_id = float(args.get("page_id", "1"))
        review_id = float(args.get("review_id", "1"))

        review = PageReview(
            id=0,
            page_id=page_id,
            review_id=review_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        review_id = await insert_page_review(db, review)
        print(f"Review inserted with ID {review_id}")