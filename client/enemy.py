import time
import random

class Enemy:
  def __init__(self, hp, attack, defense, name, position, lines, level=1, isBoss=False):
    self.enemyPosition = position
    self.level = level
    self.isBoss = isBoss
    
    if isBoss:
      self.hp = (hp + (level - 1) * 5) * 3
      self.maxHp = self.hp
      self.attack = (attack + (level - 1) * 2) * 2
      self.defense = (defense + (level - 1) * 1) * 2
      self.name = name + ' (BOSS)'
      self.goldDrop = random.randint(level * 50, level * 100)
      self.xpDrop = random.randint(level * 100, level * 200)
    else:
      self.hp = hp + (level - 1) * 5
      self.maxHp = self.hp
      self.attack = attack + (level - 1) * 2
      self.defense = defense + (level - 1) * 1
      self.name = name
      self.goldDrop = random.randint(level * 5, level * 15)
      self.xpDrop = random.randint(level * 10, level * 25)
    
    self.id = random.randint(0, 1000000)
    self.isInCombat = False
    self.lines = lines

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

  def setDefense(self, defense):
    self.defense = defense

  def attackPlayer(self, player):
    playerLuck = player.getLuck() 

    missChance = random.random() < playerLuck / 100

    if not missChance:
      if self.attack - player.getDefense() >= 0:
        player.setHp(player.getHp() - (self.attack - player.getDefense()))

      print("The enemy attacked you for " + str(self.attack - player.getDefense()) + " damage!")
    else:
      print("The enemy's attack missed!")
