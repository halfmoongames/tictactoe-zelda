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
BENCHMARK_ALLOWED_RUNNING_TIME_S: int = 10

last_move_position: int = NOT_FOUND

def benchmark_step(use_alpha_beta_pruning: bool) -> (int, int):
    board = new_blank_board()

    board[0] = CELL_X

    start_time = time.time()
    total_call_count = 0

    for _ in range(CELL_COUNT):
        _, call_count = minimax(board, CELL_COUNT, False, use_alpha_beta_pruning)

        total_call_count += call_count

    end_time = time.time()
    elapsed_time_ms = (end_time - start_time) * TIME_FACTOR_MS

    return (elapsed_time_ms, total_call_count)

def print_benchmark_results(
    naive_step_reference_time_ms: int,
    actual_benchmark_duration_s: int,
    iterations: int,
    with_alpha_beta_step_time_sum: int,
    with_alpha_beta_call_count: int,
    without_alpha_beta_step_time_sum: int,
    without_alpha_beta_call_count: int
) -> None:
    DECIMAL_PRECISION = 3

    with_alpha_beta_time_avg = round(with_alpha_beta_step_time_sum / iterations, DECIMAL_PRECISION)
    without_alpha_beta_time_avg = round(without_alpha_beta_step_time_sum / iterations, DECIMAL_PRECISION)
    improvement_percentage = round(abs(with_alpha_beta_call_count - without_alpha_beta_call_count) / without_alpha_beta_call_count * 100, DECIMAL_PRECISION)
    improvement_factor = round(without_alpha_beta_call_count / with_alpha_beta_call_count, DECIMAL_PRECISION)
    expected_benchmark_duration_s = round(naive_step_reference_time_ms * iterations / TIME_FACTOR_MS, DECIMAL_PRECISION)
    benchmark_duration_difference_percentage = round(abs(actual_benchmark_duration_s - expected_benchmark_duration_s) / expected_benchmark_duration_s * 100, DECIMAL_PRECISION)

    print_hint("Step iterations: " + str(iterations))
    print_hint("Call count [-alpha-beta pruning]: " + str(without_alpha_beta_call_count))
    print_hint("Call count [+alpha-beta pruning]: " + str(with_alpha_beta_call_count))
    print_hint("Avg. time per step [-alpha-beta pruning]: " + str(without_alpha_beta_time_avg) + "ms")
    print_hint("Avg. time per step [+alpha-beta pruning]: " + str(with_alpha_beta_time_avg) + "ms")
    print_hint("Improvement (%): " + str(improvement_percentage) + "%")
    print_hint("Improvement factor: " + str(improvement_factor) + "x")
    print_hint("Expected benchmark running time: " + str(expected_benchmark_duration_s) + "s")
    print_hint("Actual benchmark running time: " + str(round(actual_benchmark_duration_s, DECIMAL_PRECISION)) + "s")
    print_hint("Benchmark duration difference (%): " + str(benchmark_duration_difference_percentage) + "%")

def perform_benchmark_for_depth(depth: int, case_name: str) -> None:
    naive_step_reference_time_ms, _ = benchmark_step(False)
    computed_iterations = int(BENCHMARK_ALLOWED_RUNNING_TIME_S * TIME_FACTOR_MS / naive_step_reference_time_ms)

    print("Running " + color(case_name, COLOR_YELLOW) + " benchmark (depth=" + str(depth) + ")")

    benchmark_start_time = time.time()
    with_alpha_beta_step_time_sum = 0
    with_alpha_beta_call_count = 0

    # Benchmark the minimax algorithm with alpha-beta pruning.
    for _ in range(computed_iterations):
        elapsed_time, call_count = benchmark_step(True)

        with_alpha_beta_step_time_sum += elapsed_time
        with_alpha_beta_call_count += call_count

    # Benchmark the minimax algorithm without alpha-beta pruning.
    without_alpha_beta_step_time_sum = 0
    without_alpha_beta_call_count = 0

    for _ in range(computed_iterations):
        elapsed_time, call_count = benchmark_step(False)

        without_alpha_beta_step_time_sum += elapsed_time
        without_alpha_beta_call_count += call_count

    actual_benchmark_duration_s = time.time() - benchmark_start_time

    print_benchmark_results(
        naive_step_reference_time_ms,
        actual_benchmark_duration_s,
        computed_iterations,
        with_alpha_beta_step_time_sum,
        with_alpha_beta_call_count,
        without_alpha_beta_step_time_sum,
        without_alpha_beta_call_count
    )

