#ticTacToe.py

import os
import sys
import time

COLOR_RED: str = "31"
COLOR_GREEN: str = "32"
COLOR_GRAY: str = "90"
COLOR_YELLOW: str = "33"
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
TIME_FACTOR_MS = 1000
IS_BENCHMARK_MODE: bool = "--benchmark" in sys.argv
BENCHMARK_RUNNING_TIME_S: int = 10

last_move_position: int = NOT_FOUND

def benchmark_step(use_alpha_beta_pruning: bool) -> None:
    board = []

    clear_board(board)
    board[0] = CELL_X

    start_time = time.time()

    for _ in range(CELL_COUNT):
        minimax(board, CELL_COUNT, False, use_alpha_beta_pruning)

    return (time.time() - start_time) * TIME_FACTOR_MS

def print_benchmark_results(
    naive_step_reference_time_ms: int,
    actual_benchmark_duration_s: int,
    iterations: int,
    with_alpha_beta_step_time_sum: int,
    without_alpha_beta_step_time_sum: int
) -> None:
    with_alpha_beta_time_avg = with_alpha_beta_step_time_sum / iterations
    without_alpha_beta_time_avg = without_alpha_beta_step_time_sum / iterations
    improvement_percentage = abs(with_alpha_beta_time_avg - without_alpha_beta_time_avg) / without_alpha_beta_time_avg * 100
    improvement_factor = without_alpha_beta_time_avg / with_alpha_beta_time_avg
    expected_benchmark_duration_s = naive_step_reference_time_ms * iterations / TIME_FACTOR_MS
    benchmark_duration_difference_percentage = abs(actual_benchmark_duration_s - expected_benchmark_duration_s) / expected_benchmark_duration_s * 100

    print_hint("Step iterations: " + str(iterations))
    print_hint("Average time per step [-alpha-beta pruning]: " + str(without_alpha_beta_time_avg) + "ms")
    print_hint("Average time per step [+alpha-beta pruning]: " + str(with_alpha_beta_time_avg) + "ms")
    print_hint("Improvement (%): " + str(improvement_percentage) + "%")
    print_hint("Improvement factor: " + str(improvement_factor) + "x")
    print_hint("Expected benchmark running time: " + str(expected_benchmark_duration_s) + "s")
    print_hint("Actual benchmark running time: " + str(actual_benchmark_duration_s) + "s")
    print_hint("Benchmark duration difference (%): " + str(benchmark_duration_difference_percentage) + "%")

def perform_benchmark_for_depth(depth: int, case_name: str) -> None:
    naive_step_reference_time_ms = benchmark_step(False)
    computed_iterations = int(BENCHMARK_RUNNING_TIME_S * TIME_FACTOR_MS / naive_step_reference_time_ms)

    print("Running " + color(case_name, COLOR_YELLOW) + " benchmark (depth=" + str(depth) + ")")

    benchmark_start_time = time.time()
    with_alpha_beta_step_time_sum = 0

    # Benchmark the minimax algorithm with alpha-beta pruning.
    for _ in range(computed_iterations):
        with_alpha_beta_step_time_sum += benchmark_step(True)

    # Benchmark the minimax algorithm without alpha-beta pruning.
    without_alpha_beta_step_time_sum = 0

    for _ in range(computed_iterations):
        without_alpha_beta_step_time_sum += benchmark_step(False)

    actual_benchmark_duration_s = time.time() - benchmark_start_time

    print_benchmark_results(naive_step_reference_time_ms, actual_benchmark_duration_s, computed_iterations, with_alpha_beta_step_time_sum, without_alpha_beta_step_time_sum)

def benchmark_minimax_alpha_beta() -> None:
    WORST_CASE_DEPTH: int = 9
    BEST_CASE_DEPTH: int = 1
    AVERAGE_CASE_DEPTH: int = (WORST_CASE_DEPTH + BEST_CASE_DEPTH) // 2

    print_hint("Benchmark mode enabled")
    print_hint("Running time per benchmark: " + str(BENCHMARK_RUNNING_TIME_S) + "s")
    perform_benchmark_for_depth(WORST_CASE_DEPTH, "worst-case")
    perform_benchmark_for_depth(BEST_CASE_DEPTH, "best-case")
    perform_benchmark_for_depth(AVERAGE_CASE_DEPTH, "average-case")

