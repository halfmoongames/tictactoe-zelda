import os
import tic_tac_toe
import aux
import logging
import flask

app = flask.Flask(__name__)

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/session/create", methods=["POST"])
def createSession():
    id = aux.create_session_id()

    assert id not in aux.sessions, "Session ID should not already exist (collision?)"
    aux.create_session(id)
    aux.log_session(id, "Created session")

    return aux.create_session_response(id)

@app.route("/play", methods=["POST"])
def gameGateway():
    POSITION_PROP_KEY = "position"
    SESSION_ID_PROP_KEY = "sessionId"

    if not flask.request.is_json:
        return aux.create_fail_play_response("Invalid request body format (expected JSON)")

    data = flask.request.get_json()
    required_properties = [SESSION_ID_PROP_KEY, POSITION_PROP_KEY]

    for required_property_key in required_properties:
        if required_property_key not in data:
            aux.log("Request was missing required '" + required_property_key + "' property")

            return aux.create_fail_play_response("Invalid request body format (expected JSON with property '" + required_property_key + "')")

    player_position: int = data[POSITION_PROP_KEY]

    if not aux.validate_position(player_position):
        aux.log("Player tried to play at position " + str(player_position) + ", but it was invalid")

        return aux.create_fail_play_response("Invalid position (expected 1-9)")

    adjusted_player_position = player_position - 1
    session_id = str(data[SESSION_ID_PROP_KEY])

    if session_id not in aux.sessions:
        aux.log("Received a request with an invalid session id; ignoring")

        return aux.create_fail_play_response("Invalid session ID")

    board = aux.sessions[session_id]

    if tic_tac_toe.is_position_already_taken(board, adjusted_player_position):
        aux.log_session(session_id, "Tried to play at position " + str(adjusted_player_position) + ", but it was already taken")

        return aux.create_fail_play_response("Position already taken")

    computer_move_position, board_state = tic_tac_toe.next(adjusted_player_position, board)
    last_move_position = computer_move_position if computer_move_position is not None else adjusted_player_position

    aux.log_session(session_id, "Player played at position " + str(adjusted_player_position) + ".")
    aux.log_session(session_id, "Computer played at position " + str(computer_move_position) + ".")
    aux.log_session(session_id, "Board state: " + board_state)
    aux.print_board(board, last_move_position)

    if board_state != tic_tac_toe.BOARD_STATE_OPEN:
        aux.log_session(session_id, "Game over; resetting session")
        aux.reset_session(session_id)

        return aux.create_play_response(computer_move_position, board_state)

    assert computer_move_position is not None, "Computer move position should be defined when the game is still in progress"

    return aux.create_play_response(computer_move_position, board_state)

# Application entry point.
if __name__ == "__main__":
    is_debug_mode = "DEBUG_MODE" in os.environ
    logger = logging.getLogger("werkzeug")

    # Only log errors in the console.
    logger.setLevel(logging.ERROR)

    aux.log("Backend ready; awaiting requests")
    app.run(debug=is_debug_mode)
