### Database Files Structure

The `mugennodb/database/` directory contains the project's database layer.

#### Migrations

All SQL migration files live under:

```
mugennodb/database/migrations/
```

Each file is versioned and named following this convention:

```
001_create_users.sql
002_add_manga_table.sql
003_update_fansub_relation.sql
```

Migrations should be incremental and reflect schema changes over time. The first file typically sets up the base schema.

#### Interfaces

Python code responsible for querying the database is located in:

```
mugennodb/database/interface/
```

There is **one Python file per database relation (table)**. For example:

- `user.py` contains queries for the `users` table.
- `manga.py` handles access to the `manga` table.
- `fansub_group.py` deals with `fansub_groups`, etc.

These files implement logic using `asyncpg` and should follow the asynchronous code style using `async def`.

#### Auto-generated Schemas

Generated schemas based on PostgreSQL introspection are placed under:

```
mugennodb/database/autogen/
```

These include representations of database relations, typically in the form of Mango schemas or dataclass models.  
**Note:** These files are automatically generated — do not edit them manually.