def assert_position_is_valid(position: int) -> None:
    assert POSITION_MIN <= position <= POSITION_MAX, "position should be between 0 and 8"

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
    """Clears the terminal screen, with multi-platform support."""
    # On Windows, the `cls` command will clear the screen.
    if os.name == "nt":
        os.system("cls")
    # On Linux and Mac, the `clear` command will clear the screen.
    else:
        os.system("clear")

def print_hint(text: str) -> None:
    print(color(text, COLOR_GRAY))

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

def get_available_positions(board: list[str]) -> list[int]:
    """Returns a list of available moves (positions) on the given board."""
    available_positions = []

    for i in range(CELL_COUNT):
        if board[i] == CELL_EMPTY:
            available_positions.append(i)

    return available_positions

def minimax_aux(
    board: list[str],
    depth: int,
    is_maximizing_player: bool,
    alpha: int,
    beta: int,
    use_alpha_beta_pruning: bool
) -> int:
    WIN_SCORE = 10
    board_state = evaluate_board(board)
    is_board_in_terminal_state = board_state != BOARD_STATE_OPEN

    # Base case: if the game is over, return the score.
    if depth == 0 or is_board_in_terminal_state:
        if board_state == BOARD_STATE_X_WINS:
            return depth - WIN_SCORE
        elif board_state == BOARD_STATE_O_WINS:
            return WIN_SCORE - depth
        else:
            # Tie has no score.
            return 0

    comparator = max if is_maximizing_player else min
    best_score = -float("inf") if is_maximizing_player else float("inf")
    phi = alpha if is_maximizing_player else beta

    for available_position in get_available_positions(board):
        previous_position_value = board[available_position]
        board[available_position] = CELL_O if is_maximizing_player else CELL_X
        score = minimax_aux(board, depth - 1, not is_maximizing_player, alpha, beta, use_alpha_beta_pruning)
        board[available_position] = previous_position_value
        best_score = comparator(best_score, score)
        phi = comparator(phi, best_score)

        # Apply alpha-beta pruning.
        if use_alpha_beta_pruning and beta <= alpha:
            break

    return best_score

def minimax(board: list[str], depth: int, is_maximizing_player: bool, use_alpha_beta_pruning: bool) -> int:
    alpha = -float("inf") if is_maximizing_player else float("inf")
    beta = float("inf") if is_maximizing_player else -float("inf")

    assert alpha != beta, "alpha and beta should not be equal"

    return minimax_aux(board, depth, is_maximizing_player, alpha, beta, use_alpha_beta_pruning)

def clear_board(board: list[str], fill = CELL_EMPTY) -> None:
    """Clears the input board. Optionally with a different fill (default is empty cell)."""
    VALID_FILL_VALUES = [CELL_EMPTY, CELL_X, CELL_O]

    assert fill in VALID_FILL_VALUES, "fill should be one of the valid fill values"
    board.clear()

    for _ in range(CELL_COUNT):
        board.append(fill)

def print_board(board: list[str]) -> None:
    """Prints the given board, along with the integers 1-9 filling each empty cell."""
    global last_move_position

    BOARD_BORDER_CHAR = "|"
    BOARD_SIZE = 3

    for i in range(CELL_COUNT):
        cell_char = color(str(i + 1), COLOR_GRAY)

        if last_move_position == i:
            cell_char = color(board[i], COLOR_YELLOW)
        elif board[i] == CELL_X:
            cell_char = color(board[i], COLOR_RED)
        elif board[i] == CELL_O:
            cell_char = color(board[i], COLOR_GREEN)

        is_last_column = (i + 1) % BOARD_SIZE == 0

        if is_last_column:
            print(BOARD_BORDER_CHAR, cell_char, BOARD_BORDER_CHAR)
        else:
            print(BOARD_BORDER_CHAR, cell_char, end = " ")

def is_position_already_taken(board: list[str], position: int) -> bool:
    """Returns true if a move has already been played (X or O) on the board."""
    assert_position_is_valid(position)

    return board[position] != CELL_EMPTY

def evaluate_board(board: list[str]) -> str:
    """Determines if player X or O won the game on the given board, or if the game was a tie or still open."""
    win_patterns = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]

    for i in range(len(win_patterns)):
        positions = [win_patterns[i][0], win_patterns[i][1], win_patterns[i][2]]
        someone_did_win = board[positions[0]] == board[positions[1]] == board[positions[2]] != CELL_EMPTY

        if someone_did_win:
            # Choose the winner based on the symbol at the first
            # position in the win pattern.
            return BOARD_STATE_X_WINS if board[positions[0]] == CELL_X else BOARD_STATE_O_WINS

    # If there are no empty cells, the game is a tie.
    # Otherwise, the game is still open.
    return BOARD_STATE_TIE if board.count(CELL_EMPTY) == 0 else BOARD_STATE_OPEN

