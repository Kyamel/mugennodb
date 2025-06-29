from mugennodb.conection.database_protocol import DatabaseProtocol


async def destroy_database_schema(db: DatabaseProtocol) -> None:
    # Deleta todas as constraints, tabelas, views, sequences e funções no schema public
    await db.execute(
        """
    DO $$ DECLARE
        r RECORD;
    BEGIN
        -- Drop all views
        FOR r IN (
            SELECT table_name FROM information_schema.views
            WHERE table_schema = 'public'
        ) LOOP
            EXECUTE 'DROP VIEW IF EXISTS "' || r.table_name || '" CASCADE';
        END LOOP;

        -- Drop all tables
        FOR r IN (
            SELECT tablename FROM pg_tables
            WHERE schemaname = 'public'
        ) LOOP
            EXECUTE 'DROP TABLE IF EXISTS "' || r.tablename || '" CASCADE';
        END LOOP;

        -- Drop all sequences
        FOR r IN (
            SELECT sequence_name FROM information_schema.sequences
            WHERE sequence_schema = 'public'
        ) LOOP
            EXECUTE 'DROP SEQUENCE IF EXISTS "' || r.sequence_name || '" CASCADE';
        END LOOP;

        -- Drop user-defined functions (ignore extension-owned)
        FOR r IN (
            SELECT
                p.oid,
                proname,
                pg_get_function_identity_arguments(p.oid) AS args
            FROM pg_proc p
            JOIN pg_namespace n ON p.pronamespace = n.oid
            LEFT JOIN pg_depend d ON d.objid = p.oid AND d.deptype = 'e'
            WHERE n.nspname = 'public'
            AND d.objid IS NULL  -- ignora funções de extensões
        ) LOOP
            EXECUTE format(
                'DROP FUNCTION IF EXISTS %I(%s) CASCADE;',
                r.proname,
                r.args
            );
        END LOOP;

    END $$;
    """
    )
