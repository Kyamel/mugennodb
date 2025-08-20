-- Habilitar a extensão para UUIDs aleatórios
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Limpar tabelas para evitar conflitos (opcional - use com cuidado em produção)
TRUNCATE TABLE manga_reviews, chapter_reviews, page_reviews, review, read, related_mangas, manga_genres, pages, chapters, mangas, users, tags, countries RESTART IDENTITY CASCADE;

-- Inserir países
INSERT INTO countries (lang, locale_code) VALUES
('en', 'en-US'),
('pt', 'pt-BR'),
('es', 'es-ES'),
('ja', 'ja-JP'),
('fr', 'fr-FR'),
('de', 'de-DE'),
('it', 'it-IT'),
('ru', 'ru-RU'),
('zh', 'zh-CN'),
('ko', 'ko-KR')
ON CONFLICT (locale_code) DO NOTHING;

-- Verificar os IDs dos países inseridos
SELECT id, lang, locale_code FROM countries;

-- Inserir tags (gêneros e categorias)
INSERT INTO tags (tag_name, tag_type) VALUES
-- Gêneros
('Action', 'genre'),
('Adventure', 'genre'),
('Comedy', 'genre'),
('Drama', 'genre'),
('Fantasy', 'genre'),
('Horror', 'genre'),
('Mystery', 'genre'),
('Romance', 'genre'),
('Sci-Fi', 'genre'),
('Slice of Life', 'genre'),
('Sports', 'genre'),
('Supernatural', 'genre'),
('Psychological', 'genre'),
('Thriller', 'genre'),
('Isekai', 'genre'),
('Mecha', 'genre'),
('Harem', 'genre'),
('Shounen', 'genre'),
('Shoujo', 'genre'),
('Seinen', 'genre'),
('Josei', 'genre'),
('Ecchi', 'genre'),
('Yaoi', 'genre'),
('Yuri', 'genre'),
('Gore', 'genre'),
('Tragedy', 'genre'),
('Historical', 'genre'),
('Military', 'genre'),
('Police', 'genre'),
('Martial Arts', 'genre'),
('School', 'genre'),
('Music', 'genre'),
('Cooking', 'genre'),
('Game', 'genre'),
('Demons', 'genre'),
('Magic', 'genre'),
('Vampire', 'genre'),
('Monster', 'genre'),
('Zombie', 'genre'),
('Space', 'genre'),
('Cyberpunk', 'genre')
ON CONFLICT (tag_name) DO NOTHING;

