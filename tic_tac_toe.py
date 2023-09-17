#ticTacToe.py

from typing import Optional

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
TIME_FACTOR_MS: int = 1000

def assert_player_is_valid(player: str) -> None:
    VALID_PLAYERS = [CELL_X, CELL_O]

    assert player in VALID_PLAYERS, "player should be one of the valid players (either X or O)"

def assert_position_is_valid(position: int) -> None:
    assert POSITION_MIN <= position <= POSITION_MAX, "position should be between 0 and 8"

def get_available_positions(board: list[str]) -> list[int]:
    """Returns a list of available moves (positions) on the given board."""
    available_positions: list[int] = []

    for i in range(CELL_COUNT):
        if board[i] == CELL_EMPTY:
            available_positions.append(i)

    return available_positions

def minimax_aux(
    board: list[str],
    depth: int,
    is_maximizing: bool,
    player: str,
    alpha: float,
    beta: float,
    use_alpha_beta_pruning: bool
) -> tuple[float, int]:
    BIAS_SCORE = 10

    assert depth >= 0, "depth should be non-negative"
    assert_player_is_valid(player)

    board_state = evaluate_board(board)
    is_board_in_terminal_state = board_state != BOARD_STATE_OPEN

    # Base case: if the game is over in this recursion branch
    # compute the score and return it.
    if depth == 0 or is_board_in_terminal_state:
        if board_state == BOARD_STATE_TIE:
            # Tie has no score.
            return 0, 1

        winner = CELL_X if board_state == BOARD_STATE_X_WINS else CELL_O
        is_positive_outcome = (player == winner and is_maximizing) or (player != winner and not is_maximizing)
        multiplier = 1 if is_positive_outcome else -1

        # Penalize deeper depth if maximizing, or reward deeper depth if minimizing.
        # This will encourage the algorithm to win/lose (depending on whether maximizing
        # or not) as quickly as possible.
        depth_score = -depth if is_maximizing else depth

        return multiplier * BIAS_SCORE + depth_score, 1

    comparator = max if is_maximizing else min
    best_score = -float("inf") if is_maximizing else float("inf")
    total_call_count = 0

    for available_position in get_available_positions(board):
        assert board[available_position] == CELL_EMPTY, "available position should be empty"
        board[available_position] = player

        score, call_count = minimax_aux(
            board,
            depth - 1,
            # Inversion occurs because this emulates the other player's turn.
            # In other words, this emulates a turn change.
            not is_maximizing,
            CELL_O if player == CELL_X else CELL_X,
            alpha,
            beta,
            use_alpha_beta_pruning
        )

        # Restore the board to its original state to prevent contamination.
        board[available_position] = CELL_EMPTY

        best_score = comparator(best_score, score)
        total_call_count += call_count

        # Update alpha and beta values.
        if is_maximizing:
            alpha = max(alpha, best_score)
        else:
            beta = min(beta, best_score)

        # Apply alpha-beta pruning.
        if use_alpha_beta_pruning and alpha >= beta:
            break

    return (best_score, total_call_count + 1)

def minimax(
    board: list[str],
    depth: int,
    is_maximizing: bool,
    player: str,
    use_alpha_beta_pruning: bool
) -> tuple[float, int]:
    assert_player_is_valid(player)

    alpha = -float("inf")
    beta = float("inf")

    return minimax_aux(
        board,
        depth,
        is_maximizing,
        player,
        alpha,
        beta,
        use_alpha_beta_pruning
    )

def create_blank_board() -> list[str]:
    board: list[str] = []

    for _ in range(CELL_COUNT):
        board.append(CELL_EMPTY)

    return board

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

def calculate_computer_move(board: list[str]) -> int:
    """Runs the minimax algorithm to perform the computer's move."""
    available_positions = get_available_positions(board)

    # If there are no available positions, the computer cannot make a
    # move anywhere.
    if len(available_positions) == 0:
        return NOT_FOUND

    best_move_position = NOT_FOUND
    best_score = -float("inf")

    for available_position in available_positions:
        board[available_position] = CELL_O

        # Since the computer has made a move already on the current
        # available position, it is now the player's turn, and it is
        # being minimized.
        move_score, _ = minimax(board, len(available_positions), False, CELL_X, True)

        # Reset the available position to its original state to prevent
        # contamination of the board.
        board[available_position] = CELL_EMPTY

        if move_score > best_score:
            best_score = move_score
            best_move_position = available_position

    assert best_move_position != NOT_FOUND, "a computer move should always be found when there are available positions"

    return best_move_position

def perform_move(board: list[str], position: int, player: str) -> None:
    """Plays the input move on the board for the input player."""
    assert_player_is_valid(player)
    assert_position_is_valid(position)
    board[position] = player

def next(player_move_position: int, board: list[str]) -> tuple[Optional[int], str]:
    perform_move(board, player_move_position, CELL_X)

    next_board_state = evaluate_board(board)

    # If the game ended after the player moved, finalize the game.
    if next_board_state != BOARD_STATE_OPEN:
        return (None, next_board_state)

    assert len(get_available_positions(board)) > 0, "there should be at least one available position on the board if the game is still open"

    computer_move_position = calculate_computer_move(board)

    perform_move(board, computer_move_position, CELL_O)
    next_board_state = evaluate_board(board)

    return (computer_move_position, next_board_state)
