from typing import List, Optional
from mugennocore.interfaces.icountry import ICountry
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.mapping.country_map import record_to_country


async def get_all_countries(db: DatabaseProtocol) -> List[ICountry]:
    """Retorna uma lista de todos os países cadastrados, ordenados pelo código."""
    rows = await db.fetch("SELECT * FROM countries ORDER BY locale_code ASC")
    return [country for row in rows if (country := record_to_country(row)) is not None]


async def get_country_by_locale(db: DatabaseProtocol, locale_code: str) -> Optional[ICountry]:
    """Busca um país específico pelo seu código de localidade (ex: 'BR', 'JP')."""
    row = await db.fetchrow("SELECT * FROM countries WHERE locale_code = $1", locale_code.upper())
    return record_to_country(row)


async def insert_country(db: DatabaseProtocol, country: ICountry) -> int:
    """
    Insere um novo país no banco de dados.
    Recebe um objeto ICountry e retorna o ID gerado.
    """
    query = """
        INSERT INTO countries (lang, locale_code)
        VALUES ($1, $2)
        RETURNING id
    """
    row = await db.fetchrow(query, country.lang, country.locale_code.upper())
    return row["id"] if row else -1