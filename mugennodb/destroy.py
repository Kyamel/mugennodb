from mugennodb.conection.database_protocol import DatabaseProtocol


async def destroy_database_schema(db: DatabaseProtocol) -> None:
    await db.execute(
        """
    -- Drop everything in public schema but preserve essential extensions
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    
    -- Grant permissions
    GRANT ALL ON SCHEMA public TO public;
    COMMENT ON SCHEMA public IS 'standard public schema';
    
    -- Recreate essential language if needed
    CREATE EXTENSION IF NOT EXISTS plpgsql;
    """
    )