def play_computer_move(board: list[str]) -> None:
    """Runs the minimax algorithm to perform the computer's move."""
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

        # Reset the available position to its original state to prevent
        # contamination of the board.
        board[available_position] = CELL_EMPTY

        if move_score > best_score:
            best_score = move_score
            best_move_position = available_position

    assert best_move_position != NOT_FOUND, "a computer move should always be found when there are available positions"
    perform_move(board, best_move_position, CELL_O)

def perform_move(board: list[str], position: int, player: str) -> None:
    """Plays the input move on the board for the input player."""
    global last_move_position

    VALID_PLAYERS = [CELL_X, CELL_O]

    assert player in VALID_PLAYERS, "player should be one of the valid players (either X or O)"
    assert_position_is_valid(position)
    last_move_position = position
    board[position] = player

def ask_yes_or_no_question(question: str) -> bool:
    YES: str = "y"
    NO: str = "n"

    print(question + color(" [y/n] → ", COLOR_GRAY), end = "")
    response = input().strip()

    # Recur if the response is invalid.
    if response != YES and response != NO:
        return ask_yes_or_no_question(question)

    return response == YES

def finalize_round(board: list[str]) -> None:
    global last_move_position

    board_state = evaluate_board(board)

    # The game hasn't ended yet. Nothing to do here.
    if board_state == BOARD_STATE_OPEN:
        return

    hint = "Game was a tie."

    if board_state == BOARD_STATE_X_WINS:
        hint = "You beat the computer! X wins."
    elif board_state == BOARD_STATE_O_WINS:
        hint = "You were beaten by a computer! O wins."

    # Print how the game ended.
    clear_screen()
    print_hint(hint)
    print_board(board)

    player_wants_to_replay = ask_yes_or_no_question("Play another game?")

    if player_wants_to_replay:
        last_move_position = NOT_FOUND
        clear_board(board)
        clear_screen()
        print_hint("New game started. Good luck!")
        next_round(board)
    else:
        print_hint("Thanks for playing!")
        exit(0)

def ask_player_for_move_position(board: list[str]) -> int:
    raw_player_move = ""
    was_selection_invalid = False

    while True:
        if was_selection_invalid:
            print_hint("Invalid selection. Please try again.")

        print_board(board)

        # Having the move position be one-indexed when displaying it
        # to the player is more intuitive for humans.
        print("Select a move (1-9) → ", end="")

        raw_player_move = input().strip()
        clear_screen()
        is_valid_position = raw_player_move.isdigit() and int(raw_player_move) >= 1 and int(raw_player_move) <= 9

        if not is_valid_position:
            was_selection_invalid = True

            continue

        # Adjust the move to be zero-indexed after reading it from the
        # player's input. This way, the one-indexed position is only
        # shown to the player, and the zero-indexed position is used
        # internally.
        adjusted_player_move_position = int(raw_player_move) - 1

        if is_position_already_taken(board, adjusted_player_move_position):
            was_selection_invalid = True

            continue

        assert_position_is_valid(adjusted_player_move_position)

        return adjusted_player_move_position

def next_round(board: list[str]) -> None:
    # Ask the player for their move, and perform it.
    player_move_position = ask_player_for_move_position(board)
    perform_move(board, player_move_position, CELL_X)

    # If the game ended, ask if the player wishes to play again.
    if evaluate_board(board) != BOARD_STATE_OPEN:
        finalize_round(board)

    play_computer_move(board)

    # Re-evaluate the board state after the computer's move.
    if evaluate_board(board) != BOARD_STATE_OPEN:
        finalize_round(board)
    # If the game is still open, continue to the next round.
    else:
        clear_screen()
        print_hint("The computer just played. Now it's your turn!")
        next_round(board)

# Entry point; starts the game.
if __name__ == "__main__":
    # If benchmarking mode is enabled, run the benchmark and exit.
    if IS_BENCHMARK_MODE:
        benchmark_minimax_alpha_beta()
        exit(0)

    # Create and populate a blank board.
    board = []
    clear_board(board)

    # Greet the player, only once at the start of the game.
    clear_screen()
    print(color("Welcome to", COLOR_GRAY), rainbow("Tic-Tac-Toe"))
    print_hint("You\'ll be playing against the computer.")
    print_hint("Play the game by selecting any box via its corresponding value.")
    next_round(board)
