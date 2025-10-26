import random
from game.entities.enemy import Enemy
from engine.maps.procedural_board import ProceduralBoard
from game.entities.chest import Chest
from engine.maps.map import Map
from game.maps.map_transition import DungeonNextLevelTransition, DungeonToCityTransition

class Dungeon(Map):
  def __init__(self, enemies, chests, city_map=None):
    super().__init__(30, 15)
    self.enemies = enemies
    self.chests = chests
    self.currentLevel = 1
    self.portalPosition = None
    self.portalActive = False
    self.exitPortalPosition = [0, 1]  # Exit portal next to spawn point
    self.city_map = city_map

  def createBoard(self):
    board = [['.' for i in range(self.windowWidth + 1)] for j in range(self.windowHeight + 1)]

    proceduralBoard = ProceduralBoard(board, self.windowWidth, self.windowHeight)
    proceduralBoard.procedurelyGeneratedBoard()

    generatedBoard = proceduralBoard.getBoard()

    # Clear existing board before regenerating
    self.lines = []
    for i in range(self.windowHeight):
      self.lines.append([])
      for j in range(self.windowWidth):
        self.lines[i].append(generatedBoard[i][j])
    
    # Ensure exit portal position is always walkable
    self.lines[self.exitPortalPosition[0]][self.exitPortalPosition[1]] = '.'

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
  
  def drawExitPortal(self):
    """Draw exit portal at spawn point (returns to city)"""
    if self.lines[self.exitPortalPosition[0]][self.exitPortalPosition[1]] == '.':
      self.lines[self.exitPortalPosition[0]][self.exitPortalPosition[1]] = 'U'
  
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
  
  def handleCollisions(self, player, draw, term):
    """Handle enemy collisions in dungeon"""
    if player.collidedWithEnemy(self.enemies):
      for enemy in self.enemies:
        if enemy.getEnemyPosition() == player.getPlayerPosition():
          from game.ui.combatui import CombatUI
          combat = CombatUI(player, enemy, draw, term)
          combat.start()
          break
  
  def setCityMap(self, city_map):
    self.city_map = city_map
  
  def checkPortalTransition(self, player):
    """Check if player stepped on a portal"""
    # Exit portal - return to city (spawn away from entrance portal)
    if self.exitPortalPosition == player.getPlayerPosition() and self.city_map:
      city_portal = self.city_map.getPortalPosition()
      safe_spawn = [city_portal[0], city_portal[1] - 2]  # Spawn 2 tiles left of portal
      return DungeonToCityTransition(self.city_map, safe_spawn)
    
    # Next level portal
    if self.isPortalActive() and self.getPortalPosition() == player.getPlayerPosition():
      return DungeonNextLevelTransition(self, [0, 0])
    
    return None
  def createRandomEnemies(self, amount):
    from game.entities.enemies import Snake, Goblin
    
    if self.isBossStage():
      numMinions = random.randint(2, 5)
      
      boss = Enemy([random.randint(0, self.windowHeight-1), random.randint(0, self.windowWidth-1)], self.lines, self.currentLevel, isBoss=True)
      boss.name = 'Shadow Lord'
      boss.base_hp = 20
      boss.base_attack = 10
      boss.base_defense = 5
      boss._calculate_stats()
      self.enemies.append(boss)
      
      for i in range(numMinions):
        enemy_type = random.choice([Snake, Goblin])
        pos = [random.randint(0, self.windowHeight-1), random.randint(0, self.windowWidth-1)]
        self.enemies.append(enemy_type(pos, self.lines, self.currentLevel))
    else:
      for i in range(amount):
        enemy_type = random.choice([Snake, Goblin])
        pos = [random.randint(0, self.windowHeight-1), random.randint(0, self.windowWidth-1)]
        self.enemies.append(enemy_type(pos, self.lines, self.currentLevel))

  def createRandomChests(self, amount):
    for i in range(amount):
      self.chests.append(Chest([random.randint(0, self.windowHeight-1), random.randint(0, self.windowWidth-1)], self.lines))

  def init(self, players, term):
    # Only create board if it doesn't exist yet
    if len(self.lines) == 0:
      self.createBoard()
    
    self.printEnemies()
    self.printChests()

    if len(self.enemies) == 0 and not self.portalActive:
      self.spawnPortal()
    
    if self.portalActive:
      self.drawPortal()
    
    # Always draw exit portal
    self.drawExitPortal()

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
