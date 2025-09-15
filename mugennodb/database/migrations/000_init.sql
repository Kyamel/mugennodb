-- =======================================
-- Tags
-- =======================================
CREATE TABLE tags (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL,
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
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role BIGINT REFERENCES tags(id),
    nickname VARCHAR(128),
    profile_bio TEXT,
    profile_banner TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_banned BOOLEAN NOT NULL DEFAULT FALSE,
    allow_nsfw BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =======================================
-- Sistema de social (follow)
-- =======================================

CREATE TABLE user_follows (
    follower_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    following_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (follower_id, following_id),
    CONSTRAINT no_self_follow CHECK (follower_id <> following_id)
);

CREATE TABLE user_blocks (
    blocker_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    blocked_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (blocker_id, blocked_id),
    CONSTRAINT no_self_block CHECK (blocker_id <> blocked_id)
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
    status BIGINT REFERENCES tags(id),      -- (status IN ('ongoing','completed','hiatus','cancelled')) NOT NULL,
    comic_type BIGINT REFERENCES tags(id),  -- (comic_type IN ('manga','manhwa','manhua','doujinshi','novel','other')) NOT NULL,
    synopsis TEXT NOT NULL,
    cover_url TEXT NOT NULL,
    mal_id INTEGER UNIQUE,
    kitsu_id INTEGER UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

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
-- Discussões (threads)
-- =======================================
CREATE TABLE discussions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    manga_id UUID REFERENCES mangas(id) ON DELETE CASCADE,
    chapter_id UUID REFERENCES chapters(id) ON DELETE CASCADE,
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    country_id BIGINT NOT NULL REFERENCES countries(id), -- idioma principal
    required_role_level INTEGER DEFAULT 0;
    title TEXT NOT NULL,
    content TEXT NOT NULL,
 -- category TEXT NOT NULL CHECK (category IN ('discussion','theory','review','question','fanfic','fanart','fansub')), 
    is_channel BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE discussion_votes (
    discussion_id UUID NOT NULL REFERENCES discussions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vote SMALLINT NOT NULL CHECK (vote IN (-1,1)), -- upvote/downvote
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (discussion_id, user_id)
);

-- =======================================
-- Groups
-- =======================================
CREATE TABLE groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(128) NOT NULL UNIQUE,
    description TEXT,
    is_open BOOLEAN NOT NULL DEFAULT TRUE,  -- todos podem ver/seguir
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE group_members (
    group_id UUID NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE group_followers (
    group_id UUID NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE group_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    name VARCHAR(64) NOT NULL,                  -- ex: "member", "mod", "admin", "leitor"
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    level INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (group_id, name)
);

-- =======================================
-- Comentários e votos
-- =======================================
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    discussion_id UUID NOT NULL REFERENCES discussions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    reply_to UUID REFERENCES comments(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE comment_votes (
    comment_id UUID NOT NULL REFERENCES comments(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vote SMALLINT NOT NULL CHECK (vote IN (-1,1)), -- upvote/downvote
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (comment_id, user_id)
);

-- =======================================
-- Attachments
-- =======================================
CREATE TABLE discussion_attachments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    discussion_id UUID NOT NULL REFERENCES discussions(id) ON DELETE CASCADE,
    file_url TEXT NOT NULL,
    file_type BIGINT REFERENCES tags(id),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE comment_attachments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    comment_id UUID NOT NULL REFERENCES comments(id) ON DTEXT CHECK ELETE CASCADE,
    file_url TEXT NOT NULL,
    file_type BIGINT REFERENCES tags(id),  --(file_type IN ('image','video','audio','pdf','other')) DEFAULT 'image',
    created_at TIMESTAMPTZ DEFAULT now()
);


-- Junctions (sempre no momento da criação precisa ter ao menos 1 tag associada)
CREATE TABLE discussion_tags (
    discussion_id UUID NOT NULL REFERENCES discussions(id) ON DELETE CASCADE,
    tag_id BIGINT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- vários usuários podem marcar
    PRIMARY KEY (discussion_id, tag_id, user_id)
);

CREATE TABLE manga_tags (
    manga_id UUID NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    tag_id BIGINT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- vários usuários podem marcar
    PRIMARY KEY (manga_id, tag_id, user_id)
);

CREATE TABLE chapter_tags (
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    tag_id BIGINT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- vários usuários podem marcar
    PRIMARY KEY (chapter_id, tag_id, user_id)
);

-- =======================================
-- Reviews / Reading list
-- =======================================
CREATE TABLE reviews (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    manga_id UUID NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    status BIGINT REFERENCES tags(id),      -- (status IN ('planning','reading','completed','paused','dropped')),
    score NUMERIC(3,1) CHECK (score >= 0 AND score <= 10),
    review TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, manga_id)
);

CREATE TABLE reads (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    status BIGINT REFERENCES tags(id),      -- (status IN ('planning','reading','completed')),
    score NUMERIC(3,1) CHECK (score >= 0 AND score <= 10),
    review TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, chapter_id)
);

-- =======================================
-- Notificações
-- =======================================
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    discussion_id UUID NOT NULL REFERENCES discussions(id) ON DELETE CASCADE,
    last_seen_comment UUID REFERENCES comments(id),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE discussion_user_settings (
    discussion_id UUID NOT NULL REFERENCES discussions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    silenced BOOLEAN DEFAULT FALSE,        -- silencia toda a discussion para o user
    notify_replies BOOLEAN DEFAULT TRUE,   -- se false, não recebe notificação de replies
    PRIMARY KEY (discussion_id, user_id)
);

-- =======================================
-- Reports
-- =======================================
CREATE TABLE report_status (
    discussion_id UUID PRIMARY KEY REFERENCES discussions(id) ON DELETE CASCADE,
    status BIGINT REFERENCES tags(id),      --(status IN ('pending','reviewed','dismissed','accepted')) DEFAULT 'pending',
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- References content creator of a manga
-- External related links to a manga
-- Staff of a manga
    
-- Block users globaly