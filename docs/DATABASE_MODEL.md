# Próximos passos

## Criar Tabelas

No arquivo:  
[000_init.sql](../mugennodb/database/migrations/000_init.sql)

Todas as tabelas seguem o padrão `snake_case` e possuem as colunas `created_at` e `updated_at` com preenchimento automático.

### users

Armazena dados de conta dos usuários.

* id (PK)
* country_id (FK)  -- linguagem principal do usuário.
* user_name (login)
* user_password (senha)
* user_role (admin, comum...)
* join_date
* email (único)
* is_banned
* nickname
* user_profile (UUID)
* user_banner (UUID)
* is_active
* allow_nsfw
* allow_dm

### mangas

Dados de obras (mangás, manhwas, etc).

* id (PK)
* country_id (FK) -- país de origem.
* title_english
* title_native
* release_date
* finish_date
* active_status (ongoing, finished...)
* comic_type (manga, manhwa...)
* cover (UUID)
* mal_id (único)
* rating (G, PG, R...)

### chapters

Capítulos de mangás.

* id (PK)
* manga_id (FK)
* country_id (FK) -- tradução.
* title
* cover (UUID)
* ch_number (único por manga)

### pages

Páginas de um capítulo.

* id (PK)
* chapter_id (FK)
* pg_number (único por capítulo)
* source (UUID) --link para a imagem.

### tags

Tags e gêneros.

* id (PK)
* type (gênero, tema...)
* name

### countries

Idiomas ou locais.

* id (PK)
* locale_code (pt-BR, en-US...)

---

## Relacionamentos

### read (users_mangas)

Rastreamento de leitura.

* user_id (FK)
* manga_id (FK)
* status (reading, dropped...)

### reviews

Usuário que escreveu a review e seu conteúdo.

* review_id (PK)
* user_id (FK)
* score
* content

### chapters_reviews

Review de capítulo.

* review_id (FK)
* chapter_id (FK)

### mangas_reviews

Review de mangá.

* review_id (FK)
* manga_id (FK)

### pages_reviews

Review de página.

* review_id (FK)
* page_id (FK)

### related (mangas_mangas)

Relacionamentos entre mangás.

* manga_id (FK)
* related_manga_id (FK)
* relation (spin-off, etc.)

### genre (mangas_tags)

Relaciona mangás com gêneros.

* manga_id (FK)
* tag_id (FK)

### localized (mangas_countries)

Tradução de sinopses.

* manga_id (FK)
* country_id (FK)
* sinopse (texto traduzido)
* sinopse_embed (vetor NLP) --busca semântica
