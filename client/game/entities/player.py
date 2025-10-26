import json
import random
from engine.core.player import Player as BasePlayer
from game.helper import blockers
from game.mechanics.farm import Farm

class Player(BasePlayer):
  """MMO Player - extends engine Player with MMO-specific features"""
  
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
    
    # MMO-specific: Farm system
    self.farm = Farm(self)
    
    # Testing: Add mushroom seed to inventory
    from game.items.materials import seeds
    mushroom_seed = next(s for s in seeds if s['name'] == 'Mushroom Seed')
    self.inventory.append(mushroom_seed)

  # ==================== MMO-Specific ====================
  
  def getPlayerClass(self):
    """Get player class"""
    return self.playerClass.capitalize()
  
  def getLuck(self):
    """Get luck stat"""
    return self.luck
  
  def addProperty(self, property):
    """Add property to player (house, farm, etc)"""
    self.property.append(property)

  def getProperties(self):
    """Get all owned properties"""
    return self.property
  
  def getCurrentMap(self):
    """Get current map name"""
    return self.currentMap
  
  def setCurrentMap(self, mapName):
    """Set current map name"""
    self.currentMap = mapName

  # ==================== Overrides ====================
  
  def movePlayer(self, sio):
    """Override to add multiplayer network sync"""
    def network_callback(new_position):
      sio.emit('move', json.dumps({"playerId": self.name, "playerPosition": new_position}))
    
    super().movePlayer(network_callback)
  
  def levelUp(self):
    """Override to add luck stat increase"""
    super().levelUp()  # Call base levelUp
    self.luck += 1  # MMO-specific: increase luck

  def interactWithChest(self, chest):
    """Interact with chest and collect loot"""
    if chest.getPosition() == self.playerPosition and chest.open == False:
      loot = chest.openChest()
      self.addToInventory(loot)  # Use base class method

  # ==================== Combat ====================
  
  def collidedWithEnemy(self, enemies):
    """Check if player collided with any enemy"""
    for enemy in enemies:
      if enemy.getEnemyPosition() == self.playerPosition:
        return True
    return False

  def attackEnemy(self, enemy):
    """Attack an enemy with critical hit chance based on luck"""
    criticalHit = random.random() < self.luck / 100
    damage = max(1, self.attack - enemy.getDefense())
    
    if criticalHit:
      damage *= 2
      print(self.term.bold_red("Critical hit!"))

    enemy.setHp(enemy.getHp() - damage)
    print(self.term.green("You attacked the enemy for " + str(damage) + " damage!"))
    print(self.term.yellow("Enemy HP: " + str(max(0, enemy.getHp())) + "/" + str(enemy.getMaxHp())))

    if enemy.getHp() <= 0:
      print(self.term.bold_green("You killed the enemy!"))
      enemy.removeEnemy(self.lines)

  # ==================== Update ====================
  
  def init(self, sio):
    """Main update method called every frame"""
    self.movePlayer(sio)
    self.inventoryControl()
  
  def inventoryControl(self):
    """Handle inventory-related input (can be extended)"""
    pass
