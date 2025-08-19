from datetime import datetime
from mugennocore.model.reviews import Review
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.reviews import insert_review


COMMANDS = {
    "insert_review": {
        "description": "Create a test review with default values",
        "args": ["--user_id:int?", "--score:float?", "--content:str?"],
        "example": "insert_review --user_id=1 --score=5 --content='Great product!'",
    },
}


def parse_args_key_value(parts: list[str]) -> dict[str, str]:
    """
    Converts parts ["--user_id=1", "--score=5"] into {"user_id": "1", "score": "5"}
    """
    args = {}
    for part in parts:
        if "=" in part:
            key, value = part.lstrip("-").split("=", 1)
            args[key] = value
    return args


async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
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

    if cmd == "insert_review":
        user_id = int(args.get("user_id", "1"))
        score = float(args.get("score", "5"))
        content = args.get("content", "Default review content")

        review = Review(
            review_id=0,
            users_id=user_id,
            score=score,
            content=content,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        rid = await insert_review(db, review)
        print(f"Review inserted with ID {rid}")