-- =======================================
-- Sistema de Tags Categorizadas (apenas taxonomia aberta)
-- =======================================
CREATE TABLE tag_categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE tags (
    id BIGSERIAL PRIMARY KEY,
    category_id BIGINT REFERENCES tag_categories(id),
    name VARCHAR(64) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (category_id, name)
);

-- =======================================
-- Lookup tables (enums fechados)
-- =======================================
CREATE TABLE user_roles (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL, -- admin, mod, user
    description TEXT
);

CREATE TABLE manga_status (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL, -- em andamento, finalizado
    description TEXT
);

CREATE TABLE comic_types (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL, -- manga, manhwa, manhua
    description TEXT
);

CREATE TABLE file_types (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL, -- image, pdf, audio
    description TEXT
);

CREATE TABLE review_status (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL, -- planning, reading, completed, dropped
    description TEXT
);

CREATE TABLE read_status (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL, -- reading, rereading, completed
    description TEXT
);

-- =======================================
-- Tabelas base
-- =======================================
CREATE TABLE countries (
    id BIGSERIAL PRIMARY KEY,
    locale_code VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    country_id BIGINT NOT NULL REFERENCES countries(id),
    role_id BIGINT NOT NULL REFERENCES user_roles(id), -- agora FK clara
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    nickname VARCHAR(128),
    profile_bio TEXT,
    profile_banner TEXT,
    karma_score INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_banned BOOLEAN NOT NULL DEFAULT FALSE,
    allow_nsfw BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =======================================
-- Mangás
-- =======================================
CREATE TABLE mangas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    made_in BIGINT NOT NULL REFERENCES countries(id),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title_english TEXT NOT NULL,
    title_native TEXT NOT NULL,
    release_date DATE NOT NULL,
    finish_date DATE,
    status_id BIGINT NOT NULL REFERENCES manga_status(id),
    comic_type_id BIGINT NOT NULL REFERENCES comic_types(id),
    cover_url TEXT NOT NULL,
    mal_id INTEGER UNIQUE,
    kitsu_id INTEGER UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =======================================
-- Chapters
-- =======================================
CREATE TABLE chapters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    manga_id UUID NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    country_id BIGINT NOT NULL REFERENCES countries(id),
    title TEXT NOT NULL,
    cover_url TEXT NOT NULL,
    ch_number NUMERIC(6,2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT unique_manga_ch UNIQUE (manga_id, ch_number)
);

-- =======================================
-- Tags de conteúdo (taxonomia)
-- =======================================
CREATE TABLE manga_tags (
    manga_id UUID NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    tag_id BIGINT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (manga_id, tag_id, user_id)
);

CREATE TABLE chapter_tags (
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    tag_id BIGINT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (chapter_id, tag_id, user_id)
);

-- =======================================
-- Reviews / Reading list
-- =======================================
CREATE TABLE reviews (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    manga_id UUID NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    status_id BIGINT REFERENCES review_status(id),
    score NUMERIC(3,1) CHECK (score >= 0 AND score <= 10),
    review TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, manga_id)
);

CREATE TABLE reads (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    status_id BIGINT REFERENCES read_status(id),
    score NUMERIC(3,1) CHECK (score >= 0 AND score <= 10),
    review TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, chapter_id)
);

-- =======================================
-- Flags (sem polimorfismo)
-- =======================================
CREATE TABLE discussion_flags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    discussion_id UUID NOT NULL REFERENCES discussions(id) ON DELETE CASCADE,
    reporting_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reason VARCHAR(128) NOT NULL,
    description TEXT,
    status VARCHAR(64) NOT NULL DEFAULT 'pending',
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE comment_flags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    comment_id UUID NOT NULL REFERENCES comments(id) ON DELETE CASCADE,
    reporting_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reason VARCHAR(128) NOT NULL,
    description TEXT,
    status VARCHAR(64) NOT NULL DEFAULT 'pending',
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
