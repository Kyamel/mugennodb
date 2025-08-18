#!/usr/bin/env python3

# main.py
import asyncio
from shlex import split
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import NestedCompleter, WordCompleter, Completer
from typing import Dict, List

from app.endpoints import (
    user_endpoints,
    manga_endpoints,
    chapter_endpoints,
    page_endpoints,
    db_admin_endpoints,
    tag_endpoints,
    country_endpoints,
    related_manga_endpoints,
    manga_genre_endpoints,
    review_endpoints,
    read_endpoints,
)
from app.load_env import get_database_dsn
from mugennodb.conection.asyncpg_database import AsyncPGDatabase
from app import help_command

db = AsyncPGDatabase(dsn=get_database_dsn())


class HybridCompleter(Completer):
    def __init__(self, commands: Dict[str, Dict]):
        self.nested = NestedCompleter.from_nested_dict(
            self._build_nested_structure(commands)
        )
        self.positional_args = self._build_positional_args(commands)
        self.optional_args = self._build_optional_args(commands)

    def _build_nested_structure(self, commands: Dict[str, Dict]) -> Dict:
        """Build nested structure for commands and positional arguments."""
        structure = {}
        for cmd, info in commands.items():
            args = info.get("args", [])
            positional = [arg.split(":")[0] + "=" for arg in args if not arg.startswith("--")]
            structure[cmd] = {arg: None for arg in positional}
        return structure

    def _build_positional_args(self, commands: Dict[str, Dict]) -> Dict[str, List[str]]:
        """Build dictionary of positional (required) arguments for each command."""
        positional = {}
        for cmd, info in commands.items():
            args = info.get("args", [])
            positional[cmd] = [arg.split(":")[0] + "=" for arg in args if not arg.startswith("--")]
        return positional

    def _build_optional_args(self, commands: Dict[str, Dict]) -> Dict[str, List[str]]:
        """Build dictionary of optional arguments (starting with '--') for each command."""
        optional = {}
        for cmd, info in commands.items():
            args = info.get("args", [])
            optional[cmd] = [arg.split(":")[0] + "=" for arg in args if arg.startswith("--")]
        return optional

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.split()

        if not text:
            # No input yet: suggest all commands
            yield from self.nested.get_completions(document, complete_event)
            return

        cmd = text[0]

        # If unknown command, fallback
        if cmd not in self.positional_args:
            yield from self.nested.get_completions(document, complete_event)
            return

        positional = self.positional_args.get(cmd, [])
        optional = self.optional_args.get(cmd, [])

        num_args_typed = len(text) - 1  # excluding command itself

        # If still missing positional arguments, only suggest positional args (nested)
        if num_args_typed < len(positional):
            yield from self.nested.get_completions(document, complete_event)
            return

        # All required positional args typed, suggest optional args not used yet
        used_opts = {arg.split("=")[0] + "=" for arg in text[1:] if arg.startswith("--")}
        remaining_opts = [opt for opt in optional if opt not in used_opts]

        if remaining_opts:
            word_completer = WordCompleter(remaining_opts)
            yield from word_completer.get_completions(document, complete_event)



def setup_completer():
    all_commands = {
        **user_endpoints.COMMANDS,
        **manga_endpoints.COMMANDS,
        **chapter_endpoints.COMMANDS,
        **page_endpoints.COMMANDS,
        **db_admin_endpoints.COMMANDS,
        **tag_endpoints.COMMANDS,
        **country_endpoints.COMMANDS,
        **related_manga_endpoints.COMMANDS,
        **manga_genre_endpoints.COMMANDS,
        **review_endpoints.COMMANDS,
        **read_endpoints.COMMANDS,
    }

    all_commands.update(
        {
            "help": {"description": "Show help", "args": []},
            "exit": {"description": "Exit the REPL", "args": []},
            "quit": {"description": "Exit the REPL", "args": []},
        }
    )

    return HybridCompleter(all_commands)


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

            parts = split(cmd_text) # Split command into parts respecting quotes
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
                elif parts[0] in tag_endpoints.COMMANDS:
                    await tag_endpoints.handle_command(db, parts)
                elif parts[0] in country_endpoints.COMMANDS:
                    await country_endpoints.handle_command(db, parts)
                elif parts[0] in related_manga_endpoints.COMMANDS:
                    await related_manga_endpoints.handle_command(db, parts)
                elif parts[0] in manga_genre_endpoints.COMMANDS:
                    await manga_genre_endpoints.handle_command(db, parts)
                elif parts[0] in review_endpoints.COMMANDS:
                    await review_endpoints.handle_command(db, parts)
                elif parts[0] in read_endpoints.COMMANDS:   
                    await read_endpoints.handle_command(db, parts)
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
