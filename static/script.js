const Const = {
  BOARD_STATE_X_WINS: "X wins",
  BOARD_STATE_O_WINS: "O wins",
  BOARD_STATE_TIE: "Tie",
  BOARD_STATE_OPEN: "Open",
  CELL_X: "X",
  CELL_O: "O",
  CELL_EMPTY: "",
  CELL_QUERY_SELECTOR: "#board > button[data-position]",
  NONE: -1
}

const config = {
  sessionId: null,
  reloadAfterGameEndsTimeoutMs: 2000
}

function setCell(position, value) {
  assert(value == Const.CELL_X || value == Const.CELL_O, "Value should be X or O")
  assertPositionIsValid(position)

  const $cell = $getCellForPosition(position)

  $cell.innerText = value
  $cell.disabled = true
}

function assertPositionIsValid(position) {
  assert(position >= 1 && position <= 9, "Position should be in the range of 1-9")
}

function assert(condition, reasoning) {
  if (!condition)
    throw new Error("Assertion failed: " + reasoning)
}

function $getCellForPosition(position) {
  assertPositionIsValid(position)

  return document.querySelector(`#board > button[data-position="${position}"]`)
}

async function makePlayRequest(position) {
  const response = await fetch("/play", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      sessionId: config.sessionId,
      position
    })
  })

  if (!response.ok)
    throw new Error("Failed to make play request", response.status, response.statusText)

  return response.json()
}

function attachCellClickEvent($cell) {
  const position = parseInt($cell.dataset.position)

  assert(position >= 1 && position <= 9, "Cell position should be in the range of 1-9")
  console.log("Sent play request for position", position)
  setCell(position, Const.CELL_X)

  makePlayRequest(position).then(response => {
    console.log("Received play response", response)

    // If there was an error, display it to the user.
    if (response.error) {
      alert(response.error)
      setCell(position, Const.CELL_EMPTY)

      return
    }

    // Otherwise, update the board with both the player's and computer's moves.
    if (response.computerMovePosition != Const.NONE)
      setCell(response.computerMovePosition, Const.CELL_O)

    // If the game ended, display the result to the user, and reload the page.
    if (response.boardState !== Const.BOARD_STATE_OPEN) {
      document.querySelectorAll(Const.CELL_QUERY_SELECTOR).forEach($cell => $cell.disabled = true)

      setTimeout(() => {
        alert(response.boardState)
        location.reload()
      }, config.reloadAfterGameEndsTimeoutMs)
    }
  })
}

function attachEventListeners() {
  const $cells = document.querySelectorAll(Const.CELL_QUERY_SELECTOR)

  assert($cells.length == 9, "There should be 9 board buttons")

  for (const $cell of $cells) {
    assert($cell.innerText == "", "Each cell should initially be empty")
    $cell.addEventListener("click", () => attachCellClickEvent($cell))
  }

  console.log("Attached event listeners to board cells")
}

async function fetchNewSessionId() {
  const response = await fetch("/session/create", {method: "POST"})

  if (!response.ok)
    throw new Error("Failed to fetch new session id", response.status, response.statusText)

  const json = await response.json()

  if (!json.id)
    throw new Error("Failed to fetch new session id", "Response did not contain a session id")

  return json.id
}

window.addEventListener("load", () => {
  console.log("Script loaded")
  console.log("Fetching new session id")

  fetchNewSessionId()
    .then(sessionId => {
      console.log("Received new session id", sessionId)
      config.sessionId = sessionId
    })
    .then(() => attachEventListeners())
})
