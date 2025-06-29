# endpoints/chapter_endpoints.py
from datetime import datetime
from uuid import uuid4
from mugennocore.model.chapter import Chapter
from mugennodb.database.interface.chapters import (
    get_all_chapters_by_manga_id,
    insert_chapter,
)

COMMANDS = {
    "get_chapters": "List chapters for manga",
    "insert_dummy_chapter": "Add test chapter",
}


async def handle_command(db, parts):
    if parts[0] == "get_chapters":
        manga_id = int(parts[1])
        chapters = await get_all_chapters_by_manga_id(db, manga_id)
        if chapters:
            for c in chapters:
                print(c)
        else:
            print("No chapters found")

    elif parts[0] == "insert_dummy_chapter":
        manga_id = int(parts[1])
        ch_number = int(parts[2]) if len(parts) > 2 else 1
        chapter = Chapter(
            id=0,
            manga_id=manga_id,
            title="Chapter One",
            cover=uuid4(),
            ch_number=ch_number,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        cid = await insert_chapter(db, chapter)
        print(f"Chapter inserted with ID {cid}")
