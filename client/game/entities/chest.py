import random
from game.items.potions import potions
from game.items.swords import swords

class Chest:
  def __init__(self, position, lines):
    self.position = position
    self.lines = lines
    self.open = False
    self.loot = potions[random.randint(0, len(potions)-1)] if random.randint(0, 1) == 0 else swords[random.randint(0, len(swords)-1)]
    #self.loot = potions[0]
    self.id = random.randint(0, 1000000)  # Unique ID for sync

  def drawChest(self):
    if self.open == False:
      self.lines[self.position[0]][self.position[1]] = '▣'
    else:
      self.lines[self.position[0]][self.position[1]] = '□'

  def getPosition(self):
    return self.position

  def getLoot(self):
    return self.loot

  def openChest(self):
    self.open = True
    return self.getLoot()
  
  def removeChest(self):
    """Remove chest from board"""
    self.lines[self.position[0]][self.position[1]] = '.'
  
  def getID(self):
    return self.id