-- Inserir mangás populares (usando country_id correto para Japão)
-- Assumindo que o Japão tem id = 4 (ja-JP)
INSERT INTO mangas (country_id, title_english, title_native, release_date, finish_date, active_status, comic_type, cover, mal_id) VALUES
(4, 'One Piece', 'ワンピース', '1997-07-22', NULL, 'ongoing', 'manga', gen_random_uuid(), 13),
(4, 'Naruto', 'NARUTO -ナルト-', '1999-09-21', '2014-11-10', 'completed', 'manga', gen_random_uuid(), 11),
(4, 'Attack on Titan', '進撃の巨人', '2009-09-09', '2021-04-09', 'completed', 'manga', gen_random_uuid(), 23390),
(4, 'Demon Slayer', '鬼滅の刃', '2016-02-15', '2020-05-18', 'completed', 'manga', gen_random_uuid(), 38000),
(4, 'My Hero Academia', '僕のヒーローアカデミア', '2014-07-07', NULL, 'ongoing', 'manga', gen_random_uuid(), 75989),
(4, 'Berserk', 'ベルセルク', '1989-08-25', NULL, 'ongoing', 'manga', gen_random_uuid(), 2),
(4, 'Tokyo Ghoul', '東京喰種', '2011-09-08', '2018-07-05', 'completed', 'manga', gen_random_uuid(), 33327),
(4, 'Death Note', 'DEATH NOTE', '2003-12-01', '2006-05-15', 'completed', 'manga', gen_random_uuid(), 21),
(4, 'Fullmetal Alchemist', '鋼の錬金術師', '2001-07-12', '2010-07-11', 'completed', 'manga', gen_random_uuid(), 25),
(4, 'Dragon Ball', 'ドラゴンボール', '1984-11-20', '1995-05-23', 'completed', 'manga', gen_random_uuid(), 42),
(4, 'One Punch Man', 'ワンパンマン', '2012-06-14', NULL, 'ongoing', 'manga', gen_random_uuid(), 44347),
(4, 'Hunter x Hunter', 'HUNTER×HUNTER', '1998-03-03', NULL, 'hiatus', 'manga', gen_random_uuid(), 1),
(4, 'Bleach', 'BLEACH', '2001-08-07', '2016-08-22', 'completed', 'manga', gen_random_uuid(), 3),
(4, 'JoJo''s Bizarre Adventure', 'ジョジョの奇妙な冒険', '1987-01-01', NULL, 'ongoing', 'manga', gen_random_uuid(), 7),
(4, 'Vinland Saga', 'ヴィンランド・サガ', '2005-04-13', NULL, 'ongoing', 'manga', gen_random_uuid(), 642),
(4, 'Chainsaw Man', 'チェンソーマン', '2018-12-03', NULL, 'ongoing', 'manga', gen_random_uuid(), 116778),
(4, 'Jujutsu Kaisen', '呪術廻戦', '2018-03-05', NULL, 'ongoing', 'manga', gen_random_uuid(), 113138),
(4, 'Spy x Family', 'SPY×FAMILY', '2019-03-25', NULL, 'ongoing', 'manga', gen_random_uuid(), 120089),
(4, 'Oshi no Ko', '【推しの子】', '2020-04-23', NULL, 'ongoing', 'manga', gen_random_uuid(), 131585),
(4, 'Kingdom', 'キングダム', '2006-01-26', NULL, 'ongoing', 'manga', gen_random_uuid(), 16765);

-- Inserir usuários (usando country_ids existentes)
INSERT INTO users (country_id, user_name, user_password, user_role, join_date, email, is_banned, nickname, user_profile, user_banner, is_active, allow_nsfw, allow_dm) VALUES
(1, 'john_doe', 'hashed_password_123', 'user', '2023-01-15 10:30:00', 'john.doe@email.com', FALSE, 'JohnD', gen_random_uuid(), gen_random_uuid(), TRUE, TRUE, TRUE),
(2, 'maria_silva', 'hashed_password_456', 'user', '2023-02-20 14:25:00', 'maria.silva@email.com', FALSE, 'Mary', gen_random_uuid(), gen_random_uuid(), TRUE, FALSE, TRUE),
(1, 'admin_user', 'admin_hashed_pass', 'admin', '2022-12-01 09:00:00', 'admin@manga.com', FALSE, 'Admin', gen_random_uuid(), gen_random_uuid(), TRUE, TRUE, FALSE),
(3, 'carlos_ruiz', 'hashed_password_789', 'moderator', '2023-03-10 16:45:00', 'carlos.ruiz@email.com', FALSE, 'CarlosR', gen_random_uuid(), gen_random_uuid(), TRUE, TRUE, TRUE),
(4, 'takahashi_san', 'hashed_password_012', 'user', '2023-04-05 11:20:00', 'takahashi@email.jp', FALSE, 'Taka', gen_random_uuid(), gen_random_uuid(), TRUE, FALSE, FALSE),
(1, 'sarah_connor', 'hashed_password_345', 'user', '2023-01-28 08:15:00', 'sarah.connor@email.com', TRUE, 'SarahC', gen_random_uuid(), gen_random_uuid(), FALSE, TRUE, TRUE),
(2, 'pedro_alves', 'hashed_password_678', 'user', '2023-05-12 13:30:00', 'pedro.alves@email.com', FALSE, 'PedroA', gen_random_uuid(), gen_random_uuid(), TRUE, TRUE, FALSE),
(1, 'emma_watson', 'hashed_password_901', 'user', '2023-06-18 15:40:00', 'emma.watson@email.com', FALSE, 'EmmaW', gen_random_uuid(), gen_random_uuid(), TRUE, FALSE, TRUE),
(5, 'pierre_dupont', 'hashed_password_234', 'user', '2023-03-22 12:10:00', 'pierre.dupont@email.fr', FALSE, 'PierreD', gen_random_uuid(), gen_random_uuid(), TRUE, TRUE, FALSE),
(1, 'mike_jones', 'hashed_password_567', 'user', '2023-07-01 17:55:00', 'mike.jones@email.com', FALSE, 'MikeJ', gen_random_uuid(), gen_random_uuid(), TRUE, TRUE, TRUE);

