import random
import math

# Global variables
numOfRepetitions = 100
squareSize = 0
successScore = 4
table = []
quadrupletsInRows = []
quadrupletsInColumns = []
quadrupletsInDiagonalLeftToRight = []
quadrupletsInDiagonalRightToLeft = []
totalCountInRows = 0
totalCountInColumns = 0
totalCountInDiagonalLeftToRight = 0
totalCountInDiagonalRightToLeft = 0


def initiate():
    
    askForInput()

    for i in range(1, numOfRepetitions+1):
        initializeVariables()
        initializeTable()
        fillTableHalf()
        countQuadruplets()

        print("Game no.{}: quadrupletsInRows {}, quadrupletsInColumns {}, quadrupletsInDiagonalLeftToRight {}, quadrupletsInDiagonalRightToLeft {}".format(i, len(quadrupletsInRows), len(quadrupletsInColumns), len(quadrupletsInDiagonalLeftToRight), len(quadrupletsInDiagonalRightToLeft)))
    
    computeAverages()

def initializeVariables():
    global table
    global quadrupletsInRows
    global quadrupletsInColumns
    global quadrupletsInDiagonalLeftToRight
    global quadrupletsInDiagonalRightToLeft

    table = []
    quadrupletsInRows = []
    quadrupletsInColumns = []
    quadrupletsInDiagonalLeftToRight = []
    quadrupletsInDiagonalRightToLeft = []

def askForInput():
    global squareSize
    print("Define Square size:")
    input1 = input()

    while not input1.isdigit() or int(input1) < 4:
        print("Invalid size! \nDefine Square size:" )
        input1 = input()

    squareSize = int(input1)

def initializeTable():
    global table
    for i in range(squareSize):
        table.append(createTableRow())
    
def createTableRow():
    row = []
    for i in range(squareSize):
        row.append(0)
    return row

def fillTableHalf():
    global table
    tableCells = []
    x = 0
    y = 0

    nums = range(1, squareSize**2+1)
    count = math.ceil(squareSize**2/2)
    # get half the table cells randomly, based on their sequence number
    tableCells = random.sample(nums, count)

    # figure out x,y coordinates based on sequence number and fill cell with 1
    for cellSeqNumber in tableCells:
        num = math.modf(cellSeqNumber/squareSize)
        if num[0] != 0:
            x = int(num[1])
            y = round(num[0]/(1/squareSize)) - 1
        else:
            x = int(num[1]) - 1
            y = squareSize - 1

        table[x][y] = 1
    
        
    print(*table, sep = "\n")
    
def countQuadruplets():
    global totalCountInRows
    global totalCountInColumns
    global totalCountInDiagonalLeftToRight
    global totalCountInDiagonalRightToLeft

    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == 1:
                checkRow(i, j)
                checkColumn(i, j)
                checkDiagonalLeftToRight(i, j)
                checkDiagonalRightToLeft(i, j)

    totalCountInRows += len(quadrupletsInRows)
    totalCountInColumns += len(quadrupletsInColumns)
    totalCountInDiagonalLeftToRight += len(quadrupletsInDiagonalLeftToRight)
    totalCountInDiagonalRightToLeft += len(quadrupletsInDiagonalRightToLeft)

def checkRow(row, col):
    global quadrupletsInRows
    quadruplet = []
    isQuadruplet = True
    consecutiveCellsCount = 1
    isEligibleIndex = squareSize - col >= successScore

    while isEligibleIndex and consecutiveCellsCount <= successScore and isQuadruplet:
        
        if table[row][col] == 1:
            consecutiveCellsCount += 1
            quadruplet.append((row,col))
            col += 1
        else:
            isQuadruplet = False
            quadruplet = []

    if len(quadruplet) == successScore and isQuadruplet: 
        if quadruplet not in quadrupletsInRows:
            quadrupletsInRows.append(quadruplet)

def checkColumn(row, col):
    global quadrupletsInColumns
    quadruplet = []
    isQuadruplet = True
    consecutiveCellsCount = 1
    isEligibleIndex = squareSize - row >= successScore

    while isEligibleIndex and consecutiveCellsCount <= successScore and isQuadruplet:

        if table[row][col] == 1:
            consecutiveCellsCount += 1
            quadruplet.append((row,col))
            row += 1
        else:
            isQuadruplet = False
            quadruplet = []

    if len(quadruplet) == successScore and isQuadruplet: 
        if quadruplet not in quadrupletsInColumns:
            quadrupletsInColumns.append(quadruplet)

def checkDiagonalLeftToRight(row, col):
    global quadrupletsInDiagonalLeftToRight
    quadruplet = []
    isQuadruplet = True
    consecutiveCellsCount = 1
    isEligibleIndex = squareSize - row >= successScore and squareSize - col >= successScore

    while isEligibleIndex and consecutiveCellsCount <= successScore and isQuadruplet:

        if table[row][col] == 1:
            consecutiveCellsCount += 1
            quadruplet.append((row,col))
            row += 1
            col += 1
        else:
            isQuadruplet = False
            quadruplet = []

    if len(quadruplet) == successScore and isQuadruplet: 
        if quadruplet not in quadrupletsInDiagonalLeftToRight:
            quadrupletsInDiagonalLeftToRight.append(quadruplet)

def checkDiagonalRightToLeft(row, col):
    global quadrupletsInDiagonalRightToLeft
    quadruplet = []
    isQuadruplet = True
    consecutiveCellsCount = 1
    isEligibleIndex = col >= successScore - 1 and squareSize - row >= successScore

    while isEligibleIndex and consecutiveCellsCount <= successScore and isQuadruplet:

        if table[row][col] == 1:
            consecutiveCellsCount += 1
            quadruplet.append((row,col))
            row += 1
            col -= 1
        else:
            isQuadruplet = False
            quadruplet = []

    if len(quadruplet) == successScore and isQuadruplet: 
        if quadruplet not in quadrupletsInDiagonalRightToLeft:
            quadrupletsInDiagonalRightToLeft.append(quadruplet)

def computeAverages():
    
    rowsAverage = round(totalCountInRows/numOfRepetitions, 2)
    columnsAverage = round(totalCountInColumns/numOfRepetitions, 2)
    diagonalLeftToRightAverage = round(totalCountInDiagonalLeftToRight/numOfRepetitions, 2)
    diagonalRightToLeftAverage = round(totalCountInDiagonalRightToLeft/numOfRepetitions, 2)
    totalAverage = round((totalCountInRows + totalCountInColumns + totalCountInDiagonalLeftToRight + totalCountInDiagonalRightToLeft)/numOfRepetitions, 2)

    print("Rows average for {} repetitions is: {}".format(numOfRepetitions, rowsAverage))
    print("Columns average for {} repetitions is: {}".format(numOfRepetitions, columnsAverage))
    print("Diagonal Left To Right average for {} repetitions is: {}".format(numOfRepetitions, diagonalLeftToRightAverage))
    print("Diagonal Right To Left average for {} repetitions is: {}".format(numOfRepetitions, diagonalRightToLeftAverage))
    print("Total Average for {} repetitions is: {}".format(numOfRepetitions, totalAverage))
    

# Call initiate method    
initiate()