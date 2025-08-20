from datetime import datetime
from mugennocore.model.tag import Tag
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.tags import (
    get_all_tags,
    insert_tag,
)

COMMANDS = {
    "get_tags": {
        "description": "Lists all registered tags.",
        "args": ["--limit:int?", "--offset:int?"],
        "example": "get_tags --limit=10 --offset=20",
    },
    "insert_tag": {
        "description": "Adds a new tag.",
        "args": ["name:str", "type:str"],
        "example": "insert_tag name=Shounen type=Demographic",
    },
}

def parse_key_value_args(parts: list[str]) -> dict[str, str]:
    """Converte partes como ["name=Shounen", "--limit=10"] em {"name": "Shounen", "limit": "10"}"""
    args = {}
    for part in parts:
        if "=" in part:
            key, value = part.lstrip("-").split("=", 1)
            args[key] = value
    return args

async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
    """Processa e executa comandos relacionados a tags."""
    if not parts:
        print("No command for 'tag' was given.")
        return

    cmd = parts[0]
    if cmd not in COMMANDS:
        print(f"Unknown tag command: {cmd}")
        return

    args_def = COMMANDS[cmd]["args"]
    required_keys = [arg.split(":")[0] for arg in args_def if not arg.startswith("--")]
    args = parse_key_value_args(parts[1:])

    for key in required_keys:
        if key not in args:
            print(f"Missing mandatory argument: {key}")
            print(f"Usage example: {COMMANDS[cmd]['example']}")
            return

    if cmd == "get_tags":
        try:
            limit = int(args.get("limit", 0))
            offset = int(args.get("offset", 0))
        except ValueError:
            print("The values of 'limit' and 'offset' must be integers.")
            return

        tags = await get_all_tags(db)
        
        # Aplica a paginação
        tags = tags[offset:]
        if limit > 0:
            tags = tags[:limit]

        if tags:
            print("------ Tags Found ------")
            for t in tags:
                # O método __str__ do objeto Tag será chamado aqui
                print(t)
            print("------------------------")
        else:
            print("No tags found with the specified filters.")

    elif cmd == "insert_tag":
        # Argumentos 'name' e 'type' são validados pela checagem de 'required_keys'
        tag_name = args["name"]
        tag_type = args["type"]

        new_tag = Tag(
            id=0, # O ID é gerado pelo banco de dados
            name=tag_name,
            type=tag_type,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        tag_id = await insert_tag(db, new_tag)
        print(f"✅ Tag '{tag_name}' successfully inserted with ID: {tag_id}")