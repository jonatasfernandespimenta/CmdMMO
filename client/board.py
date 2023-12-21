import random
from enemy import Enemy
from procedural_board import ProceduralBoard

class Board:
  def __init__(self, enemies):
    self.windowWidth = 30
    self.windowHeight = 15
    self.lines = []
    self.enemies = enemies

  def createBoard(self):
    board = [['.' for i in range(self.windowWidth + 1)] for j in range(self.windowHeight + 1)]

    proceduralBoard = ProceduralBoard(board, self.windowWidth, self.windowHeight)
    proceduralBoard.procedurelyGeneratedBoard()

    generatedBoard = proceduralBoard.getBoard()

    for i in range(self.windowHeight):
      self.lines.append([])
      for j in range(self.windowWidth):
        self.lines[i].append(generatedBoard[i][j])

    return self.lines
  
  def printEnemies(self):
    for enemy in self.enemies:
      enemy.drawEnemy(self.getLines())

  def printBoard(self):
    for i in range(self.windowHeight):
      for j in range(self.windowWidth):
        print(self.lines[i][j], end='')
      print()

  def getEnemies(self):
    return self.enemies

  def printPlayerInfo(self, player):
    print('=' * self.windowWidth)
    print('Name: ' + player.getName() + ' | HP: ' + str(player.getHp()))
    print('Attack: ' + str(player.getAttack()) + ' | Defense: ' + str(player.getDefense()))
    print('=' * self.windowWidth)

  def getLines(self):
    return self.lines

  def getWindowWidth(self):
    return self.windowWidth
  
  def getWindowHeight(self):
    return self.windowHeight
  
  def createRandomEnemies(self, amount):
    for i in range(amount):
      self.enemies.append(Enemy(10, 5, 2, 'Snake', [random.randint(0, self.windowHeight-1), random.randint(0, self.windowWidth-1)]))

  def init(self, players):
    self.createBoard()
    self.printEnemies()

    for player in players:
      player.drawPlayer()

    for enemy in self.enemies:
      enemy.moveEnemy(self.windowWidth, self.windowHeight, self.lines)

      if enemy.getHp() <= 0:
        enemy.removeEnemy(self.getLines())
        self.enemies.remove(enemy)

    self.printPlayerInfo(players[0])
    self.printBoard()
