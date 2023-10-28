
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

    aux.log_session(session_id, "Player played at position " + str(adjusted_player_position))
    aux.log_session(session_id, "Computer played at position " + str(computer_move_position))
    aux.log_session(session_id, "Board state: " + board_state)
    aux.print_board(board, last_move_position)

    if board_state != tic_tac_toe.BOARD_STATE_OPEN:
        aux.log_session(session_id, "Game over; resetting session")
        aux.reset_session(session_id)

        return aux.create_play_response(computer_move_position, board_state)

    assert computer_move_position is not None, "Computer move position should be defined when the game is still in progress"

    return aux.create_play_response(computer_move_position, board_state)
