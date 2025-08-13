from datetime import datetime

# Importe o modelo e a interface que você criou
from mugennocore.model.country import Country
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.interface.countries import (
    get_all_countries,
    get_country_by_locale,
    insert_country,
)

# Reutilizando o parser de argumentos
from .chapter_endpoints import parse_key_value_args

COMMANDS = {
    "get_countries": {
        "description": "Lista todos os países cadastrados.",
        "args": [],
        "example": "get_countries",
    },
    "get_country": {
        "description": "Busca um país pelo seu código de localidade.",
        "args": ["locale:str"],
        "example": "get_country locale=BR",
    },
    "insert_country": {
        "description": "Adiciona um novo país.",
        "args": ["locale:str", "lang:str"],
        "example": "insert_country locale=JP lang=ja",
    },
}

async def handle_command(db: DatabaseProtocol, parts: list[str]) -> None:
    if not parts:
        print("Nenhum comando para 'country' foi fornecido.")
        return

    cmd = parts[0]
    if cmd not in COMMANDS:
        print(f"Comando de país desconhecido: {cmd}")
        return

    args = parse_key_value_args(parts[1:])

    required_keys = [arg.split(":")[0] for arg in COMMANDS[cmd].get("args", []) if not arg.startswith("--")]
    for key in required_keys:
        if key not in args:
            print(f"Argumento obrigatório ausente: {key}")
            print(f"Exemplo de uso: {COMMANDS[cmd]['example']}")
            return

    if cmd == "get_countries":
        countries = await get_all_countries(db)
        if not countries:
            print("Nenhum país encontrado.")
            return
        print("--- Países Cadastrados ---")
        for c in countries:
            print(f"  ID: {c.id:<4} | {c}") # Usa o __str__ do seu modelo
        print("--------------------------")

    elif cmd == "get_country":
        locale_code = args["locale"]
        country = await get_country_by_locale(db, locale_code)
        if country:
            # Usa o __repr__ do seu modelo para uma visão detalhada
            print(repr(country))
        else:
            print(f"País com código '{locale_code.upper()}' não encontrado.")

    elif cmd == "insert_country":
        locale_code = args["locale"]
        lang = args["lang"]

        # Cria um objeto Country para passar para a função de inserção
        new_country = Country(
            id=0,
            lang=lang,
            locale_code=locale_code,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        country_id = await insert_country(db, new_country)
        if country_id != -1:
            print(f"✅ País '{locale_code.upper()}' inserido com sucesso! ID: {country_id}")
        else:
            print(f"❌ Falha ao inserir o país. O código de localidade já existe?")