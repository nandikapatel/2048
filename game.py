app.board = makeList(4, 4)
app.colors = [ rgb(240, 230, 220), rgb(235, 225, 200), rgb(240, 180, 125),
               rgb(240, 140, 95), rgb(240, 125, 85), rgb(230, 90, 45),
               rgb(245, 215, 105), rgb(240, 210, 65), rgb(230, 200, 30),
               rgb(225, 185, 20), rgb(235, 200, 0) ]
app.textColor = rgb(105, 95, 85)

tiles = Group()

def drawBoard():

    # Create a rectangle cell for each row and column of the board.
    for row in range(len(app.board)):
        for col in range(len(app.board[row])):
            x = 10 + col * 100
            y = 10 + row * 100
            Rect(x, y, 80, 80, fill = rgb(205,195,180))
drawBoard()

startScreen = Group(
    Rect(0, 0, 400, 400, fill=app.colors[5]),
    Label("Let's play 2048!", 200, 130, fill='white', size=40),
    Label("Press the 'up', 'down', 'right', and 'left' arrow keys", 200, 160,
          fill='white', size=15),
    Label('to move the tiles on the board', 200, 180, fill='white', size=15),
    Label('If two tiles of the same number collide,', 200, 200, fill='white',
          size=15),
    Label('they will combine into one tile!', 200, 220, fill='white', size=15),
    Label('Try to get to 2048!!!', 200, 250, fill='white', size=35),
    Label('Press space to start.', 200, 280, fill='white', size=15)
    )

def drawTile(value, row, col):
    # Creates a tile piece at the row and column and labels it with the
    # number value.
    counter = 0
    tempValue = value

    # Finds the index of the colors list.
    while (tempValue > 2):
        tempValue //= 2
        counter += 1

    # Draws a tile.
    color = app.colors[counter]
    tiles.add(
        Rect(10 + (col * 100), 10 + (row * 100), 80, 80, fill=color),
        Label(value, 50 + (col * 100), 50 + (row * 100), fill=app.textColor,
              size=50, bold=True)
        )

def drawTiles():
    # For every board cell that has a number value, creates a tile.
    for rowIndex in range(len(app.board)):
        row = app.board[rowIndex]
        for colIndex in range(len(row)):
            value = row[colIndex]
            if (value != None):
                drawTile(value, rowIndex, colIndex)

    tiles.toFront()

def generateNewTile():
    newSpotFound = False


    # Loop until a new spot has been found to place a tile.
    while newSpotFound == False:

    # Each pass of the loop, pick a random cell by choosing the row and col
    # (in that order to autograde correctly).
        randomRow = randrange(0, 4)
        randomCol = randrange(0, 4)
    
        # If row, col give an empty cell, set its label to 2 and end the loop.
        if app.board[randomRow][randomCol] == None:
            app.board[randomRow][randomCol] = 2
            newSpotFound = True

def reverse(cellBlock):
    reversedCellBlock = [ ]


    # cellBlock is either a row or a column. Reverse the order of the elements
    # in the 1D list cellBlock.
    for cell in range(len(cellBlock)):
        block = cellBlock.pop()
        reversedCellBlock.append(block)
    return reversedCellBlock


def move(cellBlock):
    # cellBlock is either a row or a column. move will slide all of the values
    # in the cellBlock to one side and combine similar values.

    # First, creates a copy of the list by copying elements over one by one.
    cellBlockCopy = [ ]
    for cellIndex in range(len(cellBlock)):
        if (cellBlock[cellIndex] != None):
            cellBlockCopy.append(cellBlock[cellIndex])

    index = 0
    while (index < len(cellBlockCopy) - 1):
        # If two cells in the copy are next to each other and have the same
        # number, combines them and doubles the numer.
        if (cellBlockCopy[index] == cellBlockCopy[index + 1]):
            val = cellBlockCopy.pop(index)
            cellBlockCopy[index] = val * 2
        else:
            index += 1

    # Fills the remainder of the copy with None tiles.
    for remainingCells in range(len(cellBlock) - len(cellBlockCopy)):
        cellBlockCopy.append(None)

    return cellBlockCopy

def moveHorizontal(direction):
    # For each row, slide it in the direction.
    for rowIndex in range(len(app.board)):
        if (direction == 'right'):

            # Reverse the row then slide left using move. Then reverse the
            # resulting row.
            row = reverse(app.board[rowIndex])
            newRow = move(row)
            app.board[rowIndex] = reverse(newRow)
            


        elif (direction == 'left'):

            # Slide to the left using move.
            row = app.board[rowIndex]
            newRow = move(row) 
            app.board[rowIndex] = newRow


def getCol(board, colIndex):
    colList = [ ]


    # Go through the rows of the board and add each element at the colIndex
    # to colList.
    for row in board:
        colList.append(row[colIndex])
    return colList


def moveCols(board):
    for colIndex in range(len(board[0])):

        # For every column, slide the elements up using the move function.
        col = getCol(board, colIndex)
        newCol = move(col)
        # Then copy the values to the board.
        for rowIndex in range(len(board)):
            board[rowIndex][colIndex] = newCol[rowIndex]


def moveVertical(direction):
    if (direction == 'up'):
        # Slides up.
        moveCols(app.board)
    elif (direction == 'down'):
        # Reverses the columns then slides up. Then reverses the resulting columns.
        board = reverse(app.board)
        app.board = board
        moveCols(board)
        app.board = reverse(board)

def gameOver():
    fullRowCount = 0
    for row in range(len(app.board)):
        # Check if any row contains 2048 and end the game as a win if so.
        ### (HINT: Don't forget to call app.stop())
        ### Place Your Code Here ###
        if 2048 in app.board[row]:
            Rect(0, 100, 400, 100, fill = rgb(235,200,0))
            Label('You win!', 200, 150, fill = rgb(105,95,85), size=30)
            app.stop()

        # If every cell has a tile on it, the row is full.
        if (None not in app.board[row]):
            fullRowCount += 1

    # If every row is full, end the game as a loss.
    ### Place Your Code Here ###
    if fullRowCount == len(app.board):
        Rect(0, 100, 400, 100, fill = rgb(235,200,0))
        Label('Game Over!', 200, 150, fill = rgb(105,95,85), size=30)
        app.stop()

def onKeyPress(key):
    # If on the start screen, begin the game when space is pressed.
    if ((startScreen.visible == True) and (key == 'space')):
        startScreen.visible = False

    # If the game is playing, make moves on the key presses.
    elif (startScreen.visible == False):
        if ((key == 'right') or (key == 'left')):
            moveHorizontal(key)
        elif ((key == 'up') or (key == 'down')):
            moveVertical(key)

        tiles.clear()
        generateNewTile()
        drawTiles()
        gameOver()

def onMousePress(mouseX, mouseY):
    # Don't change this function! It is for testing purposes.
    if ((mouseX == -1) and (mouseY == -1)):
        app.board[0][0] = 2048
        gameOver()
    elif ((mouseX == 400) and (mouseY == 400)):
        for row in range(4):
            for col in range(4):
                app.board[row][col] = 2
                gameOver()
