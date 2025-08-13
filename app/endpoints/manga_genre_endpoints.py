from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.manga_genres import (
    add_genre_to_manga,
    get_genres_for_manga,
)
from mugennodb.database.interface.mangas import get_manga_by_id
from mugennodb.database.interface.tags import insert_tag
from mugennocore.model.tag import Tag
from datetime import datetime
from .chapter_endpoints import parse_key_value_args


COMMANDS = {
    "add_genre": {
        "description": "Adiciona um gênero (tag) a um mangá.",
        "args": ["manga_id:int", "tag_id:int"],
        "example": "add_genre manga_id=1 tag_id=3",
    },
    "get_genres": {
        "description": "Lista os gêneros de um mangá específico.",
        "args": ["manga_id:int"],
        "example": "get_genres manga_id=1",
    },
    "create_genre_tag": {
        "description": "Cria uma nova tag com o tipo 'GENRE'.",
        "args": ["name:str"],
        "example": "create_genre_tag name=Action",
    },
}


async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
    if not parts:
        print("Nenhum comando de gênero fornecido.")
        return

    cmd = parts[0]
    if cmd not in COMMANDS:
        print(f"Comando de gênero desconhecido: {cmd}")
        return

    args = parse_key_value_args(parts[1:])

    required_keys = [arg.split(":")[0] for arg in COMMANDS[cmd].get("args", [])]
    for key in required_keys:
        if key not in args:
            print(f"Argumento obrigatório ausente: {key}")
            print(f"Exemplo: {COMMANDS[cmd]['example']}")
            return

    if cmd == "create_genre_tag":
        name = args["name"]
        genre_tag = Tag(
            id=0,
            name=name,
            type="GENRE",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        tag_id = await insert_tag(db, genre_tag)
        if tag_id != -1:
            print(f"✅ Tag de Gênero '{name}' criada com sucesso! ID: {tag_id}")
        else:
            print(f"❌ Falha ao criar a tag de gênero. Ela já existe?")

    elif cmd == "add_genre":
        try:
            manga_id = int(args["manga_id"])
            tag_id = int(args["tag_id"])
        except ValueError:
            print("Os IDs de mangá e tag devem ser números inteiros.")
            return

        rel_id = await add_genre_to_manga(db, manga_id, tag_id)
        if rel_id != -1:
            print(f"Gênero (Tag ID: {tag_id}) adicionado ao Mangá (ID: {manga_id}) com sucesso.")
        else:
            print("Não foi possível adicionar o gênero. A relação já existe?")

    elif cmd == "get_genres":
        try:
            manga_id = int(args["manga_id"])
        except ValueError:
            print("O ID do mangá deve ser um número inteiro.")
            return
        
        manga = await get_manga_by_id(db, manga_id)
        if not manga:
            print(f"Mangá com ID {manga_id} não encontrado.")
            return

        genres = await get_genres_for_manga(db, manga_id)

        print(f"--- Gêneros para '{manga.title_english}' ---")

        if not genres:
            print(f"Nenhum gênero encontrado para o mangá de ID {manga_id}.")
            return

        genre_names = [genre.name for genre in genres]
        print(", ".join(genre_names))
        print("-----------------------------------")