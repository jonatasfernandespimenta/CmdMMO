import time
import random

class Enemy:
  def __init__(self, hp, attack, defense, name, position):
    self.enemyPosition = position
    self.hp = hp
    self.attack = attack
    self.defense = defense
    self.name = name
    self.id = random.randint(0, 1000000)
    self.isInCombat = False

  def moveEnemy(self, boardWidth, boardHeight, lines):
    if self.isInCombat == False:
      newEnemyPosition = self.enemyPosition.copy()
      direction = random.randint(0, 3)

      if direction == 0:
        if self.enemyWillBeOutOfBounds([self.enemyPosition[0]-1, self.enemyPosition[1]], boardWidth, boardHeight) == False:
          newEnemyPosition[0] -= 1
          self.removeEnemy(lines)
          self.enemyPosition = newEnemyPosition
          self.drawEnemy(lines)
      elif direction == 1:
        if self.enemyWillBeOutOfBounds([self.enemyPosition[0]+1, self.enemyPosition[1]], boardWidth, boardHeight) == False:
          newEnemyPosition[0] += 1
          self.removeEnemy(lines)
          self.enemyPosition = newEnemyPosition
          self.drawEnemy(lines)
      elif direction == 2:
        if self.enemyWillBeOutOfBounds([self.enemyPosition[0], self.enemyPosition[1]-1], boardWidth, boardHeight) == False:
          newEnemyPosition[1] -= 1
          self.removeEnemy(lines)
          self.enemyPosition = newEnemyPosition
          self.drawEnemy(lines)
      elif direction == 3:
        if self.enemyWillBeOutOfBounds([self.enemyPosition[0], self.enemyPosition[1]+1], boardWidth, boardHeight) == False:
          newEnemyPosition[1] += 1
          self.removeEnemy(lines)
          self.enemyPosition = newEnemyPosition
          self.drawEnemy(lines)


  def getIsInCombat(self):
    return self.isInCombat
  
  def setIsInCombat(self, isInCombat):
    self.isInCombat = isInCombat

  def enemyWillBeOutOfBounds(self, enemyPosition, boardWidth, boardHeight):
    if enemyPosition[0] < 0 or enemyPosition[0] > boardHeight-1 or enemyPosition[1] < 0 or enemyPosition[1] > boardWidth-1:
      return True
    else:
      return False

  def getEnemyPosition(self):
    return self.enemyPosition
  
  def drawEnemy(self, lines):
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

  def removeEnemy(self, lines):
    lines[self.enemyPosition[0]][self.enemyPosition[1]] = '.'

  def setDefense(self, defense):
    self.defense = defense

  def attackPlayer(self, player):
    if self.attack - player.getDefense() >= 0:
      player.setHp(player.getHp() - (self.attack - player.getDefense()))

    print("The enemy attacked you for " + str(self.attack - player.getDefense()) + " damage!")
