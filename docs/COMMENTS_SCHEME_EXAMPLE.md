# Comments Suggested Scheme

```sql
-- Base table for comments
    CREATE TABLE comments (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    );

    -- Comment content and relation with user
    CREATE TABLE user_comments (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        user_id BIGINT NOT NULL,
        comment_id BIGINT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE
    );

    -- Comments on mangas
    CREATE TABLE manga_comments (
        comment_id BIGINT NOT NULL,
        manga_id BIGINT NOT NULL,
        
        PRIMARY KEY (comment_id), -- A comment belongs to only one manga
        FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE,
        FOREIGN KEY (manga_id) REFERENCES mangas(id)
    );

    -- Comments on chapters
    CREATE TABLE chapter_comments (
        comment_id BIGINT NOT NULL,
        chapter_id BIGINT NOT NULL,
        
        PRIMARY KEY (comment_id), -- A comment belongs to only one chapter
        FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE,
        FOREIGN KEY (chapter_id) REFERENCES chapters(id)
    );

    -- Comments on pages
    CREATE TABLE page_comments (
        comment_id BIGINT NOT NULL,
        page_id BIGINT NOT NULL,
        
        PRIMARY KEY (comment_id), -- A comment belongs to only one page
        FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE,
        FOREIGN KEY (page_id) REFERENCES pages(id)
    );
```
