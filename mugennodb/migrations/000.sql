-- =======================================
-- Tabelas base
-- =======================================
CREATE TABLE countries (
    id SMALLSERIAL PRIMARY KEY,
    locale_code VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    country_id SMALLINT NOT NULL REFERENCES countries(id),
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role VARCHAR(16) NOT NULL CHECK (role IN ('ADMIN', 'MODERATOR', 'USER')) DEFAULT 'USER',
    nickname VARCHAR(128),
    profile_bio TEXT,
    profile_banner TEXT,
    karma_score INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_banned BOOLEAN NOT NULL DEFAULT FALSE,
    allow_nsfw BOOLEAN NOT NULL DEFAULT FALSE,
    settings JSONB DEFAULT '{}'::jsonb,
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
    country_id SMALLINT NOT NULL REFERENCES countries(id),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title_english TEXT NOT NULL,
    title_native TEXT NOT NULL,
    release_date DATE NOT NULL,
    finish_date DATE,
    age_rating VARCHAR(16) NOT NULL CHECK (age_rating IN ('G', 'PG12', 'R15', 'R18')),
    status VARCHAR(16) NOT NULL CHECK (status IN ('ONGOING', 'COMPLETED', 'HIATUS', 'CANCELLED')),
    comic_type TEXT NOT NULL CHECK (comic_type IN ('MANGA', 'DOUJINSHI', 'MANHWA', 'NOVEL', 'ONESHOT')),
    mal_id INTEGER UNIQUE,
    kitsu_id INTEGER UNIQUE,
    cover_url  TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ DEFAULT NULL;
);

-- Links externos para mangás
CREATE TABLE manga_external_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    manga_id UUID NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    link_type VARCHAR(32) NOT NULL CHECK (link_type IN ('PURCHASE', 'OFFICIAL', 'COMMUNITY', 'INFORMATION')),
    url TEXT NOT NULL,
    title VARCHAR(128),
    description TEXT,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_approved BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (manga_id, url)
);

CREATE TABLE manga_relationship_types (
    id SMALLSERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE,
    description TEXT,
    is_recursive BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE manga_relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_manga_id UUID NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    target_manga_id UUID NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    relationship_type_id SMALLINT NOT NULL REFERENCES manga_relationship_types(id),
    description TEXT,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    
    -- Um mangá não pode ter o mesmo relacionamento múltiplas vezes
    UNIQUE(source_manga_id, target_manga_id, relationship_type_id)
);

CREATE TABLE chapters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    manga_id UUID NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    country_id SMALLINT NOT NULL REFERENCES countries(id),
    title TEXT NOT NULL,
    cover_url TEXT NOT NULL,
    ch_number NUMERIC(6,2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT unique_manga_ch UNIQUE (manga_id, ch_number)
);

-- =======================================
-- Staff
-- =======================================
CREATE TABLE staff_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    name VARCHAR(128),
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT unique_staff_identity UNIQUE (user_id, name),
    CONSTRAINT either_user_or_name CHECK (
        (user_id IS NOT NULL AND name IS NULL) OR 
        (user_id IS NULL AND name IS NOT NULL)
    )
);