def benchmark_minimax_alpha_beta() -> None:
    WORST_CASE_DEPTH: int = 9
    BEST_CASE_DEPTH: int = 1

    average_case_depth = (WORST_CASE_DEPTH + BEST_CASE_DEPTH) // 2

    print_hint("Benchmark mode enabled")
    print_hint("Allowed running time per benchmark case: " + str(BENCHMARK_ALLOWED_RUNNING_TIME_S) + "s")
    perform_benchmark_for_depth(WORST_CASE_DEPTH, "worst-case")
    perform_benchmark_for_depth(BEST_CASE_DEPTH, "best-case")
    perform_benchmark_for_depth(average_case_depth, "average-case")

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
    is_maximizing_player_o: bool,
    alpha: int,
    beta: int,
    use_alpha_beta_pruning: bool
) -> (int, int):
    BIAS_SCORE = 10

    assert depth >= 0, "depth should be non-negative"

    board_state = evaluate_board(board)
    is_board_in_terminal_state = board_state != BOARD_STATE_OPEN

    # Base case: if the game is over in this recursion branch
    # compute the score and return it.
    if depth == 0 or is_board_in_terminal_state:
        encouragement = BIAS_SCORE + depth
        penalty = -(BIAS_SCORE + depth)

        if board_state == BOARD_STATE_X_WINS:
            score = penalty if is_maximizing_player_o else encouragement

            return score, 1
        elif board_state == BOARD_STATE_O_WINS:
            score = encouragement if is_maximizing_player_o else penalty

            return score, 1
        else:
            # Tie has no score.
            return 0, 1

    comparator = max if is_maximizing_player_o else min
    best_score = -float("inf") if is_maximizing_player_o else float("inf")
    total_call_count = 0

    for available_position in get_available_positions(board):
        # Save the value of the current position, so that it can be
        # restored after the recursive call.
        original_value = board[available_position]

        board[available_position] = CELL_O if is_maximizing_player_o else CELL_X

        score, call_count = minimax_aux(
            board,
            depth - 1,
            # Inversion occurs because this emulates the other player's turn.
            # In other words, this emulates a turn change.
            not is_maximizing_player_o,
            alpha,
            beta,
            use_alpha_beta_pruning
        )

        board[available_position] = original_value
        best_score = comparator(best_score, score)
        total_call_count += call_count

        # Update alpha and beta values.
        if is_maximizing_player_o:
            alpha = max(alpha, best_score)
        else:
            beta = min(beta, best_score)

        # Apply alpha-beta pruning.
        # if use_alpha_beta_pruning and alpha >= beta:
        #     break

    return (best_score, total_call_count + 1)

def minimax(
    board: list[str],
    depth: int,
    is_maximizing_player_o: bool,
    use_alpha_beta_pruning: bool
) -> (int, int):
    alpha = -float("inf")
    beta = float("inf")

    return minimax_aux(
        board,
        depth,
        is_maximizing_player_o,
        alpha,
        beta,
        use_alpha_beta_pruning
    )

def new_blank_board() -> list[str]:
    board = []

    for _ in range(CELL_COUNT):
        board.append(CELL_EMPTY)

    return board

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

        move_score, _ = minimax(board, len(available_positions), True, True)

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

def finalize_game(board: list[str]) -> None:
    global last_move_position

    board_state = evaluate_board(board)

    # The game hasn't ended yet. Nothing to do here.
    if board_state == BOARD_STATE_OPEN:
        return

    ending_state_hint = "Game was a tie."

    if board_state == BOARD_STATE_X_WINS:
        ending_state_hint = "You beat the computer! X wins."
    elif board_state == BOARD_STATE_O_WINS:
        ending_state_hint = "You were beaten by a computer! O wins."

    # Print how the game ended.
    clear_screen()
    print_hint(ending_state_hint)
    print_board(board)

    player_wants_to_replay = ask_yes_or_no_question("Play another game?")

    if player_wants_to_replay:
        last_move_position = NOT_FOUND
        clear_screen()
        print_hint("New game started. Good luck!")
        next_round(new_blank_board())
    else:
        print_hint("Thanks for playing!")
        exit(0)

def ask_player_for_move_position(board: list[str]) -> int:
    was_selection_invalid = False

    while True:
        if was_selection_invalid:
            print_hint("Invalid selection. Please try again.")

        print_board(board)

        # Having the move position be one-indexed when displaying it
        # to the player is more intuitive for humans.
        print("Select a move (1-9) → ", end="")

        one_based_player_move = input().strip()
        clear_screen()

        is_valid_position = one_based_player_move.isdigit() and \
            int(one_based_player_move) >= 1 and int(one_based_player_move) <= 9

        if not is_valid_position:
            was_selection_invalid = True

            continue

        # Adjust the move to be zero-indexed after reading it from the
        # player's input. This way, the one-indexed position is only
        # shown to the player, and the zero-indexed position is used
        # internally.
        adjusted_player_move_position = int(one_based_player_move) - 1

        if is_position_already_taken(board, adjusted_player_move_position):
            was_selection_invalid = True

            continue

        assert_position_is_valid(adjusted_player_move_position)

        return adjusted_player_move_position

def next_round(board: list[str]) -> None:
    # Ask the player for their move, and perform it.
    player_move_position = ask_player_for_move_position(board)
    perform_move(board, player_move_position, CELL_X)

    # If the game ended after the player moved, finalize the game.
    if evaluate_board(board) != BOARD_STATE_OPEN:
        return finalize_game(board)

    assert len(get_available_positions(board)) > 0, "there should be at least one available position on the board if the game is still open"
    play_computer_move(board)

    # Re-evaluate the board state after the computer's move.
    if evaluate_board(board) != BOARD_STATE_OPEN:
        finalize_game(board)
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
    board = new_blank_board()

    # Greet the player, only once at the start of the game.
    clear_screen()
    print(color("Welcome to", COLOR_GRAY), rainbow("Tic-Tac-Toe"))
    print_hint("You\'ll be playing against the computer.")
    print_hint("Play the game by selecting any box via its corresponding value.")
    next_round(board)