-- Inserir capítulos para alguns mangás
-- Capítulos para One Piece
INSERT INTO chapters (country_id, manga_id, title, cover, ch_number) VALUES
(4, 1, 'Romance Dawn', gen_random_uuid(), 1),
(4, 1, 'They Call Him "Straw Hat Luffy"', gen_random_uuid(), 2),
(4, 1, 'Enter Zoro, the Pirate Hunter', gen_random_uuid(), 3),
(4, 1, 'The Great Captain Morgan', gen_random_uuid(), 4),
(4, 1, 'The King of the Pirates and the Master Swordsman', gen_random_uuid(), 5);

-- Capítulos para Attack on Titan
INSERT INTO chapters (country_id, manga_id, title, cover, ch_number) VALUES
(4, 3, 'To You, 2,000 Years From Now', gen_random_uuid(), 1),
(4, 3, 'That Day', gen_random_uuid(), 2),
(4, 3, 'Night of the Disbanding Ceremony', gen_random_uuid(), 3),
(4, 3, 'First Battle', gen_random_uuid(), 4),
(4, 3, 'A Dull Glow in the Midst of Despair', gen_random_uuid(), 5);

-- Capítulos para Demon Slayer
INSERT INTO chapters (country_id, manga_id, title, cover, ch_number) VALUES
(4, 4, 'Cruelty', gen_random_uuid(), 1),
(4, 4, 'Trainer Sakonji Urokodaki', gen_random_uuid(), 2),
(4, 4, 'Sabito and Makomo', gen_random_uuid(), 3),
(4, 4, 'Final Selection', gen_random_uuid(), 4),
(4, 4, 'My Own Steel', gen_random_uuid(), 5);

-- Inserir páginas para os capítulos
-- Páginas para o primeiro capítulo de One Piece
INSERT INTO pages (chapter_id, pg_number, source) VALUES
(1, 1, gen_random_uuid()),
(1, 2, gen_random_uuid()),
(1, 3, gen_random_uuid()),
(1, 4, gen_random_uuid()),
(1, 5, gen_random_uuid());

-- Páginas para o primeiro capítulo de Attack on Titan
INSERT INTO pages (chapter_id, pg_number, source) VALUES
(6, 1, gen_random_uuid()),
(6, 2, gen_random_uuid()),
(6, 3, gen_random_uuid()),
(6, 4, gen_random_uuid()),
(6, 5, gen_random_uuid());

-- Associar tags aos mangás (manga_genres)
INSERT INTO manga_genres (manga_id, tag_id) VALUES
-- One Piece
(1, 1), (1, 2), (1, 5), (1, 18),
-- Naruto
(2, 1), (2, 2), (2, 18), (2, 30),
-- Attack on Titan
(3, 1), (3, 5), (3, 7), (3, 12), (3, 25),
-- Demon Slayer
(4, 1), (4, 5), (4, 12), (4, 18),
-- My Hero Academia
(5, 1), (5, 18), (5, 30),
-- Berserk
(6, 1), (6, 5), (6, 13), (6, 24), (6, 25),
-- Tokyo Ghoul
(7, 5), (7, 7), (7, 13), (7, 24),
-- Death Note
(8, 7), (8, 13), (8, 14),
-- Fullmetal Alchemist
(9, 1), (9, 2), (9, 5), (9, 18),
-- Dragon Ball
(10, 1), (10, 2), (10, 3), (10, 18);

