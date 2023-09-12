#ticTacToe.py

from typing import List

INITIAL_BOARD: List[str] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

def getAvailablePositions(currentBoard: List[int]) -> List[int]:
    """returns a list of available moves on the current board."""
    availableMoves = []

    for i in range(9):
        if currentBoard[i] == " ":
            availableMoves.append(i)

    return availableMoves

def minimax(currentBoard: List[str], depth: int, isMaximizingPlayer: bool) -> int:
    WIN_SCORE = 10

    gameEvaluation = evaluateGame(currentBoard)
    isBoardInTerminalState = gameEvaluation != "Open"

    # Base case: if the game is over, return the score.
    if depth == 0 or isBoardInTerminalState:
        if gameEvaluation == "X":
            return WIN_SCORE - depth
        elif gameEvaluation == "O":
            return depth - WIN_SCORE
        else:
            # Tie has no score.
            return 0

    comparator = max if isMaximizingPlayer else min
    bestScore = -float("inf") if isMaximizingPlayer else float("inf")

    for availablePosition in getAvailablePositions(currentBoard):
        previousPositionValue = currentBoard[availablePosition]
        currentBoard[availablePosition] = "O" if isMaximizingPlayer else "X"
        score = minimax(currentBoard, depth - 1, not isMaximizingPlayer)
        currentBoard[availablePosition] = previousPositionValue
        bestScore = comparator(bestScore, score)

    return bestScore

def clearBoard(currentBoard: List[str], fill = " ") -> None:
    """clearBoard(currentBoard, fill = " ") clears the input board. Optionally with a different fill (default is space) """
    currentBoard.clear()

    for _ in range(9):
        currentBoard.append(fill)

def printBoard(currentBoard: List[str] = INITIAL_BOARD) -> None:
    """printBoard(currentBoard = [0,1,2,3,4,5,6,7,8]) prints a board with the integers 0-8 filling each space. Optionally, insert your own board to print."""
    for i in range(9):
        if (i == 2 or i == 5 or i == 8):
            print("|", currentBoard[i], "|")
        else:
            print("|", currentBoard[i], end = " ")

def alreadyTaken(currentBoard: List[str], move: int) -> bool:
    """alreadyTaken(currentBoard, move) returns true if a move has already been played (X or O) on the board."""
    if (move >= 0 and move <= 8):
        if (currentBoard[move] == "X" or currentBoard[move] == "O"):
            return True

    return False

def evaluateGame(currentBoard: List[str]) -> str:
    """evaluateGame(currentBoard) determines if X or O won the game on the given board."""
    validWins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]
    for i in range(8):
        if (currentBoard[validWins[i][0]] == "X" and currentBoard[validWins[i][1]] == "X" and currentBoard[validWins[i][2]] == "X"):
            return "X"
        elif (currentBoard[validWins[i][0]] == "O" and currentBoard[validWins[i][1]] == "O" and currentBoard[validWins[i][2]] == "O"):
            return "O"

    return "Tie" if currentBoard.count(" ") == 0 else "Open"

def computerMove(currentBoard: List[str]) -> None:
    """computerMove(currentBoard) runs an algorithm to fill in the O move."""

    bestMovePosition = -1
    bestScore = -float("inf")
    availablePositions = getAvailablePositions(currentBoard)

    for availablePosition in availablePositions:
        currentBoard[availablePosition] = "O"
        moveScore = minimax(currentBoard, len(availablePositions), False)

        # reset the available position to its original state to prevent
        # contamination of the board.
        currentBoard[availablePosition] = " "

        if moveScore > bestScore:
            bestScore = moveScore
            bestMovePosition = availablePosition

    assert bestMovePosition != -1, "a move should always be found"
    currentBoard[bestMovePosition] = "O"

def playGame() -> None:
    """ticTacToe() plays a game of tic-tac-toe on the console."""

    # create and populate a blank board
    currentBoard = []
    clearBoard(currentBoard)

    # greet the player
    print("Welcome to Tic-Tac-Toe!")
    print("You\'ll be playing against the computer.")
    print("Play the game by selecting any box via its corresponding value:")
    printBoard()

    # starts the game
    playMore = True

    while(playMore):
        # take the players move
        move = -1
        while(move < 0 or move > 8 or alreadyTaken(currentBoard, move)):
            print("Player, you are X, select a move (0-8): ",end="")
            move = input()
            move = -1 if move.isdigit() == False else int(move)

        # plays the input move
        currentBoard[move] = "X"
        print("Current board:")
        printBoard(currentBoard)
        gameState = evaluateGame(currentBoard)

        # if the game is still open, play the computers move
        if (gameState == "Open"):
            computerMove(currentBoard)
            print("O's move:")
            printBoard(currentBoard)
            gameState = evaluateGame(currentBoard)

        # if the game ended, ask if the player wishes to play again.
        if(gameState != "Open"):
            # print how the game ended.
            if (gameState == "X"):
                print("Beat the computer! X wins.")
            elif (gameState == "O"):
                print("Beaten by a computer! O wins.")
            else:
                print("Game was a tie.")

            replayResponse = "no response"

            while(replayResponse != "y" and replayResponse != "n"):
                print("Play another game? y/n: ",end = "")
                replayResponse = input()
            if replayResponse == "n":
                playMore = False
            else:
                clearBoard(currentBoard)
                print("New Game! Here are your board options:")
                printBoard()

playGame()
