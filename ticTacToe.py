#ticTacToe.py

import os
import sys

COLOR_RED: str = "31"
COLOR_GREEN: str = "32"
COLOR_GRAY: str = "90"
COLOR_YELLOW = "33"
POSITION_MIN: int = 0
POSITION_MAX: int = 8
CELL_COUNT: int = 9
NOT_FOUND: int = -1
CELL_EMPTY: str = " "
CELL_X: str = "X"
CELL_O: str = "O"
BOARD_STATE_OPEN: str = "Open"
BOARD_STATE_TIE: str = "Tie"
BOARD_STATE_X_WINS: str = "X wins"
BOARD_STATE_O_WINS: str = "O wins"
last_move_position: int = NOT_FOUND

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

def clear_screen() -> None:
    # On Windows, the `cls` command will clear the screen.
    if os.name == "nt":
        os.system("cls")
    # On Linux and Mac, the `clear` command will clear the screen.
    else:
        os.system("clear")

def print_hint(text: str) -> None:
    print(color(text, COLOR_GRAY))

def color(text: str, color: str) -> str:
    "returns the input text with the input color."""
    # Do not colorize if the terminal does not support color.
    if not does_terminal_support_color():
        return text

    return "\033[" + color + "m" + text + "\033[0m"

def get_available_positions(board: list[int]) -> list[int]:
    """returns a list of available moves on the current board."""
    available_positions = []

    for i in range(CELL_COUNT):
        if board[i] == CELL_EMPTY:
            available_positions.append(i)

    return available_positions

def minimax(board: list[str], depth: int, is_maximizing_player: bool) -> int:
    WIN_SCORE = 10
    board_state = evaluate_board(board)
    is_board_in_terminal_state = board_state != BOARD_STATE_OPEN

    # Base case: if the game is over, return the score.
    if depth == 0 or is_board_in_terminal_state:
        if board_state == BOARD_STATE_X_WINS:
            return WIN_SCORE - depth
        elif board_state == BOARD_STATE_O_WINS:
            return depth - WIN_SCORE
        else:
            # Tie has no score.
            return 0

    comparator = max if is_maximizing_player else min
    best_score = -float("inf") if is_maximizing_player else float("inf")

    for available_position in get_available_positions(board):
        previous_position_value = board[available_position]
        board[available_position] = CELL_O if is_maximizing_player else CELL_X
        score = minimax(board, depth - 1, not is_maximizing_player)
        board[available_position] = previous_position_value
        best_score = comparator(best_score, score)

    return best_score

def clear_board(board: list[str], fill = CELL_EMPTY) -> None:
    """clears the input board. Optionally with a different fill (default is space)"""
    board.clear()

    for _ in range(CELL_COUNT):
        board.append(fill)

def print_board(board: list[str]) -> None:
    """prints a board with the integers 0-8 filling each space. Optionally, insert your own board to print."""
    global last_move_position

    BOARD_BORDER_CHAR = "|"

    for i in range(CELL_COUNT):
        character = color(str(i), COLOR_GRAY)

        if last_move_position == i:
            character = color(board[i], COLOR_YELLOW)
        elif board[i] == CELL_X:
            character = color(board[i], COLOR_RED)
        elif board[i] == CELL_O:
            character = color(board[i], COLOR_GREEN)

        if i == 2 or i == 5 or i == 8:
            print(BOARD_BORDER_CHAR, character, BOARD_BORDER_CHAR)
        else:
            print(BOARD_BORDER_CHAR, character, end = " ")

def is_position_already_taken(board: list[str], position: int) -> bool:
    """returns true if a move has already been played (X or O) on the board."""
    assert position >= POSITION_MIN and position <= POSITION_MAX, "position should be between 0 and 8"

    return board[position] != CELL_EMPTY

def evaluate_board(board: list[str]) -> str:
    """determines if X or O won the game on the given board."""
    possible_win_patterns = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]

    for i in range(POSITION_MAX):
        positions = [possible_win_patterns[i][0], possible_win_patterns[i][1], possible_win_patterns[i][2]]
        is_win = board[positions[0]] == board[positions[1]] == board[positions[2]] != CELL_EMPTY

        if is_win:
            return board[positions[0]]

    return BOARD_STATE_TIE if board.count(CELL_EMPTY) == 0 else BOARD_STATE_OPEN

def computer_move(board: list[str]) -> None:
    """computerMove(currentBoard) runs an algorithm to fill in the O move."""

    best_move_position = NOT_FOUND
    best_score = -float("inf")
    available_positions = get_available_positions(board)

    # If there are no available positions, the computer cannot make a
    # move anywhere.
    if len(available_positions) == 0:
        return

    for available_position in available_positions:
        board[available_position] = CELL_O
        move_score = minimax(board, len(available_positions), False)

        # reset the available position to its original state to prevent
        # contamination of the board.
        board[available_position] = CELL_EMPTY

        if move_score > best_score:
            best_score = move_score
            best_move_position = available_position

    assert best_move_position != NOT_FOUND, "a computer move should always be found when there are available positions"
    play_move(board, best_move_position, CELL_O)

def play_move(board: list[str], position: int, player: str) -> None:
    """playMove(currentBoard, move, player) plays the input move on the board for the input player."""
    global last_move_position

    assert position >= 0 and position <= 8, "position should be between 0 and 8"
    last_move_position = position
    board[position] = player

def ask_yes_or_no_question(question: str) -> bool:
    YES: str = "y"
    NO: str = "n"

    print(question + color(" [y/n]: ", COLOR_GRAY), end = "")
    response = input()

    # Recur if the response is invalid.
    if response != YES and response != NO:
        return ask_yes_or_no_question(question)

    return response == YES

def handle_whether_to_play_again(board: list[str], game_state: str) -> None:
    # The game hasn't ended yet. Nothing to do here.
    if game_state == BOARD_STATE_OPEN:
        return

    # Print how the game ended.
    if game_state == BOARD_STATE_X_WINS:
        print_hint("Beat the computer! X wins.")
    elif game_state == BOARD_STATE_O_WINS:
        print_hint("Beaten by a computer! O wins.")
    else:
        print_hint("Game was a tie.")

    print_board(board)
    player_wants_to_replay = ask_yes_or_no_question("Play another game?")

    if player_wants_to_replay:
        clear_board(board)
        print("New Game! Here are your board options:")
        print_board(board)
    else:
        print_hint("Thanks for playing!")
        exit(0)

def next_round(board: list[str]) -> None:
    input_player_move = NOT_FOUND

    while input_player_move < 0 or input_player_move > 8 or is_position_already_taken(board, input_player_move):
        print("Player, you are X, select a move (0-8): ", end="")
        input_player_move = input()
        clear_screen()
        input_player_move = NOT_FOUND if input_player_move.isdigit() == False else int(input_player_move)

    play_move(board, input_player_move, CELL_X)
    board_state = evaluate_board(board)

    # If the game ended, ask if the player wishes to play again.
    if board_state != "Open":
        handle_whether_to_play_again(board, board_state)
    # If the game is still open, play the computers move.
    else:
        computer_move(board)
        print_hint("O's move:")
        print_board(board)
        board_state = evaluate_board(board)
        next_round(board)

# Entry point; starts the game.
if __name__ == "__main__":
    # Create and populate a blank board.
    board = []
    clear_board(board)

    # Greet the player, only once at the start of the game.
    print_hint("Welcome to Tic-Tac-Toe!")
    print_hint("You\'ll be playing against the computer.")
    print_hint("Play the game by selecting any box via its corresponding value.")
    print_board(board)
    next_round(board)
