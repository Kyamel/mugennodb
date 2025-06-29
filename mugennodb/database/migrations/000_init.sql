-- init.sql

-- Functions
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = now();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Tables
-- Table users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(128) NOT NULL,
    user_password VARCHAR(128) NOT NULL,
    user_role VARCHAR(128) NOT NULL,
    join_date timestamptz NOT NULL,
    email VARCHAR(128) NOT NULL UNIQUE,
    is_banned BOOLEAN NOT NULL DEFAULT FALSE,
    nickname VARCHAR(128) NOT NULL,
    user_profile UUID NOT NULL,
    user_banner UUID NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    allow_nsfw BOOLEAN NOT NULL DEFAULT FALSE,
    allow_dm BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TRIGGER set_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- Table mangas
CREATE TABLE IF NOT EXISTS mangas (
    id SERIAL PRIMARY KEY,
    title_english VARCHAR(256) NOT NULL,
    title_native VARCHAR(256) NOT NULL,
    release_date DATE NOT NULL,
    finish_date DATE,
    active_status VARCHAR(32) NOT NULL,
    comic_type VARCHAR(32) NOT NULL,
    cover  UUID NOT NULL,
    mal_id INTEGER NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TRIGGER set_mangas_updated_at
BEFORE UPDATE ON mangas
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- Table chapters
CREATE TABLE IF NOT EXISTS chapters (
    id SERIAL PRIMARY KEY,
    manga_id INTEGER NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    title VARCHAR(256) NOT NULL,
    cover  UUID NOT NULL,
    ch_number INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT unique_manga_ch_number UNIQUE (manga_id, ch_number)
);

CREATE TRIGGER set_chapters_updated_at
BEFORE UPDATE ON chapters
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- Table pages
CREATE TABLE IF NOT EXISTS pages (
    id SERIAL PRIMARY KEY,
    chapter_id INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    pg_number INTEGER NOT NULL,
    source UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT unique_chapter_pg_number UNIQUE (chapter_id, pg_number)
);

CREATE TRIGGER set_pages_updated_at
BEFORE UPDATE ON pages
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- Relationships