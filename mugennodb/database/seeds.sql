-- Script de população do banco de dados de mangás
-- Inserindo dados de exemplo que imitam dados reais

-- 1. Primeiro, inserir países
INSERT INTO countries (lang, locale_code) VALUES
('English', 'en-US'),
('Japanese', 'ja-JP'),
('Portuguese', 'pt-BR'),
('Spanish', 'es-ES'),
('French', 'fr-FR'),
('Korean', 'ko-KR'),
('Chinese', 'zh-CN');

-- 2. Inserir tags (gêneros e categorias)
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
('Martial Arts', 'genre'),
('Historical', 'genre'),
('Military', 'genre'),
('Music', 'genre'),
('School', 'genre'),
('Superhero', 'genre');

-- 3. Inserir usuários de exemplo
INSERT INTO users (country_id, user_name, user_password, user_role, join_date, email, is_banned, nickname, user_profile, user_banner, is_active, allow_nsfw, allow_dm) VALUES
(1, 'john_doe', 'hashed_password_1', 'user', '2022-01-15 10:30:00', 'john@example.com', FALSE, 'JohnTheReader', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', TRUE, TRUE, TRUE),
(2, 'sakura_chan', 'hashed_password_2', 'user', '2022-02-20 14:45:00', 'sakura@example.com', FALSE, 'Sakura', 'c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'd3eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', TRUE, FALSE, TRUE),
(3, 'manga_lover_br', 'hashed_password_3', 'moderator', '2021-11-05 09:15:00', 'brfan@example.com', FALSE, 'MangaBR', 'e4eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', TRUE, TRUE, FALSE),
(1, 'admin_user', 'hashed_admin_password', 'admin', '2020-05-10 08:00:00', 'admin@manga-site.com', FALSE, 'SiteAdmin', 'a6eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'b7eebc99-9c0b-4ef8-bb6d-6bb9bd380a18', TRUE, TRUE, TRUE),
(4, 'spanish_reader', 'hashed_password_4', 'user', '2022-03-12 16:20:00', 'lector@example.com', FALSE, 'LectorES', 'c8eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'd9eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', TRUE, FALSE, TRUE);

-- 4. Inserir mangás populares
INSERT INTO mangas (country_id, title_english, title_native, release_date, finish_date, active_status, comic_type, cover, mal_id) VALUES
(2, 'One Piece', 'ワンピース', '1997-07-22', NULL, 'ongoing', 'Manga', 'f0eebc99-9c0b-4ef8-bb6d-6bb9bd380a21', 13),
(2, 'Naruto', 'NARUTO -ナルト-', '1999-09-21', '2014-11-10', 'completed', 'Manga', 'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 11),
(2, 'Attack on Titan', '進撃の巨人', '2009-09-09', '2021-04-09', 'completed', 'Manga', 'f2eebc99-9c0b-4ef8-bb6d-6bb9bd380a23', 23390),
(2, 'Demon Slayer: Kimetsu no Yaiba', '鬼滅の刃', '2016-02-15', '2020-05-18', 'completed', 'Manga', 'f3eebc99-9c0b-4ef8-bb6d-6bb9bd380a24', 38000),
(2, 'My Hero Academia', '僕のヒーローアカデミア', '2014-07-07', NULL, 'ongoing', 'Manga', 'f4eebc99-9c0b-4ef8-bb6d-6bb9bd380a25', 75989),
(2, 'Tokyo Ghoul', '東京喰種', '2011-09-08', '2014-09-18', 'completed', 'Manga', 'f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a26', 33327),
(2, 'Death Note', 'デスノート', '2003-12-01', '2006-05-15', 'completed', 'Manga', 'f6eebc99-9c0b-4ef8-bb6d-6bb9bd380a27', 21),
(2, 'Fullmetal Alchemist', '鋼の錬金術師', '2001-07-12', '2010-07-10', 'completed', 'Manga', 'f7eebc99-9c0b-4ef8-bb6d-6bb9bd380a28', 25),
(2, 'Dragon Ball', 'ドラゴンボール', '1984-11-20', '1995-05-23', 'completed', 'Manga', 'f8eebc99-9c0b-4ef8-bb6d-6bb9bd380a29', 42),
(2, 'Bleach', 'BLEACH', '2001-08-07', '2016-08-22', 'completed', 'Manga', 'f9eebc99-9c0b-4ef8-bb6d-6bb9bd380a30', 3),
(2, 'Hunter x Hunter', 'HUNTER×HUNTER', '1998-03-03', NULL, 'hiatus', 'Manga', 'g0eebc99-9c0b-4ef8-bb6d-6bb9bd380a31', 26),
(2, 'One-Punch Man', 'ワンパンマン', '2012-06-14', NULL, 'ongoing', 'Manga', 'g1eebc99-9c0b-4ef8-bb6d-6bb9bd380a32', 44347),
(2, 'Jujutsu Kaisen', '呪術廻戦', '2018-03-05', NULL, 'ongoing', 'Manga', 'g2eebc99-9c0b-4ef8-bb6d-6bb9bd380a33', 113138),
(2, 'Chainsaw Man', 'チェンソーマン', '2018-12-03', NULL, 'ongoing', 'Manga', 'g3eebc99-9c0b-4ef8-bb6d-6bb9bd380a34', 116778),
(2, 'Spy x Family', 'SPY×FAMILY', '2019-03-25', NULL, 'ongoing', 'Manga', 'g4eebc99-9c0b-4ef8-bb6d-6bb9bd380a35', 120394),
(2, 'Berserk', 'ベルセルク', '1989-08-25', '2021-09-10', 'completed', 'Manga', 'g5eebc99-9c0b-4ef8-bb6d-6bb9bd380a36', 2),
(2, 'Vinland Saga', 'ヴィンランド・サガ', '2005-04-13', NULL, 'ongoing', 'Manga', 'g6eebc99-9c0b-4ef8-bb6d-6bb9bd380a37', 642),
(2, 'Haikyuu!!', 'ハイキュー!!', '2012-02-20', '2020-07-20', 'completed', 'Manga', 'g7eebc99-9c0b-4ef8-bb6d-6bb9bd380a38', 55221),
(2, 'Kingdom', 'キングダム', '2006-01-26', NULL, 'ongoing', 'Manga', 'g8eebc99-9c0b-4ef8-bb6d-6bb9bd380a39', 583),
(2, 'Solo Leveling', '나 혼자만 레벨업', '2018-03-04', '2020-03-19', 'completed', 'Manhwa', 'g9eebc99-9c0b-4ef8-bb6d-6bb9bd380a40', 100871);

-- 5. Associar tags aos mangás (manga_genres)
-- One Piece
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(1, 1), (1, 2), (1, 5), (1, 18);

-- Naruto
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(2, 1), (2, 2), (2, 5), (2, 8), (2, 18);

-- Attack on Titan
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(3, 1), (3, 5), (3, 7), (3, 12), (3, 14), (3, 19);

-- Demon Slayer
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(4, 1), (4, 2), (4, 5), (4, 12), (4, 18);

-- My Hero Academia
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(5, 1), (5, 2), (5, 3), (5, 12), (5, 18), (5, 30);

-- Tokyo Ghoul
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(6, 1), (6, 5), (6, 6), (6, 7), (6, 12), (6, 13), (6, 19);

-- Death Note
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(7, 7), (7, 12), (7, 13), (7, 14), (7, 19);

-- Fullmetal Alchemist
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(8, 1), (8, 2), (8, 5), (8, 8), (8, 18);

-- Dragon Ball
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(9, 1), (9, 2), (9, 3), (9, 5), (9, 18);

-- Bleach
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(10, 1), (10, 5), (10, 12), (10, 18);

-- Hunter x Hunter
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(11, 1), (11, 2), (11, 5), (11, 18);

-- One-Punch Man
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(12, 1), (12, 3), (12, 5), (12, 12), (12, 18), (12, 30);

-- Jujutsu Kaisen
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(13, 1), (13, 5), (13, 6), (13, 12), (13, 18);

-- Chainsaw Man
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(14, 1), (14, 5), (14, 6), (14, 12), (14, 19);

-- Spy x Family
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(15, 1), (15, 3), (15, 8), (15, 10), (15, 14), (15, 19);

-- Berserk
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(16, 1), (16, 2), (16, 5), (16, 6), (16, 8), (16, 19);

-- Vinland Saga
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(17, 1), (17, 2), (17, 8), (17, 19), (17, 26);

-- Haikyuu!!
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(18, 3), (18, 8), (18, 10), (18, 11), (18, 18), (18, 29);

-- Kingdom
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(19, 1), (19, 2), (19, 19), (19, 26), (19, 27);

-- Solo Leveling
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(20, 1), (20, 2), (20, 5), (20, 15);

-- 6. Inserir capítulos para alguns mangás
-- Capítulos para One Piece (primeiros 5 capítulos)
INSERT INTO chapters (country_id, manga_id, title, cover, ch_number) VALUES
(2, 1, 'Romance Dawn', 'h0eebc99-9c0b-4ef8-bb6d-6bb9bd380a41', 1),
(2, 1, 'They Call Him "Straw Hat Luffy"', 'h1eebc99-9c0b-4ef8-bb6d-6bb9bd380a42', 2),
(2, 1, 'Enter Zoro, the Pirate Hunter', 'h2eebc99-9c0b-4ef8-bb6d-6bb9bd380a43', 3),
(2, 1, 'The Navy Captain Morgan', 'h3eebc99-9c0b-4ef8-bb6d-6bb9bd380a44', 4),
(2, 1, 'The King of the Pirates and the Master Swordsman', 'h4eebc99-9c0b-4ef8-bb6d-6bb9bd380a45', 5);

-- Capítulos para Attack on Titan (primeiros 5 capítulos)
INSERT INTO chapters (country_id, manga_id, title, cover, ch_number) VALUES
(2, 3, 'To You, 2,000 Years From Now', 'i0eebc99-9c0b-4ef8-bb6d-6bb9bd380a46', 1),
(2, 3, 'That Day', 'i1eebc99-9c0b-4ef8-bb6d-6bb9bd380a47', 2),
(2, 3, 'Night of the Disbanding Ceremony', 'i2eebc99-9c0b-4ef8-bb6d-6bb9bd380a48', 3),
(2, 3, 'First Battle', 'i3eebc99-9c0b-4ef8-bb6d-6bb9bd380a49', 4),
(2, 3, 'A Dull Glow in the Midst of Despair', 'i4eebc99-9c0b-4ef8-bb6d-6bb9bd380a50', 5);

-- Capítulos para Demon Slayer (primeiros 5 capítulos)
INSERT INTO chapters (country_id, manga_id, title, cover, ch_number) VALUES
(2, 4, 'Cruelty', 'j0eebc99-9c0b-4ef8-bb6d-6bb9bd380a51', 1),
(2, 4, 'Final Selection', 'j1eebc99-9c0b-4ef8-bb6d-6bb9bd380a52', 2),
(2, 4, 'Sabito and Makomo', 'j2eebc99-9c0b-4ef8-bb6d-6bb9bd380a53', 3),
(2, 4, 'First Mission', 'j3eebc99-9c0b-4ef8-bb6d-6bb9bd380a54', 4),
(2, 4, 'Muzan Kibutsuji', 'j4eebc99-9c0b-4ef8-bb6d-6bb9bd380a55', 5);

-- 7. Inserir páginas para alguns capítulos
-- Páginas para o primeiro capítulo de One Piece
INSERT INTO pages (chapter_id, pg_number, source) VALUES
(1, 1, 'k0eebc99-9c0b-4ef8-bb6d-6bb9bd380a56'),
(1, 2, 'k1eebc99-9c0b-4ef8-bb6d-6bb9bd380a57'),
(1, 3, 'k2eebc99-9c0b-4ef8-bb6d-6bb9bd380a58'),
(1, 4, 'k3eebc99-9c0b-4ef8-bb6d-6bb9bd380a59'),
(1, 5, 'k4eebc99-9c0b-4ef8-bb6d-6bb9bd380a60');

-- Páginas para o primeiro capítulo de Attack on Titan
INSERT INTO pages (chapter_id, pg_number, source) VALUES
(6, 1, 'l0eebc99-9c0b-4ef8-bb6d-6bb9bd380a61'),
(6, 2, 'l1eebc99-9c0b-4ef8-bb6d-6bb9bd380a62'),
(6, 3, 'l2eebc99-9c0b-4ef8-bb6d-6bb9bd380a63'),
(6, 4, 'l3eebc99-9c0b-4ef8-bb6d-6bb9bd380a64'),
(6, 5, 'l4eebc99-9c0b-4ef8-bb6d-6bb9bd380a65');

-- 8. Inserir relações entre mangás (related_mangas)
-- One Piece relacionado com outros mangás shounen
INSERT INTO related_mangas (source_manga_id, related_manga_id, relationship_type) VALUES
(1, 2, 'similar'),
(1, 5, 'similar'),
(1, 10, 'similar'),
(1, 11, 'similar');

-- Attack on Titan relacionado com mangás dark/seinen
INSERT INTO related_mangas (source_manga_id, related_manga_id, relationship_type) VALUES
(3, 6, 'similar'),
(3, 7, 'similar'),
(3, 14, 'similar'),
(3, 16, 'similar');

-- Demon Slayer relacionado com outros mangás de ação/supernatural
INSERT INTO related_mangas (source_manga_id, related_manga_id, relationship_type) VALUES
(4, 10, 'similar'),
(4, 13, 'similar'),
(4, 14, 'similar');

-- Sequências/prequelas (exemplo fictício)
INSERT INTO related_mangas (source_manga_id, related_manga_id, relationship_type) VALUES
(2, 21, 'sequel'), -- Naruto e Boruto (não incluso na lista)
(6, 22, 'prequel'); -- Tokyo Ghoul e Tokyo Ghoul:re (não incluso na lista)

-- 9. Adicionar mais alguns mangás para variedade
INSERT INTO mangas (country_id, title_english, title_native, release_date, finish_date, active_status, comic_type, cover, mal_id) VALUES
(2, 'Fruits Basket', 'フルーツバスケット', '1998-07-18', '2006-11-20', 'completed', 'Manga', 'm0eebc99-9c0b-4ef8-bb6d-6bb9bd380a66', 12),
(2, 'A Silent Voice', '聲の形', '2013-08-07', '2014-11-19', 'completed', 'Manga', 'm1eebc99-9c0b-4ef8-bb6d-6bb9bd380a67', 107931),
(2, 'Your Lie in April', '四月は君の嘘', '2011-04-06', '2015-02-06', 'completed', 'Manga', 'm2eebc99-9c0b-4ef8-bb6d-6bb9bd380a68', 63767),
(2, 'Vagabond', 'バガボンド', '1998-09-03', '2015-05-21', 'hiatus', 'Manga', 'm3eebc99-9c0b-4ef8-bb6d-6bb9bd380a69', 656),
(2, '20th Century Boys', '20世紀少年', '1999-04-28', '2006-10-24', 'completed', 'Manga', 'm4eebc99-9c0b-4ef8-bb6d-6bb9bd380a70', 49),
(2, 'Monster', 'モンスター', '1994-12-05', '2001-12-20', 'completed', 'Manga', 'm5eebc99-9c0b-4ef8-bb6d-6bb9bd380a71', 1),
(2, 'Goodnight Punpun', 'おやすみプンプン', '2007-03-15', '2013-11-02', 'completed', 'Manga', 'm6eebc99-9c0b-4ef8-bb6d-6bb9bd380a72', 4632),
(2, 'Oyasumi Punpun', 'おやすみプンプン', '2007-03-15', '2013-11-02', 'completed', 'Manga', 'm7eebc99-9c0b-4ef8-bb6d-6bb9bd380a73', 4632),
(2, 'Pluto', 'PLUTO', '2003-09-09', '2009-04-01', 'completed', 'Manga', 'm8eebc99-9c0b-4ef8-bb6d-6bb9bd380a74', 801),
(2, 'Uzumaki', 'うずまき', '1998-01-19', '1999-08-20', 'completed', 'Manga', 'm9eebc99-9c0b-4ef8-bb6d-6bb9bd380a75', 110);

-- Adicionar tags para os novos mangás
-- Fruits Basket
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(21, 8), (21, 10), (21, 12), (21, 20);

-- A Silent Voice
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(22, 8), (22, 10), (22, 13), (22, 19);

-- Your Lie in April
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(23, 8), (23, 10), (23, 28), (23, 29), (23, 20);

-- Vagabond
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(24, 1), (24, 2), (24, 19), (24, 25), (24, 26);

-- 20th Century Boys
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(25, 2), (25, 7), (25, 12), (25, 14), (25, 19);

-- Monster
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(26, 7), (26, 13), (26, 14), (26, 19);

-- Goodnight Punpun
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(27, 8), (27, 10), (27, 13), (27, 19);

-- Pluto
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(29, 1), (29, 7), (29, 9), (29, 14), (29, 19);

-- Uzumaki
INSERT INTO manga_genres (manga_id, tag_id) VALUES
(30, 6), (30, 12), (30, 13), (30, 19);

-- 10. Adicionar mais usuários para variedade
INSERT INTO users (country_id, user_name, user_password, user_role, join_date, email, is_banned, nickname, user_profile, user_banner, is_active, allow_nsfw, allow_dm) VALUES
(5, 'french_reader', 'hashed_password_5', 'user', '2022-04-18 11:10:00', 'french@example.com', FALSE, 'LecteurFR', 'n0eebc99-9c0b-4ef8-bb6d-6bb9bd380a76', 'o1eebc99-9c0b-4ef8-bb6d-6bb9bd380a77', TRUE, FALSE, TRUE),
(6, 'korean_fan', 'hashed_password_6', 'user', '2022-05-22 13:25:00', 'korean@example.com', FALSE, 'KoreanFan', 'p2eebc99-9c0b-4ef8-bb6d-6bb9bd380a78', 'q3eebc99-9c0b-4ef8-bb6d-6bb9bd380a79', TRUE, TRUE, FALSE),
(7, 'chinese_reader', 'hashed_password_7', 'user', '2022-06-30 15:40:00', 'chinese@example.com', FALSE, '中文读者', 'r4eebc99-9c0b-4ef8-bb6d-6bb9bd380a80', 's5eebc99-9c0b-4ef8-bb6d-6bb9bd380a81', TRUE, FALSE, TRUE),
(1, 'manga_collector', 'hashed_password_8', 'user', '2021-08-14 09:55:00', 'collector@example.com', FALSE, 'Collector', 't6eebc99-9c0b-4ef8-bb6d-6bb9bd380a82', 'u7eebc99-9c0b-4ef8-bb6d-6bb9bd380a83', TRUE, TRUE, TRUE),
(2, 'japan_otaku', 'hashed_password_9', 'user', '2020-12-03 17:05:00', 'otaku@example.com', FALSE, 'OtakuSan', 'v8eebc99-9c0b-4ef8-bb6d-6bb9bd380a84', 'w9eebc99-9c0b-4ef8-bb6d-6bb9bd380a85', TRUE, TRUE, FALSE);

-- Mensagem de confirmação
SELECT 'Database populated successfully with ' || 
       (SELECT COUNT(*) FROM users) || ' users, ' ||
       (SELECT COUNT(*) FROM mangas) || ' mangas, ' ||
       (SELECT COUNT(*) FROM chapters) || ' chapters, ' ||
       (SELECT COUNT(*) FROM pages) || ' pages, ' ||
       (SELECT COUNT(*) FROM tags) || ' tags, and ' ||
       (SELECT COUNT(*) FROM manga_genres) || ' genre associations.' AS result;