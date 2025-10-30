import time
import random

class ProceduralBoard:
  def __init__(self, board, boardWidth, boardHeight, seed=None):
    self.board = board
    self.boardWidth = boardWidth
    self.boardHeight = boardHeight
    self.finished = False
    self.path = []
    self.isBacktracking = False
    self.seed = seed
    
    # Set random seed if provided for consistent generation
    if seed is not None:
      random.seed(seed)

  def getBoard(self):
    return self.board

  def procedurelyGeneratedBoard(self):
    currentCell = [random.randint(0, self.boardHeight-1), random.randint(0, self.boardWidth-1)]
    self.board[currentCell[0]][currentCell[1]] = 'X'

    while not self.finished:
      while self.isBacktracking and len(self.path) > 0:
        currentCell = self.path[len(self.path) - 1]
        self.path.pop()

        self.moveToSpecificCell(currentCell, 'O')

        unvisitedCell = self.foundUnvisitedCell(currentCell)

        if len(unvisitedCell) > 0:
          currentCell = unvisitedCell
          self.moveToSpecificCell(currentCell)
          self.isBacktracking = False

        # print(self.getBoard())
        # time.sleep(0.5)
      
      if self.isBacktracking and len(self.path) == 0:
        self.finished = True
        break

      
      blockedDirections = self.getBlockedDirections(currentCell)

      if len(blockedDirections) == 4:
        self.isBacktracking = True

      self.move(currentCell, blockedDirections)
      # print(self.getBoard())
      # time.sleep(0.2)

      if self.checkIfThereAreNoMoreDotsInTheBoard():
        self.finished = True
    if self.finished:
      self.polishBoard()
      self.getBoard()

  def checkIfThereAreNoMoreDotsInTheBoard(self):
    for i in range(self.boardHeight):
      for j in range(self.boardWidth):
        if self.board[i][j] == '.':
          return False
    return True

  def getBlockedDirections(self, currentCell, character='X'):
    blockedDirections = []

    if currentCell[0] + 1 >= self.boardHeight:
      blockedDirections.append(0)
    elif self.board[currentCell[0] + 1][currentCell[1]] == character or self.board[currentCell[0] + 1][currentCell[1]] == 'O':
      blockedDirections.append(0)
    
    if currentCell[0] - 1 < 0:
      blockedDirections.append(1)
    elif self.board[currentCell[0] - 1][currentCell[1]] == character or self.board[currentCell[0] - 1][currentCell[1]] == 'O':
      blockedDirections.append(1)
    
    if currentCell[1] + 1 >= self.boardWidth:
      blockedDirections.append(2)
    elif self.board[currentCell[0]][currentCell[1] + 1] == character or self.board[currentCell[0]][currentCell[1] + 1] == 'O':
      blockedDirections.append(2)
    
    if currentCell[1] - 1 < 0:
      blockedDirections.append(3)
    elif self.board[currentCell[0]][currentCell[1] - 1] == character or self.board[currentCell[0]][currentCell[1] - 1] == 'O':
      blockedDirections.append(3)
    
    return blockedDirections

  def foundUnvisitedCell(self, currentCell):
    unvisitedCells = []

    if currentCell[0] + 1 < self.boardHeight:
      if self.board[currentCell[0] + 1][currentCell[1]] == '.':
        unvisitedCells.append([currentCell[0] + 1, currentCell[1]])

    if currentCell[0] - 1 >= 0:
      if self.board[currentCell[0] - 1][currentCell[1]] == '.':
        unvisitedCells.append([currentCell[0] - 1, currentCell[1]])

    if currentCell[1] + 1 < self.boardWidth:
      if self.board[currentCell[0]][currentCell[1] + 1] == '.':
        unvisitedCells.append([currentCell[0], currentCell[1] + 1])

    if currentCell[1] - 1 >= 0:
      if self.board[currentCell[0]][currentCell[1] - 1] == '.':
        unvisitedCells.append([currentCell[0], currentCell[1] - 1])

    return random.choice(unvisitedCells) if unvisitedCells else []

  def moveToSpecificCell(self, currentCell, character='X'):
    self.board[currentCell[0]][currentCell[1]] = character

  def polishBoard(self):
    for i in range(self.boardHeight):
      for j in range(self.boardWidth):
        if self.board[i][j] == 'X':
          self.board[i][j] = '#'
        if self.board[i][j] == 'O':
          self.board[i][j] = '.'

  def move(self, currentCell, blockedDirections, character='X'):
    if len(blockedDirections) < 4:
      randomDirection = random.randint(0, 3)
      while randomDirection in blockedDirections:
        randomDirection = random.randint(0, 3)

      if randomDirection == 0:
        self.board[currentCell[0] + 1][currentCell[1]] = character
        currentCell[0] += 1

      if randomDirection == 1:
        self.board[currentCell[0] - 1][currentCell[1]] = character
        currentCell[0] -= 1

      if randomDirection == 2:
        self.board[currentCell[0]][currentCell[1] + 1] = character
        currentCell[1] += 1

      if randomDirection == 3:
        self.board[currentCell[0]][currentCell[1] - 1] = character
        currentCell[1] -= 1

      self.path.append([currentCell[0], currentCell[1]])
