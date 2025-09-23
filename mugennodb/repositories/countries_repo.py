from typing import Optional
from dataclasses import fields
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennocore.model.countries import CountriesRead, CountriesCreate, CountriesUpdate


# -------------------- READ --------------------

async def get_country_by_id(db: DatabaseProtocol, country_id: int) -> Optional[CountriesRead]:
    query = "SELECT * FROM countries WHERE id = $1"
    row = await db.fetchrow(query, country_id)
    return CountriesRead(**dict(row)) if row else None


async def get_country_by_locale(db: DatabaseProtocol, locale_code: str) -> Optional[CountriesRead]:
    query = "SELECT * FROM countries WHERE locale_code = $1"
    row = await db.fetchrow(query, locale_code)
    return CountriesRead(**dict(row)) if row else None


async def list_countries(db: DatabaseProtocol, limit: int = 100, offset: int = 0) -> list[CountriesRead]:
    query = "SELECT * FROM countries ORDER BY id ASC LIMIT $1 OFFSET $2"
    rows = await db.fetch(query, limit, offset)
    return [CountriesRead(**dict(r)) for r in rows]


# -------------------- CREATE --------------------

async def create_country(db: DatabaseProtocol, data: CountriesCreate) -> CountriesRead:
    data_fields = [f.name for f in fields(data)]
    values = [getattr(data, f) for f in data_fields]

    columns = ", ".join(data_fields)
    placeholders = ", ".join(f"${i+1}" for i in range(len(values)))

    query = f"""
        INSERT INTO countries ({columns})
        VALUES ({placeholders})
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return CountriesRead(**dict(row))


# -------------------- UPDATE --------------------

async def update_country(db: DatabaseProtocol, data: CountriesUpdate) -> Optional[CountriesRead]:
    fields_to_update = {k: v for k, v in data.__dict__.items() if v is not None and k != "id"}
    if not fields_to_update:
        return await get_country_by_id(db, data.id)

    set_clause = ", ".join(f"{k} = ${i+1}" for i, k in enumerate(fields_to_update.keys()))
    values = list(fields_to_update.values())
    values.append(data.id)

    query = f"""
        UPDATE countries
        SET {set_clause}, updated_at = now()
        WHERE id = ${len(values)}
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return CountriesRead(**dict(row)) if row else None


# -------------------- DELETE --------------------

async def delete_country(db: DatabaseProtocol, country_id: int) -> bool:
    query = "DELETE FROM countries WHERE id = $1"
    result = await db.execute(query, country_id)
    return result != "DELETE 0"
