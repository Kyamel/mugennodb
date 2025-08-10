from app.endpoints import (
    user_endpoints,
    manga_endpoints,
    chapter_endpoints,
    page_endpoints,
    db_admin_endpoints,
    tag_endpoints,
)


def print_command_section(title: str, commands: dict, title_color: str):
    BLUE = "\033[34m"
    RESET = "\033[0m"

    print(f"\n{title_color}{title}:{RESET}")
    for cmd, desc in commands.items():
        print(f"  {BLUE}{cmd.ljust(20)}{RESET} {desc['description']}")
        if "args" in desc:
            args_str = ", ".join(desc["args"])
            print(f"    Args:    {args_str}")
        if "example" in desc:
            print(f"    Example: {desc['example']}")


def show_help() -> None:
    BLUE = "\033[34m"
    GREEN = "\033[32m"
    RESET = "\033[0m"

    print_command_section("Admin Commands", db_admin_endpoints.COMMANDS, GREEN)
    print_command_section("User Commands", user_endpoints.COMMANDS, GREEN)
    print_command_section("Manga Commands", manga_endpoints.COMMANDS, GREEN)
    print_command_section("Chapter Commands", chapter_endpoints.COMMANDS, GREEN)
    print_command_section("Page Commands", page_endpoints.COMMANDS, GREEN)
    print_command_section("Tag Commands", tag_endpoints.COMMANDS, GREEN)

    print(f"\n{GREEN}General Commands:{RESET}")
    print(f"  {BLUE}help".ljust(20) + f"{RESET}Show this help message")
    print(f"  {BLUE}exit/quit".ljust(20) + f"{RESET}Exit the program")
