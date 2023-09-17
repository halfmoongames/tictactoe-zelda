import os
import sys
import tic_tac_toe
import flask
from typing import Optional

COLOR_RED: str = "31"
COLOR_GREEN: str = "32"
COLOR_GRAY: str = "90"
COLOR_YELLOW: str = "33"

sessions: dict[str, list[str]] = {}

def create_session_id() -> str:
    SESSION_ID_GENERATION_SIZE = 3

    return os.urandom(SESSION_ID_GENERATION_SIZE).hex()

def create_session(id: str) -> Optional[list[str]]:
    if id in sessions:
        return None

    board = tic_tac_toe.create_blank_board()

    sessions[id] = board

    return board

def reset_session(id: str) -> bool:
    if id not in sessions:
        return False

    sessions[id] = tic_tac_toe.create_blank_board()

    return True

def destroy_session(id: str) -> bool:
    if id not in sessions:
        return False

    del sessions[id]

    return True

def create_session_response(id: str) -> flask.Response:
    return flask.jsonify({
        "id": id,
        "error": ""
    })

def create_play_response(computer_move_position: int | None, board_state: str) -> flask.Response:
    return flask.jsonify({
        "computerMovePosition": -1 if computer_move_position is None else computer_move_position + 1,
        "boardState": board_state,
        "error": ""
    })

def create_fail_play_response(message: str) -> flask.Response:
    return flask.jsonify({
        "computerMovePosition": -1,
        "boardState": "",
        "error": message,
    })

def log(text: str) -> None:
    print(color(text, COLOR_GRAY))

def log_session(session_id: str, text: str) -> None:
    print(color("[", COLOR_GRAY) + color(session_id, COLOR_YELLOW) + color("]", COLOR_GRAY), color(text, COLOR_GRAY))

def color(text: str, color: str) -> str:
    """Returns the input text with the input color."""
    # Do not colorize if the terminal does not support color.
    if not does_terminal_support_color():
        return text

    return "\033[" + color + "m" + text + "\033[0m"

def rainbow(text: str) -> str:
    """Returns the input text with a rainbow color."""
    RAINBOW_COLORS = ["31", "33", "32", "34", "35", "36"]

    return "".join([color(text[i], RAINBOW_COLORS[i % len(RAINBOW_COLORS)]) for i in range(len(text))])

def validate_position(position: int) -> bool:
    return 1 <= position <= tic_tac_toe.CELL_COUNT

def does_terminal_support_color() -> bool:
    # Check if STDOUT is a terminal.
    if not sys.stdout.isatty():
        return False

    # On Windows, ANSI escape sequences are not supported.
    if os.name == "nt":
        return False

    # Check for `TERM` environment variable.
    term = os.environ.get("TERM", "")

    # Common terminals that support color.
    color_terms = ["xterm", "xterm-color", "xterm-256color", "linux", "cygwin"]

    return term in color_terms

def print_board(board: list[str], last_move_position: int) -> None:
    """Prints the given board, along with the integers 1-9 filling each empty cell."""
    BOARD_BORDER_CHAR = "|"
    BOARD_SIZE = 3

    for i in range(tic_tac_toe.CELL_COUNT):
        cell_char = color(str(i + 1), COLOR_GRAY)

        if last_move_position == i:
            cell_char = color(board[i], COLOR_YELLOW)
        elif board[i] == tic_tac_toe.CELL_X:
            cell_char = color(board[i], COLOR_RED)
        elif board[i] == tic_tac_toe.CELL_O:
            cell_char = color(board[i], COLOR_GREEN)

        is_last_column = (i + 1) % BOARD_SIZE == 0

        if is_last_column:
            print(BOARD_BORDER_CHAR, cell_char, BOARD_BORDER_CHAR)
        else:
            print(BOARD_BORDER_CHAR, cell_char, end = " ")
