import json
import random
import time
from engine.core.player import Player as BasePlayer
from game.helper import blockers

class Player(BasePlayer):
  CLASSES = {
    'rogue': {
      'hp': 80,
      'attack': 15,
      'defense': 4,
      'luck': 8
    },
    'knight': {
      'hp': 120,
      'attack': 12,
      'defense': 10,
      'luck': 3
    },
    'wizard': {
      'hp': 70,
      'attack': 18,
      'defense': 3,
      'luck': 5
    }
  }

  def __init__(self, lines, windowWidth, windowHeight, playerPosition, name, playerClass, term):
    # Initialize base player
    super().__init__(lines, windowWidth, windowHeight, playerPosition, name, term, blockers)
    
    # MMO-specific: Player class system
    self.playerClass = playerClass.lower()
    classStats = self.CLASSES[self.playerClass]
    
    # Override base stats with class stats
    self.hp = classStats['hp']
    self.maxHp = classStats['hp']
    self.attack = classStats['attack']
    self.defense = classStats['defense']
    self.luck = classStats['luck']
    
    # MMO-specific: Properties (houses, farms, etc)
    self.property = []
    self.currentMap = 'dungeon'

  def addProperty(self, property):
    self.property.append(property)

  def getProperties(self):
    return self.property

  def movePlayer(self, sio):
    """Override to add multiplayer network sync"""
    def network_callback(new_position):
      sio.emit('move', json.dumps({"playerId": self.name, "playerPosition": new_position}))
    
    super().movePlayer(network_callback)
  
  def getName(self):
    return self.name
  
  def getPlayerClass(self):
    return self.playerClass.capitalize()
  
  def getMaxHp(self):
    return self.maxHp
  
  def getGold(self):
    return self.gold
  
  def addGold(self, amount):
    self.gold += amount
  
  def getXp(self):
    return self.xp
  
  def getLevel(self):
    return self.level
  
  def getXpToNextLevel(self):
    return self.xpToNextLevel
  
  def addXp(self, amount):
    self.xp += amount

    while self.xp >= self.xpToNextLevel:
      self.levelUp()
  
  def levelUp(self):
    self.xp -= self.xpToNextLevel
    self.level += 1
    self.xpToNextLevel = int(self.xpToNextLevel * 1.5)
    
    self.maxHp += 10
    self.hp = self.maxHp 
    self.attack += 2
    self.defense += 1
    self.luck += 1
    
    self.notificationMessage = f"LEVEL UP! You are now level {self.level}!"
    self.notificationTime = time.time()

  def getPlayerPosition(self):
    return self.playerPosition

  def drawPlayer(self):
    self.lines[self.playerPosition[0]][self.playerPosition[1]] = 'X'

  def getHp(self):
    return self.hp
  
  def getAttack(self):
    return self.attack

  def getLuck(self):
    return self.luck
  
  def getDefense(self):
    return self.defense
  
  def setHp(self, hp):
    self.hp = hp

  def interactWithChest(self, chest):
    if chest.getPosition() == self.playerPosition and chest.open == False:
      loot = chest.openChest()
      self.inventory.append(loot)
      import time
      self.notificationMessage = f"You collected: {loot['name']}!"
      self.notificationTime = time.time()

  def setPlayerPosition(self, playerPosition):
    self.playerPosition = playerPosition
  
  def setBoard(self, lines, windowWidth, windowHeight):
    self.lines = lines
    self.windowWidth = windowWidth
    self.windowHeight = windowHeight

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
    criticalHit = random.random() < self.luck / 100
    damage = max(1, self.attack - enemy.getDefense())
    if criticalHit:
      damage *= 2
      print(self.term.bold_red("Critical hit!"))

    enemy.setHp(enemy.getHp() - damage)
    print(self.term.green("You attacked the enemy for " + str(damage) + " damage!"))
    print(self.term.yellow("Enemy HP: " + str(max(0, enemy.getHp())) + "/" + str(enemy.getMaxHp())))

    if(enemy.getHp() <= 0):
      print(self.term.bold_green("You killed the enemy!"))
      enemy.removeEnemy(self.lines)

  def getInventory(self):
    inventory = self.inventory.copy()

    for item in inventory:
      item['quantity'] = self.inventory.count(item)

    inventory = list({v['name']:v for v in inventory}.values())

    return inventory
  
  def getIsInventoryOpen(self):
    return self.isInventoryOpen
  
  def setIsInventoryOpen(self, isInventoryOpen):
    self.isInventoryOpen = isInventoryOpen

  def inventoryControl(self):
    pass

  def dropItem(self, itemIndex):
    self.inventory.remove(self.inventory[int(itemIndex)])

  def equipItem(self, itemIndex):
    item = self.inventory[int(itemIndex)]

    if 'hp' in item:
      self.hp += item['hp']
    elif 'attack' in item:
      self.attack += item['attack']

  def init(self, sio):
    self.movePlayer(sio)
    self.inventoryControl()
  
  def getNotification(self):
    import time
    if self.notificationTime > 0 and time.time() - self.notificationTime < 3:
      return self.notificationMessage
    return ''
  
  def getCurrentMap(self):
    return self.currentMap
  
  def setCurrentMap(self, mapName):
    self.currentMap = mapName