-- Inserir relacionamentos entre mangás
INSERT INTO related_mangas (source_manga_id, related_manga_id, relationship_type) VALUES
(2, 10, 'same_author'), -- Naruto e Boruto (mesmo autor)
(1, 13, 'similar_genre'), -- One Piece e Bleach (shounen similar)
(3, 7, 'similar_theme'), -- Attack on Titan e Tokyo Ghoul (dark fantasy)
(4, 17, 'same_magazine'), -- Demon Slayer e Jujutsu Kaisen (Jump)
(5, 16, 'same_magazine'), -- My Hero Academia e Chainsaw Man (Jump)
(8, 9, 'recommendation'), -- Death Note e Fullmetal Alchemist (recomendação)
(11, 12, 'same_author'), -- One Punch Man e Mob Psycho 100 (mesmo autor)
(14, 15, 'similar_style'); -- JoJo e Golden Kamuy

-- Inserir leituras de usuários
INSERT INTO read (user_id, manga_id, status) VALUES
(1, 1, 'reading'),
(1, 3, 'completed'),
(1, 8, 'plan_to_read'),
(2, 4, 'completed'),
(2, 5, 'reading'),
(2, 11, 'dropped'),
(3, 1, 'reading'),
(3, 2, 'completed'),
(3, 3, 'completed'),
(4, 6, 'reading'),
(4, 9, 'completed'),
(5, 7, 'reading'),
(5, 10, 'completed');

-- Inserir reviews
INSERT INTO review (users_id, score, content) VALUES
(1, 9.5, 'One Piece is a masterpiece of storytelling and world-building. Oda''s creativity knows no bounds!'),
(1, 8.8, 'Attack on Titan has one of the most complex and well-written plots in manga history.'),
(2, 9.2, 'Demon Slayer has amazing art and emotional depth. The character development is exceptional.'),
(3, 9.7, 'Berserk is dark, brutal, and beautiful. The art is unparalleled in the manga industry.'),
(4, 8.5, 'Fullmetal Alchemist balances action, humor, and philosophy perfectly. A complete story.'),
(5, 7.9, 'Tokyo Ghoul starts strong but loses some momentum in later parts. Still worth reading.');

-- Associar reviews a mangás
INSERT INTO manga_reviews (manga_id, review_id) VALUES
(1, 1),
(3, 2),
(4, 3),
(6, 4),
(9, 5),
(7, 6);

-- Inserir reviews de capítulos
INSERT INTO review (users_id, score, content) VALUES
(2, 10.0, 'The final chapter of Attack on Titan was absolutely mind-blowing!'),
(3, 9.5, 'Chapter 1043 of One Piece changed everything we thought we knew!'),
(1, 8.0, 'Good setup chapter for the upcoming arc');

INSERT INTO chapter_reviews (review_id, chapter_id) VALUES
(7, 6), -- Review para capítulo 1 de Attack on Titan
(8, 1), -- Review para capítulo 1 de One Piece
(9, 2); -- Review para capítulo 2 de One Piece

-- Inserir reviews de páginas
INSERT INTO review (users_id, score, content) VALUES
(4, 10.0, 'The double-page spread in this page is absolutely breathtaking!'),
(5, 9.0, 'Amazing artwork and composition in this page');

INSERT INTO page_reviews (page_id, review_id) VALUES
(1, 10), -- Review para página 1 do capítulo 1 de One Piece
(6, 11); -- Review para página 1 do capítulo 1 de Attack on Titan

-- Atualizar algumas datas de updated_at para serem diferentes de created_at
UPDATE users SET updated_at = '2023-08-01 10:00:00' WHERE id = 1;
UPDATE mangas SET updated_at = '2023-07-15 14:30:00' WHERE id = 1;
UPDATE chapters SET updated_at = '2023-07-20 16:45:00' WHERE id = 1;
UPDATE read SET updated_at = '2023-08-05 09:15:00' WHERE user_id = 1 AND manga_id = 1;

-- Mostrar estatísticas da inserção
SELECT 
    (SELECT COUNT(*) FROM countries) as total_countries,
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM mangas) as total_mangas,
    (SELECT COUNT(*) FROM chapters) as total_chapters,
    (SELECT COUNT(*) FROM pages) as total_pages,
    (SELECT COUNT(*) FROM tags) as total_tags,
    (SELECT COUNT(*) FROM manga_genres) as total_genre_relations,
    (SELECT COUNT(*) FROM related_mangas) as total_related_mangas,
    (SELECT COUNT(*) FROM read) as total_read_statuses,
    (SELECT COUNT(*) FROM review) as total_reviews;