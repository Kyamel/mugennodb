# main.py
import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory

from app.endpoints import (
    user_endpoints,
    manga_endpoints,
    chapter_endpoints,
    page_endpoints,
    db_admin_endpoints,
)
from app.load_env import get_database_dsn
from mugennodb.conection.asyncpg_database import AsyncPGDatabase
from app import help_command

db = AsyncPGDatabase(dsn=get_database_dsn())


def setup_completer():
    # Combine all commands from all modules
    commands = (
        ["help", "exit", "quit"]
        + list(user_endpoints.COMMANDS.keys())
        + list(manga_endpoints.COMMANDS.keys())
        + list(chapter_endpoints.COMMANDS.keys())
        + list(page_endpoints.COMMANDS.keys())
        + list(db_admin_endpoints.COMMANDS.keys())
    )
    return WordCompleter(commands, ignore_case=True)


async def repl():
    session = PromptSession(
        history=FileHistory(".repl_history.txt"),
        completer=setup_completer(),
        complete_while_typing=True,
    )

    await db.connect()
    print(
        "Connected to database. Type 'help' for commands, 'exit' to quit. (Tab for autocomplete)"
    )

    while True:
        try:
            # First await the prompt, then process the result
            cmd_text = await session.prompt_async("db> ")
            cmd = cmd_text.strip().lower()

            if cmd in ("exit", "quit"):
                break

            if cmd == "help":
                help_command.show_help()
                continue

            parts = cmd.split()
            if not parts:
                continue

            try:
                # Route commands to appropriate modules
                if parts[0] in db_admin_endpoints.COMMANDS:
                    await db_admin_endpoints.handle_command(db, parts)
                elif parts[0] in user_endpoints.COMMANDS:
                    await user_endpoints.handle_command(db, parts)
                elif parts[0] in manga_endpoints.COMMANDS:
                    await manga_endpoints.handle_command(db, parts)
                elif parts[0] in chapter_endpoints.COMMANDS:
                    await chapter_endpoints.handle_command(db, parts)
                elif parts[0] in page_endpoints.COMMANDS:
                    await page_endpoints.handle_command(db, parts)
                else:
                    print("Invalid command. Type 'help' for available commands.")

            except IndexError:
                print("Insufficient arguments for this command.")
            except ValueError:
                print("Error parsing number. Check your arguments.")
            except Exception as e:
                print(f"Error: {e}")

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

    await db.close()
    print("Disconnected. Goodbye!")


if __name__ == "__main__":
    asyncio.run(repl())
