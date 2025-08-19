from mugennocore.model.chapter_review import ChapterReview
from mugennodb.database.interface.chapter_review import insert_chapter_review

COMMANDS = {
    "insert_chapter_review": {
        "description": "Cria relação entre um capítulo e uma review",
        "args": ["review_id:int", "chapter_id:int"],
        "example": "insert_chapter_review review_id=1 chapter_id=10",
    }
}

def parse_args_key_value(parts: list[str]) -> dict[str, str]:
    """
    Converte lista ["review_id=1", "chapter_id=10"] em {"review_id": "1", "chapter_id": "10"}
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

    # Checa se argumentos obrigatórios foram informados
    for key in required_keys:
        if key not in args:
            print(f"Missing required argument: {key}")
            return

    if cmd == "insert_chapter_review":
        try:
            review_id = int(args["review_id"])
            chapter_id = int(args["chapter_id"])
        except ValueError:
            print("Os argumentos 'review_id' e 'chapter_id' devem ser números inteiros.")
            return

        relation = ChapterReview(
            review_id=review_id,
            chapter_id=chapter_id
        )

        success = await insert_chapter_review(db, relation)
        if success:
            print(f"Relação inserida: review_id={review_id}, chapter_id={chapter_id}")
        else:
            print("Falha ao inserir a relação.")
