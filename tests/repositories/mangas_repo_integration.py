import asyncio
import sys
from uuid import UUID, uuid4
from datetime import date, datetime
from app.load_env import get_database_dsn
from mugennocore.model.enums import EMangaStatus, EAgeRating
from mugennocore.model.mangas import Mangas
from mugennodb.conection.asyncpg_database import AsyncPGDatabase

# Importa as funções a serem testadas
from mugennodb.destroy import destroy_database_schema
from mugennodb.init import create_database_schema
from mugennodb.repositories.mangas_repo import (
    get_manga_by_id,
    get_manga_by_mal_id,
    get_manga_by_kitsu_id,
    get_mangas_by_title,
    get_mangas_by_status,
    get_mangas_by_author,
    get_recent_mangas,
    create_manga,
    create_manga_with_id,
    update_manga,
    update_manga_status,
    delete_manga,
    soft_delete_manga,
    count_mangas_by_status,
    count_all_mangas,
    get_manga_stats,
    manga_title_exists,
    manga_external_id_exists
)

async def setup_test_database():
    """Configura o banco real para os testes"""
    db = AsyncPGDatabase(dsn=get_database_dsn())
    await db.connect()
    
    # Limpa e recria o schema
    await destroy_database_schema(db)
    await create_database_schema(db)

    # IDs para os dados de teste
    country_id = 1
    comic_type_id = 1
    user_id = uuid4()
    manga_id = uuid4()
    
    # Insere dados de dependências primeiro
    await db.execute(
        "INSERT INTO countries (id, locale_code) VALUES ($1, $2)", 
        country_id, 'BR'
    )
    
    await db.execute(
        "INSERT INTO comic_types (id, name, description) VALUES ($1, $2, $3)",
        comic_type_id, 'Shonen', 'Manga for young boys'
    )
    
    await db.execute("""
        INSERT INTO users (id, country_id, username, email, password_hash, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    """, user_id, country_id, 'testuser', 'test@example.com', 
         'hashedpassword', datetime.now(), datetime.now())
    
    # Dados de teste para o mangá
    test_manga = Mangas(
        id=manga_id,
        country_id=country_id,
        user_id=user_id,
        title_english='Naruto Test Integration',
        title_native='ナルトテスト統合',
        release_date=date(1999, 9, 21),
        finish_date=date(2014, 11, 10),
        age_rating=EAgeRating.PG12,
        status=EMangaStatus.COMPLETED,
        comic_type_id=comic_type_id,
        mal_id=9999,
        kitsu_id=8888,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Insere o mangá de teste no banco
    m = await create_manga_with_id(db, test_manga)
    print(f"Mangas inserted with ID {m.id}")
    
    return db, manga_id, user_id, country_id, comic_type_id

async def cleanup_test_database(db):
    """Limpa os dados de teste"""
    try:
        await destroy_database_schema(db)
    except Exception as e:
        print(f"Erro ao limpar dados de teste: {e}")
    finally:
        await db.close()

async def test_get_manga_by_id(db, manga_id):
    """Testa busca de mangá por ID com banco real"""
    print("Testando get_manga_by_id...")
    
    # Act
    print(manga_id)
    result = await get_manga_by_id(db, manga_id)
    
    # Assert
    assert result is not None, "Mangá não encontrado por ID"
    assert result.id == manga_id, "ID do mangá não corresponde"
    assert result.title_english == 'Naruto Test Integration', "Título em inglês incorreto"
    assert result.title_native == 'ナルトテスト統合', "Título nativo incorreto"
    assert result.status == EMangaStatus.COMPLETED, "Status incorreto"
    assert result.age_rating == EAgeRating.PG12, "Classificação etária incorreta"
    assert result.mal_id == 9999, "MAL ID incorreto"
    assert result.kitsu_id == 8888, "Kitsu ID incorreto"
    assert isinstance(result.created_at, datetime), "created_at não é datetime"
    assert isinstance(result.updated_at, datetime), "updated_at não é datetime"
    
    print("✓ get_manga_by_id passou")

async def test_get_manga_by_id_not_found(db):
    """Testa busca de mangá por ID inexistente"""
    print("Testando get_manga_by_id_not_found...")
    
    # Act
    result = await get_manga_by_id(db, uuid4())
    
    # Assert
    assert result is None, "Mangá inexistente foi encontrado"
    
    print("✓ get_manga_by_id_not_found passou")

async def test_get_manga_by_mal_id(db):
    """Testa busca de mangá por MAL ID com banco real"""
    print("Testando get_manga_by_mal_id...")
    
    # Act
    result = await get_manga_by_mal_id(db, 9999)
    
    # Assert
    assert result is not None, "Mangá não encontrado por MAL ID"
    assert result.mal_id == 9999, "MAL ID incorreto"
    assert result.title_english == 'Naruto Test Integration', "Título em inglês incorreto"
    
    print("✓ get_manga_by_mal_id passou")

async def test_get_manga_by_mal_id_not_found(db):
    """Testa busca de mangá por MAL ID inexistente"""
    print("Testando get_manga_by_mal_id_not_found...")
    
    # Act
    result = await get_manga_by_mal_id(db, 0)
    
    # Assert
    assert result is None, "Mangá com MAL ID inexistente foi encontrado"
    
    print("✓ get_manga_by_mal_id_not_found passou")

async def test_get_manga_by_kitsu_id(db):
    """Testa busca de mangá por Kitsu ID com banco real"""
    print("Testando get_manga_by_kitsu_id...")
    
    # Act
    result = await get_manga_by_kitsu_id(db, 8888)
    
    # Assert
    assert result is not None, "Mangá não encontrado por Kitsu ID"
    assert result.kitsu_id == 8888, "Kitsu ID incorreto"
    assert result.title_english == 'Naruto Test Integration', "Título em inglês incorreto"
    
    print("✓ get_manga_by_kitsu_id passou")

async def test_get_manga_by_kitsu_id_not_found(db):
    """Testa busca de mangá por Kitsu ID inexistente"""
    print("Testando get_manga_by_kitsu_id_not_found...")
    
    # Act
    result = await get_manga_by_kitsu_id(db, 0)
    
    # Assert
    assert result is None, "Mangá com Kitsu ID inexistente foi encontrado"
    
    print("✓ get_manga_by_kitsu_id_not_found passou")

async def test_get_mangas_by_title(db):
    """Testa busca de mangás por título com banco real"""
    print("Testando get_mangas_by_title...")
    
    # Act
    results = await get_mangas_by_title(db, 'Naruto', limit=10, offset=0)
    
    # Assert
    assert len(results) >= 1, "Nenhum mangá encontrado pelo título"
    
    naruto_found = any(m.title_english == 'Naruto Test Integration' for m in results)
    assert naruto_found, "Mangá de teste não encontrado na busca por título"
    
    for manga in results:
        assert isinstance(manga, Mangas), "Objeto retornado não é do tipo Mangas"
        assert isinstance(manga.id, UUID), "ID não é do tipo UUID"
        assert isinstance(manga.title_english, str), "Título em inglês não é string"
        assert isinstance(manga.status, EMangaStatus), "Status não é do tipo EMangaStatus"
    
    print("✓ get_mangas_by_title passou")

async def test_get_mangas_by_title_empty_result(db):
    """Testa busca de mangás por título inexistente"""
    print("Testando get_mangas_by_title_empty_result...")
    
    # Act
    results = await get_mangas_by_title(db, 'NonExistentManga', limit=10, offset=0)
    
    # Assert
    assert len(results) == 0, "Mangás encontrados para título inexistente"
    
    print("✓ get_mangas_by_title_empty_result passou")

async def test_get_mangas_by_status(db, manga_id):
    """Testa busca de mangás por status com banco real"""
    print("Testando get_mangas_by_status...")
    
    # Act
    results = await get_mangas_by_status(db, EMangaStatus.COMPLETED, limit=10, offset=0)
    
    # Assert
    assert len(results) >= 1, "Nenhum mangá encontrado pelo status"
    
    completed_manga_found = any(
        m.status == EMangaStatus.COMPLETED and m.id == manga_id 
        for m in results
    )
    assert completed_manga_found, "Mangá de teste não encontrado na busca por status"
    
    for manga in results:
        assert manga.status == EMangaStatus.COMPLETED, "Status do mangá não corresponde ao filtro"
    
    print("✓ get_mangas_by_status passou")

async def test_get_mangas_by_status_pagination(db, country_id, user_id, comic_type_id):
    """Testa paginação na busca por status"""
    print("Testando get_mangas_by_status_pagination...")
    
    # Cria mais mangás para testar paginação
    extra_mangas = []
    for i in range(3):
        extra_manga = Mangas(
            country_id=country_id,
            user_id=user_id,
            title_english=f'Extra Manga {i}',
            title_native=f'エクストラマンガ{i}',
            release_date=date(2020, 1, 1),
            age_rating=EAgeRating.G,
            status=EMangaStatus.COMPLETED,
            comic_type_id=comic_type_id
        )
        created = await create_manga(db, extra_manga)
        extra_mangas.append(created)
    
    try:
        # Act - primeira página
        page1 = await get_mangas_by_status(db, EMangaStatus.COMPLETED, limit=2, offset=0)
        
        # Act - segunda página
        page2 = await get_mangas_by_status(db, EMangaStatus.COMPLETED, limit=2, offset=2)
        
        # Assert
        assert len(page1) == 2, "Tamanho da primeira página incorreto"
        assert len(page2) >= 1, "Segunda página vazia"
        
        # Verifica que não há sobreposição
        page1_ids = {m.id for m in page1}
        page2_ids = {m.id for m in page2}
        assert len(page1_ids.intersection(page2_ids)) == 0, "Sobreposição entre páginas"
    
    finally:
        # Cleanup
        for manga in extra_mangas:
            await delete_manga(db, manga.id)
    
    print("✓ get_mangas_by_status_pagination passou")

async def test_get_recent_mangas(db):
    """Testa busca de mangás recentes com banco real"""
    print("Testando get_recent_mangas...")
    
    # Act
    results = await get_recent_mangas(db, limit=5, offset=0)
    
    # Assert
    assert len(results) >= 1, "Nenhum mangá recente encontrado"
    
    # Verifica que estão ordenados por data decrescente
    dates = [m.created_at for m in results]
    assert dates == sorted(dates, reverse=True), "Mangás não estão ordenados por data decrescente"
    
    print("✓ get_recent_mangas passou")

async def test_create_manga(db, country_id, user_id, comic_type_id):
    """Testa criação de novo mangá com banco real"""
    print("Testando create_manga...")
    
    # Arrange
    new_manga_data = Mangas(
        country_id=country_id,
        user_id=user_id,
        title_english='One Piece Test Integration',
        title_native='ワンピーステスト統合',
        synopsis='Test story about pirates for integration testing',
        release_date=date(1997, 7, 22),
        finish_date=None,
        age_rating=EAgeRating.PG12,
        status=EMangaStatus.ONGOING,
        comic_type_id=comic_type_id,
        mal_id=7777,
        kitsu_id=6666
    )
    
    # Act
    created_manga = await create_manga(db, new_manga_data)
    
    try:
        # Assert
        assert created_manga is not None, "Mangá não foi criado"
        assert isinstance(created_manga.id, UUID), "ID não é do tipo UUID"
        assert created_manga.title_english == 'One Piece Test Integration', "Título em inglês incorreto"
        assert created_manga.status == EMangaStatus.ONGOING, "Status incorreto"
        assert created_manga.mal_id == 7777, "MAL ID incorreto"
        assert isinstance(created_manga.created_at, datetime), "created_at não é datetime"
        assert isinstance(created_manga.updated_at, datetime), "updated_at não é datetime"
        
        # Verifica que foi realmente salvo no banco
        retrieved = await get_manga_by_id(db, created_manga.id)
        assert retrieved is not None, "Mangá criado não encontrado no banco"
        assert retrieved.title_english == 'One Piece Test Integration', "Título do mangá recuperado incorreto"
    
    finally:
        # Cleanup
        await delete_manga(db, created_manga.id)
    
    print("✓ create_manga passou")

async def test_create_manga_with_id(db, country_id, user_id, comic_type_id):
    """Testa criação de mangá com ID específico"""
    print("Testando create_manga_with_id...")
    
    # Arrange
    specific_id = uuid4()
    new_manga_data = Mangas(
        id=specific_id,
        country_id=country_id,
        user_id=user_id,
        title_english='Manga With Specific ID',
        title_native='特定IDマンガ',
        synopsis='Manga created with specific ID',
        release_date=date(2020, 1, 1),
        age_rating=EAgeRating.G,
        status=EMangaStatus.ONGOING,
        comic_type_id=comic_type_id
    )
    
    # Act
    created_manga = await create_manga_with_id(db, new_manga_data)
    
    try:
        # Assert
        assert created_manga is not None, "Mangá não foi criado"
        assert created_manga.id == specific_id, "ID não corresponde ao especificado"
        assert created_manga.title_english == 'Manga With Specific ID', "Título em inglês incorreto"
    
    finally:
        # Cleanup
        await delete_manga(db, specific_id)
    
    print("✓ create_manga_with_id passou")

async def test_update_manga(db, manga_id):
    """Testa atualização de mangá com banco real"""
    print("Testando update_manga...")
    
    # Arrange
    original_manga = await get_manga_by_id(db, manga_id)
    original_updated_at = original_manga.updated_at
    updates = {
        'title_english': 'Naruto Updated Integration',
        'status': EMangaStatus.HIATUS,
        'mal_id': 1111
    }
    
    # Act
    updated_manga = await update_manga(db, manga_id, updates)
    
    # Assert
    assert updated_manga is not None, "Mangá não foi atualizado"
    assert updated_manga.title_english == 'Naruto Updated Integration', "Título atualizado incorreto"
    assert updated_manga.status == EMangaStatus.HIATUS, "Status atualizado incorreto"
    assert updated_manga.mal_id == 1111, "MAL ID atualizado incorreto"
    assert updated_manga.updated_at > original_updated_at, "updated_at não foi atualizado"
    
    # Verifica que as mudanças persistiram
    retrieved = await get_manga_by_id(db, manga_id)
    assert retrieved.title_english == 'Naruto Updated Integration', "Título persistido incorreto"
    assert retrieved.status == EMangaStatus.HIATUS, "Status persistido incorreto"
    
    print("✓ update_manga passou")

async def test_update_manga_status(db, manga_id):
    """Testa atualização de status do mangá com banco real"""
    print("Testando update_manga_status...")
    
    # Arrange
    original_manga = await get_manga_by_id(db, manga_id)
    original_updated_at = original_manga.updated_at
    
    # Act
    updated_manga = await update_manga_status(
        db, manga_id, EMangaStatus.ONGOING, None
    )
    
    # Assert
    assert updated_manga is not None, "Status do mangá não foi atualizado"
    assert updated_manga.status == EMangaStatus.ONGOING, "Status atualizado incorreto"
    assert updated_manga.finish_date is None, "finish_date não é None"
    assert updated_manga.updated_at > original_updated_at, "updated_at não foi atualizado"
    
    print("✓ update_manga_status passou")

async def test_soft_delete_manga(db, country_id, user_id, comic_type_id):
    """Testa soft delete de mangá"""
    print("Testando soft_delete_manga...")
    
    # Arrange - cria um mangá temporário
    temp_manga = Mangas(
        country_id=country_id,
        user_id=user_id,
        title_english='Temp Manga for Soft Delete',
        title_native='ソフトデリートテンプマンガ',
        synopsis='Temporary manga for soft deletion test',
        release_date=date(2020, 1, 1),
        age_rating=EAgeRating.G,
        status=EMangaStatus.ONGOING,
        comic_type_id=comic_type_id
    )
    created_manga = await create_manga(db, temp_manga)
    
    # Act
    soft_deleted = await soft_delete_manga(db, created_manga.id)
    
    # Assert
    assert soft_deleted is not None, "Soft delete falhou"
    assert soft_deleted.deleted_at is not None, "deleted_at não foi preenchido"
    
    # Cleanup
    await delete_manga(db, created_manga.id)
    
    print("✓ soft_delete_manga passou")

async def test_delete_manga(db, country_id, user_id, comic_type_id):
    """Testa exclusão permanente de mangá com banco real"""
    print("Testando delete_manga...")
    
    # Arrange - cria um mangá temporário para deletar
    temp_manga = Mangas(
        country_id=country_id,
        user_id=user_id,
        title_english='Temp Manga for Delete',
        title_native='デリートテンプマンガ',
        synopsis='Temporary manga for deletion test',
        release_date=date(2020, 1, 1),
        age_rating=EAgeRating.G,
        status=EMangaStatus.ONGOING,
        comic_type_id=comic_type_id
    )
    created_manga = await create_manga(db, temp_manga)
    
    # Act
    delete_result = await delete_manga(db, created_manga.id)
    
    # Assert
    assert delete_result, "Exclusão falhou"
    
    # Verifica que realmente foi deletado
    deleted_manga = await get_manga_by_id(db, created_manga.id)
    assert deleted_manga is None, "Mangá ainda existe após exclusão"
    
    print("✓ delete_manga passou")

async def test_count_mangas_by_status(db):
    """Testa contagem de mangás por status com banco real"""
    print("Testando count_mangas_by_status...")
    
    # Act
    count = await count_mangas_by_status(db, EMangaStatus.COMPLETED)
    
    # Assert
    assert isinstance(count, int), "Contagem não é inteiro"
    assert count >= 1, "Contagem menor que o esperado"
    
    print("✓ count_mangas_by_status passou")

async def test_count_all_mangas(db):
    """Testa contagem total de mangás com banco real"""
    print("Testando count_all_mangas...")
    
    # Act
    count = await count_all_mangas(db)
    
    # Assert
    assert isinstance(count, int), "Contagem total não é inteiro"
    assert count >= 1, "Contagem total menor que o esperado"
    
    print("✓ count_all_mangas passou")

async def test_get_manga_stats(db):
    """Testa obtenção de estatísticas de mangás"""
    print("Testando get_manga_stats...")
    
    # Act
    stats = await get_manga_stats(db)
    
    # Assert
    assert stats is not None, "Estatísticas não retornadas"
    assert isinstance(stats, dict), "Estatísticas não são um dicionário"
    
    print("✓ get_manga_stats passou")

async def test_manga_title_exists(db):
    """Testa verificação de título existente com banco real"""
    print("Testando manga_title_exists...")
    
    # Act - testa com título que existe
    exists = await manga_title_exists(db, 'Naruto Test Integration', 'ナルトテスト統合')
    
    # Act - testa com título que não existe
    not_exists = await manga_title_exists(db, 'NonExistentTitle', 'ノンエグジステントタイトル')
    
    # Assert
    assert exists, "Título existente não foi encontrado"
    assert not not_exists, "Título inexistente foi encontrado"

    print("✓ manga_title_exists passou")

async def test_manga_external_id_exists(db, manga_id):
    """Testa verificação de IDs externos existentes com banco real"""
    print("Testando manga_external_id_exists...")
    
    # Act
    mal_exists = await manga_external_id_exists(db, mal_id=9999)
    kitsu_exists = await manga_external_id_exists(db, kitsu_id=8888)
    mal_not_exists = await manga_external_id_exists(db, mal_id=0)
    kitsu_not_exists = await manga_external_id_exists(db, kitsu_id=0)
    
    # Act - testando exclusão de ID próprio
    mal_exists_excluding_self = await manga_external_id_exists(
        db, mal_id=9999, exclude_id=manga_id
    )
    
    # Assert
    assert mal_exists, "MAL ID existente não foi encontrado"
    assert kitsu_exists, "Kitsu ID existente não foi encontrado"
    assert not mal_not_exists, "MAL ID inexistente foi encontrado"
    assert not kitsu_not_exists, "Kitsu ID inexistente foi encontrado"
    assert not mal_exists_excluding_self, "MAL ID foi encontrado mesmo excluindo o próprio ID"
    
    print("✓ manga_external_id_exists passou")

async def test_get_mangas_by_author(db):
    """Testa busca de mangás por autor"""
    print("Testando get_mangas_by_author...")
    
    # Act
    results = await get_mangas_by_author(db, "TestAuthor", limit=10, offset=0)
    
    # Assert
    assert isinstance(results, list), "Resultado não é uma lista"
    
    print("✓ get_mangas_by_author passou")

async def run_all_tests():
    """Executa todos os testes"""
    print("Iniciando testes de integração do repositório de mangás...")
    # Setup
    db, manga_id, user_id, country_id, comic_type_id = await setup_test_database()
        
    
    try:
      
        # Executa todos os testes
        await test_get_manga_by_id(db, manga_id)
        await test_get_manga_by_id_not_found(db)
        await test_get_manga_by_mal_id(db)
        await test_get_manga_by_mal_id_not_found(db)
        await test_get_manga_by_kitsu_id(db)
        await test_get_manga_by_kitsu_id_not_found(db)
        await test_get_mangas_by_title(db)
        await test_get_mangas_by_title_empty_result(db)
        await test_get_mangas_by_status(db, manga_id)
        await test_get_mangas_by_status_pagination(db, country_id, user_id, comic_type_id)
        await test_get_recent_mangas(db)
        await test_create_manga(db, country_id, user_id, comic_type_id)
        await test_create_manga_with_id(db, country_id, user_id, comic_type_id)
        await test_update_manga(db, manga_id)
        await test_update_manga_status(db, manga_id)
        await test_soft_delete_manga(db, country_id, user_id, comic_type_id)
        await test_delete_manga(db, country_id, user_id, comic_type_id)
        await test_count_mangas_by_status(db)
        await test_count_all_mangas(db)
        await test_get_manga_stats(db)
        await test_manga_title_exists(db)
        await test_manga_external_id_exists(db, manga_id)
        await test_get_mangas_by_author(db)
        
        print("\n✅ Todos os testes passaram com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    #finally:
        # Cleanup
        #await cleanup_test_database(db)
    
    return True

if __name__ == '__main__':
    # Configuração para executar testes assíncronos
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Executa os testes
    success = asyncio.run(run_all_tests())
    
    # Retorna código de saída apropriado
    sys.exit(0 if success else 1)