CREATE TABLE staff_roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL CHECK (name IN ('AUTHOR', 'ILLUSTRRATOR', 'PUBLISHER', 'EDITOR', 'TRANSLATOR')),
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE manga_staff (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    manga_id UUID NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    staff_profile_id UUID NOT NULL REFERENCES staff_profiles(id) ON DELETE CASCADE,
    staff_role_id INT NOT NULL REFERENCES staff_roles(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (manga_id, staff_profile_id, staff_role_id)
);

-- =======================================
-- Tags (Taxonomia Aberta)
-- =======================================
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =======================================
-- Groups
-- =======================================
CREATE TABLE groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(128) NOT NULL UNIQUE,
    description TEXT,
    is_open BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE group_members (
    group_id UUID NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_moderator BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (group_id, user_id)
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
    country_id SMALLINT NOT NULL REFERENCES countries(id),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    is_read_only BOOLEAN DEFAULT FALSE,
    is_mod_only BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,
    karma_score INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE discussion_votes (
    discussion_id UUID NOT NULL REFERENCES discussions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vote SMALLINT NOT NULL CHECK (vote IN (-1, 1)),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (discussion_id, user_id)
);

CREATE TABLE discussion_reads (
    discussion_id UUID NOT NULL REFERENCES discussions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    last_read_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (discussion_id, user_id)
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
    karma_score INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE comment_votes (
    comment_id UUID NOT NULL REFERENCES comments(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vote SMALLINT NOT NULL CHECK (vote IN (-1, 1)),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (comment_id, user_id)
);

-- =======================================
-- Attachments
-- =======================================
CREATE TABLE attachment_types (
    id SMALLSERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL,
    mime_type VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE attachments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_type TEXT NOT NULL CHECK (target_type IN ('discussion','comment','manga','chapter')),
    target_id UUID NOT NULL,
    file_name TEXT NOT NULL,
    file_url TEXT NOT NULL,
    type_id SMALLINT NOT NULL REFERENCES attachment_types(id),
    file_size BIGINT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =======================================
-- Sistema de Tags para Conteúdo
-- =======================================
CREATE TABLE discussion_tags (
    discussion_id UUID NOT NULL REFERENCES discussions(id) ON DELETE CASCADE,
    tag_id INT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (discussion_id, tag_id, user_id)
);

CREATE TABLE manga_tags (
    manga_id UUID NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    tag_id INT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (manga_id, tag_id, user_id)
);

CREATE TABLE chapter_tags (
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    tag_id INT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (chapter_id, tag_id, user_id)
);

-- =======================================
-- Reviews / Reading list
-- =======================================
CREATE TABLE reviews (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    manga_id UUID NOT NULL REFERENCES mangas(id) ON DELETE CASCADE,
    status VARCHAR(16) NOT NULL CHECK (status IN ('PLANNING','READING','COMPLETED','DROPPED')) DEFAULT 'PLANNING',
    score SMALLINT CHECK (score >= 0 AND score <= 10),
    review TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, manga_id)
);

CREATE TABLE reading_progress (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    status VARCHAR(16) NOT NULL CHECK (status IN  ('PLANNING','READING','COMPLETED')) DEFAULT 'PLANNING',
    score SMALLINT CHECK (score >= 0 AND score <= 10),
    review TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, chapter_id)
);

-- =======================================
-- Notificações (Polimórficas)
-- =======================================
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    target_type TEXT NOT NULL CHECK (target_type IN ('discussion', 'comment', 'manga', 'chapter')),
    target_id UUID NOT NULL,
    type VARCHAR(32) NOT NULL, -- ex: 'new_comment', 'new_chapter', 'manga_update'
    title VARCHAR(128) NOT NULL,
    content TEXT,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    --last_seen_comment UUID REFERENCES comments(id),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =======================================
-- Sistema de Flags/Reports (Polimórfico)
-- =======================================
CREATE TABLE flags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_type TEXT NOT NULL CHECK (target_type IN ('discussion', 'comment', 'manga', 'chapter')),
    target_id UUID NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reason TEXT NOT NULL,
    status VARCHAR(16) NOT NULL CHECK (status IN ('PENDING', 'REVIEWED', 'DISMISSED', 'ACCEPTED')) DEFAULT 'PENDING',
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);


-- =======================================
-- Índices para melhor performance
-- =======================================
CREATE INDEX idx_mangas_status ON mangas(status);
CREATE INDEX idx_mangas_type ON mangas(comic_type_id);
CREATE INDEX idx_discussions_manga ON discussions(manga_id);
CREATE INDEX idx_discussions_group ON discussions(group_id);
CREATE INDEX idx_chapters_manga ON chapters(manga_id);
CREATE INDEX idx_comments_discussion ON comments(discussion_id);
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id) WHERE is_read = false;
CREATE INDEX idx_group_members_user ON group_members(user_id);
CREATE INDEX idx_user_follows_follower ON user_follows(follower_id);
CREATE INDEX idx_user_follows_following ON user_follows(following_id);
CREATE INDEX idx_tags_name ON tags(name);
CREATE INDEX idx_mangas_user ON mangas(user_id);
CREATE INDEX idx_chapters_user ON chapters(user_id);
CREATE INDEX idx_discussions_user ON discussions(user_id);
CREATE INDEX idx_comments_user ON comments(user_id);
CREATE INDEX idx_manga_relationships_source ON manga_relationships(source_manga_id);
CREATE INDEX idx_manga_relationships_target ON manga_relationships(target_manga_id);
CREATE INDEX idx_manga_relationships_type ON manga_relationships(relationship_type_id);
CREATE INDEX idx_manga_relationships_user ON manga_relationships(user_id);

-- Índices para otimizar as queries dos triggers
CREATE INDEX idx_discussion_votes_discussion ON discussion_votes(discussion_id);
CREATE INDEX idx_comment_votes_comment ON comment_votes(comment_id);
CREATE INDEX idx_notifications_target ON notifications(target_type, target_id);
CREATE INDEX idx_manga_tags_manga ON manga_tags(manga_id);
CREATE INDEX idx_discussion_tags_discussion ON discussion_tags(discussion_id);
CREATE INDEX idx_comments_created ON comments(created_at);
CREATE INDEX idx_discussions_created ON discussions(created_at);


-- =======================================
-- TRIGGERS PARA VALIDAÇÃO DE DADOS
-- =======================================
CREATE OR REPLACE FUNCTION validate_manga_dates()
RETURNS TRIGGER AS $$
BEGIN
    -- Garantir que finish_date seja posterior a release_date
    IF NEW.finish_date IS NOT NULL AND NEW.finish_date < NEW.release_date THEN
        RAISE EXCEPTION 'finish_date must be after release_date';
    END IF;
    
    -- Se status é 'completed', finish_date não pode ser nulo
    IF NEW.status = 'completed' AND NEW.finish_date IS NULL THEN
        RAISE EXCEPTION 'finish_date cannot be null for completed manga';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_manga_dates
BEFORE INSERT OR UPDATE ON mangas
FOR EACH ROW EXECUTE FUNCTION validate_manga_dates();

-- Notificações
CREATE OR REPLACE FUNCTION validate_notification_target()
RETURNS trigger AS $$
BEGIN
    IF NEW.target_type = 'discussion' THEN
        IF NOT EXISTS (SELECT 1 FROM discussions WHERE id = NEW.target_id) THEN
            RAISE EXCEPTION 'Invalid discussion ID %', NEW.target_id;
        END IF;
    ELSIF NEW.target_type = 'comment' THEN
        IF NOT EXISTS (SELECT 1 FROM comments WHERE id = NEW.target_id) THEN
            RAISE EXCEPTION 'Invalid comment ID %', NEW.target_id;
        END IF;
    ELSIF NEW.target_type = 'manga' THEN
        IF NOT EXISTS (SELECT 1 FROM mangas WHERE id = NEW.target_id) THEN
            RAISE EXCEPTION 'Invalid manga ID %', NEW.target_id;
        END IF;
    ELSIF NEW.target_type = 'chapter' THEN
        IF NOT EXISTS (SELECT 1 FROM chapters WHERE id = NEW.target_id) THEN
            RAISE EXCEPTION 'Invalid chapter ID %', NEW.target_id;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_notification_target
BEFORE INSERT OR UPDATE ON notifications
FOR EACH ROW EXECUTE FUNCTION validate_notification_target();


-- Flags
CREATE OR REPLACE FUNCTION validate_flag_target()
RETURNS trigger AS $$
BEGIN
    IF NEW.target_type = 'discussion' THEN
        IF NOT EXISTS (SELECT 1 FROM discussions WHERE id = NEW.target_id) THEN
            RAISE EXCEPTION 'Invalid discussion ID %', NEW.target_id;
        END IF;
    ELSIF NEW.target_type = 'comment' THEN
        IF NOT EXISTS (SELECT 1 FROM comments WHERE id = NEW.target_id) THEN
            RAISE EXCEPTION 'Invalid comment ID %', NEW.target_id;
        END IF;
    ELSIF NEW.target_type = 'manga' THEN
        IF NOT EXISTS (SELECT 1 FROM mangas WHERE id = NEW.target_id) THEN
            RAISE EXCEPTION 'Invalid manga ID %', NEW.target_id;
        END IF;
    ELSIF NEW.target_type = 'chapter' THEN
        IF NOT EXISTS (SELECT 1 FROM chapters WHERE id = NEW.target_id) THEN
            RAISE EXCEPTION 'Invalid chapter ID %', NEW.target_id;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_flag_target
BEFORE INSERT OR UPDATE ON flags
FOR EACH ROW EXECUTE FUNCTION validate_flag_target();


-- =======================================
-- TRIGGERS PARA ATUALIZAÇÃO AUTOMÁTICA DE TIMESTAMPS
-- =======================================

-- Atualiza automaticamente o campo updated_at nas tabelas
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger de updated_at para todas as tabelas relevantes
CREATE TRIGGER trg_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_mangas_updated_at BEFORE UPDATE ON mangas FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_chapters_updated_at BEFORE UPDATE ON chapters FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_discussions_updated_at BEFORE UPDATE ON discussions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_comments_updated_at BEFORE UPDATE ON comments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_groups_updated_at BEFORE UPDATE ON groups FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_staff_profiles_updated_at BEFORE UPDATE ON staff_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_manga_external_links_updated_at BEFORE UPDATE ON manga_external_links FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_flags_updated_at BEFORE UPDATE ON flags FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =======================================
-- TRIGGERS PARA SISTEMA DE KARMA/VOTOS
-- =======================================

-- Mantém o karma_score dos discussions atualizado automaticamente
CREATE OR REPLACE FUNCTION update_discussion_karma()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        UPDATE discussions 
        SET karma_score = COALESCE((
            SELECT SUM(vote) 
            FROM discussion_votes 
            WHERE discussion_id = COALESCE(NEW.discussion_id, OLD.discussion_id)
        ), 0)
        WHERE id = COALESCE(NEW.discussion_id, OLD.discussion_id);
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE discussions 
        SET karma_score = COALESCE((
            SELECT SUM(vote) 
            FROM discussion_votes 
            WHERE discussion_id = OLD.discussion_id
        ), 0)
        WHERE id = OLD.discussion_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_discussion_votes_karma
AFTER INSERT OR UPDATE OR DELETE ON discussion_votes
FOR EACH ROW EXECUTE FUNCTION update_discussion_karma();

-- Mantém o karma_score dos comments atualizado automaticamente
CREATE OR REPLACE FUNCTION update_comment_karma()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        UPDATE comments 
        SET karma_score = COALESCE((
            SELECT SUM(vote) 
            FROM comment_votes 
            WHERE comment_id = COALESCE(NEW.comment_id, OLD.comment_id)
        ), 0)
        WHERE id = COALESCE(NEW.comment_id, OLD.comment_id);
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE comments 
        SET karma_score = COALESCE((
            SELECT SUM(vote) 
            FROM comment_votes 
            WHERE comment_id = OLD.comment_id
        ), 0)
        WHERE id = OLD.comment_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_comment_votes_karma
AFTER INSERT OR UPDATE OR DELETE ON comment_votes
FOR EACH ROW EXECUTE FUNCTION update_comment_karma();


-- =======================================
-- TRIGGERS PARA ATUALIZAÇÃO DE CONTADORES
-- =======================================

-- Atualiza o timestamp da discussão quando novos comentários são adicionados/removidos
CREATE OR REPLACE FUNCTION update_discussion_comment_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE discussions 
        SET updated_at = now() -- Marcar como atualizado
        WHERE id = NEW.discussion_id;
        
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE discussions 
        SET updated_at = now()
        WHERE id = OLD.discussion_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_discussion_comment_count
AFTER INSERT OR DELETE ON comments
FOR EACH ROW EXECUTE FUNCTION update_discussion_comment_count();

-- Atualiza o timestamp do grupo quando membros são adicionados/removidos
CREATE OR REPLACE FUNCTION update_group_member_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE groups 
        SET updated_at = now()
        WHERE id = NEW.group_id;
        
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE groups 
        SET updated_at = now()
        WHERE id = OLD.group_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_group_member_count
AFTER INSERT OR DELETE ON group_members
FOR EACH ROW EXECUTE FUNCTION update_group_member_count();
