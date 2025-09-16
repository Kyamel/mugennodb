from typing import Optional, Any
from uuid import UUID
from datetime import date
from mugennocore.model.enums import EAgeRating, EMangaStatus
from mugennocore.model.mangas import Mangas
from mugennodb.conection.database_protocol import DatabaseProtocol

# =======================================
# Funções de Leitura (Read)
# =======================================

async def get_manga_by_id(db: DatabaseProtocol, manga_id: UUID) -> Optional[Mangas]:
    """Busca um mangá pelo ID"""
    query = """
        SELECT id, country_id, user_id, title_english, title_native,
               release_date, finish_date, age_rating, status, comic_type_id,
               mal_id, kitsu_id, created_at, updated_at
        FROM mangas 
        WHERE id = $1
    """
    row = await db.fetchrow(query, manga_id)
    return Mangas(**row) if row else None


async def get_manga_by_mal_id(db: DatabaseProtocol, mal_id: int) -> Optional[Mangas]:
    """Busca um mangá pelo ID do MyAnimelist"""
    query = """
        SELECT id, country_id, user_id, title_english, title_native,
               release_date, finish_date, age_rating, status, comic_type_id,
               mal_id, kitsu_id, created_at, updated_at
        FROM mangas 
        WHERE mal_id = $1
    """
    row = await db.fetchrow(query, mal_id)
    return Mangas(**row) if row else None


async def get_manga_by_kitsu_id(db: DatabaseProtocol, kitsu_id: int) -> Optional[Mangas]:
    """Busca um mangá pelo ID do Kitsu"""
    query = """
        SELECT id, country_id, user_id, title_english, title_native,
               release_date, finish_date, age_rating, status, comic_type_id,
               mal_id, kitsu_id, created_at, updated_at
        FROM mangas 
        WHERE kitsu_id = $1
    """
    row = await db.fetchrow(query, kitsu_id)
    return Mangas(**dict(row)) if row else None


async def get_mangas_by_title(
    db: DatabaseProtocol, 
    title_query: str, 
    limit: int = 20, 
    offset: int = 0
) -> list[Mangas]:
    """Busca mangás por título (case-insensitive)"""
    query = """
        SELECT id, country_id, user_id, title_english, title_native,
               release_date, finish_date, age_rating, status, comic_type_id,
               mal_id, kitsu_id, created_at, updated_at
        FROM mangas 
        WHERE title_english ILIKE $1 OR title_native ILIKE $1
        ORDER BY title_english
        LIMIT $2 OFFSET $3
    """
    rows = await db.fetch(query, f"%{title_query}%", limit, offset)
    return [Mangas(**row) for row in rows]


async def get_mangas_by_status(
    db: DatabaseProtocol, 
    status: EMangaStatus, 
    limit: int = 20, 
    offset: int = 0
) -> list[Mangas]:
    """Busca mangás por status"""
    query = """
        SELECT id, country_id, user_id, title_english, title_native,
               release_date, finish_date, age_rating, status, comic_type_id,
               mal_id, kitsu_id, created_at, updated_at
        FROM mangas 
        WHERE status = $1
        ORDER BY title_english
        LIMIT $2 OFFSET $3
    """
    rows = await db.fetch(query, status.value, limit, offset)
    return [Mangas(**row) for row in rows]



async def get_mangas_by_author(
    db: DatabaseProtocol, 
    author_id: UUID, 
    limit: int = 20, 
    offset: int = 0
) -> list[Mangas]:
    """Busca mangás por autor/staff"""
    query = """
        SELECT m.id, m.country_id, m.user_id, m.title_english, m.title_native,
               m.release_date, m.finish_date, m.age_rating, m.status, m.comic_type_id,
               m.mal_id, m.kitsu_id, m.created_at, m.updated_at
        FROM mangas m
        JOIN manga_staff ms ON m.id = ms.manga_id
        JOIN staff_profiles sp ON ms.staff_profile_id = sp.id
        WHERE sp.user_id = $1 OR sp.name ILIKE $2
        ORDER BY m.title_english
        LIMIT $3 OFFSET $4
    """
    rows = await db.fetch(query, author_id, f"%{author_id}%", limit, offset)
    return [Mangas(**row) for row in rows]


async def get_recent_mangas(
    db: DatabaseProtocol, 
    limit: int = 20, 
    offset: int = 0
) -> list[Mangas]:
    """Busca mangás mais recentes"""
    query = """
        SELECT id, country_id, user_id, title_english, title_native,
               release_date, finish_date, age_rating, status, comic_type_id,
               mal_id, kitsu_id, created_at, updated_at
        FROM mangas 
        ORDER BY created_at DESC
        LIMIT $1 OFFSET $2
    """
    rows = await db.fetch(query, limit, offset)
    return [Mangas(**row) for row in rows]

# =======================================
# Funções de Criação (Create)
# =======================================

async def create_manga(db: DatabaseProtocol, manga_data: Mangas) -> Mangas:
    """Cria um novo mangá"""
    query = """
        INSERT INTO mangas (
            country_id, user_id, title_english, title_native,
            release_date, finish_date, age_rating, status, comic_type_id,
            mal_id, kitsu_id
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        RETURNING id, country_id, user_id, title_english, title_native,
                  release_date, finish_date, age_rating, status, comic_type_id,
                  mal_id, kitsu_id, created_at, updated_at
    """
    row = await db.fetchrow(
        query,
        manga_data.country_id,
        manga_data.user_id,
        manga_data.title_english,
        manga_data.title_native,
        manga_data.release_date,
        manga_data.finish_date,
        manga_data.age_rating.value,
        manga_data.status.value,
        manga_data.comic_type_id,
        manga_data.mal_id,
        manga_data.kitsu_id
    )
    return Mangas(**row)


