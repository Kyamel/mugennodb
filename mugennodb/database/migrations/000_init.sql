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

-- Table tags
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    tag_name VARCHAR(128) NOT NULL UNIQUE,
    tag_type VARCHAR(64) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TRIGGER set_tags_updated_at
BEFORE UPDATE ON tags
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- Table countries
CREATE TABLE IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY,
    lang VARCHAR(10) NOT NULL,
    locale_code VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TRIGGER set_countries_updated_at
BEFORE UPDATE ON countries
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Relationships

-- Table related_mangas (Junction table for Manga to Manga relationship)
CREATE TABLE IF NOT EXISTS related_mangas (
    id SERIAL PRIMARY KEY,
    source_manga_id INTEGER NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    related_manga_id INTEGER NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    relationship_type VARCHAR(64) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT unique_manga_relation UNIQUE (source_manga_id, related_manga_id, relationship_type),
    CONSTRAINT check_manga_not_self CHECK (source_manga_id <> related_manga_id)
);

CREATE TRIGGER set_related_mangas_updated_at
BEFORE UPDATE ON related_mangas
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- Table manga_genres (Junction table for Manga to Tag relationship)
CREATE TABLE IF NOT EXISTS manga_genres (
    id SERIAL PRIMARY KEY,
    manga_id INTEGER NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT unique_manga_genre UNIQUE (manga_id, tag_id)
);
CREATE TRIGGER set_manga_genres_updated_at
BEFORE UPDATE ON manga_genres
FOR EACH ROW 
EXECUTE FUNCTION set_updated_at();

-- Table read (Junction table for User to Manga relationship - Reading tracking)
CREATE TABLE IF NOT EXISTS read (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    manga_id INTEGER NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'reading',
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, manga_id)
);

CREATE TRIGGER set_read_updated_at
BEFORE UPDATE ON read
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- Table review
CREATE TABLE IF NOT EXISTS review (
    review_id SERIAL PRIMARY KEY,
    users_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    score NUMERIC(3,2) NOT NULL CHECK (score >= 0 AND score <= 10),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TRIGGER set_review_updated_at
BEFORE UPDATE ON review
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- Table chapter_reviews
CREATE TABLE IF NOT EXISTS chapter_reviews (
    review_id INT NOT NULL,
    chapter_id INT NOT NULL,
    PRIMARY KEY (review_id, chapter_id),
    FOREIGN KEY (review_id) REFERENCES review(review_id) ON DELETE CASCADE,
    FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE
);

CREATE TRIGGER set_chapter_reviews_updated_at
BEFORE UPDATE ON chapter_reviews
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();