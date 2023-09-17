from flask import Flask
from flask import request
from flask import render_template
import os
import tic_tac_toe
import aux

app = Flask(__name__)
board = tic_tac_toe.create_blank_board()

@app.route("/")
def index():
    if request.method != "GET":
        return "Invalid request method"

    return render_template("index.html")

@app.route("/play", methods=["POST"])
def gameGateway():
    global board

    POSITION_PROP_KEY = "position"

    if not request.is_json:
        return "Invalid request body format (expected JSON)"

    data = request.get_json()

    if POSITION_PROP_KEY not in data:
        aux.print_hint("Player tried to play, but the request body did not contain the '" + POSITION_PROP_KEY + "' property")

        return "Invalid request body format (expected JSON with property '" + POSITION_PROP_KEY + "')"

    player_position: int = data[POSITION_PROP_KEY]

    if not aux.validate_position(player_position):
        aux.print_hint("Player tried to play at position " + str(player_position) + ", but it was invalid")

        return "Invalid position (expected 1-9)"

    adjusted_player_position = player_position - 1

    if tic_tac_toe.is_position_already_taken(board, adjusted_player_position):
        aux.print_hint("Player tried to play at position " + str(adjusted_player_position) + ", but it was already taken")

        return "Position already taken"

    computer_move_position, board_state = tic_tac_toe.next(adjusted_player_position, board)
    last_move_position = computer_move_position if computer_move_position is not None else adjusted_player_position

    aux.print_hint("Player played at position " + str(adjusted_player_position) + ".")
    aux.print_hint("Computer played at position " + str(computer_move_position) + ".")
    aux.print_hint("Board state: " + board_state)
    aux.print_board(board, last_move_position)

    if board_state != tic_tac_toe.BOARD_STATE_OPEN:
        board = tic_tac_toe.create_blank_board()
        print(aux.rainbow("Game ended; board was reset"))

        return "Game over; " + board_state

    assert computer_move_position is not None, "Computer move position should be defined when the game is still in progress"

    return "Computer move: " + str(computer_move_position + 1)

if __name__ == "__main__":
    is_debug_mode = "DEBUG_MODE" in os.environ

    app.run(debug=is_debug_mode)
