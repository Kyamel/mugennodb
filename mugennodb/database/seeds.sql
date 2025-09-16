-- seeds.sql
-- Insere dados de dependências para testes

-- Insere país
INSERT INTO countries (id, locale_code, created_at, updated_at) 
VALUES (1, 'BR', NOW(), NOW());

-- Insere tipo de quadrinho
INSERT INTO comic_types (id, name, description, created_at, updated_at) 
VALUES (1, 'Shonen', 'Manga for young boys', NOW(), NOW());

-- Insere usuário com UUID fixo (convertendo 1 para UUID)
INSERT INTO users (id, country_id, username, email, password_hash, created_at, updated_at)
VALUES (
    '00000000-0000-0000-0000-000000000001', 
    1, 
    'testuser', 
    'test@example.com', 
    'hashedpassword', 
    NOW(), 
    NOW()
);

-- Insere mangá de teste com UUID fixo
INSERT INTO mangas (
    id, 
    country_id, 
    user_id, 
    title_english, 
    title_native, 
    release_date, 
    finish_date, 
    age_rating, 
    status, 
    comic_type_id, 
    mal_id, 
    kitsu_id, 
    created_at, 
    updated_at
) VALUES (
    '00000000-0000-0000-0000-000000000001',
    1,
    '00000000-0000-0000-0000-000000000001',
    'Naruto Test Integration',
    'ナルトテスト統合',
    '1999-09-21',
    '2014-11-10',
    'PG12',
    'COMPLETED',
    1,
    9999,
    8888,
    NOW(),
    NOW()
);

-- Insere mais alguns dados de exemplo
INSERT INTO users (id, country_id, username, email, password_hash, created_at, updated_at)
VALUES (
    '00000000-0000-0000-0000-000000000002', 
    1, 
    'anotheruser', 
    'another@example.com', 
    'hashedpassword2', 
    NOW(), 
    NOW()
);

INSERT INTO mangas (
    id, 
    country_id, 
    user_id, 
    title_english, 
    title_native, 
    release_date, 
    finish_date, 
    age_rating, 
    status, 
    comic_type_id, 
    mal_id, 
    kitsu_id, 
    created_at, 
    updated_at
) VALUES (
    '00000000-0000-0000-0000-000000000002',
    1,
    '00000000-0000-0000-0000-000000000002',
    'One Piece Test',
    'ワンピーステスト',
    '1997-07-22',
    NULL,
    'PG12',
    'ONGOING',
    1,
    7777,
    6666,
    NOW(),
    NOW()
);