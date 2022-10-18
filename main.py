"""This is it folks. Lets play."""


import os
from shutil import get_terminal_size
from sys import argv

from simple_term_menu import TerminalMenu  # pip install simple-term-menu

from src.chess import Chess

TERMINAL_COLS = get_terminal_size().columns
TERMINAL_ROWS = get_terminal_size().lines

SINGLE_SEPARATOR = "─" * TERMINAL_COLS
DOUBLE_SEPARATOR = "═" * TERMINAL_COLS

MENU_CONFIGURATION = {
#   "accept_keys": DEFAULT_ACCEPT_KEYS,
    "clear_menu_on_exit": True,
    "clear_screen": True,
#   "cursor_index": None,
#   "cycle_cursor": DEFAULT_CYCLE_CURSOR,
#   "exit_on_shortcut": DEFAULT_EXIT_ON_SHORTCUT,
    "menu_cursor": "",
#   "menu_cursor_style": DEFAULT_MENU_CURSOR_STYLE,
    "menu_highlight_style": (
        "fg_red",
    ),
#   "multi_select": DEFAULT_MULTI_SELECT,
#   "multi_select_cursor": DEFAULT_MULTI_SELECT_CURSOR,
#   "multi_select_cursor_brackets_style": DEFAULT_MULTI_SELECT_CURSOR_BRACKETS_STYLE,
#   "multi_select_cursor_style": DEFAULT_MULTI_SELECT_CURSOR_STYLE,
#   "multi_select_empty_ok": False,
#   "multi_select_keys": DEFAULT_MULTI_SELECT_KEYS,
#   "multi_select_select_on_accept": DEFAULT_MULTI_SELECT_SELECT_ON_ACCEPT,
#   "preselected_entries": None,
#   "preview_border": DEFAULT_PREVIEW_BORDER,
#   "preview_command": None,
#   "preview_size": DEFAULT_PREVIEW_SIZE,
#   "preview_title": DEFAULT_PREVIEW_TITLE,
#   "quit_keys": DEFAULT_QUIT_KEYS,
#   "raise_error_on_interrupt": False,
#   "search_case_sensitive": DEFAULT_SEARCH_CASE_SENSITIVE,
#   "search_highlight_style": DEFAULT_SEARCH_HIGHLIGHT_STYLE,
#   "search_key": DEFAULT_SEARCH_KEY,
#   "shortcut_brackets_highlight_style": DEFAULT_SHORTCUT_BRACKETS_HIGHLIGHT_STYLE,
#   "shortcut_key_highlight_style": DEFAULT_SHORTCUT_KEY_HIGHLIGHT_STYLE,
#   "show_multi_select_hint": DEFAULT_SHOW_MULTI_SELECT_HINT,
#   "show_multi_select_hint_text": None,
#   "show_search_hint": DEFAULT_SHOW_SEARCH_HINT,
#   "show_search_hint_text": None,
#   "show_shortcut_hints": DEFAULT_SHOW_SHORTCUT_HINTS,
#   "show_shortcut_hints_in_status_bar": DEFAULT_SHOW_SHORTCUT_HINTS_IN_STATUS_BAR,
#   "skip_empty_entries": False,
#   "status_bar": None,
#   "status_bar_below_preview": DEFAULT_STATUS_BAR_BELOW_PREVIEW,
#   "status_bar_style": DEFAULT_STATUS_BAR_STYLE,
    "title": "CHESS" + "\n" + DOUBLE_SEPARATOR,
}


def status(entry: str) -> str:
    """Get description of meny entry with index.

    Args:
        index: Of the menu entry.

    Returns:
        Description string.
    """
    return SINGLE_SEPARATOR + "\n" + {
        "♚ NEW GAME": "Start a new (2-player) game of chess.",
        "♞ LOAD GAME": "Load game from a file with a list of input moves.",
        "♟ EXIT": "Exit the game.",
    }[entry]


if __name__ == "__main__":
    entry = -1

    while entry is not None and entry != 2:
        menu = TerminalMenu(
            [
                "♚ NEW GAME",
                "♞ LOAD GAME",
                "♟ EXIT",
            ],
            status_bar=status,
        **MENU_CONFIGURATION)
        entry = menu.show()

        try:
            if entry == 0:
                new_game = Chess()

                while not new_game.termination:
                    new_game.turn()

            if entry == 1:
                saved_prefix = "./saves"
                saved_menu = [file for (_, _, filenames) in os.walk(saved_prefix) for file in filenames]
                saved_entry = TerminalMenu(saved_menu, **MENU_CONFIGURATION).show()

                new_game = Chess(game_file=os.path.join(saved_prefix, saved_menu[saved_entry]))  # type: ignore

                while not new_game.termination:
                    new_game.turn()

        except KeyboardInterrupt:
            continue
