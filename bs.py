
SQUARE_TYPE = {"NONE": " ", "HIT": "X", "MISS": "O"}
TOP_ROW_INDEX = 1
BOTTOM_ROW_INDEX = 10
RIGHTMOST_COLUMN_INDEX = 10
MAX_COLUMNS = 10
MAX_ROWS = 10

# BOARD STYLING
letters = "ABCDEFGHIJ"
boxPadding = "|      "
rowPadding = (boxPadding * 10) + "|\n"
boxBorder = "  |" + ("-" * 69) + "|\n"


def appendLetters(output):
    output += "   "
    for i in range(10):
        output += "   " + letters[i] + "   "
    output += "\n"
    return output


def newBoard():
    board = []
    for rows in range(MAX_ROWS):
        newRow = []
        for columns in range(MAX_COLUMNS):
            newRow.append({"ship": None, "type": SQUARE_TYPE["NONE"]})
        board.append(newRow)
    return board


def printBoard(board, showShips):
    if not currentState["visibleBoard"]:
        return
    boardOutput = "\n"
    boardOutput = appendLetters(boardOutput)
    boardOutput += boxBorder

    for row in range(MAX_ROWS):
        boardOutput += "  " + rowPadding
        if row + 1 > 9:
            boardOutput += str(row + 1) + ""
        else:
            boardOutput += str(row + 1) + " "

        for column in range(MAX_COLUMNS):
            spot = board[row][column]
            boxChar = ""
            if showShips and spot["ship"]:
                boxChar = spot["ship"]
            else:
                boxChar = spot["type"]
            boardOutput += "|   " + str(boxChar) + "  "

        boardOutput += "| " + str(row + 1) + "\n"
        boardOutput += "  " + rowPadding
        boardOutput += boxBorder

    boardOutput = appendLetters(boardOutput)
    print(boardOutput)


def getNewState():
    return {
        "visibleBoard": True,
        "player1Turn": True,
        "p1board": newBoard(),
        "p2board": newBoard(),
    }
	
def deep_copy(obj):
    if isinstance(obj, list):
        return [deep_copy(item) for item in obj]
    elif isinstance(obj, dict):
        return {deep_copy(key): deep_copy(value) for key, value in obj.items()}
    elif isinstance(obj, set):
        return {deep_copy(item) for item in obj}
    elif isinstance(obj, tuple):
        return tuple(deep_copy(item) for item in obj)
    else:
        return obj


# game state
# not showing to prevent overwriting
savedGames = {}
currentState = getNewState()


def play():
    print("Welcome to BattleShip! (NOT the movie)")
    evalMenuChoice(getMenuOption())


def getMenuOption():
    print("Please select an option:")
    print("1 Start new game")
    print("2 Load saved game")
    print("3 See rules")
    print("4 Settings")
    print("5 Quit")
    return input("Enter menu option")


def loadSavedGame():
    msg = "Choose a game by its game name:\n"
    for gameName in savedGames.keys():
        msg += "- " + gameName + "\n"

    chosenGameName = input(msg)
    if chosenGameName in savedGames:
        currentState = deep_copy(savedGames[chosenGameName])
        makeGuesses()
    else:
        print("Game not found :(")
        evalMenuChoice(getMenuOption())


def evalMenuChoice(c):
    if c == "1":
        setupBoard(1)
        setupBoard(2)
        makeGuesses()
    elif c == "2":
        loadSavedGame()
    elif c == "3":
        print("You don't know how to play BattleShip?... FFFF\n\n\n")
        evalMenuChoice(getMenuOption())
    elif c == "4":
        print("Sorry we only have 1 setting")
        print("Enter Yes/yes/Y/or y if you want to play with a visible board.")
        print("Any other option will make the board invisible")
        choice = input("Show board or play invisibly: ")
        if choice.upper() in ["YES", "Y"]:
            currentState["visibleBoard"] = True
        else:
            currentState["visibleBoard"] = False
        evalMenuChoice(getMenuOption())
    elif c == "5":
        print("GG")
    else:
        print("Input Error, try again")
        evalMenuChoice(getMenuOption())


