# endpoints/page_endpoints.py
from datetime import datetime
from uuid import uuid4
from mugennocore.model.page import Page
from mugennodb.database.interface.pages import (
    get_page_by_chapter_and_number,
    insert_page,
)

COMMANDS = {"get_page": "Get specific page", "insert_dummy_page": "Add test page"}


async def handle_command(db, parts):
    if parts[0] == "get_page":
        chapter_id = int(parts[1])
        pg_number = int(parts[2])
        page = await get_page_by_chapter_and_number(db, chapter_id, pg_number)
        print(page or "Page not found")

    elif parts[0] == "insert_dummy_page":
        chapter_id = int(parts[1])
        pg_number = int(parts[2]) if len(parts) > 2 else 1
        page = Page(
            id=0,
            chapter_id=chapter_id,
            pg_number=pg_number,
            source=uuid4(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        pid = await insert_page(db, page)
        print(f"Page inserted with ID {pid}")
