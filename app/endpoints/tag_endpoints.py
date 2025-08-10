from datetime import datetime
from mugennocore.model.tag import Tag
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.tags import (
    get_all_tags,
    insert_tag,
)

COMMANDS = {
    "get_tags": {
        "description": "Lista todas as tags cadastradas.",
        "args": ["--limit:int?", "--offset:int?"],
        "example": "get_tags --limit=10 --offset=20",
    },
    "insert_tag": {
        "description": "Adiciona uma nova tag.",
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
        print("Nenhum comando para 'tag' foi fornecido.")
        return

    cmd = parts[0]
    if cmd not in COMMANDS:
        print(f"Comando de tag desconhecido: {cmd}")
        return

    args_def = COMMANDS[cmd]["args"]
    required_keys = [arg.split(":")[0] for arg in args_def if not arg.startswith("--")]
    args = parse_key_value_args(parts[1:])

    for key in required_keys:
        if key not in args:
            print(f"Argumento obrigatório ausente: {key}")
            print(f"Exemplo de uso: {COMMANDS[cmd]['example']}")
            return

    if cmd == "get_tags":
        try:
            limit = int(args.get("limit", 0))
            offset = int(args.get("offset", 0))
        except ValueError:
            print("Os valores de 'limit' e 'offset' devem ser números inteiros.")
            return

        tags = await get_all_tags(db)
        
        # Aplica a paginação
        tags = tags[offset:]
        if limit > 0:
            tags = tags[:limit]

        if tags:
            print("--- Tags Encontradas ---")
            for t in tags:
                # O método __str__ do objeto Tag será chamado aqui
                print(t)
            print("------------------------")
        else:
            print("Nenhuma tag encontrada com os filtros especificados.")

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
        print(f"✅ Tag '{tag_name}' inserida com sucesso com o ID: {tag_id}")