def allHitsMade(board):
    for i in range(MAX_ROWS):
        for j in range(MAX_COLUMNS):
            spot = board[i][j]
            if spot["ship"] and spot["type"] != SQUARE_TYPE["HIT"]:
                return False
    return True


def isGameOver():
    if currentState["player1Turn"]:
        return allHitsMade(currentState["p2board"])
    else:
        return allHitsMade(currentState["p1board"])


def saveGame():
    global savedGames, currentState
    gameName = input(
        "Enter a name to save this game under, it will overwrite anything with the same name: "
    )
    savedGames[gameName] = deep_copy(currentState)
    currentState = getNewState()


def makeGuesses():
    while True:
        goAgain = False
        print("Player " + str(1 if currentState["player1Turn"] else 2) + " it is your turn")
        printBoard(currentState["p2board"] if currentState["player1Turn"] else currentState["p1board"], False)

        guess = input("Where should we aim? (Enter QUIT to save and quit): ")
        if guess.upper() == "QUIT":
            saveGame()
            print("See you soon!")
            play()
            break
        else:
            goAgain = handleGuess(guess)

        if isGameOver():
            print("Player " + str(1 if currentState["player1Turn"] else 2) + " wins!")
            play()
            break
        if not goAgain:
            currentState["player1Turn"] = not currentState["player1Turn"]


def handleGuess(guess):
    if not guess:
        print("Wasted turn")
        return
    row = int(guess[1:]) - 1
    col = letters.index(guess[0].upper())
    if col < 0 or col > 9 or row < 0 or row > 9:
        print("Wasted turn")
        return
    spot = ""
    if currentState["player1Turn"]:
        spot = currentState["p2board"][row][col]
    else:
        spot = currentState["p1board"][row][col]

    if spot["type"] != SQUARE_TYPE["NONE"]:
        print("Wasted turn")
        return

    if spot["ship"]:
        print("HIT")
        spot["type"] = SQUARE_TYPE["HIT"]
        return True
    else:
        print("MISS")
        spot["type"] = SQUARE_TYPE["MISS"]


def setupBoard(playerNum):
    curBoard = currentState["p1board"] if playerNum == 1 else currentState["p2board"]
    setupShip(playerNum, curBoard, "aircraft carrier", 5)
    setupShip(playerNum, curBoard, "battleship", 4)
    setupShip(playerNum, curBoard, "destroyer", 3)
    setupShip(playerNum, curBoard, "submarine", 3)
    setupShip(playerNum, curBoard, "cruiser", 2)


def setupShip(playerNum, board, msg, size):
    printBoard(board, True)
    start = None
    end = None

    while not validateShipPlacement(start, end, size):
        start = input("Player " + str(playerNum) + ", Where would you like your " + msg + " (size " + str(size) + ") to start? e.g. A1: ")
        end = input("Player " + str(playerNum) + ", Where would you like your " + msg + " (size " + str(size) + ") to end? e.g. A2: ")

    addShip(board, start, end, size)
    print(msg + " added!")


# TODO don't place ships on other ships
def validateShipPlacement(start, end, size):
    if not start or not end:
        return False
    if start == "quit" or end == "quit":
        raise Exception("cheat code to restart")

    startLetter = start[0].upper()
    endLetter = end[0].upper()
    startNumber = int(start[1:])
    endNumber = int(end[1:])

    return (
        (startLetter == endLetter and abs(startNumber - endNumber) == size - 1)
        or (
            startNumber == endNumber
            and abs(letters.index(startLetter) - letters.index(endLetter)) == size - 1
        )
    )


def addShip(board, start, end, size):
    if start[0].upper() == end[0].upper():
        i = int(start[1:]) - 1
        j = letters.index(start[0].upper())
        for k in range(size):
            board[i + k][j]["ship"] = size
    else:
        i = int(start[1:]) - 1
        j = letters.index(start[0].upper())
        for k in range(size):
            board[i][j + k]["ship"] = size


# start game
play()