async def create_manga_with_id(db: DatabaseProtocol, manga_data: Mangas) -> Mangas:
    """Cria um novo mangá com ID específico (útil para testes)"""
    query = """
        INSERT INTO mangas (
            id, country_id, user_id, title_english, title_native,
            release_date, finish_date, age_rating, status, comic_type_id,
            mal_id, kitsu_id
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        RETURNING id, country_id, user_id, title_english, title_native,
                  release_date, finish_date, age_rating, status, comic_type_id,
                  mal_id, kitsu_id, created_at, updated_at
    """
    row = await db.fetchrow(
        query,
        manga_data.id,
        manga_data.country_id,
        manga_data.user_id,
        manga_data.title_english,
        manga_data.title_native,
        manga_data.release_date,
        manga_data.finish_date,
        manga_data.age_rating.value,
        manga_data.status.value,
        manga_data.comic_type_id,
        manga_data.mal_id,
        manga_data.kitsu_id
    )
    return Mangas(**row)

# =======================================
# Funções de Atualização (Update)
# =======================================

async def update_manga(db: DatabaseProtocol, manga_id: UUID, updates: dict[str, Any]) -> Optional[Mangas]:
    """Atualiza um mangá existente"""
    if not updates:
        return await get_manga_by_id(db, manga_id)
    
    set_clauses = []
    values = []
    i = 1
    
    for field, value in updates.items():
        if field in ['age_rating', 'status'] and hasattr(value, 'value'):
            value = value.value
        set_clauses.append(f"{field} = ${i}")
        values.append(value)
        i += 1
    
    values.append(manga_id)
    
    query = f"""
        UPDATE mangas 
        SET {', '.join(set_clauses)}, updated_at = NOW()
        WHERE id = ${i}
        RETURNING id, country_id, user_id, title_english, title_native,
                  release_date, finish_date, age_rating, status, comic_type_id,
                  mal_id, kitsu_id, created_at, updated_at
    """
    
    row = await db.fetchrow(query, *values)
    return Mangas(**row) if row else None


async def update_manga_status(
    db: DatabaseProtocol, 
    manga_id: UUID, 
    status: EMangaStatus,
    finish_date: Optional[date] = None
) -> Optional[Mangas]:
    """Atualiza o status de um mangá"""
    query = """
        UPDATE mangas 
        SET status = $1, finish_date = $2, updated_at = NOW()
        WHERE id = $3
        RETURNING id, country_id, user_id, title_english, title_native,
                  release_date, finish_date, age_rating, status, comic_type_id,
                  mal_id, kitsu_id, created_at, updated_at
    """
    row = await db.fetchrow(query, status.value, finish_date, manga_id)
    return Mangas(**row) if row else None

# =======================================
# Funções de Exclusão (Delete)
# =======================================

async def delete_manga(db: DatabaseProtocol, manga_id: UUID) -> bool:
    """Exclui um mangá"""
    query = "DELETE FROM mangas WHERE id = $1"
    result = await db.execute(query, manga_id)
    return "DELETE" in result


async def soft_delete_manga(db: DatabaseProtocol, manga_id: UUID) -> bool:
    """Marca um mangá como excluído (soft delete)"""
    query = "UPDATE mangas SET is_deleted = TRUE, updated_at = NOW() WHERE id = $1"
    result = await db.execute(query, manga_id)
    return "UPDATE" in result

# =======================================
# Funções de Contagem e Estatísticas
# =======================================

async def count_mangas_by_status(db: DatabaseProtocol, status: EMangaStatus) -> int:
    """Conta mangás por status"""
    query = "SELECT COUNT(*) FROM mangas WHERE status = $1"
    return await db.fetchval(query, status.value)


async def count_all_mangas(db: DatabaseProtocol) -> int:
    """Conta todos os mangás"""
    query = "SELECT COUNT(*) FROM mangas"
    return await db.fetchval(query)


async def get_manga_stats(db: DatabaseProtocol) -> dict[str, int]:
    """Retorna estatísticas de mangás"""
    query = """
        SELECT 
            status,
            COUNT(*) as count
        FROM mangas 
        GROUP BY status
    """
    rows = await db.fetch(query)
    return {row['status']: row['count'] for row in rows}

# =======================================
# Funções de Validação
# =======================================

async def manga_title_exists(
    db: DatabaseProtocol, 
    title_english: str, 
    title_native: str,
) -> bool:
    """Verifica se um título de mangá já existe"""

    query = """
        SELECT EXISTS(
            SELECT 1 FROM mangas 
            WHERE title_english = $1 OR title_native = $2
        )
    """
    return await db.fetchval(query, title_english, title_native)


async def manga_external_id_exists(
    db: DatabaseProtocol, 
    mal_id: Optional[int] = None, 
    kitsu_id: Optional[int] = None
) -> bool:
    """Verifica se um ID externo já existe"""
    if mal_id and kitsu_id:
        query = """
            SELECT EXISTS(
                SELECT 1 FROM mangas 
                WHERE mal_id = $1 OR kitsu_id = $2
            )
        """
        return await db.fetchval(query, mal_id, kitsu_id)
    elif mal_id:
        query = "SELECT EXISTS(SELECT 1 FROM mangas WHERE mal_id = $1)"
        return await db.fetchval(query, mal_id)
    elif kitsu_id:
        query = "SELECT EXISTS(SELECT 1 FROM mangas WHERE kitsu_id = $1)"
        return await db.fetchval(query, kitsu_id)
    return False