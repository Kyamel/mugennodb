from datetime import datetime
from mugennocore.model.reviews import Review
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.reviews import insert_manga_review, list_manga_reviews

COMMANDS = {
    "insert_review": {
        "description": "Create a test review for a manga with default values",
        "args": ["user_id:int", "manga_id:int", "--score:float?", "--content:str?"],
        "example": "insert_review user_id=1 manga_id=42 --score=5 --content='Great manga!'",
    },
    "list_reviews": {
        "description": "List all reviews for a specific manga",
        "args": ["manga_id:int"],
        "example": "list_reviews manga_id=42",
    },
}


def parse_args_key_value(parts: list[str]) -> dict[str, str]:
    """
    Converts parts ["user_id=1", "--score=5"] into {"user_id": "1", "score": "5"}
    """
    args = {}
    for part in parts:
        if "=" in part:
            clean_part = part.lstrip("-")
            key, value = clean_part.split("=", 1)
            args[key] = value
    return args


async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
    cmd = parts[0]
    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}")
        return

    args_def = COMMANDS[cmd]["args"]
    required_keys = []
    for arg in args_def:
        arg_name = arg.split(":")[0].lstrip("-")
        if not arg.endswith("?"):
            required_keys.append(arg_name)

    args = parse_args_key_value(parts[1:])

    # Check required args
    for key in required_keys:
        if key not in args:
            print(f"Missing required argument: {key}")
            print(f"Argumentos fornecidos: {list(args.keys())}")
            return

    if cmd == "insert_review":
        user_id = int(args["user_id"])
        manga_id = int(args["manga_id"])
        score = float(args.get("score", "5"))
        content = args.get("content", "Default review content")

        review = Review(
            review_id=0,
            users_id=user_id,
            score=score,
            content=content,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        rid = await insert_manga_review(db, review, manga_id)
        print(f"Review inserted with ID {rid} for manga {manga_id}")

    elif cmd == "list_reviews":
        manga_id = int(args["manga_id"])
        reviews = await list_manga_reviews(db, manga_id)

        print(f"\nReviews for manga_id {manga_id}:")
        print("=" * 50)
        for review in reviews:
            print(f"ID: {review.review_id}")
            print(f"User ID: {review.users_id}")
            print(f"Score: {review.score}")
            print(f"Content: {review.content[:100]}...")
            print(f"Created: {review.created_at}")
            print("-" * 30)

        print(f"\nTotal reviews: {len(reviews)}")
