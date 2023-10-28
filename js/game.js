const POSITION_MIN = 0
const POSITION_MAX = 8
const CELL_COUNT = 9
const NOT_FOUND = -1
const CELL_EMPTY = " "
const CELL_X = "X"
const CELL_O = "O"
const BOARD_STATE_OPEN = "Open"
const BOARD_STATE_TIE = "Tie"
const BOARD_STATE_X_WINS = "X wins"
const BOARD_STATE_O_WINS = "O wins"
const TIME_FACTOR_MS = 1000

function assert(condition) {
  if (!condition) {
    const failureMessage = `assertion failed: ${condition}`

    alert(failureMessage)

    throw failureMessage
  }
}

function assertPlayerIsValid(player) {
  const VALID_PLAYERS = [CELL_X, CELL_O]

  assert(VALID_PLAYERS.includes(player), "player should be one of the valid players (either X or O)")
}

function assertPositionIsValid(position) {
  assert(POSITION_MIN <= position <= POSITION_MAX, "position should be between 0 and 8")
}

function getAvailablePositions(board) {
  const available_positions = []

  for (let i = 0; i < CELL_COUNT; i++) {
    if (board[i] == CELL_EMPTY)
      available_positions.push(i)
  }

  return available_positions
}

function minimax_aux(
  board,
  depth,
  is_maximizing,
  player,
  alpha,
  beta,
  use_alpha_beta_pruning
) {
  BIAS_SCORE = 10

  assert(depth >= 0, "depth should be non-negative")
  assertPlayerIsValid(player)

  board_state = evaluateBoard(board)
  is_board_in_terminal_state = board_state != BOARD_STATE_OPEN

  // Base case: if the game is over in this recursion branch
  // compute the score and return it.
  if (depth == 0 || is_board_in_terminal_state) {
    if (board_state == BOARD_STATE_TIE)
      // Tie has no score.
      return 0, 1

    winner = board_state == BOARD_STATE_X_WINS ? CELL_X : CELL_O
    is_positive_outcome = (player == winner && is_maximizing) || (player != winner && !is_maximizing)
    multiplier = is_positive_outcome ? 1 : -1

    // Penalize deeper depth if maximizing, or reward deeper depth if minimizing.
    // This will encourage the algorithm to win/lose (depending on whether maximizing
    // or not) as quickly as possible.
    depth_score = is_maximizing ? -depth : depth

    return multiplier * BIAS_SCORE + depth_score, 1
  }

  comparator = is_maximizing ? max : min
  best_score = is_maximizing ? -float("inf") : float("inf")
  total_call_count = 0
  for (const available_position of getAvailablePositions(board)) {
    assert(board[available_position] == CELL_EMPTY, "available position should be empty")
    board[available_position] = player

    score, call_count = minimax_aux(
      board,
      depth - 1,
      // Inversion occurs because this emulates the other player's turn.
      // In other words, this emulates a turn change.
      !is_maximizing,
      player == CELL_X ? CELL_O : CELL_X,
      alpha,
      beta,
      use_alpha_beta_pruning
    )

    // Restore the board to its original state to prevent contamination.
    board[available_position] = CELL_EMPTY

    best_score = comparator(best_score, score)
    total_call_count += call_count

    // Update alpha and beta values.
    if (is_maximizing)
      alpha = max(alpha, best_score)
    else
      beta = min(beta, best_score)

    // Apply alpha-beta pruning.
    if (use_alpha_beta_pruning && alpha >= beta)
      break
  }

  return (best_score, total_call_count + 1)
}

function minimax(
  board,
  depth,
  is_maximizing,
  player,
  use_alpha_beta_pruning
) {
  assertPlayerIsValid(player)

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
}

function createBlankBoard() {
  const board = []

  for (let i = 0; i < CELL_COUNT; i++) {
    board.push(CELL_EMPTY)
  }

  return board
}

function isPositionAlreadyTaken(board, position) {
  assertPositionIsValid(position)

  return board[position] != CELL_EMPTY
}

function evaluateBoard(board) {
  const WIN_PATTERNS = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]
  let someoneDidWin = false

  for (let i = 0; i < WIN_PATTERNS.length; i++) {
    positions = [WIN_PATTERNS[i][0], WIN_PATTERNS[i][1], WIN_PATTERNS[i][2]]
    someoneDidWin = board[positions[0]] == board[positions[1]] == board[positions[2]] != CELL_EMPTY
  }

  if (someoneDidWin)
    // Choose the winner based on the symbol at the first
    // position in the win pattern.
    return board[positions[0]] == CELL_X ? BOARD_STATE_X_WINS : BOARD_STATE_O_WINS

  // If there are no empty cells, the game is a tie.
  // Otherwise, the game is still open.
  return board.count(CELL_EMPTY) == 0 ? BOARD_STATE_TIE : BOARD_STATE_OPEN
}

function calculateComputerMove(board) {
  const available_positions = getAvailablePositions(board)

  // If there are no available positions, the computer cannot make a
  // move anywhere.
  if (available_positions.length == 0)
    return NOT_FOUND

  best_move_position = NOT_FOUND
  best_score = -float("inf")

  for (const available_position of available_positions)
    board[available_position] = CELL_O

  // Since the computer has made a move already on the current
  // available position, it is now the player's turn, and it is
  // being minimized.
  move_score, _ = minimax(board, len(available_positions), False, CELL_X, True)

  // Reset the available position to its original state to prevent
  // contamination of the board.
  board[available_position] = CELL_EMPTY

  if (move_score > best_score)
    best_score = move_score

  best_move_position = available_position
  assert(best_move_position != NOT_FOUND, "a computer move should always be found when there are available positions")

  return best_move_position
}

function perform_move(board, position, player) {
  assertPlayerIsValid(player)
  assertPositionIsValid(position)
  board[position] = player
}

function next(player_move_position, board) {
  perform_move(board, player_move_position, CELL_X)

  next_board_state = evaluateBoard(board)

  // If the game ended after the player moved, finalize the game.
  if (next_board_state != BOARD_STATE_OPEN)
    return (None, next_board_state)

  assert(len(getAvailablePositions(board)) > 0, "there should be at least one available position on the board if the game is still open")

  computer_move_position = calculateComputerMove(board)

  perform_move(board, computer_move_position, CELL_O)
  next_board_state = evaluateBoard(board)

  return (computer_move_position, next_board_state)
}
