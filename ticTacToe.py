#ticTacToe.py

from typing import List
import os

INITIAL_BOARD: List[str] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
COLOR_RED: str = "31"
COLOR_GREEN: str = "32"
COLOR_GRAY: str = "90"
COLOR_YELLOW = "33"
POSITION_MIN: int = 0
POSITION_MAX: int = 8
CELL_COUNT: int = 9
NOT_FOUND: int = -1
LAST_MOVE_POSITION: int = NOT_FOUND

def clearConsole() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def printHint(text: str) -> None:
    print(color(text, COLOR_GRAY))

def color(text: str, color: str) -> str:
    "returns the input text with the input color."""
    return "\033[" + color + "m" + text + "\033[0m"

def get_available_positions(board: List[int]) -> List[int]:
    """returns a list of available moves on the current board."""
    available_positions = []

    for i in range(CELL_COUNT):
        if board[i] == " ":
            available_positions.append(i)

    return available_positions

def minimax(board: List[str], depth: int, is_maximizing_player: bool) -> int:
    WIN_SCORE = 10
    board_evaluation = evaluate_board(board)
    is_board_in_terminal_state = board_evaluation != "Open"

    # Base case: if the game is over, return the score.
    if depth == 0 or is_board_in_terminal_state:
        if board_evaluation == "X":
            return WIN_SCORE - depth
        elif board_evaluation == "O":
            return depth - WIN_SCORE
        else:
            # Tie has no score.
            return 0

    comparator = max if is_maximizing_player else min
    best_score = -float("inf") if is_maximizing_player else float("inf")

    for available_position in get_available_positions(board):
        previous_position_value = board[available_position]
        board[available_position] = "O" if is_maximizing_player else "X"
        score = minimax(board, depth - 1, not is_maximizing_player)
        board[available_position] = previous_position_value
        best_score = comparator(best_score, score)

    return best_score

def clear_board(board: List[str], fill = " ") -> None:
    """clearBoard(currentBoard, fill = " ") clears the input board. Optionally with a different fill (default is space) """
    board.clear()

    for _ in range(CELL_COUNT):
        board.append(fill)

def print_board(board: List[str] = INITIAL_BOARD) -> None:
    """printBoard(currentBoard = [0,1,2,3,4,5,6,7,8]) prints a board with the integers 0-8 filling each space. Optionally, insert your own board to print."""
    BOARD_BORDER_CHAR = "|"

    for i in range(CELL_COUNT):
        character = color(str(i), COLOR_GRAY)

        if LAST_MOVE_POSITION == i:
            character = color(board[i], COLOR_YELLOW)
        elif board[i] == "X":
            character = color(board[i], COLOR_RED)
        elif board[i] == "O":
            character = color(board[i], COLOR_GREEN)

        if (i == 2 or i == 5 or i == 8):
            print(BOARD_BORDER_CHAR, character, BOARD_BORDER_CHAR)
        else:
            print(BOARD_BORDER_CHAR, character, end = " ")

def is_position_already_taken(board: List[str], position: int) -> bool:
    """alreadyTaken(currentBoard, move) returns true if a move has already been played (X or O) on the board."""
    assert position >= POSITION_MIN and position <= POSITION_MAX, "position should be between 0 and 8"

    return board[position] != " "

def evaluate_board(board: List[str]) -> str:
    """evaluateGame(currentBoard) determines if X or O won the game on the given board."""
    validWins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]
    for i in range(POSITION_MAX):
        if board[validWins[i][0]] == "X" and board[validWins[i][1]] == "X" and board[validWins[i][2]] == "X":
            return "X"
        elif board[validWins[i][0]] == "O" and board[validWins[i][1]] == "O" and board[validWins[i][2]] == "O":
            return "O"

    return "Tie" if board.count(" ") == 0 else "Open"

def computer_move(board: List[str]) -> None:
    """computerMove(currentBoard) runs an algorithm to fill in the O move."""

    bestMovePosition = NOT_FOUND
    bestScore = -float("inf")
    available_positions = get_available_positions(board)

    # If there are no available positions, the computer cannot make a
    # move anywhere.
    if len(available_positions) == 0:
        return

    for availablePosition in available_positions:
        board[availablePosition] = "O"
        moveScore = minimax(board, len(available_positions), False)

        # reset the available position to its original state to prevent
        # contamination of the board.
        board[availablePosition] = " "

        if moveScore > bestScore:
            bestScore = moveScore
            bestMovePosition = availablePosition

    assert bestMovePosition != NOT_FOUND, "a computer move should always be found when there are available positions"
    board[bestMovePosition] = "O"

def play_move(board: List[str], position: int, player: str) -> None:
    """playMove(currentBoard, move, player) plays the input move on the board for the input player."""
    assert position >= 0 and position <= 8, "position should be between 0 and 8"
    board[position] = player

def ask_yes_or_no_question(question: str) -> bool:
    print(question + " [y/n]: ", end = "")
    response = input()

    # Recur if the response is invalid.
    if response != "y" and response != "n":
        return ask_yes_or_no_question(question)

    return response == "y"

def handle_whether_to_play_again(board: List[str], game_state: str) -> None:
    if game_state == "Open":
        return

    # Print how the game ended.
    if (game_state == "X"):
        print("Beat the computer! X wins.")
    elif (game_state == "O"):
        print("Beaten by a computer! O wins.")
    else:
        print("Game was a tie.")

    print_board(board)
    replayResponse = ask_yes_or_no_question("Play another game?")

    if replayResponse == "n":
        exit(0)
    else:
        clear_board(board)
        print("New Game! Here are your board options:")
        print_board()

def next_round(board: List[str]) -> None:
    # take the players move
    input_player_move = NOT_FOUND

    while input_player_move < 0 or input_player_move > 8 or is_position_already_taken(board, input_player_move):
        print("Player, you are X, select a move (0-8): ", end="")
        input_player_move = input()
        clearConsole()
        input_player_move = NOT_FOUND if input_player_move.isdigit() == False else int(input_player_move)

    play_move(board, input_player_move, "X")
    board_state = evaluate_board(board)

    # If the game ended, ask if the player wishes to play again.
    if board_state != "Open":
        handle_whether_to_play_again(board, board_state)
    # If the game is still open, play the computers move.
    else:
        computer_move(board)
        printHint("O's move:")
        print_board(board)
        board_state = evaluate_board(board)
        next_round(board)

def start_game() -> None:
    """ticTacToe() plays a game of tic-tac-toe on the console."""

    # Create and populate a blank board.
    board = []
    clear_board(board)

    # Greet the player, only once at the start of the game.
    printHint("Welcome to Tic-Tac-Toe!")
    printHint("You\'ll be playing against the computer.")
    printHint("Play the game by selecting any box via its corresponding value.")
    print_board()
    next_round(board)

start_game()
