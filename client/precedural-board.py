import time
import random

class ProceduralBoard:
  def __init__(self, board):
    self.board = board
    self.boardWidth = 8
    self.boardHeight = 4
    self.finished = False
    self.path = []

  def getBoard(self):
    for i in range(self.boardHeight):
      for j in range(self.boardWidth):
        print(self.board[i][j], end='')
      print()

  def procedurelyGeneratedBoard(self):
    currentCell = [random.randint(0, self.boardHeight-1), random.randint(0, self.boardWidth-1)]
    self.board[currentCell[0]][currentCell[1]] = 'X'

    while not self.finished:
      blockedDirections = self.getBlockedDirections(currentCell)
      self.move(currentCell, blockedDirections)
      print(self.getBoard())
      time.sleep(1)

  def getBlockedDirections(self, currentCell):
    blockedDirections = []
    
    if self.board[currentCell[0] + 1][currentCell[1]] == 'X':
      blockedDirections.append(0)
    
    if self.board[currentCell[0] - 1][currentCell[1]] == 'X':
      blockedDirections.append(1)
    
    if self.board[currentCell[0]][currentCell[1] + 1] == 'X':
      blockedDirections.append(2)
    
    if self.board[currentCell[0]][currentCell[1] - 1] == 'X':
      blockedDirections.append(3)

    if currentCell[0] + 1 >= self.boardHeight:
      blockedDirections.append(0)

    if currentCell[0] - 1 < 0:
      blockedDirections.append(1)

    if currentCell[1] + 1 >= self.boardWidth:
      blockedDirections.append(2)

    if currentCell[1] - 1 < 0:
      blockedDirections.append(3)
    
    return blockedDirections

  
  def move(self, currentCell, blockedDirections):
    randomDirection = random.randint(0, 3)
    while randomDirection in blockedDirections:
      randomDirection = random.randint(0, 3)

    if randomDirection == 0:
      self.board[currentCell[0] + 1][currentCell[1]] = 'X'
      currentCell[0] += 1

    if randomDirection == 1:
      self.board[currentCell[0] - 1][currentCell[1]] = 'X'
      currentCell[0] -= 1

    if randomDirection == 2:
      self.board[currentCell[0]][currentCell[1] + 1] = 'X'
      currentCell[1] += 1

    if randomDirection == 3:
      self.board[currentCell[0]][currentCell[1] - 1] = 'X'
      currentCell[1] -= 1


board = [['.' for i in range(30)] for j in range(15)]
proceduralBoard = ProceduralBoard(board)

proceduralBoard.procedurelyGeneratedBoard()
proceduralBoard.getBoard()
