from typing import Optional
from uuid import UUID
from dataclasses import fields
from mugennocore.model.users import UsersRead, UsersCreate, UsersUpdate
from mugennocore.model.enums import EUserRole
from mugennodb.conection.database_protocol import DatabaseProtocol


# -------------------- READ --------------------

async def get_user_by_id(db: DatabaseProtocol, user_id: UUID) -> Optional[UsersRead]:
    query = "SELECT * FROM users WHERE id = $1 AND deleted_at IS NULL"
    row = await db.fetchrow(query, user_id)
    return UsersRead(**dict(row)) if row else None


async def get_user_by_username(db: DatabaseProtocol, username: str) -> Optional[UsersRead]:
    query = "SELECT * FROM users WHERE username = $1 AND deleted_at IS NULL"
    row = await db.fetchrow(query, username)
    return UsersRead(**dict(row)) if row else None


async def list_users(db: DatabaseProtocol, limit: int = 100, offset: int = 0) -> list[UsersRead]:
    query = "SELECT * FROM users WHERE deleted_at IS NULL ORDER BY created_at DESC LIMIT $1 OFFSET $2"
    rows = await db.fetch(query, limit, offset)
    return [UsersRead(**dict(r)) for r in rows]


# -------------------- CREATE --------------------

async def create_user(db: DatabaseProtocol, data: UsersCreate) -> UsersRead:
    data_fields = [f.name for f in fields(data)]
    values = [getattr(data, f) for f in data_fields]

    # Converte enum role para string
    if "role" in data_fields:
        idx = data_fields.index("role")
        values[idx] = values[idx].value

    columns = ", ".join(data_fields)
    placeholders = ", ".join(f"${i+1}" for i in range(len(values)))

    query = f"""
        INSERT INTO users ({columns})
        VALUES ({placeholders})
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return UsersRead(**dict(row))


# -------------------- UPDATE --------------------

async def update_user(db: DatabaseProtocol, data: UsersUpdate) -> Optional[UsersRead]:
    fields_to_update = {k: v for k, v in data.__dict__.items() if v is not None and k != "id"}
    if not fields_to_update:
        return await get_user_by_id(db, data.id)

    # Converte enum role para string se necessário
    if "role" in fields_to_update and isinstance(fields_to_update["role"], EUserRole):
        fields_to_update["role"] = fields_to_update["role"].value

    set_clause = ", ".join(f"{k} = ${i+1}" for i, k in enumerate(fields_to_update.keys()))
    values = list(fields_to_update.values())
    values.append(data.id)

    query = f"""
        UPDATE users
        SET {set_clause}, updated_at = now()
        WHERE id = ${len(values)} AND deleted_at IS NULL
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return UsersRead(**dict(row)) if row else None


# -------------------- SOFT DELETE --------------------

async def delete_user(db: DatabaseProtocol, user_id: UUID) -> bool:
    query = "UPDATE users SET deleted_at = now() WHERE id = $1 AND deleted_at IS NULL"
    result = await db.execute(query, user_id)
    return result != "UPDATE 0"


# -------------------- RESTORE --------------------

async def restore_user(db: DatabaseProtocol, user_id: UUID) -> bool:
    query = "UPDATE users SET deleted_at = NULL WHERE id = $1 AND deleted_at IS NOT NULL"
    result = await db.execute(query, user_id)
    return result != "UPDATE 0"
