# Next Steps

## Create Tables

In the file:
[000_init.sql](../mugennodb/database/migrations/000_init.sql)

All tables follow the `snake_case` naming convention and have `created_at` and `updated_at` columns with automatic timestamps.

### users

Stores user account data.

* id (PK)
* country_id (FK)  -- main language of the user.
* user_name (login)
* user_password (password)
* user_role (admin, regular...)
* join_date
* email (unique)
* is_banned
* nickname
* user_profile (UUID)
* user_banner (UUID)
* is_active
* allow_nsfw
* allow_dm

### mangas

Information about works (mangas, manhwas, etc).

* id (PK)
* country_id (FK) -- country of origin.
* title_english
* title_native
* release_date
* finish_date
* active_status (ongoing, finished...)
* comic_type (manga, manhwa...)
* cover (UUID)
* mal_id (unique)
* rating (G, PG, R...)

### chapters

Chapters of mangas.

* id (PK)
* manga_id (FK)
* country_id (FK) -- translation language.
* title
* cover (UUID)
* ch_number (unique per manga)

### pages

Pages of a chapter.

* id (PK)
* chapter_id (FK)
* pg_number (unique per chapter)
* source (UUID) -- link to the image.

### tags

Tags and genres.

* id (PK)
* type (genre, theme...)
* name

### countries

Languages or locations.

* id (PK)
* locale_code (pt-BR, en-US...)

---

## Relationships

### read (users_mangas)

Reading tracking.

* user_id (FK)
* manga_id (FK)
* status (reading, dropped...)

### reviews

User who wrote the review and its content.

* review_id (PK)
* user_id (FK)
* score
* content

### chapters_reviews

Chapter review.

* review_id (FK)
* chapter_id (FK)

### mangas_reviews

Manga review.

* review_id (FK)
* manga_id (FK)

### pages_reviews

Page review.

* review_id (FK)
* page_id (FK)

### related (mangas_mangas)

Relationships between mangas.

* manga_id (FK)
* related_manga_id (FK)
* relation (spin-off, etc.)

### genre (mangas_tags)

Associates mangas with genres.

* manga_id (FK)
* tag_id (FK)

### localized (mangas_countries)

Translation of synopses.

* manga_id (FK)
* country_id (FK)
* synopsis (translated text)
* synopsis_embed (NLP vector) -- semantic search
