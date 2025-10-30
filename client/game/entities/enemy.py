import time
import random
from game.mechanics.combat import CombatSystem

class Enemy:
  def __init__(self, position, lines, level=1, isBoss=False, elementType=None, term=None,):
    self.enemyPosition = position
    self.level = level
    self.isBoss = isBoss
    self.lines = lines
    self.isInCombat = False
    self.id = random.randint(0, 1000000)
    self.term = term
    self.elementType = elementType
    
    # Combat system (will be initialized if term is provided)
    if term:
      self.combat = CombatSystem(term)
    
    if not hasattr(self, 'base_hp'):
      self.base_hp = 10
    if not hasattr(self, 'base_attack'):
      self.base_attack = 5
    if not hasattr(self, 'base_defense'):
      self.base_defense = 2
    if not hasattr(self, 'base_luck'):
      self.base_luck = 2
    if not hasattr(self, 'name'):
      self.name = "Enemy"
    
    self._calculate_stats()
    
    # Drops padrão
    self._calculate_drops()
    self.item_drops = []  # Lista de possíveis items com chance
  
  def _calculate_stats(self):
    """Calcula os stats baseado no level e se é boss"""
    if self.isBoss:
      self.hp = (self.base_hp + (self.level - 1) * 5) * 3
      self.maxHp = self.hp
      self.attack = (self.base_attack + (self.level - 1) * 2) * 2
      self.defense = (self.base_defense + (self.level - 1) * 1) * 2
      self.luck = (self.base_luck + (self.level - 1)) * 2
      if not self.name.endswith('(BOSS)'):
        self.name = self.name + ' (BOSS)'
    else:
      self.hp = self.base_hp + (self.level - 1) * 5
      self.maxHp = self.hp
      self.attack = self.base_attack + (self.level - 1) * 2
      self.defense = self.base_defense + (self.level - 1) * 1
      self.luck = self.base_luck + (self.level - 1)
  
  def _calculate_drops(self):
    """Calcula os drops baseado no level e se é boss"""
    if self.isBoss:
      self.goldDrop = random.randint(self.level * 50, self.level * 100)
      self.xpDrop = random.randint(self.level * 100, self.level * 200)
    else:
      self.goldDrop = random.randint(self.level * 5, self.level * 15)
      self.xpDrop = random.randint(self.level * 10, self.level * 25)

  def moveEnemy(self, boardWidth, boardHeight, lines):
    if self.isInCombat == False:
      newEnemyPosition = self.enemyPosition.copy()
      direction = random.randint(0, 3)

      if direction == 0:
        if self.pathIsBlocked([self.enemyPosition[0]-1, self.enemyPosition[1]], boardWidth, boardHeight) == False:
          newEnemyPosition[0] -= 1
          self.removeEnemy(lines)
          self.enemyPosition = newEnemyPosition
          self.drawEnemy(lines)
      elif direction == 1:
        if self.pathIsBlocked([self.enemyPosition[0]+1, self.enemyPosition[1]], boardWidth, boardHeight) == False:
          newEnemyPosition[0] += 1
          self.removeEnemy(lines)
          self.enemyPosition = newEnemyPosition
          self.drawEnemy(lines)
      elif direction == 2:
        if self.pathIsBlocked([self.enemyPosition[0], self.enemyPosition[1]-1], boardWidth, boardHeight) == False:
          newEnemyPosition[1] -= 1
          self.removeEnemy(lines)
          self.enemyPosition = newEnemyPosition
          self.drawEnemy(lines)
      elif direction == 3:
        if self.pathIsBlocked([self.enemyPosition[0], self.enemyPosition[1]+1], boardWidth, boardHeight) == False:
          newEnemyPosition[1] += 1
          self.removeEnemy(lines)
          self.enemyPosition = newEnemyPosition
          self.drawEnemy(lines)


  def getIsInCombat(self):
    return self.isInCombat
  
  def setIsInCombat(self, isInCombat):
    self.isInCombat = isInCombat

  def getElementType(self):
    """Get enemy's elemental type"""
    return self.elementType

  def pathIsBlocked(self, enemyPosition, boardWidth, boardHeight):
    if enemyPosition[0] < 0 or enemyPosition[0] > boardHeight-1 or enemyPosition[1] < 0 or enemyPosition[1] > boardWidth-1:
      return True
    
    if self.lines[enemyPosition[0]][enemyPosition[1]] == '#':
      return True

    return False

  def getEnemyPosition(self):
    return self.enemyPosition
  
  def drawEnemy(self, lines):
    if self.isBoss:
      lines[self.enemyPosition[0]][self.enemyPosition[1]] = 'B'
    else:
      lines[self.enemyPosition[0]][self.enemyPosition[1]] = 'E'

  def getHp(self):
    return self.hp
  
  def getAttack(self):
    return self.attack
  
  def getDefense(self):
    return self.defense
  
  def getLuck(self):
    return self.luck
  
  def setHp(self, hp):
    self.hp = hp

  def setAttack(self, attack):
    self.attack = attack

  def getID(self):
    return self.id
  
  def getLevel(self):
    return self.level
  
  def getGoldDrop(self):
    return self.goldDrop
  
  def getXpDrop(self):
    return self.xpDrop
  
  def getMaxHp(self):
    return self.maxHp
  
  def getName(self):
    return self.name
  
  def getIsBoss(self):
    return self.isBoss

  def removeEnemy(self, lines):
    lines[self.enemyPosition[0]][self.enemyPosition[1]] = '.'
  
  def get_drops(self):
    """Retorna os drops do inimigo (gold, xp e items)"""
    drops = {
      'gold': self.goldDrop,
      'xp': self.xpDrop,
      'items': []
    }
    
    # Calcular drops de items baseado em chance
    for item_drop in self.item_drops:
      if random.random() < item_drop['chance']:
        drops['items'].append(item_drop['item'])
    
    return drops

  def setDefense(self, defense):
    self.defense = defense

  def attackPlayer(self, player):
    """Attack player using combat system if available"""
    self.combat.attack(self, player, "The enemy", "you")