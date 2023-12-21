import json
import keyboard

class Player:
  def __init__(self, lines, windowWidth, windowHeight, playerPosition, name):
    self.lines = lines
    self.windowWidth = windowWidth
    self.windowHeight = windowHeight
    self.playerPosition = playerPosition
    self.hp = 100
    self.attack = 10
    self.defense = 6
    self.name = name

  def removePlayer(self):
    self.lines[self.playerPosition[0]][self.playerPosition[1]] = '.'

  def movePlayer(self, sio):
    newPlayerPosition = self.playerPosition.copy()

    if keyboard.is_pressed('up'):
      self.lines[self.playerPosition[0]][self.playerPosition[1]] = '.'
      if self.pathIsBlocked([self.playerPosition[0]-1, self.playerPosition[1]]) == False:
        newPlayerPosition[0] -= 1

    elif keyboard.is_pressed('down'):
      self.lines[self.playerPosition[0]][self.playerPosition[1]] = '.'
      if self.pathIsBlocked([self.playerPosition[0]+1, self.playerPosition[1]]) == False:
        newPlayerPosition[0] += 1

    elif keyboard.is_pressed('left'):
      self.lines[self.playerPosition[0]][self.playerPosition[1]] = '.'
      if self.pathIsBlocked([self.playerPosition[0], self.playerPosition[1]-1]) == False:
        newPlayerPosition[1] -= 1

    elif keyboard.is_pressed('right'):
      self.lines[self.playerPosition[0]][self.playerPosition[1]] = '.'
      if self.pathIsBlocked([self.playerPosition[0], self.playerPosition[1]+1]) == False:
        newPlayerPosition[1] += 1
    
    sio.emit('move', json.dumps({"playerId": self.name, "playerPosition": newPlayerPosition}))
    sio.sleep(0.1)
    self.playerPosition = newPlayerPosition

  def pathIsBlocked(self, playerPosition):
    if playerPosition[0] < 0 or playerPosition[0] > self.windowHeight-1 or playerPosition[1] < 0 or playerPosition[1] > self.windowWidth-1:
      return True
    elif self.lines[playerPosition[0]][playerPosition[1]] == '#':
      return True
    
    return False
  
  def getName(self):
    return self.name

  def getPlayerPosition(self):
    return self.playerPosition

  def drawPlayer(self):
    self.lines[self.playerPosition[0]][self.playerPosition[1]] = 'X'

  def getHp(self):
    return self.hp
  
  def getAttack(self):
    return self.attack
  
  def getDefense(self):
    return self.defense
  
  def setHp(self, hp):
    self.hp = hp

  def setPlayerPosition(self, playerPosition):
    self.playerPosition = playerPosition

  def setAttack(self, attack):
    self.attack = attack

  def setDefense(self, defense):
    self.defense = defense

  def collidedWithEnemy(self, enemies):
    for enemy in enemies:
      if enemy.getEnemyPosition() == self.playerPosition:
        return True
    return False

  def attackEnemy(self, enemy):
    enemy.setHp(enemy.getHp() - (self.attack - enemy.getDefense()))
    print("You attacked the enemy for " + str(self.attack - enemy.getDefense()) + " damage!")

    if(enemy.getHp() <= 0):
      print("You killed the enemy!")
      enemy.removeEnemy(self.lines)

  def init(self, sio):
    self.movePlayer(sio)

