from datetime import datetime
from typing import Dict, List, Optional

THEMES: Dict[str, Dict[str, str]] = {
    "classic": {
        "border": "\033[32m",
        "title": "\033[1;32m",
        "text": "\033[0m",
        "accent": "\033[36m",
        "warn": "\033[33m",
        "error": "\033[31m",
        "reset": "\033[0m",
    },
    "ocean": {
        "border": "\033[36m",
        "title": "\033[1;36m",
        "text": "\033[37m",
        "accent": "\033[33m",
        "warn": "\033[35m",
        "error": "\033[31m",
        "reset": "\033[0m",
    },
}

DEFAULT_THEME = "classic"


def get_theme(name: str) -> Dict[str, str]:
    return THEMES.get(name.lower(), THEMES[DEFAULT_THEME])


def available_themes() -> List[str]:
    return list(THEMES.keys())


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def style(text: str, color_code: str, theme_name: str = DEFAULT_THEME) -> str:
    theme = get_theme(theme_name)
    return f"{theme.get(color_code, '')}{text}{theme['reset']}"


def print_banner(title: str, subtitle: str = "", theme_name: str = DEFAULT_THEME) -> None:
    theme = get_theme(theme_name)
    width = 64
    border = theme["border"]
    title_col = theme["title"]
    reset = theme["reset"]

    print(f"{border}+{'-' * (width - 2)}+{reset}")
    print(f"{border}|{reset} {title_col}{title.center(width - 4)}{reset} {border}|{reset}")
    if subtitle:
        print(f"{border}|{reset} {subtitle.center(width - 4)} {border}|{reset}")
    print(f"{border}+{'-' * (width - 2)}+{reset}")


def print_dashboard(
    user: Optional[Dict[str, str]],
    counts: Dict[str, int],
    theme_name: str = DEFAULT_THEME,
) -> None:
    clear_screen()
    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    username = user["username"] if user else "Guest"
    role = user["role"].upper() if user else "NONE"

    print_banner("SCHOOL ATTENDANCE SYSTEM", "CSC 204-A TERMINAL EDITION", theme_name)
    print(style(f"  User     : {username} ({role})", "accent", theme_name))
    print(style(f"  Date/Time: {now}", "text", theme_name))
    print(
        style(
            f"  Records  : Students={counts.get('students', 0)} | "
            f"Subjects={counts.get('subjects', 0)} | "
            f"Attendance={counts.get('attendance', 0)}",
            "text",
            theme_name,
        )
    )
    print(style("-" * 64, "border", theme_name))


def print_menu(options: List[tuple[str, str]], theme_name: str = DEFAULT_THEME) -> None:
    for key, label in options:
        print(f"  {style(f'[{key}]', 'accent', theme_name)} {label}")
    print(style("-" * 64, "border", theme_name))


def print_table(
    headers: List[str],
    rows: List[List[str]],
    theme_name: str = DEFAULT_THEME,
) -> None:
    theme = get_theme(theme_name)
    border = theme["border"]
    reset = theme["reset"]

    if not rows:
        print(style("  No records found.", "warn", theme_name))
        return

    widths = [len(h) for h in headers]
    for row in rows:
        for idx, val in enumerate(row):
            if idx < len(widths):
                widths[idx] = max(widths[idx], len(str(val)))

    sep = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    header_line = (
        "| "
        + " | ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))
        + " |"
    )

    print(f"{border}{sep}{reset}")
    print(f"{border}{header_line}{reset}")
    print(f"{border}{sep}{reset}")
    for row in rows:
        line = (
            "| "
            + " | ".join(str(row[i]).ljust(widths[i]) for i in range(len(headers)))
            + " |"
        )
        print(f"{border}{line}{reset}")
    print(f"{border}{sep}{reset}")


def print_message(message: str, level: str = "text", theme_name: str = DEFAULT_THEME) -> None:
    print(style(f"  {message}", level, theme_name))


def pause(theme_name: str = DEFAULT_THEME) -> None:
    input(style("\n  Press Enter to continue...", "accent", theme_name))