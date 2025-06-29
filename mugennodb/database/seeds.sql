CREATE EXTENSION IF NOT EXISTS "pgcrypto"; -- for gen_random_uuid()

-- Users
INSERT INTO users (
    user_name, user_password, user_role, join_date, email,
    is_banned, nickname, user_profile, user_banner,
    is_active, allow_nsfw, allow_dm
) VALUES
('admin', 'hashedpassword1', 'admin', now(), 'admin@example.com', FALSE, 'AdminMan', gen_random_uuid(), gen_random_uuid(), TRUE, TRUE, TRUE),
('user1', 'hashedpassword2', 'user', now(), 'user1@example.com', FALSE, 'User1', gen_random_uuid(), gen_random_uuid(), TRUE, FALSE, TRUE),
('user2', 'hashedpassword3', 'user', now(), 'user2@example.com', TRUE, 'BannedUser', gen_random_uuid(), gen_random_uuid(), FALSE, FALSE, FALSE);

-- Mangas
INSERT INTO mangas (
    title_english, title_native, release_date, finish_date,
    active_status, comic_type, cover, mal_id
) VALUES
('My Hero Academia', '僕のヒーローアカデミア', '2014-07-07', NULL, 'ongoing', 'shounen', gen_random_uuid(), 12345),
('Death Note', 'デスノート', '2003-12-01', '2006-05-15', 'finished', 'seinen', gen_random_uuid(), 54321);

-- Chapters
INSERT INTO chapters (
    manga_id, title, cover, ch_number
) VALUES
(1, 'Izuku Midoriya: Origin', gen_random_uuid(), 1),
(1, 'What It Takes to Be a Hero', gen_random_uuid(), 2),
(2, 'Boredom', gen_random_uuid(), 1),
(2, 'L', gen_random_uuid(), 2);

-- Pages
INSERT INTO pages (
    chapter_id, pg_number, source
) VALUES
(1, 1, gen_random_uuid()),
(1, 2, gen_random_uuid()),
(2, 1, gen_random_uuid()),
(2, 2, gen_random_uuid()),
(3, 1, gen_random_uuid()),
(4, 1, gen_random_uuid());
