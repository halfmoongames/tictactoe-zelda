const Const = {
  BOARD_STATE_X_WINS: "X wins",
  BOARD_STATE_O_WINS: "O wins",
  BOARD_STATE_TIE: "Tie",
  BOARD_STATE_OPEN: "Open",
  CELL_X: "X",
  CELL_O: "O",
  CELL_EMPTY: "",
  CELL_QUERY_SELECTOR: ".cell",
  NONE: -1,
  AUDIO_FEEDBACK: "feedback",
  AUDIO_THEME_MUSIC: "background-music",
  AUDIO_NAVI_LISTEN: "navi-listen",
  AUDIO_KOROK_APPEARS: "korok-appears",
  AUDIO_GOT_ITEM: "got-item",
  AUDIO_CHEST: "chest",
  COVER_QUERY_SELECTOR: "#cover",
  WRAPPER_QUERY_SELECTOR: ".wrapper",
  COVER_LABEL_QUERY_SELECTOR: "#cover > label",
  MESSAGE_COVER_SELECTOR: "#message-cover",
  CELL_WRAPPER_QUERY_SELECTOR: ".cell-wrapper",
  COVER_SHOW_CLASS: "show"
}

const config = {
  sessionId: null,
  roundEndTimeout: 4000,
  roundEndScreenShowDelay: 1000,
  themeMusicDelay: 2000,
  coverLabelFadeTime: 1000,
  coverFadeTime: 3000,
  simulatedComputerMoveDelay: 1000,
}

const state = {
  audioCache: {},
  isUserInteractionDisabled: false
}

function performMove(position, player) {
  assert(player == Const.CELL_X || player == Const.CELL_O, "Value should be X or O")
  assertPositionIsValid(position)

  const $cell = $getCellForPosition(position)

  // Trigger animation on the parent wrapper.
  const $wrapper = $cell.parentElement

  $wrapper.classList.add("click")
  $cell.innerText = player
  $cell.disabled = true
  playAudio(Const.AUDIO_FEEDBACK)
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

  return document.querySelector(`button[data-position="${position}"].cell`)
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

async function resetGame() {
  document.querySelector(Const.MESSAGE_COVER_SELECTOR)
    .classList
    .remove(Const.COVER_SHOW_CLASS)

  document.querySelectorAll(Const.CELL_QUERY_SELECTOR).forEach($cell => {
    $cell.innerText = Const.CELL_EMPTY
    $cell.disabled = false
  })

  state.isUserInteractionDisabled = false
}

function handleCellClickEvent($cell) {
  if (state.isUserInteractionDisabled)
    return

  state.isUserInteractionDisabled = true

  const position = parseInt($cell.dataset.position)

  assert(position >= 1 && position <= 9, "Cell position should be in the range of 1-9")
  console.log("Sent play request for position", position)
  performMove(position, Const.CELL_X)

  makePlayRequest(position).then(response => {
    console.log("Received play response", response)

    // If there was an error, display it to the user.
    if (response.error) {
      alert(response.error)
      window.location.reload()

      return
    }

    // Otherwise, update the board with the computer's move.
    if (response.computerMovePosition != Const.NONE)
      setTimeout(() => {
        performMove(response.computerMovePosition, Const.CELL_O)


        if (response.boardState === Const.BOARD_STATE_OPEN)
          state.isUserInteractionDisabled = false
      }, config.simulatedComputerMoveDelay)

    // If the game ended, display the result to the user, and reload the page.
    if (response.boardState !== Const.BOARD_STATE_OPEN) {
      const $messageCover = document.querySelector(Const.MESSAGE_COVER_SELECTOR)

      $messageCover.innerText = response.boardState
      document.querySelectorAll(Const.CELL_QUERY_SELECTOR).forEach($cell => $cell.disabled = true)

      setTimeout(() => {
        $messageCover.classList.add(Const.COVER_SHOW_CLASS)

        const audioEffectName = response.boardState === Const.BOARD_STATE_TIE
          ? Const.AUDIO_NAVI_LISTEN
          : response.boardState === Const.BOARD_STATE_X_WINS
            ? Const.AUDIO_GOT_ITEM
            : Const.AUDIO_CHEST

        playAudio(audioEffectName)

        setTimeout(() => resetGame(), config.roundEndTimeout)
      }, config.roundEndScreenShowDelay)
    }
  })
}

function attachEventListeners() {
  const $cells = document.querySelectorAll(Const.CELL_QUERY_SELECTOR)

  assert($cells.length == 9, "There should be 9 board buttons")

  for (const $cell of $cells) {
    assert($cell.innerText == "", "Each cell should initially be empty")
    $cell.addEventListener("click", () => handleCellClickEvent($cell))
  }

  const $cellWrappers = document.querySelectorAll(Const.CELL_WRAPPER_QUERY_SELECTOR)

  for (const $cellWrapper of $cellWrappers)
    $cellWrapper.addEventListener("animationend", () => $cellWrapper.classList.remove("click"))

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

function playAudio(name) {
  if (state.audioCache[name] === undefined)
    state.audioCache[name] = new Audio(`/assets/audio/${name}.mp3`)

  const audio = state.audioCache[name]

  // Reset the audio to the beginning, and play it.
  // This is so that the audio can be played multiple times in a row,
  // just in case that the audio is played at rapid succession.
  audio.currentTime = 0

  audio.play()

  return audio
}

function initialize() {
  console.log("Fetching new session id")

  fetchNewSessionId()
    .then(sessionId => {
      console.log("Received new session id", sessionId)
      config.sessionId = sessionId
    })
    .then(() => attachEventListeners())

  // Initialize Vanilla tilt for the 3D effect on the board.
  VanillaTilt.init(document.querySelectorAll(Const.CELL_QUERY_SELECTOR), {
    max: 25,
    speed: 400
  })

  setTimeout(() => {
    const themeMusicAudio = playAudio(Const.AUDIO_THEME_MUSIC)

    // Loop the theme music.
    themeMusicAudio.loop = true
  }, 1000)
}

function handleFirstUserInteraction() {
  window.removeEventListener("click", handleFirstUserInteraction)
  playAudio(Const.AUDIO_KOROK_APPEARS)
  console.log("Received user interaction; initializing game")

  const $coverLabel = document.querySelector(Const.COVER_LABEL_QUERY_SELECTOR)

  $coverLabel.classList.add("fade")

  // Fade out the cover after the label has faded out.
  setTimeout(() => {
    document.querySelector(Const.COVER_QUERY_SELECTOR).classList.add("fade")
  }, config.coverLabelFadeTime)

  // Fade in the board after the cover has faded out.
  setTimeout(() => {
    document.querySelector(Const.WRAPPER_QUERY_SELECTOR).classList.add("animate")
  }, config.coverLabelFadeTime + config.coverFadeTime)

  initialize()
}

window.addEventListener("load", () => console.log("Script loaded; awaiting user interaction"))
window.addEventListener("click", handleFirstUserInteraction)
