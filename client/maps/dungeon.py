import random
from enemy import Enemy
from .procedural_board import ProceduralBoard
from chest import Chest
from .map import Map

class Dungeon(Map):
  def __init__(self, enemies, chests):
    super().__init__(30, 15)
    self.enemies = enemies
    self.chests = chests
    self.currentLevel = 1
    self.portalPosition = None
    self.portalActive = False

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

  def printChests(self):
    for chest in self.chests:
      chest.drawChest()

  def printBoard(self, term):
    for i in range(self.windowHeight):
      line = ''
      for j in range(self.windowWidth):
        char = self.lines[i][j]
        if char == '#':
          line += term.bold_white(char)
        elif char == 'X':
          line += term.bold_cyan(char)
        elif char == 'B':
          line += term.bold_red_reverse(char)
        elif char == 'E':
          line += term.bold_red(char)
        elif char == 'C':
          line += term.bold_yellow(char)
        elif char == 'U':
          line += term.bold_magenta(char)
        else:
          line += term.green(char)
      print(line)

  def getEnemies(self):
    return self.enemies

  def printPlayerInfo(self, player, term):
    print(term.bold_white('=' * self.windowWidth))
    hp_color = term.green if player.getHp() > player.getMaxHp() * 0.5 else term.yellow if player.getHp() > player.getMaxHp() * 0.2 else term.red
    print(term.cyan('Name: ') + term.bold(player.getName()) + term.cyan(' [') + term.magenta(player.getPlayerClass()) + term.cyan('] Lvl: ') + term.bold_green(str(player.getLevel())))
    print(term.cyan('HP: ') + hp_color(str(player.getHp()) + '/' + str(player.getMaxHp())) + term.cyan(' | XP: ') + term.green(str(player.getXp()) + '/' + str(player.getXpToNextLevel())))
    print(term.cyan('ATK: ') + term.yellow(str(player.getAttack())) + term.cyan(' | DEF: ') + term.blue(str(player.getDefense())) + term.cyan(' | Gold: ') + term.yellow(str(player.getGold())) + term.cyan(' | Stage: ') + term.magenta(str(self.currentLevel)))
    notification = player.getNotification()
    if notification:
      print(term.bold_green(notification))
    print(term.bold_white('=' * self.windowWidth))

  def getLines(self):
    return self.lines

  def getWindowWidth(self):
    return self.windowWidth
  
  def getWindowHeight(self):
    return self.windowHeight
  
  def getCurrentLevel(self):
    return self.currentLevel
  
  def spawnPortal(self):
    import random
    while True:
      pos = [random.randint(0, self.windowHeight-1), random.randint(0, self.windowWidth-1)]
      if self.lines[pos[0]][pos[1]] == '.':
        self.portalPosition = pos
        self.portalActive = True
        break
  
  def drawPortal(self):
    if self.portalActive and self.portalPosition:
      self.lines[self.portalPosition[0]][self.portalPosition[1]] = 'U'
  
  def getPortalPosition(self):
    return self.portalPosition
  
  def isPortalActive(self):
    return self.portalActive
  
  def nextLevel(self):
    self.currentLevel += 1
    self.enemies.clear()
    self.chests.clear()
    self.portalActive = False
    self.portalPosition = None
    self.createRandomEnemies(5 + self.currentLevel)
    self.createRandomChests(3 + self.currentLevel // 2)
  
  def isBossStage(self):
    return self.currentLevel % 5 == 0
  
  def createRandomEnemies(self, amount):
    if self.isBossStage():
      # Boss room: spawn boss + random minions
      numMinions = random.randint(2, 5)
      
      # Spawn boss
      self.enemies.append(Enemy(20, 10, 5, 'Shadow Lord', [random.randint(0, self.windowHeight-1), random.randint(0, self.windowWidth-1)], self.lines, self.currentLevel, isBoss=True))
      
      # Spawn minions
      for i in range(numMinions):
        self.enemies.append(Enemy(10, 5, 2, 'Minion', [random.randint(0, self.windowHeight-1), random.randint(0, self.windowWidth-1)], self.lines, self.currentLevel))
    else:
      # Normal room
      for i in range(amount):
        self.enemies.append(Enemy(10, 5, 2, 'Snake', [random.randint(0, self.windowHeight-1), random.randint(0, self.windowWidth-1)], self.lines, self.currentLevel))

  def createRandomChests(self, amount):
    for i in range(amount):
      self.chests.append(Chest([random.randint(0, self.windowHeight-1), random.randint(0, self.windowWidth-1)], self.lines))

  def init(self, players, term):
    self.createBoard()
    self.printEnemies()
    self.printChests()

    if len(self.enemies) == 0 and not self.portalActive:
      self.spawnPortal()
    
    if self.portalActive:
      self.drawPortal()

    for player in players:
      player.drawPlayer()

    for chest in self.chests:
      if chest.getPosition() == players[0].getPlayerPosition():
        player.interactWithChest(chest)

    for enemy in self.enemies:
      enemy.moveEnemy(self.windowWidth, self.windowHeight, self.lines)

      if enemy.getHp() <= 0:
        enemy.removeEnemy(self.getLines())
        self.enemies.remove(enemy)

    self.printPlayerInfo(players[0], term)
    self.printBoard(term)
