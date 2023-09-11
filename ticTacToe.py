#ticTacToe.py

def clearBoard(currentBoard, fill = " "):
    """clearBoard(currentBoard, fill = " ") clears the input board. Optionally with a different fill (default is space) """
    currentBoard.clear()
    for i in range(9):
        currentBoard.append(fill)

def printBoard(currentBoard = [0,1,2,3,4,5,6,7,8]):
    """printBoard(currentBoard = [0,1,2,3,4,5,6,7,8]) prints a board with the integers 0-8 filling each space. Optionally, insert your own board to print."""
    for i in range(9):
        if(i == 2 or i == 5 or i == 8):
            print("|", currentBoard[i], "|")
        else:
            print("|", currentBoard[i], end = " ")

def alreadyTaken(currentBoard, move):
    """alreadyTaken(currentBoard, move) returns true if a move has already been played (X or O) on the board."""
    if (move >= 0 or move <= 8):
        if (currentBoard[move] == "X" or currentBoard[move] == "O"):
            return True
    return False

def evaluateGame(currentBoard):
    """evaluateGame(currentBoard) determines if X or O won the game on the given board."""
    validWins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]
    for i in range(8):
        if (currentBoard[validWins[i][0]] == "X" and currentBoard[validWins[i][1]] == "X" and currentBoard[validWins[i][2]] == "X"):
            return "X"
        elif (currentBoard[validWins[i][0]] == "O" and currentBoard[validWins[i][1]] == "O" and currentBoard[validWins[i][2]] == "O"):
            return "O"
    return "Tie" if currentBoard.count(" ") == 0 else "Open"

def computerMove(currentBoard):
    """computerMove(currentBoard) runs an algorithm to fill in the O move."""

    #TODO replace call to min max
    for i in range(9):
        if (currentBoard[i] == " "):
            currentBoard[i] = "O"
            break

def ticTacToe():
    """ticTacToe() plays a game of tic-tac-toe on the console."""

    # create and populate a blank board
    currentBoard = []
    clearBoard(currentBoard)

    # greet the player
    print("Welcome to Tic-Tac-Toe!")
    print("You\'ll be playing against the computer.")
    print("Play the game by selecting any box via its corrisponding value:")
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

ticTacToe() #play the game!
