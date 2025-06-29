# endpoints/help_command.py
from app.endpoints import (
    user_endpoints,
    manga_endpoints,
    chapter_endpoints,
    page_endpoints,
    db_admin_endpoints,
)


def show_help() -> None:
    print("Available commands:")

    print("\nAdmin Commands:")
    for cmd, desc in db_admin_endpoints.COMMANDS.items():
        print(f"  {cmd.ljust(20)} {desc}")

    print("\nUser Commands:")
    for cmd, desc in user_endpoints.COMMANDS.items():
        print(f"  {cmd.ljust(20)} {desc}")

    print("\nManga Commands:")
    for cmd, desc in manga_endpoints.COMMANDS.items():
        print(f"  {cmd.ljust(20)} {desc}")

    print("\nChapter Commands:")
    for cmd, desc in chapter_endpoints.COMMANDS.items():
        print(f"  {cmd.ljust(20)} {desc}")

    print("\nPage Commands:")
    for cmd, desc in page_endpoints.COMMANDS.items():
        print(f"  {cmd.ljust(20)} {desc}")

    print("\nGeneral Commands:")
    print("  help".ljust(20) + "Show this help message")
    print("  exit/quit".ljust(20) + "Exit the program")
